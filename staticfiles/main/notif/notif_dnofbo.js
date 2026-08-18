setInterval(function () {
    $.get('/notif/dnofbo/badge/', function (data) {
        document.getElementById("notifdnofbobadge").innerHTML = data.value;
    });
    $.get('/notif/dnofbo/ev/', function (data) {
        document.getElementById("notifdnofboev").innerHTML = data.value;
    });
}, 5000);
