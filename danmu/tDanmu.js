//transmit Danmu
var casper = require('casper').create(
        {
            clientScripts: ['jquery.js'],
            viewportSize: {
                    width: 1200,
                    height: 1000
            }
        }  
);
var mouse = require("mouse").create(casper);
casper.options.waitTimeout = 15000;
var fs = require('fs');
var freq=0;
var clientx = [410,415,418,421,425,430,433,438,444,450,455,460,464,469,471,472,474,474,477,479,483,484,487,489,490,491,492,495,497,499,500,502,505,506,507,509,510,511,512,514,515,517,518,519,521,522,523,524,525,527,529,530,531,532,533,535,537,538,539,540,541,543,544,545,546,549,550,551,552,553,555,556,557,558,559,571,572,573,574,575,577,578,579,580,581,582,583,584,585,586,587,588,591,592,593,594,596,597,598,599,601,602,603,604]; 
var clienty = [500,500,499,498,497,497,496,495,495,495,495,495,495,495,495,495,495,495,495,495,495,495,495,495,495,494,494,494,494,494,494,494,494,494,494,494,494,494,494,494,494,493,493,493,493,493,493,493,493,493,493,493,493,493,492,492,492,492,492,492,492,492,492,492,492,492,492,492,492,492,492,491,491,491,491,491,491,491,491,491,491,491,491,491,491,491,491,490,490,490,490,490,490,490,490,490,489,489,489,489,489,489,489,489];
var points =  [0,1,2,3,4,5,6,7,8,9,10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,49 ,50 ,51 ,52 ,53 ,54 ,55 ,56 ,57 ,58 ,59 ,60 ,61 ,62 ,63 ,64 ,65 ,66 ,67 ,68 ,69 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89 ,90 ,91 ,92 ,93 ,94 ,95 ,96 ,97 ,98 ,99 ,100,101,102,103];
var sliders = [];
var flag = 0;
var number = 0;
var testNum = 0;
function repeat() {    
      casper.wait(2000,function(){   
          casper.echo('flag:'+flag);
             switch(flag){
                case 0:  number = fs.readFileSync("number");
                              casper.echo('number:'+number)
                              if(number>1){
                                 flag = 1;
                               }
                              casper.echo('status0');
                              break;
                case 1:  sliders.length = 0;
                              for(var i=0;i<number;i++){
                                sliders[i]=points[i];
                              }
                              number--;
                              casper.echo(number);
                              casper.each(sliders,function(self,slider){
                                  self.then(function(){
                                          if(slider==0){
                                            this.mouse.down('.gt_slider_knob');
                                          }
                                          this.mouse.move(clientx[slider],clienty[slider]);
                                          if(slider==number-1){
                                            this.mouse.up('.gt_slider_knob');
                                          }
                                   })
                                })
                                casper.then(function(){
                                     var sign = this.evaluate(function(){
                                          if($('.gt_ajax_tip').hasClass('ready')){
                                              var status = 0;
                                          };
                                          if($('.gt_ajax_tip').hasClass('fail')){
                                              var status = 0;
                                          };
                                          if($('.gt_ajax_tip').hasClass('success')){
                                              var status =1;
                                          };
                                          return status;
                                     })
                                     //require('utils').dump(this.getElementsInfo('.gt_ajax_tip'));
                                     this.echo('sign:'+sign);
                                     if(sign){
                                        flag = 2;
                                     }else{
                                        testNum++;
                                        if(testNum>5){
                                            flag = 4;
                                        }
                                     }
                                     this.echo('testNum:'+testNum);
                               })      
                               break;
                            case 2:  casper.then(function(){
                                                  this.fill('form', {                                 
                                                      'username': username,                 
                                                      'password': password           
                                                  }, true);      
                                          });
                                          casper.wait(1000);
                                          casper.thenOpen('http://www.douyu.com/directory/game/yqly');
                                          casper.then(function() {                                     
                                              this.echo('Page url is ' + this.getCurrentUrl());
                                              this.echo('Page title is ' + this.getTitle());
                                          });
                                          casper.thenClick('#live-list-contentbox li:nth-child('+channel+') a');
                                          casper.then(function() {                                   
                                                  this.echo('Page url is ' + this.getCurrentUrl());
                                                  this.echo('Page title is ' + this.getTitle());        
                                          });
                                      flag = 3;
                                      break;
                  case 3: casper.wait(11000,function(){
                                    freq++;
                                    this.echo(freq);
                                    var danmu = this.evaluate(function(){
                                                      var  message = $('#chat_line_list li');
                                                      if(message.length>30){
                                                              $("#chat_line_list li").remove();   
                                                      }
                                                      return message.length;
                                      }) ;
                                      this.echo('length:'+danmu); 
                                      casper.then(function(){
                                               var random = this.evaluate(function(){
                                                      return Math.floor(Math.random()*10+1);
                                               })
                                               var data = fs.readFileSync("text.txt");
                                               this.echo(random);
                                               if(freq%2){
                                                      data = data+"6666666"+random;
                                               }else{
                                                      data = data+"6666"+random;
                                               }
                                               if(data&&(danmu>30)){
                                                      this.echo('read sucess'+data);
                                                      this.sendKeys('#sms_chandiv textarea#chart_content', data);
                                                      this.click('#sendmsg'); 
                                                }
                                      });
                                });
                                break;
                  case 4 : casper.then(function(){
                                      this.echo("Test too much,please retry");
                                      var path = 'number';
                                      var content = '1';
                                      fs.write(path, content, 'w');
                                })
          }
        });
    casper.run(repeat);
}

casper.start('http://douyu.tv/');
var channel = casper.cli.get(0);
var username = casper.cli.get(1);
var password = casper.cli.get(2);
casper.then(function(){
    this.echo('channel:'+channel);
    this.echo('username:'+username);
    this.echo('password:'+password);
})
casper.then(function() {                                      
    this.echo('Page url is ' + this.getCurrentUrl());
    this.echo('Page title is ' + this.getTitle());
});
casper.thenClick('.o-unlogin a',function(){
    this.echo("clicked login");
});
casper.waitForSelector('.gt_slider',function(){
    this.echo('find gt_slider');
});
casper.then(function(){
    this.mouse.move(".gt_slider_knob");
    this.echo('mouse move');
    this.wait(200);
});

casper.then(function(){
    require('utils').dump(this.getElementBounds(".gt_slider_knob"));
})

casper.then(function(){
    this.mouse.doubleclick(".gt_slider_knob");
    this.wait(200);
})
casper.then(function(){
    this.mouse.down('.gt_slider_knob');
})
casper.each(points,function(self,point){
     self.then(function(){
            this.mouse.move(clientx[point],clienty[point]);
            this.captureSelector(point+'.png', '.gt_cut_fullbg');
            this.echo(point);
     })
})
casper.then(function(){
    this.mouse.up('.gt_slider_knob');
})
casper.then(function(){
    var path = 'number';
    var content = '1';
    fs.write(path, content, 'w');
})
casper.then(function(){
    this.wait(2000);
})
casper.run(repeat);