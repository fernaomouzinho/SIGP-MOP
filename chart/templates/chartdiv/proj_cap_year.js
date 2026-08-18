
var endpoint = '/api/chart/div/proj/cap/{{div.id}}/{{year}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: ["rgba(51,179,90,0.6)", "#FF6384", "#FFCE56"],
                borderWidth: 1
            }]
        };
        
        const config_projcap = {
            type: 'pie',
            data: dt,
            options: pieoption
        };
        const projcap_data = new Chart(
            document.getElementById('projcap_data'),
            config_projcap
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
