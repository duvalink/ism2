const clienteSelect = document.getElementById('cliente-select'); // Obtiene el elemento <select> de los clientes
const contactosList = document.getElementById('contactos-list'); // Obtiene la lista de contactos

// Evento que se dispara cuando se cambia el valor del elemento <select> de los clientes
clienteSelect.addEventListener('change', () => {
    const clienteId = clienteSelect.value; // Obtiene el id del cliente seleccionado

    // Realiza una petición GET a la ruta /cotizaciones/contactos/{clienteId} para obtener los contactos del cliente seleccionado
    fetch(`/cotizaciones/contactos/${clienteId}`)
        .then(response => response.json()) // Convierte la respuesta a formato JSON
        .then(contactos => { // Recibe la lista de contactos
            contactosList.innerHTML = ''; // Limpia la lista de contactos 
            // Recorre la lista de contactos
            contactos.forEach(contacto => {
                const contactoItem = document.createElement('li'); // Crea un elemento <li>

                // Crea un elemento <input> y le establece sus atributos
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox'; // Establece el tipo del elemento <input>
                checkbox.name = 'contactos[]'; // Establece el nombre del elemento <input>
                checkbox.value = contacto[0]; // Establece el valor del elemento <input>
                
                // Establece el id del elemento <input>
                const label = document.createElement('label');
                label.textContent = contacto[1]; // Establece el texto del elemento <label>
                label.addEventListener('click', () => { // Evento que se dispara cuando se hace click en el elemento <label>
                    checkbox.checked = !checkbox.checked; // Cambia el estado del checkbox
                    label.classList.toggle('selected'); // Agrega o quita la clase 'selected' al elemento <label>
                });

                contactoItem.appendChild(checkbox); // Agrega el elemento <input> al elemento <li>
                contactoItem.appendChild(label); // Agrega el elemento <label> al elemento <li>
                contactosList.appendChild(contactoItem); // Agrega el elemento <li> a la lista de contactos
            });
        });
});
