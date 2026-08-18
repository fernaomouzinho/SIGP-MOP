
var endpoint = '/chart/api/pay/ann/dash/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total',
                data: data.obj,
                backgroundColor: [
                    'rgba(75,192,192,1)','rgba(255,206,86,1)','rgba(203,203,203,1)',
                    'rgba(255,99,132,1)','rgba(51,179,90,1)'
                ],
                borderWidth: 1
            }]
        };
        
        const config_paydash = {
            type: 'bar',
            data: dt,
            options: curbaroption
        };
        const paydash_data = new Chart(
            document.getElementById('paydash_data'),
            config_paydash
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
