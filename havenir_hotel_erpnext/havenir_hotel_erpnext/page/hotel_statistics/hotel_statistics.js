frappe.pages['hotel-statistics'].on_page_load = function(wrapper) {
	new MyPage(wrapper);
}


// PAGE CONTENT
MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Hotel Dashboard',
			single_column: true
		});
		// make page
		this.make();
	},

	// make page
	make: function(){
		// grab the class
		let me = $(this);
		let scrtag = document.createElement('script');
		scrtag.src = "https://www.gstatic.com/charts/loader.js"
		scrtag.type = "text/javascript";
		// append script tage to page
	  document.head.appendChild(scrtag);
		// push dom elemt to page
	// HTML CONTENT
	let body = `
				<div id="_content">

				</div>
	`;
	// frappe.estate_app_page = {}
	frappe.estate_app_page = {
		body: body
	}

	let content_ = `<h1>Dashboard</h1>`;

		$(frappe.render_template(body, this)).appendTo(this.page.main);
		frappe.call({
        method: "havenir_hotel_erpnext.havenir_hotel_erpnext.page.hotel_statistics.hotel_statistics.render", //dotted path to server method
        callback: function(r) {
            // code snippet
						document.querySelector('#_content').innerHTML = r.message
						// $(frappe.render_template(r.message, this)).appendTo(this.page.main);
						// Load google charts
						let scrtag = document.createElement('script');
						scrtag.src = "https://www.gstatic.com/charts/loader.js"
						scrtag.type = "text/javascript";
						// append script tage to page
					  document.head.appendChild(scrtag);
						google.charts.load('current', {'packages':['corechart']});
						google.charts.setOnLoadCallback(drawChart);

						// Draw the chart and set the chart values
						function drawChart() {
						  var data = google.visualization.arrayToDataTable([
						  ['Room', 'Occupancy'],
							['Free', 2],
						  ['Occupied', 8]
						]);

						  // Optional; add a title and set the width and height of the chart
						  var options = {'title':'Room Occupancy', 'width':300, 'height':110};

						  // Display the chart inside the <div> element with id="piechart"
						  var chart = new google.visualization.PieChart(document.getElementById('room_occupancy'));
						  chart.draw(data, options);
						}
        }
    })
		}
	// end of class
})
