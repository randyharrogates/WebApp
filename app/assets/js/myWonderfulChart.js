
// define ctx as variable for chart
var ctx = document.getElementById("myWonderfulChart").getContext("2d");
// use ajax to get data from endpoint
$.ajax({
	url: "/getDashboard",
	type: "GET",
	data: {},
	// If error alert with error message
	error: function () {
		alert("Error");
	},
	// if success, render chart
	success: function (data) {
		console.log(data);
		var myWonderfulChart = new Chart(ctx, {
			type: "line",
			data: {
				//Labels for xAxis (dates)
				labels: data.xAxis,
				datasets: [],
			},
			options: {
				responsive: true,
				maintainaspectratio: false,
				title: {
					display: true,
					text: "Total daily booking income for each hotel",
				},
			}
		});
		// Push relevant data and pupoulate into chart
		for (i = 0; i < data.labels.length; i++) {
			myWonderfulChart.data.datasets.push({
				label: data.labels[i],
				type: "line",
				borderColor: "#" + (0x1100000 + Math.random() * 0xffffff).toString(16).substr(1, 6),
				backgroundColor: "rgba(249, 238, 236, 0.74)",
				data: data.prices[i],
				spanGaps: true,
			});
			myWonderfulChart.update();
		}
	},
});
