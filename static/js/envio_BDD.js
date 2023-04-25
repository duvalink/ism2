function guardarCotizacion() {
    const cliente_id = document.getElementById('selected-client-id').value;
    console.log("Cliente ID:", cliente_id);

    const xhr = new XMLHttpRequest();
    const url = "/cotizaciones";
    console.log("URL:", url);

    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        console.log("xhr.readyState:", xhr.readyState);
        console.log("xhr.status:", xhr.status);

        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("xhr.responseText:", xhr.responseText);

            const response = JSON.parse(xhr.responseText);
            console.log("response:", response);

            if (response.status === "success") {
                alert("Cotización guardada en la base de datos.");
            } else {
                alert("Error al guardar la cotización en la base de datos.");
            }
        }
    };

    const formData = new FormData();
    formData.append("save_to_db", "true");
    formData.append("cliente_id", cliente_id);

    xhr.send(new URLSearchParams([...formData.entries()]));
}
