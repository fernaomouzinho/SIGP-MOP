
var endpoint = '/api/chart/pay/monthly/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Execusaun',
                data: data.obj,
                backgroundColor: "rgba(51, 179, 90, 0.38)",
                borderColor: "rgba(51, 179, 90, 1)",
                borderWidth: 1
            }]
        };
        
        const config_paymonthly = {
            type: 'line',
            data: dt,
            options: curbaroption
        };
        const paymonthly_data = new Chart(
            document.getElementById('paymonthly_data'),
            config_paymonthly
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
