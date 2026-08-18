setInterval(function(){
    $.get('/notif/div/badge/',function(data) {
        document.getElementById("notifdivbadge").innerHTML = data.value;
    });
    $.get('/notif/div/eval/',function(data) {
        document.getElementById("notifdiveval").innerHTML = data.value;
    });
    $.get('/notif/div/eval/disp/',function(data) {
        document.getElementById("notifdivevaldisp").innerHTML = data.value;
    });
    $.get('/notif/div/inv/disp/',function(data) {
        document.getElementById("notifdivinvdisp").innerHTML = data.value;
    });
    $.get('/notif/div/inv/',function(data) {
        document.getElementById("notifdivinv").innerHTML = data.value;
    });
    $.get('/notif/div/ver/',function(data) {
        document.getElementById("notifdivver").innerHTML = data.value;
    });
}, 5000);
