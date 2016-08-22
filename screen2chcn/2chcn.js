var casper = require('casper').create(
        {
            clientScripts: ['jquery.js'],
            viewportSize: {
                    width: 768,
                    height: 1000
            }
        }  
);
var name = casper.cli.args[0]
// var path = casper.cli.args[1]

casper.options.waitTimeout = 15000;
casper.start('file:////home/hao/bot/screen2chcn/wx2ch'+casper.cli.args[1]+'.html');
// casper.then(function(){
//     this.evaluate(function(){
//         $("body").css("background","url(./wx2ch_files/background/"+path+")")
//     })
// })
casper.then(function(){
    this.capture("./image/"+name+".png");  
})
casper.then(function(){
  this.echo("done")
})
casper.run();
