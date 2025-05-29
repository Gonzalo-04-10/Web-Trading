document.getElementById("registerForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  // Validaciones básicas (opcional)
  if (!username || !password) {
    alert("Por favor, completá todos los campos.");
    return;
  }

  // Enviamos los datos al backend
  fetch('https://web-production-027f4.up.railway.app/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => {
    if (response.ok) {
      return response.json(); // Si el login fue exitoso, parseamos la respuesta
    } else {
      return response.json().then(data => {
        throw new Error(data.mensaje);
      });
    }
  })
  .then(data => {
    // Guardar el usuario logueado si querés
    localStorage.setItem("usuarioLogueado", JSON.stringify(data.usuario));

    // Redireccionar
    alert("Inicio de sesión exitoso");
    window.location.href = "../index.html";
  })
  .catch(error => {
    alert("Error al iniciar sesión: " + error.message);
    console.error("Error:", error);
  });
});

  