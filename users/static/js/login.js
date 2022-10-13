

(function(){
    var inputs = document.querySelectorAll('.form .input-group input');
var button = document.getElementById('login');

    inputs.forEach((input) => {
        input.addEventListener('focusout', (e) => {
            if (e.target.value === "") {
                return e.target.classList.remove('has-value');
            }

            return e.target.classList.add('has-value');
        });
    });
})();

