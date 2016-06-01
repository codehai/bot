$("#sign-in").asEventStream('click').onValue(function(){
      	$("#mymodal").modal("toggle");	
}) 
$(document).asEventStream('click').onValue(function(){
	var status = $("#navbar").attr("aria-expanded");
	if (status == 'true'){
		$("#navbar").collapse('toggle');
	}
})