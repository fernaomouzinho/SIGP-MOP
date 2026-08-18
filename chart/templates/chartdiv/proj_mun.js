
var endpoint = '/api/chart/div/proj/mun/{{div.id}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: "rgba(54,162,235,0.6)",
                borderWidth: 1
            }]
        };
        
        const config_projmun = {
            type: 'bar',
            data: dt,
            options: baroption
        };
        const projmun_data = new Chart(
            document.getElementById('projmun_data'),
            config_projmun
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
