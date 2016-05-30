


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


/*
 * 登陆
 */
function loginIn()
{
		var username = $("#loginUsername").val();
		if(username==""){
			alert("请填写用户名");
			return false;
		}
		if(username.length<3||username.length>15)
		{
			alert("用户名应为3-15位");
			return false;
		}
		if ($("#loginPassword").val()==""){
			alert("请输入密码");
			return  false;
		}else if($("#loginPassword").val().length<6){
			alert("密码至少6位");
			return false;
		}
		postLogin();
}

function postLogin(){
	$.ajax({
        type: "POST",
        url: "login.html",
        data: {username:$("#loginUsername").val(),password:$("#loginPassword").val()},
        dataType: "json", 
        contentType: "application/x-www-form-urlencoded; charset=utf-8", 
        success: function(data){
        	if(data.status=="success"){
				$.cookie('username', $("#loginUsername").val(), { expires: 60 });
				$.cookie('password',$("#loginPassword").val(), { expires:60});
				location.reload();
			}else{
				alert(data.value);
				//用户信息完整，不做操作,更新页面而已
			}
        }
    });
}


/*
 * 退出
 */
function loginOut()
{
	$.ajax({ 
		type: "post", 
		url:"exit.html",
		dataType: "json", 
		success: function (data) { 
			if(data.status=="success"){
				/*$.cookie('username', "", { expires: 60 });
				$.cookie('password',"", { expires:60});*/
				//用户信息不完整，则填写完整信息
				window.location.href="index.html";
			}
		}, 
		error: function (XMLHttpRequest, textStatus, errorThrown) { 
			location.reload();
		} 
	});
}

//js获取项目根路径，如： http://localhost:8083/uimcardprj
function getRootPath(){
//	获取当前网址，如： http://localhost:8083/uimcardprj/share/meun.jsp
	var curWwwPath=window.document.location.href;
//	获取主机地址之后的目录，如： uimcardprj/share/meun.jsp
	var pathName=window.document.location.pathname;
	var pos=curWwwPath.indexOf(pathName);
//	获取主机地址，如： http://localhost:8083
	var localhostPaht=curWwwPath.substring(0,pos);
//	获取带"/"的项目名，如：/uimcardprj
	var projectName=pathName.substring(0,pathName.substr(1).indexOf('/')+1);
	return(localhostPaht+projectName);
}


/*
 * 判断是否为手机
 */
var os = function() {
	var ua = navigator.userAgent,
	isWindowsPhone = /(?:Windows Phone)/.test(ua),
	isSymbian = /(?:SymbianOS)/.test(ua) || isWindowsPhone, 
	isAndroid = /(?:Android)/.test(ua), 
	isFireFox = /(?:Firefox)/.test(ua), 
	isChrome = /(?:Chrome|CriOS)/.test(ua),
	isTablet = /(?:iPad|PlayBook)/.test(ua) || (isAndroid && !/(?:Mobile)/.test(ua)) || (isFireFox && /(?:Tablet)/.test(ua)),
	isPhone = /(?:iPhone)/.test(ua) && !isTablet,
	isPc = !isPhone && !isAndroid && !isSymbian;
	return {
		isTablet: isTablet,
		isPhone: isPhone,
		isAndroid : isAndroid,
		isPc : isPc
	};
}();
function getPhoneType(){
	if(os.isAndroid || os.isPhone || os.isTablet){
		return true;
	}else{
		return false;
	}
}


/*
 * 更换验证码
 */
function loadimage(){ 
	 document.getElementById("randImage").src = "resource/js/image.jsp?"+Math.random(); 
} 


/*
 * iframe自适应高度
 */

function SetWinHeight(obj) 
{ 
	var win=obj; 
	if (document.getElementById) 
	{ 
		if (win && !window.opera) 
		{ 
			if (win.contentDocument && win.contentDocument.body.offsetHeight) 
				win.height = win.contentDocument.body.offsetHeight; 
			else if(win.Document && win.Document.body.scrollHeight) 
				win.height = win.Document.body.scrollHeight; 
		} 
	} 
} 


function showLoginForm(){
	$('#loginInfo').modal('show');
}


