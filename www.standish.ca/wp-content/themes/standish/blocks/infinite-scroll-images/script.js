const initInfiniteScroll = function (blockElement) {
    if (typeof gsap === 'undefined') return;

    const track = blockElement.querySelector('.infinite-scroll-images__track');
    const items = blockElement.querySelectorAll('.infinite-scroll-images__item');
    
    const halfCount = items.length / 2;

    if (!track || items.length === 0 || !items[halfCount]) return;

    // On attend un peu que le navigateur applique le CSS (les rem, la taille, etc.)
    setTimeout(() => {
        // Force la position à 0 avant le calcul pour éviter les décalages
        gsap.set(track, { x: 0 });

        // On prend les coordonnées exactes (en pixels) sur l'écran
        const firstItemPos = items[0].getBoundingClientRect().left;
        const loopItemPos = items[halfCount].getBoundingClientRect().left;
        
        // La distance parfaite = la position du double MOINS la position du premier
        const loopDistance = loopItemPos - firstItemPos;

        // Si pour une raison quelconque la distance est nulle (ex: display: none), on stoppe
        if (loopDistance <= 0) return;

        // On lance la boucle parfaite
        gsap.killTweensOf(track);
        gsap.to(track, {
            x: -loopDistance,
            duration: 30, // Ajuste la vitesse ici
            ease: "none",
            repeat: -1
        });
    }, 800); 
};

window.addEventListener('load', function () {
    const blocks = document.querySelectorAll('.infinite-scroll-images');
    blocks.forEach(block => initInfiniteScroll(block));
});