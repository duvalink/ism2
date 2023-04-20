from flask import Flask, render_template, flash
from modules.routes import clientes_bp, configure_db
from modules.contactos import contactos_bp
from modules.cotizaciones import cotizaciones_bp, configure_db, descargar_cotizacion
from modules.atajos_teclados import registrar_atajo
from modules.pdf_generator import create_pdf

import keyboard

app = Flask(__name__)
app.register_blueprint(clientes_bp)
app.register_blueprint(contactos_bp)
app.register_blueprint(cotizaciones_bp)

configure_db(app)

# Configurar mensajes flash
app.config['SECRET_KEY'] = 'clave-secreta'

@app.route('/')
def index():
    return render_template('index.html')

# Manejar errores 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Manejar errores 500
@app.errorhandler(500)
def internal_error(error):
    flash('Ha ocurrido un error interno en el servidor')
    return render_template('500.html'), 500

if __name__ == '__main__':
    registrar_atajo(app)
    app.run(debug=True)
    keyboard.unhook_all()
