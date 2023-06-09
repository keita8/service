
    
    $(document).ready(function(){
        function renderChart(id, data, labels) {

       const ctx = $('#' + id)


        console.log(ctx)
      
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: labels,
            datasets: [{
              label: 'Revenue generée',
              data: data,
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
            
        }
    
    
    
    
    
    
    
       function getSalesData(id, type){
            var url = "/analytics/sales/data/"
            var method = "GET"
            var data = {"type":type}

                
            $.ajax({
                url:url,
                method:method,
                data:data,
                success: function(responseData){

                    renderChart(id, responseData.data, responseData.labels)
                },
                error: function(error){

                    alert("Une erreur est survenue !!!")
                }
            })

       }



       var chartsToRender = $('.keita-render-chart')

       $.each(chartsToRender, function(index, html){
            var $this = $(this)
            if ($this.attr('id') && $this.attr('data-type')) { 
                getSalesData($this.attr('id'), $this.attr('data-type'))
                
            }
       })







        var url2 = "/analytics/sales/data/"
        var method2 = "GET"
        var data2 = {"type":"4week"}
    
        $.ajax({
            url:url2,
            method:method2,
            data:data2,
            success: function(responseData){
                console.log(responseData)
                renderChart("fourWeekSales", responseData.data, responseData.labels)
            },
            error: function(error){
                console.log(error)
                alert("Une erreur est survenue !!!")
            }
        })
    })

