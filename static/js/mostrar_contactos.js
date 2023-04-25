const clienteSelect = document.getElementById('cliente-select'); // Obtiene el elemento <select> de los clientes
const contactosList = document.getElementById('contactos-list'); // Obtiene la lista de contactos

// Evento que se dispara cuando se cambia el valor del elemento <select> de los clientes
clienteSelect.addEventListener('change', () => {
    const clienteId = clienteSelect.value; // Obtiene el id del cliente seleccionado

    // Realiza una petición GET a la ruta /cotizaciones/contactos/{clienteId} para obtener los contactos del cliente seleccionado
    fetch(`/cotizaciones/contactos/${clienteId}`)
        .then(response => response.json())
        .then(contactos => {
            contactosList.innerHTML = '';
            console.log(`Retrieved ${contactos.length} contacts`);
            contactos.forEach(contacto => {
                const contactoItem = document.createElement('li');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'contactos[]';
                checkbox.value = contacto[0];
                const label = document.createElement('label');
                label.textContent = contacto[1];
                label.addEventListener('click', () => {
                    checkbox.checked = !checkbox.checked;
                    label.classList.toggle('selected');
                });

                contactoItem.appendChild(checkbox);
                contactoItem.appendChild(label);
                contactosList.appendChild(contactoItem);
            });
        });

});
