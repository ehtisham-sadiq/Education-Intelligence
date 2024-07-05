document.addEventListener('DOMContentLoaded', function () {
    var loginSelect = document.querySelector('select');

    loginSelect.addEventListener('change', function () {
        var location = this.value;
        if (location) {
            window.location.href = location;
        }
    });
});
