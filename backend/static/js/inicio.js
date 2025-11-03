document.addEventListener('DOMContentLoaded', async () =>{
    const idsNovedades = [2, 14, 6, 15, 7, 11];
    const productGrid = document.querySelector('.product-grid');

    try {
        const response = await fetch (`/api/catalogo/perfume`, {credentials: "include"});

        if (!response.ok) throw new Error("Error al cargar perfumes");
        const productos = await response.json()

        const novedades = productos.filter(p => idsNovedades.includes(p.id));
        if (novedades.length === 0){
            productGrid.innerHTML = "<p>No hay novedades disponibles.</p>"
            return;
        }
        productGrid.innerHTML = novedades.map(p => 
            `<a href="/producto_detalle?id=${p.id}" class="product-card">
                <img src="${p.imagen_url}" alt="${p.nombre}">
                <h3>${p.nombre}</h3>
            </a>`
        ).join("");
    }catch (error){
        console.error("Error en inicio.js", error);
        productGrid.innerHTML = "<p>Error al cargar productos.</p>"
    }
});

document.addEventListener('DOMContentLoaded', async () =>{
    try{
        const res = await fetch('/api/verificar_sesion', {credentials: "include"});
        if (res.ok){
            const data = await res.json();
            if (data.autenticado){
                const loginLink = document.querySelector('a[href="/login"]');
                if (loginLink) loginLink.computedStyleMap.display = 'none';
                const nav = document.querySelector('nav ul');
                if (nav) {
                    const li = document.getElementById('li');
                    li.innerHTML = `<a href="#" id="logout">Cerrar Sesión (${data.usuario.username})</a>`;
                    nav.appendChild(li);

                    document.getElementById('logout').addEventListener('click', async () =>{
                        await fetch('/api/logout', {
                            method: "POST",
                            credentials: "include"
                        });
                    });
                }
            }
        }
    }catch (error){
        console.error("Error al verificar sesion:", error);
    }
});

document.addEventListener('DOMContentLoaded', async () => {
    try{
        const res = await fetch('/api/sesion', {credentials: "include"});
        const data = await res.json();

        const loginLink = document.getElementById('link-login');
        const logoutLink = document.getElementById('link-logout');

        if (data.login){
            if (loginLink) loginLink.style.display = 'none';
            if (logoutLink) logoutLink.style.display = 'inline-block';
        }else{
            if (loginLink) loginLink.style.display = 'inline-block';
            if (logoutLink) logoutLink.style.display = 'none';   
        }
    }catch (error){
        console.error("Error al verificar sesion.", error);
    }
});