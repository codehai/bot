/*
 * post请求
 */
function post(URL, PARAMS) {      
    var temp = document.createElement("form");      
    temp.action = URL;      
    temp.method = "post";      
    temp.style.display = "none";      
    for (var x in PARAMS) {      
        var opt = document.createElement("textarea");      
        opt.name = x;      
        opt.value = PARAMS[x];      
        // alert(opt.name)      
        temp.appendChild(opt);      
    }      
    document.body.appendChild(temp);      
    temp.submit();      
    return temp;
}

function search(){
	var searchInfo = $("#searchInfo").val();
	if(escape(searchInfo).indexOf("%u") < 0) 
	{ 
		//不包含中文，统一环   2014-04-121214
		if(searchInfo.length<10){
			$("#contentWaringInfo").html($("#searchInfo").val());
			$('#message').modal('show');
			return ;
		}else{
			var part1 = searchInfo.substring(0,4);
			var part2 = searchInfo.substring(4,5);
			var part3 = searchInfo.substring(5,7);
			var part4 = searchInfo.substring(7,8);
			var part5 = searchInfo.substring(8,searchInfo.length);
			if(part2!="-"){
				if(getPhoneType()){
					alert("抱歉，您输入的内容：<span id='contentWaringInfo' style='color:#00c;'>"+$("#searchInfo").val()+"</span> &nbsp;格式错误！");
				}else{
					$("#contentWaringInfo").html($("#searchInfo").val());
					$('#message').modal('show');
				}
				return ;
			}
			if(part4!="-"){
				if(getPhoneType()){
					alert("抱歉，您输入的内容：<span id='contentWaringInfo' style='color:#00c;'>"+$("#searchInfo").val()+"</span> &nbsp;格式错误！");
				}else{
					$("#contentWaringInfo").html($("#searchInfo").val());
					$('#message').modal('show');
				}
				return ;
			}
			if(part5.length<3){
				if(getPhoneType()){
					alert("抱歉，您输入的内容：<span id='contentWaringInfo' style='color:#00c;'>"+$("#searchInfo").val()+"</span> &nbsp;格式错误！");
				}else{
					$("#contentWaringInfo").html($("#searchInfo").val());
					$('#message').modal('show');
				}
				return ;
			}
		}
	}
	post("search.html",{searchInfo:$("#searchInfo").val()});
}


function searchNoLogin(){
	var searchInfo = $("#searchInfo").val();
	if(escape(searchInfo).indexOf("%u") < 0) 
	{ 
		//不包含中文，统一环   2014-04-121214
		if(searchInfo.length<10){
			if(getPhoneType()){
				alert("抱歉，您输入的内容：<span id='contentWaringInfo' style='color:#00c;'>"+$("#searchInfo").val()+"</span> &nbsp;格式错误！");
			}else{
				$('#message').modal('show');
			}
			return ;
		}else{
			var part1 = searchInfo.substring(0,4);
			var part2 = searchInfo.substring(4,5);
			var part3 = searchInfo.substring(5,7);
			var part4 = searchInfo.substring(7,8);
			var part5 = searchInfo.substring(8,searchInfo.length);
			if(part2!="-"){
				if(getPhoneType()){
					alert("抱歉，您输入的内容："+$("#searchInfo").val()+" 格式错误！");
				}else{
					$('#message').modal('show');
				}
				return ;
			}
			if(part4!="-"){
				if(getPhoneType()){
					alert("抱歉，您输入的内容："+$("#searchInfo").val()+" 格式错误！");
				}else{
					$('#message').modal('show');
				}
				return ;
			}
			if(part5.length<3){
				if(getPhoneType()){
					alert("抱歉，您输入的内容："+$("#searchInfo").val()+" 格式错误！");
				}else{
					$('#message').modal('show');
				}
				return ;
			}
		}
	}
	if(getPhoneType()){
		alert("抱歉，请先登陆再进行查询！");
	}else{
		$('#loginInfo').modal('show');
	}
}

function loginSearch()
{
		var username = $("#username_search").val();
		if(username==""){
			$("#username_search_span").html("请填写用户名");
			return false;
		}
		if(username.length<3||username.length>15)
		{
			$("#username_search_span").html("用户名应为3-15位");
			return false;
		}
		$("#username_search_span").html("");
		if ($("#password_search").val()==""){
			$("#password_search_span").html("请输入密码");
			return  false;
		}else if($("#password_search").val().length<6){
			$("#password_search_span").html("密码至少6位");
			return false;
		}
		$("#password_search_span").html("");
		postLoginSearch();
		//loginSearch  即 在未登录的情况下提示登陆 并跳转到登陆页面        postLoginSearch();
}

function postLoginSearch(){
	$.ajax({
        type: "POST",
        url: "login.html",
        data: {username:$("#username_search").val(),password:$("#password_search").val()},
        dataType: "json", 
        contentType: "application/x-www-form-urlencoded; charset=utf-8", 
        success: function(data){
        	if(data.status=="success"){
				location.reload();
			}else{
				alert(data.value);
				//用户信息完整，不做操作,更新页面而已
			}
        }
    });
}

function memberInfoSearch(){
	alert("由于网站用户太多，为保证网站正常运行，目前只有开通网站年会员才能进行查询，年会员50元包年，开通日期截止至11月13号，逾期将停止用户开通！剩余用户将进行封号清理！高级查询包年费用50元         联系qq:835263300  电话:18050282442 ");
	$('#allInfo').modal('show');
}

function clickToSeeAlll(searchRecordId){
	if(getPhoneType()){
		alert("查看该鸽主的所参加的所有比赛成绩，需要开通年费会员无限次数查询。高级查询包年费用50元，开通联系qq：835263300，微信：zgsaige");
			//sureToSeeAll(searchRecordId);
	}else{
		$('#allInfo').modal('show');
	}
}

function clickToSeeAlllByCoin(searchRecordId){
	if(getPhoneType()){
		if(confirm("查看该鸽主的所参加的所有比赛成绩，需要扣除2鸽币，您确定查看吗？")){
			sureToSeeAll(searchRecordId);
		}else{
			return false;
		}
	}else{
		$('#allInfo').modal('show');
	}
}


function sureToSeeAll(searchRecordId){
	$.ajax({ 
		type: "post", 
		url: "paidForSearchResult.html?searchRecordId="+searchRecordId, 
		dataType: "json", 
		success: function (data) { 
			if(data.status=="success"){
				post("searchPaid.html",{searchRecordId :searchRecordId});
			}else{
				//积分不够
				if(getPhoneType()){
					if(confirm("抱歉，您的鸽币不够！充值请点击确定")){
						 window.location.href="help/254313.html";
						 return true;
					}else return false;
				}else{
					$('#coinNotEnough').modal('show');
					$('#allInfo').modal('hide');
				}
				//用户信息完整，不做操作,更新页面而已
			}
		}, 
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
			location.reload();
		} 
	});
}



//这个就是键盘触发的函数
var SubmitOrHidden = function(evt){
evt = window.event || evt;
if(evt.keyCode==13){//如果取到的键值是回车
  //do something       
		search();
	 // $("#"+currentIdStr).modal('hide');
	//
}else{
//其他键  dosomething
}
};

window.document.onkeydown=SubmitOrHidden;//当有键按下时执行函数