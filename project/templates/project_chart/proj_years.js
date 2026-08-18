
var endpoint = '/api/project/years/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total',
                data: data.obj,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                // backgroundColor: [
                //     '#8dd3c7','#ffffb3','#bebada','#80b1d3','#fb8072','#fdb462'
                // ],
                borderWidth: 1
            }]
        };
        
        const config_projyears = {
            type: 'bar',
            data: dt,
            options: baroption
        };
        const projyears_data = new Chart(
            document.getElementById('projyears_data'),
            config_projyears
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
