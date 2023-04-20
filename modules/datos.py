# Se define una lista vacía llamada "cotizacion" fuera de cualquier función,
# lo que la hace una variable global
cotizacion = []

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


# Se define una función llamada "initialize_data" que no recibe argumentos
def initialize_data():
    # Dentro de la función, se define una nueva lista llamada "cotizacion",
    # pero esta variable no es la misma que la variable global "cotizacion"
    cotizacion = []

# Se define una función llamada "add_cotizacion" que recibe un argumento "nueva_cotizacion"
def add_cotizacion(nueva_cotizacion):
    global cotizacion
    cotizacion.append(nueva_cotizacion)
    subtotal = sum([to_float(c['precio']) * to_int(c['cantidad']) for c in cotizacion if 'precio' in c])
    iva = subtotal * 0.08
    total = subtotal + iva
    materiales = subtotal * 0.6
    mano_obra = subtotal * 0.4

    for c in cotizacion:
        c['subtotal'] = subtotal
        c['iva'] = iva
        c['total'] = total
        c['materiales'] = materiales
        c['mano_obra'] = mano_obra


# Se define una función llamada "get_cotizacion" que no recibe argumentos
def get_cotizacion():
    # Se devuelve la lista global "cotizacion"
    return cotizacion

def limpiar_cotizaciones():
    global cotizacion
    cotizacion = []


# OBSERVACIONES:
# Si se borra la variable global "cotizacion[]", las funciones no podrán acceder 
# a ella para agregar o obtener cotizaciones. Es decir, si se llama a la función 
# add_cotizacion() después de haber borrado la variable global "cotizacion[]", se 
# producirá un error porque la lista cotizacion ya no existe. De igual forma, si 
# se llama a la función get_cotizacion() después de haber borrado la variable 
# global "cotizacion[]", se producirá otro error porque la función intentará devolver 
# una lista que ya no existe.
