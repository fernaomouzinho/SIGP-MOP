
var endpoint = '/api/chart/proj/cat/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: ["rgba(51, 179, 90, 1)", "#FF6384", "#FFCE56"],
                borderWidth: 1
            }]
        };
        
        const config_projcat = {
            type: 'polarArea',
            data: dt,
            options: pieoption
        };
        const projcat_data = new Chart(
            document.getElementById('projcat_data'),
            config_projcat
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
