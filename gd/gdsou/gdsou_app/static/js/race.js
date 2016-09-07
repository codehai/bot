$(".visible-xs tr").click(function(e){
    tr = $(e.currentTarget);
    tbody = tr.parent();
    trs = tbody.find("tr");
    if(tr.find("span").hasClass("glyphicon-chevron-right")){    
        $(trs[0]).find("span").removeClass("glyphicon-chevron-right");
        $(trs[0]).find("span").addClass("glyphicon-chevron-down");
        for(i=1;i<trs.length;i++){
            $(trs[i]).removeClass("hidden");
        }
    }else{
        $(trs[0]).find("span").addClass("glyphicon-chevron-right");
        $(trs[0]).find("span").removeClass("glyphicon-chevron-down");
        for(i=1;i<trs.length;i++){
            $(trs[i]).addClass("hidden");
        }
    }
})