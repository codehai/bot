//receive Danmu
var casper = require('casper').create(
        {clientScripts: ['jquery.js']}  
);

function repeat() {  
    casper.wait(1000,function(){
        var danmus = this.evaluate(function(){
                        var  message = $('#chat_line_list li');
                        var text_cont = [ ];
                        for(var v=0;v<message.length;v++){
                             var dom = $("#chat_line_list li:eq("+v+")").detach();
                             text_cont[v] = $(dom).find('p span:eq(1)').text();   
                        }
                        return text_cont;
                        // var  message = $('#chat_line_list li');
                        // if(message.length>20){
                        //         $("#chat_line_list li").remove();   
                        // }
                        // return message.length;
        }) ;
        var time = this.evaluate(function(){
                var myDate=new Date();
                return myDate.toLocaleTimeString();
        })
                //this.echo(time+":"+danmu); 
            if(danmus.length){
                this.each(danmus,function(self,danmu){
                        self.then(function(){
                            if(danmu){
                                this.echo(time+":"+danmu);
                            }
                        })
                })                
            }
    });
    casper.run(repeat);
}

casper.start('http://douyu.tv/');
var channel = casper.cli.get(0);
casper.then(function() {                                      //在第二个新页面加载完成后,输出一些信息到控制台中
    this.echo('Page url is ' + this.getCurrentUrl());
    this.echo('Page title is ' + this.getTitle());
});
//casper.thenClick('.head .live a');
casper.thenOpen('http://www.douyu.com/directory/game/yqly');
casper.then(function() {                                      //在第二个新页面加载完成后,输出一些信息到控制台中
    this.echo('Page url is ' + this.getCurrentUrl());
    this.echo('Page title is ' + this.getTitle());
});
casper.thenClick('#live-list-contentbox li:nth-child('+channel+') a');
casper.then(function() {                                      //在第二个新页面加载完成后,输出一些信息到控制台中
        this.echo('Page url is ' + this.getCurrentUrl());
        this.echo('Page title is ' + this.getTitle());        
});

casper.run(repeat);