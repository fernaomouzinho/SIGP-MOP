
var endpoint = '/api/chart/div/proj/year/{{div.id}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Planu',
                data: data.obj1,
                backgroundColor: "rgba(51, 179, 90, 0.38)",
                borderColor: "rgba(51, 179, 90, 1)",
                borderWidth: 1
            },{
                label: 'Total Implementasaun',
                data: data.obj2,
                backgroundColor: "rgba(75, 192, 192, 0.4)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
            }]
        };
        
        const config_projyear = {
            type: 'line',
            data: dt,
            options: pieoption
        };
        const projyear_data = new Chart(
            document.getElementById('projyear_data'),
            config_projyear
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
