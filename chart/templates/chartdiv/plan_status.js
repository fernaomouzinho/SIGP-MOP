
var endpoint = '/api/chart/div/plan/status/{{div.id}}/'
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
                    'rgba(255,99,132,0.6)','rgba(54,162,235,0.6)','rgba(255,205,86,0.6)',
                    'rgba(153,204,0,0.6)','rgba(51,179,90,0.6)'
                ],
                borderWidth: 1
            }]
        };
        
        const config_plan = {
            type: 'bar',
            data: dt,
            options: baroption
        };
        const plan_data = new Chart(
            document.getElementById('plan_data'),
            config_plan
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
