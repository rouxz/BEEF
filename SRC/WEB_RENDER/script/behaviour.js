/* clear space of name */	
'use strict';
(function(){
	
	// displaying a split per quarter
	var quarter_split_charts = function(id, mydata){
		//Get context with jQuery - using jQuery's .get() method.
		var ctx = $(id).get(0).getContext("2d");
		//This will get the first returned node in the jQuery collection.
		var chart = new Chart(ctx);
		var data = {
			labels : ["Q1","Q2","Q3","Q4","Annual"],
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
					title : "RPK"
				},
				{
					fillColor : "rgba(81, 140, 252,0.7)",
					strokeColor : "rgba(81, 140, 252,1)",
					data : mydata.yield,
					title : "yield"
				},
				{
					fillColor : "rgba(255, 0, 0,0.7)",
					strokeColor : "rgba(255, 0, 0,1)",
					data : mydata.RASK,
					title : "RASK"
				}
			]
		};
		
		var options = {
			animation : true,

			//Number - Number of animation steps
			animationSteps : 60,
			
			//String - Animation easing effect
			animationEasing : "easeOutQuart",

			//Function - Fires when the animation is complete
			onAnimationComplete : null
		};
		
		// actually draw the chart
		chart.Bar(data, options);
	
	
		//add the legend
		legend($(id + "_legend").get(0), data);
	}
	
	
	// displaying chart with a split per flow
	var flow_split_charts = function(id, mydata){
		//Get context with jQuery - using jQuery's .get() method.
		var ctx = $(id).get(0).getContext("2d");
		//This will get the first returned node in the jQuery collection.
		var chart = new Chart(ctx);
		var data = {
			labels : ["All flows","Local","SH-MH", "MH-MH","Long-haul"],
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
		
		var options = {
			animation : true,

			//Number - Number of animation steps
			animationSteps : 60,
			
			//String - Animation easing effect
			animationEasing : "easeOutQuart",

			//Function - Fires when the animation is complete
			onAnimationComplete : null
		};
		
		// actually draw the chart
		chart.Bar(data, options);
	
	
		//add the legend
		legend($(id + "_legend").get(0), data);
	
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