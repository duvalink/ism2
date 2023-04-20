from flask import Blueprint, render_template, request, url_for, redirect, flash
from models import mysql

contactos_bp = Blueprint('contactos', __name__)

# Agregar nuevo contacto
@contactos_bp.route('/contactos', methods=['GET', 'POST'])
def agregar_contacto():
    # Obtener los datos del formulario enviado por el usuario
    if request.method == 'POST':
        contacto = request.form['contacto']
        correo = request.form['correo']
        cliente_id = request.form['cliente_id']
        
        # Insertar datos del formulario en la base de datos
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO clientes_contactos (contacto, correo, cliente_id) VALUES (%s, %s, %s)"
        val = (contacto, correo, cliente_id)
        cursor.execute(sql, val)
        mysql.connection.commit()

        flash('Nuevo contacto agregado')
        return redirect(url_for('contactos.agregar_contacto'))

    # Mostrar datos en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_cliente, nombre FROM clientes")
    clientes = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute( '''
        SELECT clientes_contactos.id_contacto, clientes_contactos.contacto, clientes_contactos.correo, clientes.nombre
        FROM clientes_contactos
        JOIN clientes ON clientes_contactos.cliente_id = clientes.id_cliente;
        ''')
    contactos = cursor.fetchall()
    
    return render_template('contactos.html', contactos=contactos, clientes=clientes)


# Editar contacto existente
@contactos_bp.route('/editar_contacto', methods=['POST'])
def editar_contacto():
    id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes_contactos WHERE id_contacto=%s", (id,))
    datos = cursor.fetchone()
    return render_template('contactos.html', datos=datos, editar=True)


# Actualizar contacto
@contactos_bp.route('/actualizar_contacto', methods=['POST'])
def actualizar_contacto():
    id = request.form['id']
    contacto = request.form['contacto']
    correo = request.form['correo']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE clientes_contactos SET contacto=%s, correo=%s WHERE id_contacto=%s",
                   (contacto, correo, id))
    mysql.connection.commit()
    flash('Contacto actualizado')
    return redirect(url_for('contactos.agregar_contacto'))


# Eliminar contacto
@contactos_bp.route('/eliminar_contacto', methods=['POST'])
def eliminar_contacto():
    id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clientes_contactos WHERE id_contacto=%s", (id,))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('contactos.agregar_contacto'))
