function guardarCotizacion() {
    let cliente_id = document.getElementById('selected-client-id').value;
    const xhr = new XMLHttpRequest();
    const url = "/cotizaciones";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response.status === "success") {
                alert("Cotización guardada en la base de datos.");
            } else {
                alert("Error al guardar la cotización en la base de datos.");
            }
        }
    };

    const formData = new FormData();
    formData.append("save_to_db", "true");
    formData.append("cliente_id", cliente_id); // Asegurarse de enviar el valor de cliente_id
    console.log("Cliente ID:", cliente_id);

    xhr.send(new URLSearchParams([...formData.entries()]));
}
