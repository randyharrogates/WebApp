
function getChartDates() {}
var ctx = document.getElementById("myChart").getContext("2d");

$.ajax({
	url: "/getDashboard",
	type: "GET",
	data: {},
	error: function () {
		alert("Error");
	},

	success: function (data, status, xhr) {
		console.log(data);
		var myChart = new Chart(ctx, {
			type: "line",
			data: {
				labels: data.xAxis,
				datasets: [],
			},
			options: {
				responsive: true,
				maintainaspectratio: false,
				title: {
					display: true,
					text: "World population per region (in millions)",
				},
			},
		});

		for (i = 0; i < data.labels.length; i++) {
			myChart.data.datasets.push({
				label: data.labels[i],
				type: "line",
				borderColor: "#" + (0x1100000 + Math.random() * 0xffffff).toString(16).substr(1, 6),
				backgroundColor: "rgba(249, 238, 236, 0.74)",
				data: data.prices[i],
				spanGaps: true,
			});
			myChart.update();
		}
	},
});
