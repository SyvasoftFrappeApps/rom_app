
frappe.ui.form.on("Reset Inventory Summary", {
	// refresh start
	refresh(frm) {


		frm.add_custom_button('Reset Inv. Summary ', function(){

				let branch = frm.doc.branch;
				let start_date = frm.doc.recalculate_inventory_summary_date;
				if(!branch) {
					alert('branch is empty');
					return;

				}

				if(!start_date) {
					alert('start_date is empty');
					return;
				}

				console.log('branch ',branch);
				console.log('start_date ',start_date);
// ------------------reset_inventory_summary---------------------------
				let api_url = "rom_app.scheduled_tasks.reset_inventory_summary"
				frappe.call(
					{
						method: api_url,
						args:
						{
							branch: branch,
							start_date: start_date
						},
						async:false,
						freeze:true,
						freeze_message: "Processing",
						callback: function(res)
						{
							console.log(res.message);
						}
					},);
				// ------------------reset_inventory_summary---------------------------
				
				// let api_url = "rom_app.scheduled_tasks.inventory_summary"
				// frappe.call(
				// 	{
				// 		method: api_url,
				// 		args:
				// 		{
				// 			P_branch: branch,
				// 			p_date: start_date
				// 		},
				// 		async:false,
				// 		freeze:true,
				// 		freeze_message: "Processing",
				// 		callback: function(res)
				// 		{
				// 			console.log(res.message);
				// 		}
				// 	},);

		});

		 // }),
	// }
	// refresh end

	}

}

);
