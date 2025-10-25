document.addEventListener('DOMContentLoaded', () => {
    
    const subtotalEl = document.getElementById('summary-subtotal');
    const envioEl = document.getElementById('summary-envio');
    const totalEl = document.getElementById('summary-total');

    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    if (carrito.length > 0) {
    
        fetch('js/productos.json')
            .then(response => response.json())
            .then(todosLosProductos => {
                
                let subtotal = 0;
                for (const itemDelCarrito of carrito) {
                    const producto = todosLosProductos.find(p => p.id == itemDelCarrito.id);
                    if (producto) {
                        subtotal += parseFloat(producto.precio) * itemDelCarrito.quantity;
                    }
                }
                
                const costoEnvio = 0.00; 
                const total = subtotal + costoEnvio;

               
                subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
                envioEl.textContent = `$${costoEnvio.toFixed(2)}`;
                totalEl.textContent = `$${total.toFixed(2)}`;
            });
    }


   
    
    const paymentForm = document.getElementById('payment-form');
    
    paymentForm.addEventListener('submit', (e) => {
       
        e.preventDefault(); 

       
        if (carrito.length === 0) {
            alert('Tu carrito está vacío. No puedes proceder al pago.');
            return; 
        }

        
        const datosEnvio = {
            nombre: document.getElementById('nombre').value,
            direccion: document.getElementById('direccion').value,
            ciudad_cp: document.getElementById('ciudad_cp').value,
            tarjeta: document.getElementById('tarjeta').value, 
        };

        
        const datosCarrito = JSON.parse(localStorage.getItem('carrito'));

        
        const pedidoCompleto = {
            infoEnvio: datosEnvio,
            items: datosCarrito
        };

        
        console.log("--- SIMULANDO ENVÍO AL BACKEND ---");
        console.log("Se enviaría el siguiente objeto:");
        console.log(pedidoCompleto);

       
        alert('¡Gracias por tu compra! Tu pedido ha sido procesado.');
        
      
        localStorage.removeItem('carrito'); 
        
      
        setTimeout(() => {
            window.location.href = 'inicio.html'; 
        }, 2000);
    });
});