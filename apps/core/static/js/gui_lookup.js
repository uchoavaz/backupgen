
$(document).ready(function(){
	function update_list() {
		$.ajax({
			type: "GET",
			url: "/gui_lookup",
			data: {backup_name:$("#backup_name").val()}
		}).done(function(tr_lookup){
			$("#body_lookups").empty();
			$("#body_lookups").append(tr_lookup);
			setTimeout(update_list, 500);

		});
	}

	update_list();
});