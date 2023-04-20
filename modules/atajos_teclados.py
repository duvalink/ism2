import keyboard


def registrar_atajo(app):
    @app.route('/on_f7')
    def on_f7():
        keyboard.write('°')
        return 'Symbol added'

    @app.route('/on_f8')
    def on_f8():
        keyboard.write('#')
        return 'Symbol added'

    @app.route('/on_f9')
    def on_f9():
        keyboard.write('Ø')
        return 'Symbol added'

    # REGISTRAR ATAJOS DE TECLADO
    keyboard.add_hotkey('F7', lambda: app.test_client().get('/on_f7'))
    keyboard.add_hotkey('F8', lambda: app.test_client().get('/on_f8'))
    keyboard.add_hotkey('F9', lambda: app.test_client().get('/on_f9'))
