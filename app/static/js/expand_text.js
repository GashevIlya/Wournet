document.addEventListener('click', function (ev) {
    if (ev.target.classList.contains('expand-text')) {
        if (ev.target.innerHTML === 'Развернуть') {
            document.getElementById(`collapse-${ev.target.dataset.collapseId}`).style.maxHeight='100%';
            ev.target.innerHTML='Свернуть';
        } else {
            document.getElementById(`collapse-${ev.target.dataset.collapseId}`).style.maxHeight='150px';
            ev.target.innerHTML='Развернуть';
        }
    }
})


