document.addEventListener('DOMContentLoaded', () => {

    const itemsContainer = document.getElementById('cart-items-container');
    const emptyMsg = document.getElementById('empty-cart-msg');
    const summaryContainer = document.getElementById('cart-summary-container');
    const subtotalEl = document.getElementById('summary-subtotal');
    const envioEl = document.getElementById('summary-envio');
    const totalEl = document.getElementById('summary-total');

    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    if (carrito.length === 0) {
        emptyMsg.style.display = 'block';
        summaryContainer.style.display = 'none';
        return;
    }

    emptyMsg.style.display = 'none';
    summaryContainer.style.display = 'block';
    
    fetch('js/productos.json')
        .then(response => response.json())
        .then(todosLosProductos => {
            
            let subtotal = 0;
            let htmlItems = ''; 

            for (const itemDelCarrito of carrito) {
                const producto = todosLosProductos.find(p => p.id == itemDelCarrito.id);

                if (producto) {
                    const totalItem = parseFloat(producto.precio) * itemDelCarrito.quantity;
                    subtotal += totalItem;

                    htmlItems += `
                        <div class="cart-item">
                            <img src="${producto.imagen}" alt="${producto.nombre}" class="cart-item-img">
                            <div class="cart-item-info">
                                <h3>${producto.nombre}</h3>
                                <p>Precio: $${producto.precio}</p>
                                
                                <div class="cart-item-quantity">
                                    <button class="quantity-btn btn-decrease" data-id="${producto.id}">-</button>
                                    <span class="quantity-text">${itemDelCarrito.quantity}</span>
                                    <button class="quantity-btn btn-increase" data-id="${producto.id}">+</button>
                                </div>
                            </div>
                            <div class="cart-item-price">
                                <p>$${totalItem.toFixed(2)}</p>
                            </div>
                            <button class="cart-item-remove" data-id="${producto.id}">&times;</button>
                        </div>
                    `;
                }
            } 

            itemsContainer.innerHTML = htmlItems;
            
            const costoEnvio = 0.00;
            const total = subtotal + costoEnvio;

            subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
            envioEl.textContent = `$${costoEnvio.toFixed(2)}`;
            totalEl.textContent = `$${total.toFixed(2)}`;

            addRemoveListeners();
            addQuantityListeners();

        })
        .catch(error => {
            console.error('Error al cargar productos del carrito:', error);
            itemsContainer.innerHTML = '<p>Error al cargar el carrito. Intenta de nuevo.</p>';
        });
});

function addRemoveListeners() {
    const removeBtns = document.querySelectorAll('.cart-item-remove');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const idParaEliminar = e.target.dataset.id;
            removerDelCarrito(idParaEliminar);
        });
    });
}

function removerDelCarrito(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const nuevoCarrito = carrito.filter(item => item.id != id);
    localStorage.setItem('carrito', JSON.stringify(nuevoCarrito));
    location.reload(); 
}

function addQuantityListeners() {
    const increaseBtns = document.querySelectorAll('.btn-increase');
    increaseBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.target.dataset.id;
            aumentarCantidad(id);
        });
    });

    const decreaseBtns = document.querySelectorAll('.btn-decrease');
    decreaseBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.target.dataset.id;
            disminuirCantidad(id);
        });
    });
}

function aumentarCantidad(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const productoEnCarrito = carrito.find(p => p.id == id);

    if (productoEnCarrito) {
        productoEnCarrito.quantity += 1;
    }
    
    localStorage.setItem('carrito', JSON.stringify(carrito));
    location.reload();
}

function disminuirCantidad(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const itemIndex = carrito.findIndex(p => p.id == id); 

    if (itemIndex > -1) { 
        if (carrito[itemIndex].quantity > 1) {
            carrito[itemIndex].quantity -= 1;
        } else {
            carrito.splice(itemIndex, 1);
        }
    }
    
    localStorage.setItem('carrito', JSON.stringify(carrito));
    location.reload(); 
}