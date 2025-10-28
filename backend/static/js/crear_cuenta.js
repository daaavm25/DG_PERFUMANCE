document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-crear-cuenta');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            nombres: document.getElementById('nombres').value.trim(),
            apellidos: document.getElementById('apellidos').value.trim(),
            telefono: document.getElementById('telefono').value.trim(),
            email: document.getElementById('email').value.trim(),
            username: document.getElementById('username').value.trim(),
            password: document.getElementById('password').value.trim()
        };

        try {
            const res = await fetch('http://localhost:5000/api/registro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (res.ok) {
                alert('Cuenta creada exitosamente');
                window.location.href = '/login';
            } else {
                alert(result.error || result.errores?.join('\n') || 'Error al registrar el usuario');
            }
        } catch (error) {
            console.error('Error al enviar los datos:', error);
            alert('Ocurrió un error al crear la cuenta.');
        }
    });
});
