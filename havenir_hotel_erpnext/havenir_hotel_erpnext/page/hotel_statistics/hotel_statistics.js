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
		let $btn = this.page.set_primary_action('Refresh', () => this.get_data(), 'octicon octicon-plus')
		this.make();
	},

	// make page
	make: function(){
		// grab the class
		let me = $(this);
		let scrtag = document.createElement('script');
		let scrtag1 = document.createElement('script');
		let scrtag2 = document.createElement('script');
		let scrtag3 = document.createElement('script');
		let scrtag4 = document.createElement('script');
		scrtag.src = "https://www.gstatic.com/charts/loader.js"
		scrtag.type = "text/javascript";
		document.head.appendChild(scrtag);
		scrtag1.src = "https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js"
		document.head.appendChild(scrtag1);
		scrtag2.src = "https://cdn.datatables.net/1.11.3/js/dataTables.bootstrap4.min.js"
		document.head.appendChild(scrtag2);
		scrtag3.src = "https://cdn.datatables.net/fixedheader/3.2.0/js/dataTables.fixedHeader.min.js"
		document.head.appendChild(scrtag3);
		// append script tage to page
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
			// get data
			this.get_data()
	},
	get_data: function(){
		frappe.call({
				method: "havenir_hotel_erpnext.havenir_hotel_erpnext.page.hotel_statistics.hotel_statistics.render", //dotted path to server method
				callback: function(r) {
						// code snippet
						document.querySelector('#_content').innerHTML = r.message.template
						res = r.message;
						google.charts.load('current', {'packages':['corechart']});
						google.charts.setOnLoadCallback(roomOccupancy);

						// Draw the chart and set the chart values
						// start room occupancy
						function roomOccupancy() {
							var data = google.visualization.arrayToDataTable([
							['Room', 'Occupancy'],
							['Reserved', res.reserved],
							['Checked In', res.checked_in],
							['Available', res.available],
							['Room Service', res.room_service]
						]);

							// Optional; add a title and set the width and height of the chart
							var options = {'title':'Room Occupancy', 'width':280, 'height':100};
							// Display the chart inside the <div> element with id="piechart"
							var chart = new google.visualization.PieChart(document.getElementById('room_occupancy'));
							chart.draw(data, options);
						}
						// end room occupancy

						// INITILIAZE TABLE
							// update hous keeping table
							// console.log(res.house_keeping)
							document.querySelector("#housekeeping-tbody").innerHTML = res.house_keeping;
								var table = $('#housekeeping-table').DataTable( {
										fixedHeader: true,
										"lengthMenu": [[5, 10, 20, -1], [5, 10, 20, "All"]]
								} );

				}
		})
	}
	// end of class

})
