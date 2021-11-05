frappe.pages['restaurant-dashboard'].on_page_load = function(wrapper) {
	new MyPage(wrapper);
}


// PAGE CONTENT
MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Restaurant Daily Monitoring',
			single_column: true
		});
		// make page
		// let $btn = this.page.set_primary_action('Refresh', () => this.get_data(), 'octicon octicon-plus')
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
				<div class="row">
					<div class="col-md-12">
						<form class="form-inline" id="search_form">
						  <div class="form-group mb-2">
							<label for="from_date" class=""><b>From Date</b></label>
							<input type="date" class="form-control" id="from_date" value="" name="from_date">
						  </div>
						  <div class="form-group mx-sm-3 mb-2">
							<label for="to_date" class="">To Date</label>
							<input type="date" class="form-control" id="to_date" name="to_date">
						  </div>
						  <button type="submit" class="btn btn-primary mb-2">Generate</button>
						</form>
					</div>
				</div>
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
			let get_data = this.get_data;
			get_data({from_date:null, to_date:null});
			// process form
			  $("#search_form").submit(function (e) {
			   e.preventDefault();
			    var formData = {
			      from_date: $("#from_date").val(),
			      to_date: $("#to_date").val(),
			    };
				if(formData.from_date && formData.to_date){
					get_data(formData);
				} else if(new Date(formData.from_date) > new Date(formData.to_date)){
					frappe.throw("From date cannot be greater than To date.");
				} else {
					frappe.throw("From and To date must be selected");
					return;
				}

			  });

	},
	get_data: function(_dict){
		frappe.call({
				method: "havenir_hotel_erpnext.havenir_hotel_erpnext.page.restaurant_dashboard.restaurant_dashboard.render", //dotted path to server method
				args: _dict,
				callback: function(r) {
						// code snippet
						document.querySelector('#_content').innerHTML = r.message.template
						google.charts.load("current", {packages:["corechart"]});
						google.charts.setOnLoadCallback(drawChart);
						function drawChart() {
							let datacolumn = [["Element", "Sold", { role: "bar" } ]];
							r.message.top_10_today.forEach((item, i) => {
								datacolumn.push([item.item_code, item.qty, ''])
							});

							var data = google.visualization.arrayToDataTable(datacolumn);

							var view = new google.visualization.DataView(data);
							view.setColumns([0, 1,
															 { calc: "stringify",
																 sourceColumn: 1,
																 type: "string",
																 role: "annotation" },
															 2]);

							var options = {
								title: "TOP 10 TODAY",
								width: '100%',
								height: 300,
								bar: {groupWidth: "50%"},
								legend: { position: "none" },
							};
							var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
							chart.draw(view, options);
					}


						// res = r.message;
						// google.charts.load('current', {'packages':['corechart']});
						// google.charts.setOnLoadCallback(roomOccupancy);
						//
						// // Draw the chart and set the chart values
						// // start room occupancy
						// function roomOccupancy() {
						// 	var data = google.visualization.arrayToDataTable([
						// 	['Room', 'Occupancy'],
						// 	['Reserved', res.reserved],
						// 	['Checked In', res.checked_in],
						// 	['Available', res.available],
						// 	['Room Service', res.room_service]
						// ]);
						//
						// 	// Optional; add a title and set the width and height of the chart
						// 	var options = {'title':'Room Occupancy', 'width':280, 'height':100};
						// 	// Display the chart inside the <div> element with id="piechart"
						// 	var chart = new google.visualization.PieChart(document.getElementById('room_occupancy'));
						// 	chart.draw(data, options);
						// }
						// // end room occupancy
						//
						// // INITILIAZE TABLE
						// 	// update hous keeping table
						// 	// console.log(res.house_keeping)
						// 	document.querySelector("#housekeeping-tbody").innerHTML = res.house_keeping;
						// 		var table = $('#housekeeping-table').DataTable( {
						// 				fixedHeader: true,
						// 				"lengthMenu": [[5, 10, 20, -1], [5, 10, 20, "All"]]
						// 		} );

				}
		})
	}
	// end of class

})
