setInterval(function(){
    $.get('/notif/dna/badge/',function(data) {
        document.getElementById("notifdnabadge").innerHTML = data.value;
    });
    $.get('/notif/dna/eval/',function(data) {
        document.getElementById("notifdnaeval").innerHTML = data.value;
    });
    $.get('/notif/dna/eval/disp/',function(data) {
        document.getElementById("notifdnaevaldisp").innerHTML = data.value;
    });
    $.get('/notif/dna/proc/',function(data) {
        document.getElementById("notifdnaproc").innerHTML = data.value;
    });
    $.get('/notif/dna/inv1/',function(data) {
        document.getElementById("notifdnainv1").innerHTML = data.value;
    });
    $.get('/notif/dna/inv/disp/',function(data) {
        document.getElementById("notifdnainvdisp").innerHTML = data.value;
    });
}, 5000);