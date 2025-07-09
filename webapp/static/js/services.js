    // Gestion des interactions tactiles
    function handleTouchInteractions() {
        if ('ontouchstart' in window) {
            document.querySelectorAll('.grid-item').forEach(item => {
                let touchStartTime = 0;
                item.addEventListener('touchstart', (e) => {
                    touchStartTime = Date.now();
                    item.classList.add('hover');
                });
                item.addEventListener('touchend', (e) => {
                    const touchDuration = Date.now() - touchStartTime;
                    if (touchDuration < 300) {
                        const link = item.querySelector('a');
                        if (link) link.click();
                    }
                    item.classList.remove('hover');
                });
                item.addEventListener('touchmove', () => {
                    item.classList.remove('hover');
                });
            });
        }
    }

    // Initialisation
    window.addEventListener('load', () => {
        handleTouchInteractions();
    });
