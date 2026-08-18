setInterval(function(){
    $.get('/notif/dna/badge/',function(data) {
        document.getElementById("notifdnabadge").innerHTML = data.value;
    });
    $.get('/notif/dna/cpv/',function(data) {
        document.getElementById("notifdnacpv").innerHTML = data.value;
    });
    $.get('/notif/dna/po/',function(data) {
        document.getElementById("notifdnapo").innerHTML = data.value;
    });
    $.get('/notif/dna/eval/',function(data) {
        document.getElementById("notifdnaeval").innerHTML = data.value;
    });
    $.get('/notif/dna/proc/',function(data) {
        document.getElementById("notifdnaproc").innerHTML = data.value;
    });
    $.get('/notif/dna/inv/',function(data) {
        document.getElementById("notifdnainv").innerHTML = data.value;
    });
}, 5000);