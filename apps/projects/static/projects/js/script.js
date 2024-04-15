document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.removeAttribute('required');
    });

    const textarae = document.querySelector('textarea')
    textarae.removeAttribute('required');

    const select = document.querySelector('select');
    select.removeAttribute('required');
});


