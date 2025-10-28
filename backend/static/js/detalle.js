let currentProductId = null;

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const productoId = params.get('id');

    if (!productoId) {
        document.getElementById('producto-nombre').textContent = 'Producto no encontrado.';
        return; 
    }

    try {
        const response = await fetch(`http://localhost:5000/api/catalogo/perfumes/${productoId}`);
        if (!response.ok) throw new Error("No se encontro el producto.")
        const producto = await response.json();

        document.title = producto.nombre;
        document.getElementById('producto-nombre').textContent = producto.nombre;
        document.getElementById('producto-precio').textContent = `$${producto.precio}`;
        document.getElementById('producto-descripcion').textContent = producto.descripcion;
        document.getElementById('producto-imagen').src = producto.imagen_url;
        document.getElementById('producto-imagen').alt = producto.nombre;

        currentProductId = producto.id;
    }catch (error){
        console.error("Error al cargar producto:", error);
        document.getElementById('producto-nombre').textContent = 'Error al cargar el producto.';
    }
    const btnComprar = document.querySelector('.btn');
    const toastAlerta = document.getElementById('toast-alerta');

    if (btnComprar) {
        btnComprar.addEventListener('click', async () =>{
            try{
                const res = await fetch(`http://localhost:5000/api/carrito`,{
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    credentials: "include",
                    body: JSON.stringify({id_perfume: currentProductId, cantidad: 1})
                });
                
                if (res.status === 401){
                    window.location.href = "/login";
                    return;
                }
                if (!res.ok) throw new Error("Error al agregar al carrito.");

                const data = await res.json()
                console.log("Carrito actuaalizado:", data);

                const toastAlerta = document.getElementById('toast-alerta');
                if (toastAlerta){
                    toastAlerta.classList.add('show');
                    setTimeout(() => toastAlerta.classList.remove('show'), 3000);
                }
            }catch (err){
                console.error("Error al agregar al carrito:", err);
                alert("No se pudo agregar al carrito");
            }
        });
    }
});
