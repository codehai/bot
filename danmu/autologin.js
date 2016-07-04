//pojie yanzhengma
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
function repeat() {    
     casper.wait(1000,function(){
        var number = fs.readFileSync("number");
        if(number==1)
        {
            casper.then(function(){
              this.reload();
            })
            casper.then(function(){
                this.wait(500);
                this.echo('wait');
            })
            casper.then(function(){
                    var max = this.evaluate(function(){
                            function sortNumber(a,b)                        {
                                return a - b;
                            };
                            var  message = $('span');
                            var numArr = [ ];
                            var len = message.length; 
                            for(var i = 5 ;i<len  ;i++){
                                numArr [i-5] = $("span:eq("+i+")").text();
                            }
                            var result = numArr.sort(sortNumber);
                            var maxNum = result[result.length-1];
                            for(var i =0;i<len;i++){
                                if(maxNum==$("span:eq("+i+")").text()){
                                    var maxID = i;
                                    break;
                              }
                            }
                            return  maxID;
                    });
                    this.echo(max);
                    var path = 'number';
                    var content = max;
                    fs.write(path, content, 'w');
            })
        }
    });
    casper.run(repeat);
}
casper.start('file:///home/hao/%E6%A1%8C%E9%9D%A2/casperjs/index.html');
casper.run(repeat);
