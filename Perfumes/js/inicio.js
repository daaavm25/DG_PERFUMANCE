const idsNovedades = [2, 14, 6, 15, 7, 11];

const productGrid = document.querySelector('.product-grid');

if (productGrid) {
    fetch('js/productos.json')
        .then(response => response.json())
        .then(productos => {
            
            const productosNovedades = idsNovedades.map(id => {
                return productos.find(p => p.id == id);
            }).filter(p => p != null); 

            let htmlParaInsertar = ''; 
            
            for (const producto of productosNovedades) {
                htmlParaInsertar += `
                    <a href="producto-detalle.html?id=${producto.id}" class="product-card">
                        <img src="${producto.imagen}" alt="Perfume ${producto.nombre}">
                        <h3>${producto.nombre}</h3>
                    </a>
                `;
            }

            productGrid.innerHTML = htmlParaInsertar;
        })
        .catch(error => {
            console.error('Error al cargar las novedades:', error);
            productGrid.innerHTML = '<p>No se pudieron cargar las novedades.</p>';
        });
}