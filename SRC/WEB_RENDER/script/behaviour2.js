/* clear space of name */	
'use strict';
(function(){
	
	// displaying a split per quarter
	var quarter_split_charts = function(id, mydata){

		
		$(id).highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: 'Quarterly KPI split'
            },
            subtitle: {
                text: 'Source: Revenue management'
            },
            xAxis: [{
                categories: ["Q1","Q2","Q3","Q4","Annual"]
            }],
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}%',
                    style: {
                        color: 'black'
                    }
                },
                title: {
                    text: 'YoY Evolution',
                    style: {
                        color: 'black'
                    }
                }
            }],
            tooltip: {
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 120,
                verticalAlign: 'top',
                y: 100,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
            series: [{
                name: 'ASK',
                color: "rgba(201,201,201,0.7)",
                type: 'column',
                data:  mydata.ASK,
                tooltip: {
                    valueSuffix: '%'
                }
            }, {
                name: 'RPK',
                color: "rgba(22,56,120,1)",
                type: 'column',
                data: mydata.RPK,
                tooltip: {
                    valueSuffix: '%'
                }
            }, {
                name: 'Yield',
                color: "rgba(81, 140, 252,1)",
                type: 'column',
                data: mydata.yield,
                tooltip: {
                    valueSuffix: '%'
                }
            }, {
                name: 'RASK',
                color: "rgba(255, 0, 0,1)",
                type: 'spline',
                data: mydata.RASK,
                tooltip: {
                    valueSuffix: '%'
                }
            }]
        });
		
		
	}
	
	
	// displaying chart with a split per flow
	var flow_split_charts = function(id, mydata){

		var data = {

			datasets : [
				{
					fillColor : "rgba(201,201,201,0.7)",
					strokeColor : "rgba(201,201,201,1)",
					data : mydata.ASK,
					title : "ASK"
				},
				{
					fillColor : "rgba(22,56,120,0.7)",
					strokeColor : "rgba(22,56,120,1)",
					data : mydata.RPK,
					title: "RPK"
				},
				{
					fillColor : "rgba(81, 140, 252,0.7)",
					strokeColor : "rgba(81, 140, 252,1)",
					data : mydata.yield,
					title: "Yield"
				}
			]
		};
		
		
	
		$(id).highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: 'Split per flow'
            },
            subtitle: {
                text: 'Source: Revenue management'
            },
            xAxis: [{
                categories: ["All flows","Local","SH-MH", "MH-MH","Long-haul"]
            }],
            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}%',
                    style: {
                        color: 'black'
                    }
                },
                title: {
                    text: 'YoY Evolution',
                    style: {
                        color: 'black'
                    }
                }
            }],
            tooltip: {
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 120,
                verticalAlign: 'top',
                y: 100,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
            series: [{
                name: 'ASK',
                color: "rgba(201,201,201,0.7)",
                type: 'column',
                data:  mydata.ASK,
                tooltip: {
                    valueSuffix: '%'
                }
            }, {
                name: 'RPK',
                color: "rgba(22,56,120,1)",
                type: 'column',
                data: mydata.RPK,
                tooltip: {
                    valueSuffix: '%'
                }
            }, {
                name: 'Yield',
                color: "rgba(81, 140, 252,1)",
                type: 'column',
                data: mydata.yield,
                tooltip: {
                    valueSuffix: '%'
                }
            }]
        });
	}
			

	// load all informations on the webpage		
	var loading = function(){
		//add data information
		$.getJSON("json/json_information.json")
			.done(function(data){
				var info = "<h2>Information</h2>" + "<p class='small_title'>Scope: " + data.scope + "</p>" 
				info +=  "<p class='small_title'>ref data: " + data.reference_data + "</p>" 
				info +=   "<p>" + data.reference_type + "</p>" 
				$("#legend").html(info);
			})
			.fail(function(){
				$("#messager").html("Failed to information about perimeter");
			})
			
			
		
		
		
		// split per flow for Annual and quarters
		$.getJSON("json/json_flow.json")
			.done(function(data){
				$.each(data, function(index, value){
					// console.log(value.chart + " " + value.data);
					flow_split_charts(value.chart, value.data);
				});
			})
			.fail(function(){
				$("#messager").html("Failed to flow information");
			})
			
		// split per quarters no flow
		$.getJSON("json/json_quarter.json")
			/*load meta data of the perimeter */
			.done(function(data){
				$.each(data, function(index, value){
					console.log(value.chart + " " + value.data);
					quarter_split_charts(value.chart, value.data);
				});
			})
			.fail(function(){
				$("#messager").html("Failed to quarter information");
			})
	}
			
	
	
	/* load when the DOM is ready */
	$().ready(function(){
		
		
		loading();
		
		//regulary reload information every minutes
        setInterval("loading()", 60000);
        
         
		
	});			
		
})();