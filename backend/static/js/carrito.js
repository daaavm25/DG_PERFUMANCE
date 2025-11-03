document.addEventListener('DOMContentLoaded', async () => {

    const itemsContainer = document.getElementById('cart-items-container');
    const emptyMsg = document.getElementById('empty-cart-msg');
    const summaryContainer = document.getElementById('cart-summary-container');
    const subtotalEl = document.getElementById('summary-subtotal');
    const envioEl = document.getElementById('summary-envio');
    const totalEl = document.getElementById('summary-total');

    try{
        const res = await fetch(`/api/carrito_api`, {credentials: "include"});

        if (res.status === 401){
            window.location.href = "/login";
            return;
        }
        
        if (!res.ok) throw new Error(`Respuesta invalida: ${res.status}`);

        const data = await res.json()
        const carrito = data.carrito || [];

        if (carrito.length === 0){
            emptyMsg.style.display = 'block';
            summaryContainer.style.display = 'none';
            return;            
        }

        emptyMsg.style.display = 'none';
        summaryContainer.style.display = 'block';

        let subtotal = 0;
        itemsContainer.innerHTML = carrito.map(item => {
            const subtotalItem = Number(item.subtotal || (item.precio * item.cantidad || 0));
            subtotal += subtotalItem;
            const imagen = item.imagen_url || `/static/img/perfume_${item.id_perfume}.jpg`;
            const nombre = item.nombre || `Producto ${item.id_perfume}`;
            return `
                <div class="cart-item" data-id="${item.id_perfume || item.id}">
                    <img src="${imagen}" alt="${nombre}" class="cart-item-img">
                    <div class="cart-item-info">
                        <h3>${nombre}</h3>
                        <p>Precio: $${(item.precio ?? 0).toFixed(2)}</p>
                        <p>Cantidad: ${item.cantidad}</p>
                        <button class="btn-eliminar">Eliminar</button>
                    </div>
                    <div class="cart-item-price">
                        <p>$${subtotalItem.toFixed(2)}</p>
                    </div>
                </div>`;
        }).join("");

        document.querySelectorAll('.btn-eliminar').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const itemDiv = e.target.closest('.cart-item');
                const id_perfume = parseInt(itemDiv.dataset.id);
                console.log("ID del perfume a eliminar:", id_perfume);

                if (!id_perfume){
                    alert("Error: No se encontro el ID del producto.");
                }

                if (!confirm("¿Deseas eliminar este producto del carrito?")) return;
                try{
                    const res = await fetch('/api/carrito/eliminar', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        credentials: 'include',
                        body: JSON.stringify({id_perfume})
                    });

                    if (!res.ok) throw new Error('Error al eliminar producto');
                    const data = await res.json();
                    
                    console.log("Producto eliminado:", data);
                    itemDiv.remove();

                    if (document.querySelectorAll('.cart-item').length === 0){
                        emptyMsg.style.display = 'block';
                        summaryContainer.style.display = 'none';
                    }
                }catch (err){
                    console.error("Error al intentar eliminar producto:", err);
                }
            });
        });

        const  envio = 0.00;
        const total = subtotal + envio;

        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        envioEl.textContent = `$${envio.toFixed(2)}`;
        totalEl.textContent = `$${total.toFixed(2)}`;

    }catch (error){
        console.error("Error en carrito.js", error);
        itemsContainer.innerHTML = "<p>Error al cargar el carrito.</p>";
        const summary = document.getElementById('cart-summary-contaainer');
        if (summary) summary.style.display = 'none';
    }
});