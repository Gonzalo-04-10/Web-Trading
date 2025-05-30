// Si querés cambiar dinámicamente el nombre del curso en base a parámetros de URL, podés usar esto:
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const curso = params.get('curso');
    if (curso) {
      document.getElementById('nombre-curso').textContent = curso;
    }
  });

 document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuarioLogueado'));

  if (!usuario) {
    alert('Tenés que iniciar sesión para completar la compra');
    window.location.href = '../Registros/register.html';
    return;
  }

  const botonPago = document.querySelector('.boton-pago');

  if (!botonPago) return;

  botonPago.addEventListener('click', (event) => {
    console.log('Click detectado');

    const nombreCurso = document.title || 'Curso desconocido';
    const monto = parseFloat(botonPago.getAttribute('data-monto')) || 0;
    const fecha = new Date().toISOString().split('T')[0];

    fetch('https://backend-trading-03z4.onrender.com//api/registrar-compra', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: usuario.username,
        nombre_curso: nombreCurso,
        fecha: fecha,
        monto: monto
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          console.log('Compra registrada correctamente');
        } else {
          console.error('Error en la compra:', data.error || 'Error desconocido');
        }
      })
      .catch(error => {
        console.error('Error de red al registrar la compra:', error);
      });
  });
});
