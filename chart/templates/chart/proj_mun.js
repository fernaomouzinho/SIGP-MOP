{% comment %} 
var endpoint = '/api/chart/proj/mun/'
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

 {% endcomment %}

var endpoint = '/api/chart/proj/mun/';

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const ctx = document.getElementById('projmun_data');

        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Projetu',
                data: data.obj,
                backgroundColor: "rgba(54,162,235,0.6)",
                borderWidth: 1
            }]
        };

        const projmun_data = new Chart(ctx, {
            type: 'bar',
            data: dt,
            options: {
                ...baroption,
                onClick: function(evt) {
                const points = this.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

                if (points.length) {
                    const first = points[0];
                    const index = first._index;          
                    const datasetIndex = first._datasetIndex;

                    if (index !== undefined && datasetIndex !== undefined) {
                        const id = data.id[index];     
                        console.log("Clicked label:", data.label[index], "ID:", id);
                        window.location.href = `/report/proj/mun/list/${id}/`;
                    } else {
                        console.error("⚠ Could not resolve index or datasetIndex", first);
                    }
                } else {
                    console.warn("⚠ No active elements found for this click");
                }
            },
                hover: { mode: 'nearest', intersect: true },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.dataset.label}: ${ctx.formattedValue}`
                        }
                    }
                }
            }
        });
    },
    error: function(error_data){
        console.error("Error loading data:", error_data);
    }
});