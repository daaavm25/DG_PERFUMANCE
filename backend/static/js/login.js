document.querySelector('form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.querySelector('input[placeholder="Usuario"]').value;
  const password = document.querySelector('input[placeholder="Contraseña"]').value;

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message);
      window.location.href = data.redirect; // redirige según rol
    } else {
      alert(data.error || 'Error al iniciar sesión');
    }

  } catch (err) {
    console.error('Error:', err);
    alert('Error de conexión con el servidor.');
  }
});
