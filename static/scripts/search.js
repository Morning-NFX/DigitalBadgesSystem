// This script is used for redirecting the search based on the toggle button
function setSearch(type){
	search_type = type;
	window.localStorage.setItem("badgesearch_state", type);
}

$(document).ready(function() {
	search_type_storage = window.localStorage.getItem("badgesearch_state");
	if(search_type_storage){
		search_type = search_type_storage;
	}else{
		search_type = "badge";
	}

	switch(search_type){
		case "student":
			$("#radio1").prop("checked", true);
			break;
		case "badge":
			$("#radio2").prop("checked", true);
			break;
		default:
			break;
	}

	$('#search_form').on("submit", function(e) {
		e.preventDefault();
		var id = $(this).serializeArray()[0].value;
		if(search_type == "badge"){
			window.location.href = "/badges/" + id;
		}else{
			var hash = CryptoJS.SHA256(id).toString();
			window.location.href = "/student/portfolio/" + hash;
		}
	});
})

