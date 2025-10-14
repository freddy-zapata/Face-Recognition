async function cargarAccesos() {
    const response = await fetch('/accesos');  // Asegúrate que esta ruta devuelve un arreglo ordenado descendente (último primero)
    const accesos = await response.json();

    if (accesos.length === 0) {
        // Si no hay accesos, mostrar guiones y foto por defecto
        document.getElementById('nombrePersona').textContent = '---';
        document.getElementById('apellidoPersona').textContent = '---';
        document.getElementById('cargoPersona').textContent = '---';
        document.getElementById('fechaHoraAcceso').textContent = '---';
        document.getElementById('fotoAcceso').src = '/static/default.png';
        return;
    }

    // Solo tomamos el primer (último acceso)
    const ultimoAcceso = accesos[0];

    document.getElementById('nombrePersona').textContent = ultimoAcceso.nombre || '---';
    document.getElementById('apellidoPersona').textContent = ultimoAcceso.apellido || '---';
    document.getElementById('cargoPersona').textContent = ultimoAcceso.cargo || '---';
    document.getElementById('fechaHoraAcceso').textContent = ultimoAcceso.fecha_hora || '---';

    // Mostrar la foto si existe, si no la foto por defecto
    if (ultimoAcceso.foto) {
        document.getElementById('fotoAcceso').src = `data:image/jpeg;base64,${ultimoAcceso.foto}`;
    } else {
        document.getElementById('fotoAcceso').src = '/static/default.png';
    }
}

// Actualizar la info cada 5 segundos
setInterval(cargarAccesos, 5000);
cargarAccesos();
