  
  document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita que se recargue la página
  
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
  
    const nuevoUsuario = { username, email, password };
  
    // Validaciones
    if (!email.includes('@') || !email.includes('.com')) {
      alert('Por favor, ingresa un email válido que contenga "@" y ".com".');
      return;
    }
  
    const contieneNumero = /\d/.test(password);
    if (!contieneNumero) {
      alert('La contraseña debe contener al menos un número.');
      return;
    }
  
    // Enviar al backend
    fetch('https://backend-trading-03z4.onrender.com/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nuevoUsuario)
    })
    .then(response => {
      if (response.ok) {
        alert('¡Registro exitoso!');
        window.location.href = "inicio.html";
        this.reset(); // Limpia el formulario
      } else {
        return response.json().then(data => {
          alert('Error al registrar: ' + data.mensaje);
        });
      }
    })
    .catch(error => {
      console.error('Error de red:', error);
      alert('Hubo un error al conectar con el servidor.');
    });
  });