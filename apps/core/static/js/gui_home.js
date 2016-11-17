
$(document).ready(function(){
	function update_list() {
		$.ajax({
			type: "GET",
			url: "/gui_home",
			data: {}
		}).done(function(tr_lookup){
			$("#body_home").empty();
			$("#body_home").append(tr_lookup);
			setTimeout(update_list, 500);

		});
	}

	update_list();
});