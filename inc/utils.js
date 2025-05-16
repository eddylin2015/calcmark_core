const grp = require('eslib').it_support_right;
const config = require('eslib').config;
const PHP_HOST = config.get('PHP_HOST');
const PHP_PORT = config.get('PHP_PORT');
const SLOCK = config.get('LOCK_POST_SMARK');
const PLOCK = config.get('LOCK_POST_PMARK');
const SCMMTLOCK = config.get('LOCK_POST_SCMMT');
const PCMMTLOCK = config.get('LOCK_POST_PCMMT');
const rediscli=require("../../../db/esc_redis_v4")
function getModel() { return require(`./model-mysql-pool`); }


const author_admin_user_list = ',2002024,2000003,2006011'
function GetAOT(req, fn) {
    let aot = 10;
    if (req.user && req.user.marksys_info) {
        aot = req.user.marksys_info[0][0].allowOpSect;
    }
    if (fn && req.user && req.user.marksys_info) {
        if (fn.startsWith("I")) { aot = req.user.marksys_info[0][0].p_allowOpSect; }
        if (fn.startsWith("P")) { aot = req.user.marksys_info[0][0].p_allowOpSect; }
        if (fn.startsWith("S")) { aot = req.user.marksys_info[0][0].allowOpSect; }
    }
    return aot;
}

function GetMyClass(req) {
    if (author_admin_user_list.indexOf(req.user.id) > -1 && req.query.fn) {
        let myc_ = req.query.fn.substring(0, 4);
        if (myc_.startsWith("P")) myc_ = myc_.substring(0, 3);
        return myc_;
    }
    return (req.user && req.user.marksys_info) ? req.user.marksys_info[1][0].classno : null;
}

function GetSID(req) { return (req.user && req.user.marksys_info) ? req.user.marksys_info[0][0].session_id : null;}

function GetCDIDS(req) {
    let right = [];
    if (req.user && req.user.marksys_info) {
        for (let i = 0; i < req.user.marksys_info[2].length; i++) {
            right.push(req.user.marksys_info[2][i].course_d_id);
        }
    }
    return right.join(",");
}

function CheckCDID(req, cdid) {
    if (req.user && author_admin_user_list.indexOf(req.user.id) > -1) return true;
    let right = false;
    if (req.user && req.user.marksys_info) {
        if (req.user.marksys_info[1][0].RoleID == 1
            || req.user.marksys_info[1][0].RoleID == 8
            || req.user.marksys_info[1][0].RoleID == 9
        ) {
            right = true;
        }
        else {
            for (let i = 0; i < req.user.marksys_info[2].length; i++) {
                if (req.user.marksys_info[2][i].course_d_id == cdid) {
                    right = true;
                }
            }
        }
    }
    return right;
}

function CheckCLASSNO(req, classno) {
    if (author_admin_user_list.indexOf(req.user.id) > -1) {
        console.log(`${req.user.id} modify pingyu`);
        return true;
    }
    let right = false;
    if (req.user && req.user.marksys_info) {
        if (req.user.marksys_info[1][0].RoleID == 1
            || req.user.marksys_info[1][0].RoleID == 8
            || req.user.marksys_info[1][0].RoleID == 9
        ) {
            return true;
        }
        else {
            return req.user.marksys_info[1][0].classno == classno;
        }
    }
    return right;
}

function showMarksysInfo(req, res) {
    let esess = req.user.marksys_info[0][0];
    let euser = req.user.marksys_info[1][0];
    let ecourse = req.user.marksys_info[2];
    let classcourse = req.user.marksys_info[3];
    res.render('markup/index.pug', {
        profile: req.user,
        esess: esess,
        euser: euser,
        ecourse: ecourse,
        eclasscourse: classcourse,
        markadmin: grp.GRP_R_MARK_ADMIN(req.user),
        pstafpanel: grp.GRP_R_Pri_OA(req.user),
        sstafpanel: grp.GRP_R_Sec_OA(req.user),
        Pri_IE_CRS: grp.GRP_R_Pri_IE_CRS(req.user),
        aot: GetAOT(req, "S"),
        paot: GetAOT(req, "P"),
        classno: GetMyClass(req),
        SLOCK: SLOCK,
        PLOCK: PLOCK,
    });
}

function CheckAdmin(req) {
    if (req.user.id == 2002024) return true;
    return false;
}

function CheckOfficeStaff(req) {
    if (req.user.id == 2002024) return true;
    return false;
}

function CheckCLASSCDID(req, cdid) {
    if (!req.user.marksys_info[3]) return false;
    let right = false;
    for (let i = 0; i < req.user.marksys_info[3].length; i++) {
        if (req.user.marksys_info[3][i].course_d_id == cdid) {
            right = true;
        }
    }
    return right;
}

async function redis_lock_status(RESET=false, cb=null){
    let redis_lock=await rediscli.hgetall("MARKUP_CONFIG")  //hget("MARKUP_CONFIG","LOCK")
    console.log(redis_lock)
    let lock_data=[0,0,0,0]
    if(redis_lock && !RESET){
        lock_data[0]=redis_lock.SLOCK
        lock_data[1]=redis_lock.SLCMMT
        lock_data[2]=redis_lock.PLOCK
        lock_data[3]=redis_lock.PLCMMT
    }else{
        let dt_=await getModel().DB_reader('select * from mrs_session_def where curr_flag=1;',[])
        lock_data[0]=dt_[0].SLOCK
        lock_data[1]=dt_[0].SLCMMT
        lock_data[2]=dt_[0].PLOCK
        lock_data[3]=dt_[0].PLCMMT
        rediscli.hset("MARKUP_CONFIG","LOCK",1)
        rediscli.hset("MARKUP_CONFIG","SLOCK",dt_[0].SLOCK)
        rediscli.hset("MARKUP_CONFIG","SLCMMT",dt_[0].SLCMMT)
        rediscli.hset("MARKUP_CONFIG","PLOCK",dt_[0].PLOCK)
        rediscli.hset("MARKUP_CONFIG","PLCMMT",dt_[0].PLCMMT)
    }
    if(cb) {
        cb(lock_data)
    }
    else{
        return lock_data;
    }
}

async function MarkLock(req, res, next) {
    const { header, method, url } = req;
    if(req.rawHeaders.indexOf("sidkey")>-1) return next();
    if(method=="POST" && req.user && req.user.marksys_info){
      ////let status=[0,0,0,0]
      let status=await redis_lock_status(false);
      let euser = req.user.marksys_info[1][0];
      let Lock_ = euser.spk == "2" ? (status[2]=="1"|| PLOCK) :(status[0]=="1"|| SLOCK);
      let Lock_CMMT = euser.spk == "2" ? (status[3]=="1"||PCMMTLOCK) : (status[0]=="1"||SCMMTLOCK);
      if(req.user.id=="2006011") {Lock_=false;Lock_CMMT=false;}
      if(req.user.id=="2003006") {Lock_=false;Lock_CMMT=false;}
      if(req.user.id=="2002024") {Lock_=false;Lock_CMMT=false;}
      if(req.user.id=="2000003") {Lock_=false;Lock_CMMT=false;}
      if (Lock_ && (
          url.indexOf("/marksave.php") > -1
          || url.indexOf("/marksavejson") > -1
          || url.indexOf("/editgrademark/grademarksave.php") > -1
          || url.indexOf("/editgrademark/grademarksavejson.php") > -1
          || url.indexOf("/editParentEval/grademarksave.php") > -1
          || url.indexOf("/editParentEval/grademarksavejson.php") > -1
          || url.indexOf("/editParentEval") > -1
          || url.indexOf("/act/studGradeUpdate") > -1
      )) 
      {
        return res.end("ERR:Locked. 制表期間,暫停修改.")
      }
      if (Lock_CMMT && (
          url.indexOf("/condusave") > -1
          || url.indexOf("/pingyusave") > -1
      )) {
      return res.end("ERR:Locked. 制表期間,暫停修改.")
      }
    }
    if(req.user && req.user.marksys_info){
        return next();
    }else{
        return res.end("ERR:No Auth!")
    }
}
 
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

function ExpArrayToXls(arraydata_str, exportfilename, respone) {
    let param_postData = arraydata_str;
    let options = {
        hostname: '127.0.0.1', port: 8082, path: '/api/NpoiXls/ExpArrayToXls', method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(param_postData) }
    };
    let req = http.request(options, (res) => {
        respone.setHeader("Content-type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        respone.setHeader("Content-Disposition", "attachment; filename=" + encodeURI(exportfilename) + ";");
        res.on('data', (chunk) => { respone.write(chunk); }); res.on('end', () => { respone.end(); });
    });
    req.on('error', (e) => { console.error(`problem with request: ${e.message}`); });
    req.write(param_postData); req.end();
}

module.exports = {
    MarkLock: MarkLock,
    redis_lock_status:redis_lock_status,
    GetAOT: GetAOT,
    GetMyClass: GetMyClass,
    showMarksysInfo: showMarksysInfo,
    GetSID: GetSID,
    CheckCDID: CheckCDID,
    CheckCLASSNO: CheckCLASSNO,
    GetCDIDS: GetCDIDS,
    CheckCLASSCDID: CheckCLASSCDID,
    HttpGet_pyapi:HttpGet_pyapi,
    ExpArrayToXls:ExpArrayToXls,
};

