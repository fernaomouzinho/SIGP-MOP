
var endpoint = '/api/chart/div/proj/status/{{div.id}}/'
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
                    'rgba(75,192,192,0.6)','rgba(54,162,235,0.6)'
                ],
                borderWidth: 1
            }]
        };
        
        const config_projs = {
            type: 'bar',
            data: dt,
            options: baroption
        };
        const projs_data = new Chart(
            document.getElementById('projs_data'),
            config_projs
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
