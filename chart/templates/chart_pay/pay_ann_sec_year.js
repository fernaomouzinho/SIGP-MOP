
var endpoint = '/chart/api/pay/ann/sec/{{year}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [
            {
                label: 'Kontratu',
                data: data.obj1,
                backgroundColor: 'rgba(75,192,192,1)',
                borderWidth: 1
            },
            {
                label: 'Pagamentu',
                data: data.obj2,
                backgroundColor: 'rgba(255,206,86,1)',
                borderWidth: 1
            },
            {
                label: 'Balansu',
                data: data.obj3,
                backgroundColor: 'rgba(203,203,203,1)',
                borderWidth: 1
            },
            ]
        };
        
        const config_paysec = {
            type: 'bar',
            data: dt,
            options: groupoption
        };
        const paysec_data = new Chart(
            document.getElementById('paysec_data'),
            config_paysec
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
