# Se importan los módulos necesarios de Flask
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, make_response

# Se importan la variable "mysql" de "models" y la clase "Config" de "config"
from models import mysql
from config import Config

#  importa dos funciones del módulo datos que se utilizan en la función agregar_cotizacion definida en el objeto Blueprint cotizaciones_bp.
from datos import add_cotizacion, get_cotizacion, limpiar_cotizaciones, to_float, to_int
from datetime import datetime
from flask import send_file
from pdf_generator import create_pdf
import io
import locale

# Se crea un objeto "Blueprint" con el nombre "cotizaciones_bp"
cotizaciones_bp = Blueprint('cotizaciones', __name__)

# Se define una función llamada "configure_db" que recibe un argumento "app"


def configure_db(app):
    # Se configura la aplicación Flask utilizando la clase "Config"
    app.config.from_object(Config)
    # Se inicializa la conexión a MySQL utilizando la variable "mysql" de "models"
    mysql.init_app(app)

# Funciones para convertir de manera segura las cadenas a números


def to_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0


def to_int(value):
    try:
        return int(value)
    except ValueError:
        return 0

# Se define una ruta para agregar nuevas cotizaciones


@cotizaciones_bp.route('/cotizaciones', methods=['GET', 'POST'])
def agregar_cotizacion():

    clear_table = request.args.get('clear_table', 'False') == 'True'

    if clear_table:
        limpiar_cotizaciones()

    cursor = mysql.connection.cursor()
    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d")

    cursor.execute(
        'SELECT id_presupuesto FROM presupuestos ORDER BY id_presupuesto DESC LIMIT 1')
    result = cursor.fetchone()
    if not result:
        next_id = 1
    else:
        next_id = result[0] + 1

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = to_int(request.form['cantidad'])
        precio = to_float(request.form['p_unitario'])
        importe = to_float(request.form['importe'])
        material = request.form['material']

        cotizacion = {'descripcion': descripcion, 'cantidad': cantidad,
                      'precio': precio, 'importe': importe, 'material': material,
                      'fecha': fecha}

        add_cotizacion(cotizacion)
        # session['cotizaciones'] = get_cotizacion()
        return redirect(url_for('cotizaciones.agregar_cotizacion'))

    else:
        cotizaciones = get_cotizacion()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        clear_table = request.args.get('clear_table') == 'True'
        return render_template('cotizaciones.html', clientes=clientes, fecha=fecha, next_id=next_id, clear_table=clear_table, cotizaciones=get_cotizacion())


@cotizaciones_bp.route('/cotizaciones/contactos/<int:id_cliente>', methods=['GET'])
# Se define una función que recibe el ID del cliente como argumento
def obtener_contactos(id_cliente):

    # Se realiza una consulta a la base de datos para obtener los contactos del cliente con el ID proporcionado
    # Se crea un cursor para ejecutar consultas a la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM clientes_contactos WHERE cliente_id = %s", (id_cliente,))  # Se ejecuta la consulta
    contactos = cursor.fetchall()  # Se obtienen los resultados de la consulta

    # Se devuelve la lista de contactos como un objeto JSON
    return jsonify(contactos)


@cotizaciones_bp.route('/guardar_cotizacion', methods=['POST'])
def guardar_cotizacion():
    try:
        cotizaciones = get_cotizacion()

        if not cotizaciones:
            return "No hay cotizaciones para guardar", 400

        try:
            cliente_id = request.form['cliente_id']
            print("Cliente ID:", cliente_id)
        except Exception as e:
            print("Error al obtener cliente_id:", e)
            return "Error al obtener cliente_id", 400

        cursor = mysql.connection.cursor()

        fecha = cotizaciones[0]['fecha']
        materiales = sum([to_float(cotizacion['precio']) * to_int(cotizacion['cantidad']) * 0.6
                          for cotizacion in cotizaciones if 'precio' in cotizacion])
        mano_obra = sum([to_float(cotizacion['precio']) * to_int(cotizacion['cantidad']) * 0.4
                         for cotizacion in cotizaciones if 'precio' in cotizacion])
        subtotal = materiales + mano_obra
        iva = subtotal * 0.08
        total = subtotal + iva

        cursor.execute("""
            INSERT INTO presupuestos (cliente_id, fecha, materiales, mano_obra, subtotal, iva, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cliente_id, fecha, materiales, mano_obra, subtotal, iva, total))

        id_presupuesto = cursor.lastrowid

        for index, cotizacion in enumerate(cotizaciones):
            cursor.execute("""
                INSERT INTO presupuestos_partidas (presupuesto_id, partida, descripcion, cantidad, precio, importe)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_presupuesto, index + 1, cotizacion['descripcion'], cotizacion['cantidad'],
                  cotizacion['precio'], cotizacion['importe']))

        mysql.connection.commit()
        id_presupuesto = str(id_presupuesto)
        limpiar_cotizaciones()
        return jsonify({"status": "success", "id_presupuesto": id_presupuesto, "reload_url": url_for('cotizaciones.agregar_cotizacion', clear_table=True)})

    except Exception as e:
        print(e)
        return "Ocurrió un error al guardar la cotización", 500


@cotizaciones_bp.route('/descargar_cotizacion/<int:id_presupuesto>')
def descargar_cotizacion(id_presupuesto):
    cotizaciones = obtener_cotizaciones_por_id(id_presupuesto)

    pdf_data = create_pdf(cotizaciones)
    pdf_buffer = io.BytesIO(pdf_data)
    pdf_buffer.seek(0)

    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cotizacion.pdf'
    return response


def obtener_cotizaciones_por_id(id_presupuesto):
    cursor = mysql.connection.cursor()

    query = """
    SELECT c.id_cliente, c.nombre, c.direccion, p.id_presupuesto, p.fecha, p.materiales, p.mano_obra, p.subtotal, p.iva, p.total,
           pp.id_partida, pp.partida, pp.descripcion, pp.cantidad, pp.precio, pp.importe
    FROM presupuestos p
    JOIN clientes c ON p.cliente_id = c.id_cliente
    JOIN presupuestos_partidas pp ON p.id_presupuesto = pp.presupuesto_id
    WHERE p.id_presupuesto = %s
    ORDER BY p.id_presupuesto, pp.partida
    """
    cursor.execute(query, (id_presupuesto,))
    cotizaciones_raw = cursor.fetchall()

    cotizaciones = []
    for cotizacion in cotizaciones_raw:
        cotizacion_dict = {
            'id_cliente': cotizacion[0],
            'nombre_cliente': cotizacion[1],
            'direccion_cliente': cotizacion[2],
            'id_presupuesto': cotizacion[3],
            'fecha': cotizacion[4],
            'materiales': cotizacion[5],
            'mano_obra': cotizacion[6],
            'subtotal': cotizacion[7],
            'iva': cotizacion[8],
            'total': cotizacion[9],
            'id_partida': cotizacion[10],
            'partida': cotizacion[11],
            'descripcion': cotizacion[12],
            'cantidad': cotizacion[13],
            'precio': cotizacion[14],
            'importe': cotizacion[15]
        }
        cotizaciones.append(cotizacion_dict)

    return cotizaciones
