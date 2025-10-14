const API_URL = "http://localhost:6001";

// Cargar personas y mostrarlas en la tabla
async function cargarPersonas() {
    try {
        const res = await fetch(`${API_URL}/personas`);
        const personas = await res.json();

        const tbody = document.querySelector("#tabla-personas tbody");
        tbody.innerHTML = ""; // Limpiar tabla

        personas.forEach(p => {
            const tr = document.createElement("tr");

            // Foto cuadrada y pequeña
            const fotoTd = document.createElement("td");
            if (p.foto) {
                fotoTd.innerHTML = `<img src="data:image/jpeg;base64,${p.foto}" alt="Foto" class="img-thumbnail" style="width:60px; height:60px; object-fit: cover;">`;
            } else {
                fotoTd.textContent = "Sin foto";
            }

            tr.appendChild(fotoTd);

            tr.innerHTML += `
                <td class="align-middle">${p.nombre}</td>
                <td class="align-middle">${p.apellido}</td>
                <td class="align-middle">${p.cargo}</td>
                <td class="text-center align-middle">
                    <button class="btn btn-danger btn-sm btn-eliminar" data-id="${p.id}">Eliminar</button>
                </td>
            `;

            tbody.appendChild(tr);
        });

        // Añadir event listeners a botones eliminar
        document.querySelectorAll(".btn-eliminar").forEach(btn => {
            btn.addEventListener("click", async (e) => {
                const id = e.target.dataset.id;
                if (confirm("¿Seguro que quieres eliminar esta persona?")) {
                    await eliminarPersona(id);
                    await cargarPersonas();
                }
            });
        });

    } catch (error) {
        console.error("Error cargando personas:", error);
        alert("No se pudieron cargar las personas.");
    }
}

// Agregar persona desde el modal
async function agregarPersona() {
    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const cargo = document.getElementById("cargo").value.trim();

    if (!nombre || !apellido || !cargo) {
        alert("Completa todos los campos.");
        return;
    }

    const personaData = { nombre, apellido, cargo };

    try {
        const res = await fetch(`${API_URL}/personas`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(personaData)
        });

        if (!res.ok) throw new Error("Error en el servidor");

        const data = await res.json();

        // Mostrar modal con el ID generado
        document.getElementById("personaIdModal").textContent = data.id;
        const modalId = new bootstrap.Modal(document.getElementById("modalPersonaId"));
        modalId.show();

        // Cerrar modal agregar persona
        const modalAgregar = bootstrap.Modal.getInstance(document.getElementById("agregarPersonaModal"));
        modalAgregar.hide();

        // Limpiar formulario
        document.getElementById("formAgregarPersona").reset();

        // Recargar tabla
        cargarPersonas();

    } catch (error) {
        console.error("Error al agregar persona:", error);
        alert("Error al agregar la persona.");
    }
}

// Eliminar persona por ID
async function eliminarPersona(id) {
    try {
        const res = await fetch(`${API_URL}/personas/${id}`, {
            method: "DELETE"
        });

        if (!res.ok) throw new Error("Error eliminando persona");

    } catch (error) {
        console.error("Error eliminando persona:", error);
        alert("No se pudo eliminar la persona.");
    }
}

// Cargar personas al inicio
document.addEventListener("DOMContentLoaded", cargarPersonas);
