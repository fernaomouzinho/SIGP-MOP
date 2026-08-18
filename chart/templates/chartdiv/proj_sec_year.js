
var endpoint = '/api/chart/div/proj/sec/{{div.id}}/{{year}}/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: ["rgba(75,192,192,1)","rgba(51,179,90,1)", "#rgba(255,99,132,1)", "rgba(255,206,86,1)",
                "rgba(75,192,192,0.6)","rgba(51,179,90,0.6)","#rgba(255,99,132,0.6)","rgba(255,206,86,0.6)"],
                borderWidth: 1
            }]
        };
        
        const config_projsec = {
            type: 'doughnut',
            data: dt,
            options: pieoption
        };
        const projsec_data = new Chart(
            document.getElementById('projsec_data'),
            config_projsec
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
