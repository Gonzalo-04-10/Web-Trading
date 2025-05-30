document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuarioLogueado'));

  if (!usuario) {
    alert('Debes iniciar sesión para ver tus compras');
    window.location.href = '../Registros/register.html';
    return;
  }

  // Hacemos la petición al backend
  fetch('https://backend-trading-03z4.onrender.com//api/compras', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username: usuario.username })
  })
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        document.getElementById('sin-compras').style.display = 'none';
        document.getElementById('con-compras').style.display = 'block';

        const tbody = document.getElementById('tabla-compras-body');

        data.forEach(compra => {
          const fila = document.createElement('tr');
          fila.innerHTML = `
            <td>${compra.nombre}</td>
            <td>${compra.fecha}</td>
            <td>$${compra.monto}</td>
          `;
          tbody.appendChild(fila);
        });
      } else {
        document.getElementById('sin-compras').style.display = 'block';
        document.getElementById('con-compras').style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Error al obtener las compras:', error);
    });
});

  