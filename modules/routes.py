import sys
sys.path.append('C:\\Users\\Orlando\\Desktop\\ism2\\modules')
from models import mysql
from flask import Blueprint, render_template, request, url_for, redirect, flash
from config import Config

clientes_bp = Blueprint('clientes', __name__)

# Configurar la conexión a MySQL


def configure_db(app):
    app.config.from_object(Config)
    mysql.init_app(app)


# Agregar nuevo cliente
@clientes_bp.route('/clientes', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        cp = request.form['cp']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        rfc = request.form['rfc']

        # Insertar datos del formulario en la base de datos
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO clientes (nombre, direccion, cp, ciudad, telefono, rfc) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (nombre, direccion, cp, ciudad, telefono, rfc)
        cursor.execute(sql, val)
        mysql.connection.commit()

        flash('Nuevo cliente agregado')

        return redirect(url_for('clientes.formulario'))

    # Mostrar datos en la tabla
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    datos = cursor.fetchall()

    return render_template('clientes.html', datos=datos)


# Editar cliente existente
@clientes_bp.route('/editar', methods=['POST'])
def editar():
    id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id,))
    datos = cursor.fetchone()
    return render_template('clientes.html', datos=datos, editar=True)


# Actualizar cliente
@clientes_bp.route('/actualizar', methods=['POST'])
def actualizar():
    id = request.form['id']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    cp = request.form['cp']
    ciudad = request.form['ciudad']
    telefono = request.form['telefono']
    rfc = request.form['rfc']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE clientes SET nombre=%s, direccion=%s, cp=%s, ciudad=%s, telefono=%s, rfc=%s WHERE id_cliente=%s",
                   (nombre, direccion, cp, ciudad, telefono, rfc, id))
    mysql.connection.commit()
    flash('Cliente actualizado')
    return redirect(url_for('clientes.formulario'))


# Eliminar cliente
@clientes_bp.route('/eliminar', methods=['POST'])
def eliminar():
    id = request.form['id']
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,))
    mysql.connection.commit()
    flash('Cliente eliminado')
    return redirect(url_for('clientes.formulario'))
