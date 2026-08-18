setInterval(function(){
    $.get('/notif/dep/badge/',function(data) {
        document.getElementById("notifdepbadge").innerHTML = data.value;
    });
    $.get('/notif/dep/ver/',function(data) {
        document.getElementById("notifdepver").innerHTML = data.value;
    });
}, 5000);