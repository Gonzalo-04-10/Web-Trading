// Si querés cambiar dinámicamente el nombre del curso en base a parámetros de URL, podés usar esto:
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const curso = params.get('curso');
    if (curso) {
      document.getElementById('nombre-curso').textContent = curso;
    }
  });
  