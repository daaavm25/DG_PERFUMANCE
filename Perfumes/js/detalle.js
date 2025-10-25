let currentProductId = null;

document.addEventListener('DOMContentLoaded', () => {

    const params = new URLSearchParams(window.location.search);
    const productoId = params.get('id');

    if (!productoId) {
        document.getElementById('producto-nombre').textContent = 'Producto no encontrado.';
        return; 
    }

    fetch('js/productos.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo cargar el archivo de productos.');
            }
            return response.json(); 
        })
        .then(productos => {
            
            const producto = productos.find(p => p.id == productoId);

            if (producto) {
                document.title = producto.nombre; 
                document.getElementById('producto-nombre').textContent = producto.nombre;
                document.getElementById('producto-precio').textContent = `$${producto.precio}`;
                document.getElementById('producto-descripcion').textContent = producto.descripcion;
                document.getElementById('producto-imagen').src = producto.imagen;
                document.getElementById('producto-imagen').alt = producto.nombre;
                
                currentProductId = producto.id;

            } else {
                document.getElementById('producto-nombre').textContent = 'Producto no encontrado.';
            }
        })
        .catch(error => {
            console.error('Error en el script:', error);
            document.getElementById('producto-nombre').textContent = 'Error al cargar el producto.';
        });

    
    const btnComprar = document.querySelector('.btn');
    const toastAlerta = document.getElementById('toast-alerta');

    if (btnComprar) {
        btnComprar.addEventListener('click', () => {
            
            if (!currentProductId) {
                console.error('Error: ID de producto nulo. No se puede añadir al carrito.');
                return;
            }

            agregarAlCarrito(currentProductId);

            if (toastAlerta) {
                toastAlerta.classList.add('show'); 
                
                setTimeout(() => {
                    toastAlerta.classList.remove('show');
                }, 3000); 
            }
        });
    }
});


function agregarAlCarrito(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    const productoEnCarrito = carrito.find(p => p.id === id);

    if (productoEnCarrito) {
        productoEnCarrito.quantity += 1;
    } else {
        carrito.push({
            id: id,
            quantity: 1 
        });
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));

    console.log('Carrito actualizado:', carrito);
}