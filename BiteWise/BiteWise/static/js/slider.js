document.addEventListener('DOMContentLoaded', function () {
    const slider = document.querySelector('.ingredients-options-container');
    let isDown = false;
    let startX;
    let scrollLeft;

    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        slider.classList.add('active');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });

    
    slider.addEventListener('mouseleave', () => {
        isDown = false;
        slider.classList.remove('active');
    });

    slider.addEventListener('mouseup', () => {
        isDown = false;
        slider.classList.remove('active');
    });

    
    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Multiplique por 2 para aumentar a sensibilidade
        slider.scrollLeft = scrollLeft - walk;
    });


    let startTouchX;
    slider.addEventListener('touchstart', (e) => {
        startTouchX = e.touches[0].pageX;
        scrollLeft = slider.scrollLeft;
    });

    slider.addEventListener('touchmove', (e) => {
        const touchX = e.touches[0].pageX;
        const walk = (startTouchX - touchX) * 2;
        slider.scrollLeft = scrollLeft + walk;
    });
});
