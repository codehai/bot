var sshotPfx = 'ss/';
function genSSCallback(label){
	return function(msg){
		cas.echo(label);
		cas.echo(msg);
		cas.captureSelector(sshotPfx + label +'.png','body');
	}
}
function genS1Callback(label){
	return function(msg){
		cas.echo(label);
		cas.echo(msg);
		cas.capture(sshotPfx + label +'.png');
	}
}
var cas = require('casper').create({
	pageSettings:{
		//localToRemoteUrlAccessEnabled:true, 
		//webSecurityEnabled:false
	},
	viewportSize:{ width: 320, height: 568 },
	onTimeout:genS1Callback("Timeout"),
	onStepTimeout:genS1Callback("StepTimeout"),
	onWaitTimeout:genS1Callback("WaitTimeout"),
	onAlert:genSSCallback("Alert"),
	onDie:genSSCallback("Die"),
	//onError:genSSCallback("Error"),
	onLoadError:genSSCallback("LoadError"),
	/*onPageInitialized:function(page){
		cas.echo('AAAAAAAAAAAAAAAAAAAAAAAAAA');
		utils.dump(page.viewportSize);
		page.evaluate(function(w, h) {
			document.body.style.width = w + "px";
			document.body.style.height = h + "px";
		}, page.viewportSize.width, page.viewportSize.height);
		page.clipRect = {
			top:0,
			left:0,
			width:page.viewportSize.width,
			height:page.viewportSize.height
		};
	},*/
	onStepComplete:function(){
		var n = cas.cli.get('stepcam');
		var s = ('00000000000'+cas.step).replace(/^.*(.....)$/,'$1');
		if(n||0){
			//utils.dump([cas.page.viewportSize,s]);
			s1('stepcam/'+s+'.png');
		}
		for(var i=1;i<n;++i){
			(function(){
				var t = i*100;
				setTimeout(function(){
					s1('stepcam/'+s+'-'+t+'.png');
				},t);
			})();
		}
	},
	waitTimeout:10000
});
var utils = require('utils');

/*cas.echo(cas.base64encode);
cas.echo(cas.callUtils);
cas.echo(cas.download);*/

//cas.echo(cas.then);
//cas.echo(cas.each);

//var wp1 = require('webpage').create();
//
//================================================================================
//================================================================================
// Extending Casper functions for dumpSteps()

/**
 * Dump Navigation Steps for debugging
 * When you call this function, you cat get current all information about CasperJS Navigation Steps
 * This is compatible with label() and goto() functions already.
 *
 * @param   Boolen   showSource    showing the source code in the navigation step?
 *
 * All step No. display is (steps array index + 1),  in order to accord with logging [info] messages.
 *
 */

cas.dumpSteps = function dumpSteps( showSource ) {
  this.echo( "=========================== Dump Navigation Steps ==============================", "RED_BAR");
  if( this.current ){ this.echo( "Current step No. = " + (this.current+1) , "INFO"); }
  this.echo( "Next    step No. = " + (this.step+1) , "INFO");
  this.echo( "steps.length = " + this.steps.length , "INFO");
  this.echo( "================================================================================", "WARNING" );

  for( var i=0; i<this.steps.length; i++){
    var step  = this.steps[i];
    var msg   = "Step: " + (i+1) + "/" + this.steps.length + "     level: " + step.level
    if( step.executed ){ msg = msg + "     executed: " + step.executed }
    var color = "PARAMETER";
    if( step.label    ){ color="INFO"; msg = msg + "     label: " + step.label }

    if( i == this.current ) {
      this.echo( msg + "     <====== Current Navigation Step.", "COMMENT");
    } else {
      this.echo( msg, color );
    }
    if( showSource ) {
      this.echo( "--------------------------------------------------------------------------------" );
      this.echo( this.steps[i] );
      this.echo( "================================================================================", "WARNING" );
    }
  }
};

// End of Extending Casper functions for dumpSteps()
//================================================================================
//================================================================================


function report(a,b){
	var t=(new Date()).toTimeString();
	cas.echo(a+' timeout '+b+' '+t);
	s1(a+'Timeout '+t+'.png');
	cas.exit();
}

cas.echo("init");
function wfp(a,then){
	cas.waitForPopup(a,then,function(){
		report('waitForPopup',sel);
	});
}
function wfs(sel,then){
	cas.waitForSelector(sel,then,function(){
		report('waitForSelector',sel);
	});
}
function wuv(sel,then){
	cas.waitUntilVisible(sel,then,function(){
		report('waitUntilVisible',sel);
	});
}
function humanDelay(){
	cas.wait(150+Math.random()*300);
}
function humanLike0(f){ cas.wait(50+Math.random()*50,f); }
function humanLike(f){ cas.wait(150+Math.random()*300,f); }
function humanLikeS(f){ cas.wait(1500+Math.random()*300,f); }
function humanLikeSS(f){ cas.wait(3500+Math.random()*300,f); }
function humanTap(c){
	cas.wait(100+Math.random()*50,function(){
		cas.page.sendEvent('keypress',c,null,null,0);
		//cas.echo('humantap');
	});
}
function longDelay(){
	cas.wait(20000);
}
function humanClick(sel){
	//wfs(sel, function(){
	cas.echo('humanClick 0 '+sel);
	humanDelay();
	wuv(sel, function(){
		cas.echo('humanClick 1 '+sel);
		//utils.dump(cas.getElementsInfo(sel));
		cas.click(sel);
		cas.echo('DONE humanClick '+sel);
	});
}
function humanClick1(sel){
	wuv(sel);
	humanLike(function(){
		cas.echo('humanClick1 '+sel);
		//utils.dump(cas.getElementsInfo(sel));
		cas.click(sel);
		cas.echo('DONE humanClick1 '+sel);
	});
}

function randCoeff(){
	return (Math.random()-0.5)*2;
}
function randomNormalDistribution(){
	var u=0.0, v=0.0, w=0.0, c=0.0;
	do{
		//获得两个（-1,1）的独立随机变量
		u=Math.random()*2-1.0;
		v=Math.random()*2-1.0;
		w=u*u+v*v;
	}while(w==0.0||w>=1.0)
	//这里就是 Box-Muller转换
	c=Math.sqrt((-2*Math.log(w))/w);
	//返回2个标准正态分布的随机数，封装进一个数组返回
	//当然，因为这个函数运行较快，也可以扔掉一个
	//return [u*c,v*c];
	return u*c;
}
function execNaturalClick(sel){
	cas.echo('naturalClick '+sel);
	var info = cas.getElementsInfo(sel);
	var w = info[0].width;
	var h = info[0].height*0.5;
	var x = info[0].x+w*0.5+randCoeff()*w*0.3;
	var y = info[0].y+h*0.5+randCoeff()*h*0.3;
	cas.evaluate(function(s){
		__utils__.echo(JSON.stringify(document.querySelector(s).getBoundingClientRect()));
	},sel);
	//utils.dump(cas.getElementBounds(sel));
	utils.dump([x,y]);
	cas.page.sendEvent('mousedown',x,y, 'left');
	var delay = 50+Math.random()*50;
	setTimeout(function(){
		cas.page.sendEvent('mouseup',x,y, 'left');
		cas.echo('DONE naturalClick '+sel);
	},delay);
}
function humanClick1M(sel){
	wuv(sel);
	humanLike(function(){
		cas.echo('humanClick1M '+sel);
		//utils.dump(cas.getElementsInfo(sel));
		execNaturalClick(sel);
	});
	humanLike(function(){
		//cas.mouse.click(sel);
		cas.echo('DONE humanClick1M '+sel);
	});
}
function instantClick(sel){
	wuv(sel,function(){
		cas.echo('instantClick '+sel);
		cas.click(sel);
		cas.echo('DONE instantClick '+sel);
	});
}
function quickFill(sel,val){
}
function humanFillS(sel,val){
	humanDelay();
	wuv(sel, function(){
		cas.echo('humanFill '+sel+' '+val);
		//utils.dump(cas.getElementsInfo(sel));
		//cas.fill(name,val);
		//cas.fillSelectors(sel,val);
		//cas.sendKeys(sel,val);
		//cas.fill("form",name,val);
		//cas.evaluate(function(s) { document.querySelector(s).focus(); }, sel);
		//cas.evaluate(function(s) { document.querySelector(s).select(); }, sel);
		execNaturalClick(sel);
		/*
		cas.evaluate(function(s){
			var mouseEvent = document.createEvent("MouseEvents");
			mouseEvent.initMouseEvent("click",true,true,window,
		});*/
	});
	humanLike(function(){
		cas.echo('humanFill focused');
	});
	//cas.echo(val);
	//utils.dump(val);
	var str = new String(val);
	//utils.dump(str);
	var cs = str.split('');
	humanDelay();
	for(var i in cs){ humanTap(cs[i]); }
	/*humanLike(function(){
		//cas.evaluate(function(s,v) { document.querySelector(s).value = v; }, sel, val);
		//cas.sendKeys(sel,val,{reset:false, keepFocus:true});
		//cas.echo('SSSSSSSSSSSSSSS');
		//cas.page.sendEvent('keypress','A',null,null,0);
		//cas.page.sendEvent('keypress',val,null,null,0);
	});*/
	humanLike(function(){
		cas.evaluate(function(s) { document.querySelector(s).blur(); }, sel);
		cas.echo('DONE humanFill '+sel);
	});
}
function humanFillN(name,val){
	humanFillS('input[name='+name+']',val);
}
//cas.userAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.61.1 (KHTML, like Gecko) Version/7.0 Mobile/11A4449d Safari/9537.53');
cas.userAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53');
cas.start('http://tieba.baidu.com', function(){ cas.echo('open tieba'); });
if(cas.cli.get('cam')){
	cas.then(function(){
		var i = 0;
		setInterval(function(){
			s1((++i)+".png");
		},100);
	});
}
humanClick1M('#index-app-continue');
//humanClick('.tab_index_content .j_login_ad_btn.login_ad_btn');
cas.then(function(){});
humanClick1M('.j_login_ad_btn.login_ad_btn');
humanFillN('username',cas.cli.get(0));
humanFillN('password',cas.cli.get(1));
//humanClick('.pass-button-submit.pass-button-disabled');
//humanLike(function(){ cas.echo('zzzzzzzzzzzzzzz'); utils.dump(cas.getElementsInfo('img.pass-verifycode')); });

//humanClick1('.pass-button-submit');
humanClick1M('.pass-button-submit:not(.pass-button-disabled)');
/*	cas.waitUntilVisible('.pass-button-submit:not(.pass-button-disabled)',function(){
		cas.echo('ssssssssssssssssssss');
		cas.mouse.click('.pass-button-submit:not(.pass-button-disabled)');
	});*/

/*humanLike(function(){
	cas.echo('zzzzzzzzzzzzzzz');
	utils.dump(cas.getElementsInfo('img.pass-verifycode'));
});*/

//cas.waitUntilVisible('img.pass-verifycode',function(){
//humanLike(function(){ cas.captureSelector(sshotPfx + 'captchafilled0.png','body'); });
humanClick1M('input[name=verifycode]');

function ss(fname){
	cas.captureSelector(sshotPfx + fname,'body');
}
function s1(fname){
	cas.capture(sshotPfx + fname);
}

humanClick1M('a.top_search');
humanLikeS(function(){ s1('entering_ba.png'); });
var cmd_url = cas.cli.get(2);
function get_tiez(){
	var fA = function(root,sel){
		return [].map.call(root.querySelectorAll(sel),function(x){return x.textContent;});
	};
	var f = function(root,sel){ return fA(root,sel).join('###@@@###@@@###'); };
	return __utils__.findAll('ul#frslistcontent>li>a.j_common').map(function(a){
		return {
			'title': f(a,'.ti_title span:not(.ti_title_icon)'),
			'special': f(a,'.ti_title span.ti_title_icon'),
			'abs': fA(a,'.ti_abs'),
			'img': [].map.call(a.querySelectorAll('img'),function(x){
				return {
					'src':x.getAttribute('src'),
					'link':x.getAttribute('link'),
					'data-load-start':x.getAttribute('data-load-start'),
					'data-url':x.getAttribute('data-url')
				};
			}),
			'author': f(a,'.ti_author'),
			'time': f(a,'.ti_time'),
			'n-zan': f(a,'.ti_zan_reply .j_btn_zan_text.btn_zan_text'),
			'n-reply': f(a,'.ti_zan_reply .ti_func_btn.btn_reply'),
			'href':a.href,
			'tid': a.getAttribute('tid')//,
			//'offsetTop':a.offsetTop
		}
	});
}
function get_tiez_1(){
	var tiez = cas.evaluate(get_tiez);
	cas.echo('got tiez>>>>');
	//utils.dump(tiez);
	cas.echo('<<<<got tiez');
	//TODO: upload tiez;
	return tiez;
}
cas.then(function(){
	cas.echo('SSSSSSSSSSSSSSSSSSSSSS');
	cas.echo(cmd_url);
	cas.echo('SSSSSSSSSSSSSSSSSSSSSS');
	utils.dump(cas.page.cookies);

	/*var p0 = cas.page;
	cas.echo('CCCCCCCCCCCCCCCCCCCCCC');
	//cas.echo(cas.newPage);
	var p1 = require('webpage').create();
	cas.echo('AAAAAAAAAAAAAAAAAAAAAA');*/

	cas.evaluate(function(url){ 
		window.open(url,'','width=200,height=100');
	},cmd_url);
	//cas.echo(cas.waitForPopup);
	wfp(cmd_url,function(){
		cas.echo('popped');
		var popup = cas.popups.find(cmd_url);
		//cas.echo(popup.plainText);
		var dat = JSON.parse(popup.plainText);
		popup.close();
		dat.forEach(function(cmd){
			if(cmd.ba || 0){
				//utils.dump(cmd);
				cas.then(function(){
					cas.echo('进入贴吧 '+cmd.ba);
				});
				//humanClick1M("div.ui_search.j_tab_con_search");
				humanFillS("input.j_search_input.search_input",cmd.ba);
				humanClick1M(".j_search_button.search_button.enter_forum#btn");
				wfs('#frslistcontent',function(){
					//if(visible('.frs_pb_leadapp_pop_show')){ humanClick('.frs_pb_leadapp_pop_show'); }
					var tiez = get_tiez_1();
					if(cmd.hui||0){
						var hui = cmd.hui;
						var rec = {};
						var posts = hui.posts;
						var f = function(tiez,iPost){
							var post = hui.posts[iPost];
							if(post||false){
								var candidates = tiez.filter(function(tie){
									var r = tie["n-reply"];
									return r>=hui["lou-min"] && r<=hui["lou-max"] && (!rec[tie.tid]);
								});
								cas.echo('post');
								cas.echo(candidates.length);
								if(candidates.length>0){
									var target = candidates[Math.floor(Math.random()*(candidates.length-0.0001))];
									cas.echo('got target>>>>');
									utils.dump(target);
									cas.echo('<<<<got target');
									/*var sel = "ul#frslistcontent>li>a[tid=\""+target.tid+"\"].j_common";
									//cas.echo('scroll to '+target.offsetTop);
									cas.evaluate(function(s) { 
										__utils__.echo('VVVVVVVVVVVVVVVVVVVVVVVV');
										__utils__.echo(document.querySelector(s).scrollIntoView);
										__utils__.echo('GGGGGGGGGGGGGGGGGGGGGGGG');
										document.querySelector(s).scrollIntoView({ 
											behavior: "instant", block: "start" 
										}); 
										__utils__.echo('KKKKKKKKKKKKKKKKKKKKKKKK');
									}, sel);
									cas.wait(1000);
									//cas.scrollTo(target.offsetTop);
									humanClick1M(sel);*/
									cas.open(target.href,function(){
										//cas.scrollToBottom();
										cas.echo('HTML========================');
										cas.echo(cas.getHTML('#j_main_editor_container'));
									});
									//todo: upload thread content
									humanClick1M(".j_btn_reply");
									cas.waitUntilVisible('textarea.editor_content',function(){
										//cas.echo('HTML========================');
										//cas.echo(cas.getHTML('#j_main_editor_container'));
										post.map(function(x){
											if(typeof x === "string"){
												humanFillS("textarea.editor_content",x);
											}else{
												switch(x[0]){
													case "i": 
														humanClick1M("input#pic");
														humanLike(function(){
															var p = x[1];
															var p1 = p.replace(/.*\//,'');
															cas.echo("pic: "+p+' '+p1);
															cas.page.uploadFile("input#pic",p);
															humanLike();
															wfs('img[name="'+p1+'"]',function(){
																cas.echo('upload successful '+p1);
																//cas.echo('HTML========================');
																//cas.echo(cas.getHTML('#j_main_editor_container'));
															});
														}); 
													break;
												}
											}
											humanClick1M("textarea.editor_content");
										});
									});
									//cas.then(function(){
										//s1('filled.png');
									//});
									humanClick1M('.j_submit_btn');
									rec[target.tid]=0;
									//f(tiez,iPost+1);
									//cas.waitForUrl(/.*/,function(){});
									//humanLikeS(function(){});
									//humanClick1M('.j_back_btn');
									humanLike(function(){
										s1('sent.png');
										cas.back();
									});
									wfs('#frslistcontent',function(){
										cas.echo('back-to #frslistcontent');
									});
									humanLikeS(function(){
										f(get_tiez_1(),iPost+1);
									});
								}else{
									cas.echo('wait and refresh');
									humanLikeSS(function(){
										cas.reload(function(){
											f(get_tiez_1(),iPost);
										});
									});
								}
							}
						};
						f(tiez,0);
					}
				});
				cas.then(function(){});
				humanLikeS(function(){});
				humanClick1M('a.search_btn');
			}
		});
	});

	//cas.withPopup(cmd_url,function(){ cas.echo(cas.getPageContent()); });
	//cas.callUtils("getBinary",cmd_url);
});
humanLikeS(function(){
	s1('last.png');
	utils.dump(cas.popups);
});
cas.echo('run');
cas.run(function(){
//	this.dumpSteps( true );  // Dump Navigation Steps;  You can comment out this line.
	this.exit();
});

