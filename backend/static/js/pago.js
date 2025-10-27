document.addEventListener('DOMContentLoaded', async () => {
    
    const subtotalEl = document.getElementById('summary-subtotal');
    const envioEl = document.getElementById('summary-envio');
    const totalEl = document.getElementById('summary-total');
    const paymentForm = document.querySelector('form');

    try{
        const res = await fetch('http://localhost:5000/api/carrito', {credentials: "include"});
        const carrito = await res.json();
        if(!carrito || carrito.length === 0){
            alert("Carrito vacio, agrega productos que desees comprar.");
            window.location.href = "carrito.html";
            return;
        }

        let subtotal = carrito.reduce((acc, item) => acc + item.subtotal, 0);
        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        envioEl.textContent = `$0.00`;
        totalEl.textContent = `$${subtotal.toFixed(2)}`;

        paymentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            try{
                const metodoPago = "Tarjeta";
                const res = await fetch('http://localhost:5000/api/checkout', {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    credentials: "include",
                    body: JSON.stringify({metodo_Pago: metodoPago})
                });
                if(!res.ok) throw new Error("Error al procesar pago.");
                alert("¡Compra realizada con exito!");
                window.location.href = "inicio.html";
            }catch (err){
                console.error("Error en pago.js:", err);
                alert("Error al completar la compra.");
            }
        });
    }catch(err){
        console.error("Error al cargar carrito:", err);
    } 
});