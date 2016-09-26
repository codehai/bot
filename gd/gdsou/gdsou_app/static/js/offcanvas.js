$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });
});

$(".visible-xs button").click(function(e){
    console.log(e);
    button = $(e.currentTarget);
    if(button.find('span').hasClass("glyphicon-chevron-left")){
        button.find('span').removeClass("glyphicon-chevron-left");
        button.find('span').addClass("glyphicon-chevron-right");
        
    }else{
        button.find('span').removeClass("glyphicon-chevron-right");
        button.find('span').addClass("glyphicon-chevron-left");
    }
})