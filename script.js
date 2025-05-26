document.addEventListener('DOMContentLoaded', () => {
  const usuarioActivo = JSON.parse(localStorage.getItem('usuarioLogueado'));

  const navPublico = document.getElementById('nav-publico');
  const navLogueado = document.getElementById('nav-logueado');

  if (usuarioActivo) {
   navPublico.style.display = 'none';
   navLogueado.style.display = 'block';
  } else {
   navPublico.style.display = 'block';
   navLogueado.style.display = 'none';
  }
});



function cerrarSesion() {
  localStorage.removeItem('usuarioActivo');
  location.reload(); // recarga la página para volver al estado no logueado
}

document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".cursos-section");

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          section.classList.add("show");
        }
      });
    },
    { threshold: 0.3 }
  );
  observer.observe(section);
}
);
document.addEventListener("DOMContentLoaded", () => {
  const section = document.querySelector(".cursos-section");

});

document.addEventListener('DOMContentLoaded', () => {
  const iconoPerfil = document.getElementById('iconoPerfillog');
  const menuUsuario = document.getElementById('menu-usuario');

  // Mostrar/ocultar menú al hacer clic en el icono
  iconoPerfil.addEventListener('click', () => {
    menuUsuario.style.display = menuUsuario.style.display === 'block' ? 'none' : 'block';
  });

  // Cerrar el menú si se hace clic fuera de él
  document.addEventListener('click', (event) => {
    if (!iconoPerfil.contains(event.target) && !menuUsuario.contains(event.target)) {
      menuUsuario.style.display = 'none';
    }
  });
});


document.getElementById('ver-cursos').addEventListener('click', function (e) {
    e.preventDefault(); // 🔥 esto es clave
    document.getElementById('cursos').scrollIntoView({ behavior: 'smooth' });
  });
  