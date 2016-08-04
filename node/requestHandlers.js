var exec = require("child_process").exec;
var querystring = require("querystring");
formidable = require("formidable");
fs =  require("fs");

function start(response) {
    console.log("Request handler 'start' was called");

    var body = '<html>'+
        '<head>'+
        '<meta http-equiv="Content-Type" '+
        'content="text/html; charset=UTF-8" />'+
        '</head>'+
        '<body>'+
        '<form action="/upload" enctype="multipart/form-data" '+
        'method="post">'+
        '<input type="file" name="upload">'+
        '<input type="submit" value="Upload file" />'+
        '</form>'+
        '</body>'+
        '</html>';

    response.writeHead(200,{"Content-Type":"text/html","charset":"utf-8"});
    response.write(body);
    response.end();

}

function upload(response,request){
    console.log("Request handler 'upload' was called");

    var form = new formidable.IncomingForm();
    console.log("about to parse");
    form.parse(request,function (error,fields,files) {
        console.log("parse down");
        console.log(files.upload.path)
        fs.renameSync(files.upload.path,"./tmp/test.jpg");
        response.writeHead(200, {"Content-Type": "text/html"});
        response.write("received image:<br/>");
        response.write("<img src='/show'/>")
        response.end();
    })    
}



function show(response) {
    console.log("Request handler show was called.");
    
    fs.readFile("./tmp/test.jpg","binary",function (err,file) {
        if(err){
            response.writeHead(500,{"Content-Type":"text/plain"});
            response.write(err + "\n");
            response.end();
        }else{
            response.writeHead("200",{"Content-Type":"image/jpeg"});
            response.write(file,"binary");
            response.end();
        }
    });
}
exports.start = start;
exports.upload = upload;
exports.show = show;
