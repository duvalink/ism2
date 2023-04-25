$(document).ready(function () {
    $('#cliente-select').change(function (event) {
        // Establece el valor del campo oculto con el valor seleccionado del cliente
        $('#hidden-cliente-id').val(event.target.value);
    });

    $('#save-to-db').click(function () {
        console.log('Botón guardar en base de datos presionado');
        var cliente_id = $('#hidden-cliente-id').val();

        // Envía el formulario principal en lugar del formulario oculto
        $('#cotizacion-form').submit();

        console.log('Iniciando solicitud AJAX');
        $.ajax({
            url: guardarCotizacionUrl,
            method: "POST",
            data: {
                cliente_id: cliente_id,
            },
            success: function (response) {
                console.log('Solicitud AJAX completada con éxito');
                if (response.status === "success") {
                    limpiarCotizaciones();
                    window.location.href = `/descargar_cotizacion/${response.id_presupuesto}`;
                } else {
                    // Muestra un mensaje de error si el estado no es "success"
                    console.log('Error en el proceso de guardar la cotización');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('Error en la solicitud AJAX:', textStatus, errorThrown);
                // Haz algo en caso de que ocurra un error, por ejemplo, mostrar un mensaje de error
            }
        });
    });
});

function cargarCotizaciones() {
    const cotizaciones = JSON.parse(localStorage.getItem('cotizaciones')); // Obtiene las cotizaciones del almacenamiento local
    if (cotizaciones) { // Si hay cotizaciones en el almacenamiento local, las agrega a la tabla
        console.log('Obteniendo cotizaciones del almacenamiento local.');
        for (let cotizacion of cotizaciones) {
            console.log('Agregando cotizacion a la tabla: ', cotizacion);
            agregarFila(cotizacion.descripcion, cotizacion.cantidad, cotizacion.precio, cotizacion.material, cotizacion.importe);
        }
    }
}
// Guarda las cotizaciones en el almacenamiento local
function guardarCotizaciones(cotizaciones) {
    console.log('Guardando cotizaciones');
    localStorage.setItem('cotizaciones', JSON.stringify(cotizaciones));
}

// Limpia las cotizaciones del almacenamiento local
function limpiarCotizaciones() {
    console.log('Limpiando cotizaciones');
    localStorage.removeItem('cotizaciones');
}
