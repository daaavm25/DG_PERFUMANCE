let currentProductId = null;

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const productoId = params.get('id');

    if (!productoId) {
        document.getElementById('producto-nombre').textContent = 'Producto no encontrado.';
        return; 
    }

    currentProductId = parseInt(productoId);

    try {
        const response = await fetch(`/api/catalogo/perfumes/${productoId}`, {credentials: "include"});
        if (!response.ok) throw new Error("No se encontro el producto.")
        const producto = await response.json();

        document.title = producto.nombre || producto.marca;
        document.getElementById('producto-nombre').textContent = producto.nombre || producto.marca;
        document.getElementById('producto-precio').textContent = `$${producto.precio}`;
        document.getElementById('producto-descripcion').textContent = producto.presentacion || "Perfume exclusivo de alta calidad.";
        document.getElementById('producto-imagen').src = producto.imagen_url;
        document.getElementById('producto-imagen').alt = producto.nombre || producto.marca;

    }catch (error){
        console.error("Error al cargar producto:", error);
        document.getElementById('producto-nombre').textContent = 'Error al cargar el producto.';
    }

    const btnComprar = document.querySelector('.btn');
    const toastAlerta = document.getElementById('toast-alerta');
    const cantidadInput = document.getElementById('cantidad-input');
    const btnMas = document.getElementById('btn-plus');
    const btnMenos = document.getElementById('btn-minus');

    if (btnMas && btnMenos && cantidadInput){
        btnMas.addEventListener('click', () =>{
            let val = parseInt(cantidadInput.value) || 1;
            if (val < 10) cantidadInput.value = val + 1;
        });

        btnMenos.addEventListener('click', () =>{
            let val = parseInt(cantidadInput.value) || 1;
            if (val > 1) cantidadInput.value = val - 1;
        });
    }

    if (btnComprar) {
        btnComprar.addEventListener('click', async () =>{
            try{
                const cantidadSeleccionada = parseInt(cantidadInput.value) || 1;
                console.log("Agregando perfume con id:", currentProductId)

                const res = await fetch(`/api/carrito/agregar`,{
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    credentials: "include",
                    body: JSON.stringify({
                        id_perfume: currentProductId,
                        cantidad: cantidadSeleccionada
                    })
                });
                
                if (res.status === 401){
                    alert("Necesitas iniciar sesion para agregar productos al carrito.");
                    window.location.href = "/login";
                    return;
                }

                if (!res.ok) throw new Error("Error al agregar al carrito.");
                const data = await res.json()
                console.log("Carrito actualizado:", data);

                mostrarToast("Producto agregado correctamente.", true);

            }catch (err){
                console.error("Error al agregar al carrito:", err);
                mostrarToast("No se pudo agregar al carrito.", false);
            }
        });
    }
});

function mostrarToast(mensaje, exito=true){
    let toast = document.createElement('div');
    toast.className = `toast ${exito ? 'toast-exito' : 'toast-error'}`;
    toast.innerHTML = `
        <p>${mensaje}</p>
        ${exito ? '<div class="toast-buttons"><a href="/carrito" class="btn">Ver Carrito</a><button class="btn-secundario" id="seguirComprando">Seguir comprando</button></div>' :''}`;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);
    if (exito){
        document.getElementById('seguirComprando').addEventListener('click', () =>{
            toast.remove();
        });
    }
    setTimeout(() => toast.remove(), 5000);
}
