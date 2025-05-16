const http = require('http');
const querystring = require('querystring');
const {iMarkCalC_Act,TMarkCalC_Act,MarkIterateCalc}=require("./calcmark_core")
var fs = require('fs');
var path = require('path');
var mimes = {
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.7z': 'application/z-7z-compressed'
};


//
// param_postData=querystring.stringify(param_postData_obj)
//
function HttpGet_pyapi(param_path, response, method = "GET", param_postData = { str: "ABC" }) {
    if (method == "GET") {
        http.get(
            {
                hostname: "127.0.0.1", port: 85,
                path: param_path, method: 'GET',
                headers: { 'Cookie': "sidkey", "X-Authorization": "sidkey" }
            },
            (res) => {
                response.set(res.headers);
                res.pipe(response)
            }).on('error', (e) => {
                console.log(e);
            });
    } else if (method == "POST") {
        param_postData = JSON.stringify(param_postData)
        let options = {
            hostname: "127.0.0.1", port: 85,
            path: param_path, method: 'POST',
            //headers: {'Cookie': "sidkey","X-Authorization": "sidkey", 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(param_postData) }
            headers: { 'Cookie': "sidkey", "X-Authorization": "sidkey", 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(param_postData) }
        };
        let req = http.request(options, (res) => {
            response.set(res.headers);
            res.pipe(response)
        });
        req.on('error', (e) => {
            console.error(`problem with request: ${e.message}`);
        });
        req.write(param_postData);
        req.end();
    }
}

//
// param_postData=querystring.stringify(param_postData_obj)
//
function HttpGet_pyapi_cb(param_path, cb, method = "GET", param_postData = { str: "ABC" }) {
    if (method == "GET") {
        http.get(
            {
                hostname: "127.0.0.1", port: 85,
                path: param_path, method: 'GET',
                headers: { 'Cookie': "sidkey", "X-Authorization": "sidkey" }
            },
            (res) => {
              cb(res) 
              //response.set(res.headers);
              //res.pipe(response)

            }).on('error', (e) => {
                console.log(e);
            });
    } else if (method == "POST") {
        param_postData = JSON.stringify(param_postData)
        let options = {
            hostname: "127.0.0.1", port: 85,
            path: param_path, method: 'POST',
            //headers: {'Cookie': "sidkey","X-Authorization": "sidkey", 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(param_postData) }
            headers: { 'Cookie': "sidkey", "X-Authorization": "sidkey", 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(param_postData) }
        };
        let req = http.request(options, (res) => {
            cb(res) 
            //response.set(res.headers);
            //res.pipe(response)
        });
        req.on('error', (e) => {
            console.error(`problem with request: ${e.message}`);
        });
        req.write(param_postData);
        req.end();
    }
}

//
// var filename = process.argv[process.argv.length-2];
// var jpgfilename = process.argv[process.argv.length-1];
//
function Uploadfile(filename, jpgfilename) {
    var ext = path.extname(filename);
    var mime = mimes[ext.toLowerCase()];
    if (!mime) return;
    var stats = fs.statSync(filename)
    var fileSizeInBytes = stats.size;
    const base64 = fs.readFileSync(filename, "base64");
    var filesize = base64.length; //filesize,fileSizeInBytes
    var boundary = "----WebKitFormBoundaryENl50aIWkiBG2Umn";
    let options = {
        host: '192.168.101.253',
        //host: '192.168.62.253',
        port: '81',
        path: '/NewUI/',
        method: 'POST',
        headers: {
            'content-type': 'multipart/form-data; boundary=' + boundary,
            'content-length': filesize * 2
        },
        form: { 'file1': filename }
    }
    var req = http.request(options, function (res) {
        res.on('data', function (chunk) {
            console.log('BODY: ' + chunk);
        });
    });
    req.on('error', function (err) {
        console.log("upload err : " + err);
    });
    req.write("--" + boundary + "\r\n");
    req.write('Content-Disposition: form-data; name="file1"; filename="' + jpgfilename + '"\r\n');
    req.write("Content-Transfer-Encoding: base64\r\n");
    req.write(`Content-Type: ${mime}\r\n\r\n`);
    req.write(base64)
    req.write("\r\n\r\n--" + boundary + "--\r\n");
    req.end();
    console.log("send base64")
}

function Dowanloadfile(path_, fn = null, sid = null) {
    if (fn == null) fn = "temp.tmp";
    return new Promise(resolve => {
        var file = fs.createWriteStream(fn);
        http.get(
            {
                host: '192.168.62.253',
                port: '81',
                path: path_,
                method: 'GET',
                headers: { 'Cookie': sid }
            },
            (res) => {
                res.pipe(file);
                file.on('finish', function () {
                    file.close(function () {
                        if (res.statusCode == 404) { resolve(fn + ": Not File!"); }
                        else {
                            resolve(fn + ": Save File!");
                        }
                    }
                    );
                });
            }).on('error', (e) => { console.log(e); });
    });
}
module.exports = {
    HttpGet_pyapi: HttpGet_pyapi,
    HttpGet_pyapi_cb: HttpGet_pyapi_cb,
    Uploadfile: Uploadfile,
    Dowanloadfile: Dowanloadfile,
}