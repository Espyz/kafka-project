window.onload = function() {
    document.addEventListener('click', function(event) {
        const target = event.target;
        
        if (target.tagName === 'BUTTON') {
            target.classList.add('clicked');
        }
    })
}