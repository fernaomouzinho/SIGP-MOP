
var endpoint = '/api/chart/div/imp/status/{{div.id}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: [
                    'rgba(54,162,235,0.6)','rgba(255,205,86,0.6)','rgba(255,99,132,0.6)',
                    'rgba(153,204,0,0.6)','rgba(51,179,90,0.6)'
                ],
                borderWidth: 1
            }]
        };
        
        const config_imps = {
            type: 'bar',
            data: dt,
            options: baroption
        };
        const imps_data = new Chart(
            document.getElementById('imps_data'),
            config_imps
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
