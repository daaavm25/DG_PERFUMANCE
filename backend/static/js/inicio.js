document.addEventListener('DOMContentLoaded', async () =>{
    const idsNovedades = [2, 14, 6, 15, 7, 11];
    const productGrid = document.querySelector('.product-grid');

    try {
        const response = await fetch (`api/perfumes`);
        if (!response.ok) throw new Error("Error al cargar perfumes");
        const productos = await response.json()

        const novedades = productos.filter(p => idsNovedades.includes(p.id));
        if (novedades.length === 0){
            productGrid.innerHTML = "<p>No hay novedades disponibles.</p>"
            return;
        }
        productGrid.innerHTML = novedades.map(p => 
            `<a href="producto-detalle.html?id=${p.id}" class="product-card">
            <img src="${p.imagen_url}" alt="${p.nombre}">
            <h3>${p.nombre}</h3>
            </a>`
        ).join("");
    }catch (error){
        console.error("Error en inicio.js", error);
        productGrid.innerHTML = "<p>Error al cargar productos.</p>"
    }
});