$("#sign-in").asEventStream('click').onValue(function(){
        $("#mymodal").modal("toggle");	
}) 
$("#sign-up").asEventStream('click').onValue(function(){
        $("#main").hide();
        $("#register").show();
})
$(document).asEventStream('click').onValue(function(){
        var status = $("#navbar").attr("aria-expanded");
        if (status == 'true'){
	$("#navbar").collapse('toggle');
        }
})
// $(document).asEventStream('click','.navbar-brand').onValue(function(){
//         $("#main").removeClass('hide')       
        
// })
// $(document).asEventStream('click','.navbar-brand')
//         .toProperty("")
//         .sampledBy($(document).asEventStream('init'),function(){
//                 console.log('11111111111')
//         })