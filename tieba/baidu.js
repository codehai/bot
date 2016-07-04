var casper = require('casper').create(
        {
            clientScripts: ['jquery.js'],
            viewportSize: {
                    width: 1200,
                    height: 1000
            },
          pageSettings: {
                loadImages:  false,        // The WebPage instance used by Casper will
                loadPlugins: false         // use these settings
          }
        }  
);
var mouse = require("mouse").create(casper);
casper.options.waitTimeout = 15000;
var fs = require('fs');
function repeat() {    
      casper.wait(2000,function(){   
        });
    casper.run(repeat);
}

casper.start('http://tieba.baidu.com/f/index/forumclass');
var tree;
casper.then(function(){
     tree = this.evaluate(function(){
          var item = {};
          var len = $('.class-item').length;
          for(var i =0;i<len;i++){
            var title = $('.class-item:eq('+i+') .class-item-title').text();
            item[title] = {};
            var list = $('.class-item:eq('+i+') .item-list-ul li');
            for(var j=0;j<list.length;j++){
                var listName = $(list[j]).find('a').text();
                item[title][listName] = {};
            }
          }
          return item;
    });
     //this.echo('length:'+JSON.stringify(tree));
})
casper.then(function(){
    var urls = this.evaluate(function(i){
      var urls = [];
      // for(var j = 282;j<316;j++)
     for(var j = 0;j<$(".class-item li").length;j++)
     {
         // urls[j] = $(".class-item li:eq("+j+") a").attr('href'); 
         urls[j] = $(".class-item li:eq("+j+") a").attr('href');  
     } 
      return urls;
    })
    this.each(urls,function(self,url){
      self.then(function(){
          var link = 'http://tieba.baidu.com'+url;
          this.thenOpen(link,function(){
            this.echo(this.getTitle());
            var yeshu = this.evaluate(function(){
                var sy = $('.pagination a').last().attr('href') || '';
                var start = sy.indexOf('pn=') + 3;
                var end = sy.length;
                var num = sy.substr(start,end) || 1;
                return num;
            });
            var yUrl = this.evaluate(function(){
               var sy = $('.pagination a').last().attr('href') || '';
               return 'http://tieba.baidu.com'+sy;
            });
            this.echo('title:'+this.getTitle());
            var title = this.getTitle();
            var stitle = title.split('_');
            //this.echo('link:'+yUrl);
            this.echo(stitle[0]);
            this.echo(stitle[1]);
            if(yUrl){
                    var e = yUrl.indexOf('pn=')+3;
                    var s_link = yUrl.substr(0,e);
                    var y_links = [];
                    // for(var i=0;i<2;i++){
                    for(var i=0;i<yeshu;i++){
                      y_links[i] = s_link+i;
                    }
                    this.each(y_links,function(self,y_link){
                      self.then(function(){
                        this.echo(y_link);
                        this.thenOpen(y_link,function(){
                          var baName = this.evaluate(function(){
                            var name = {};
                            for(var i =0;i<$('.ba_info').length;i++){
                                 name[$('.ba_info:eq('+i+')').find('.ba_name').text()] = {
                                  '关注':$('.ba_info:eq('+i+')').find('.ba_m_num').text(),
                                  '贴子':$('.ba_info:eq('+i+')').find('.ba_p_num').text()
                                };
                            }
                            return name;
                          })
                          this.echo(stitle[0]);
                          this.echo(stitle[1]);
                          this.echo(JSON.stringify(baName));
                          for(var i in baName){
                                tree[stitle[1]][stitle[0]][i] = baName[i];
                          }
                          var path = 'tieba.json';
                          var content = JSON.stringify(tree);
                          fs.write(path, content, 'w');
                          this.echo('tree:'+JSON.stringify(tree));
                        })
                      })
                    })
            }
            else{
            }
          })
      })
    })
})
casper.run(repeat);