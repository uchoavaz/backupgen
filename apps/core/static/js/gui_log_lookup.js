
$(document).ready(function(){
	function update_list() {
		$.ajax({
			type: "GET",
			url: "/gui_log_lookup",
			data: {backup_pk:$("#backup_pk").val()}
		}).done(function(tr_lookup){
			$("#body_log_lookup").empty();
			$("#body_log_lookup").append(tr_lookup);
			setTimeout(update_list, 500);
		});
	}

	update_list();
});