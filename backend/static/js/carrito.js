document.addEventListener('DOMContentLoaded', async () => {

    const itemsContainer = document.getElementById('cart-items-container');
    const emptyMsg = document.getElementById('empty-cart-msg');
    const summaryContainer = document.getElementById('cart-summary-container');
    const subtotalEl = document.getElementById('summary-subtotal');
    const envioEl = document.getElementById('summary-envio');
    const totalEl = document.getElementById('summary-total');

    try{
        const res = await fetch('http://localhost:5000/api/carrito', {credentials: "include"});

        if (res.status === 401){
            window.location.href = "login.html";
            return;
        }

        const carrito = await res.json()
        if (!carrito || carrito.length === 0){
            emptyMsg.style.display = 'block';
            summaryContainer.style.display = 'none';
            return;            
        }

        emptyMsg.style.display = 'none';
        summaryContainer.style.display = 'block';

        let subtotal = 0;
        itemsContainer.innerHTML = carrito.map(item => {
            subtotal += item.subtotal;
            return `
                <div class="cart-item">
                    <img src="${item.imagen_url}" alt="${item.nombre}" class="cart-item-img">
                    <div class="cart-item-info">
                        <h3>${item.nombre}</h3>
                        <p>Precio: $${item.precio}</p>
                        <p>Cantidad: ${item.cantidad}</p>
                    </div>
                    <div class="cart-item-price">
                        <p>$${item.subtotal.toFixed(2)}</p>
                    </div>
                </div>`;
        }).join("");
        const  envio = 0.00;
        const total = subtotal + envio;

        subtotalEl.textContent = '$${subtotal.toFixed(2)}';
        envioEl.textContent = '$${envio.toFixed(2)}';
        totalEl.textContent = '$${total.toFixed(2)}';
    }catch (error){
        console.error("Error en carrito.js", error);
        itemsContainer.innerHTML = "<p>Error al cargar el carrito.</p>";
    }
});