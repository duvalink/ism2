// Obtener los campos de cantidad, precio unitario y total
const cantidad = document.getElementById("cantidad");
const precio = document.getElementById("p_unitario");
const total = document.getElementById("importe");

// Escuchar los cambios en los campos de cantidad y precio unitario
cantidad.addEventListener("input", actualizarTotal);
precio.addEventListener("input", actualizarTotal);

// Función para actualizar el campo de total
function actualizarTotal() {
  // Obtener los valores de cantidad y precio unitario
  const cantidadValor = cantidad.value;
  const precioValor = precio.value;

  // Calcular el total
  const totalValor = cantidadValor * precioValor;

  // Actualizar el campo de total
  total.value = totalValor;
}


function showModal(event) {
  event.preventDefault();
  const button = event.relatedTarget;
  const action = button.getAttribute('data-action');
  const modalTitle = document.querySelector('#myModal .modal-title');
  const submitBtn = document.querySelector('#myModal .modal-footer button[type="submit"]');

  if (action === 'add') {
    modalTitle.textContent = 'Agregar producto';
    submitBtn.textContent = 'Agregar';
  } else if (action === 'edit') {
    modalTitle.textContent = 'Editar producto';
    submitBtn.textContent = 'Guardar cambios';
    // Rellenar formulario con los datos del producto
    document.querySelector('#id').value = button.getAttribute('data-id');
    document.querySelector('#descripcion').value = button.getAttribute('data-descripcion');
    document.querySelector('#material').value = button.getAttribute('data-material');
    document.querySelector('#cantidad').value = button.getAttribute('data-cantidad');
    document.querySelector('#p_unitario').value = button.getAttribute('data-p_unitario');
    document.querySelector('#total').value = button.getAttribute('data-total');
  }

  // Abre el modal
  const myModal = new bootstrap.Modal(document.getElementById('myModal'));
  myModal.show();
}
