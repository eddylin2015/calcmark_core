const http = require('http');
const querystring = require('querystring');
const {iMarkCalC_Act,TMarkCalC_Act,MarkIterateCalc,View_Cross_Data,View_Cross_TotalData}=require("./calcmark_core")
const {HttpGet_pyapi,HttpGet_pyapi_cb,Uploadfile,Dowanloadfile}=require("./calcmark_pyapi")
var fs = require('fs');
var path = require('path');

function getModel() { return require(`./model-mysql-pool`); }


///
/// formatString("helo, {0}!","world") # like C# format String.
/// console.log(formatString('Hello {0}, your order {1} has been shipped.', 'John', 10001));
///
const formatString = (template, ...args) => {
    return template.replace(/{([0-9]+)}/g, function (match, index) {
        return typeof args[index] === 'undefined' ? match : args[index];
    });
}

function mk_adpt_Update(ds, tablename = "mk") {
    let sql = "update mrs_stud_course set ? where stud_c_id=?;"
    for (let arr_ of ds) {
        let mk = arr_["mk"]
        for (let r of mk) {
            let data = { total1: 0, total2: 0, total3: 0, total: 0, VOCA_MUE: 0, sub_c_p: 0, P_X: 0, eog: 0 }
            for (let k in data) data[k] = r[k];
            getModel().DataReaderQuery(sql, [data, r.stud_c_id], (err, results) => {/*console.log(err,results)*/ })
        }
    }
}

function cd_adpt_Update(ds, tablename = "cd") {
    let sql = "update mrs_stud_conduct set ? where stud_ref=?;"
    for (let arr_ of ds) {
        let mk = arr_["cd"]
        for (let r of mk) {
            let data = {
                mark1: 0, mark2: 0, mark3: 0, mark: 0, total_crs_ncp: 0,
                voca_cult_avg1: 0, voca_cult_avg2: 0, voca_cult_avg3: 0, voca_cult_avg: 0, voca_cult_mue: 0,
                voca_prof_avg1: 0, voca_prof_avg2: 0, voca_prof_avg3: 0, voca_prof_avg: 0, voca_prof_mue: 0,
                allpass1: 0, allpass2: 0, allpass3: 0,
                SchoolEval1:"", SchoolEval2:"", SchoolEval3:"", 
                SE_HONOR1:0, SE_HONOR2:0, SE_HONOR3:0,
                conduct:""
            }
            for (let k in data) data[k] = r[k];
            getModel().DataReaderQuery(sql, [data, r.stud_ref], (err, results) => {/*console.log(err,results)*/ })
        }
    }
}



/**
 * Gen Summary data from Mark Tables. Download data from the specified URL.
 * 
 * @async
 * @function GenSummaryTbl_cb
 * @param {string} classno - class no.
 * @param {string} term - term 1,2,3 .
 * @param {function} cb - call back.
 * @param {boolean} calcflag - calcflag.
 * @param {boolean} updateflag - updateflag.
 * @return {list} [std_dt, crs_dt, ng_dict, ds];
 */
async function GenSummaryTbl_cb(classno, term, cb, calcflag = true, updateflag = false) {
    let data = await GetMrkTblSet(classno, new TMarkCalC_Act(), calcflag, updateflag)
    cb(data);
}

async function GenSummaryTbl(classno, term, calcflag = true, updateflag = false) {
    let data = await GetMrkTblSet(classno, new TMarkCalC_Act(), calcflag, updateflag)
    if (term == 5) return View_cross_tbl_SecTerm(...data);
    return View_cross_tbl(...data);
}

async function GetMrkTblSet(classno, iCalc = null, calcflag = true, updateflag = false) {
    let std_dt = await getModel().DB_reader(formatString("SELECT stud_ref,dsej_ref,curr_class,curr_seat,c_name,e_name,del_flag from studinfo where curr_class='{0}' order by curr_seat", classno));
    //console.table(std_dt.slice(0, 2))
    let crs_dt = await getModel().DB_reader(formatString("SELECT course_d_id,courseName,c_T_type,c_field,groupid,tab,rate,c_ng_id FROM eschool.mrs_course_detail where classno ='{0}' order by groupid,tab;", classno));
    //console.log(crs_dt.length)
    //console.table(crs_dt.slice(0,10))
    let ng_dict = {};
    const [year, ngdr] = await getModel().DB_reader("SELECT session_desc FROM  `mrs_session_def` where curr_flag=1;select NG_ID,NG from ngrade_table");
    ngdr.forEach(elm => ng_dict[elm.NG_ID] = elm.NG);
    //console.log(year)
    //console.table(ng_dict)
    let subsql = [
        "SELECT stud_ref,GROUP_CONCAT(pingyu1 ORDER BY Lineno SEPARATOR '') as py1,GROUP_CONCAT(pingyu2 ORDER BY Lineno SEPARATOR '') as py2,GROUP_CONCAT(pingyu3 ORDER BY Lineno SEPARATOR '') as py3 FROM mrs_pingyu where classno='{0}' group by stud_ref order by seat;",
        "SELECT stud_ref,wrg_later1,wrg_absence1,wrg_truancy_t1,wrg_truancy_s1,WrgMarks1,honor1,SE_HONOR1,wrg_later2,wrg_absence2,wrg_truancy_t2,wrg_truancy_s2,WrgMarks2,honor2,SE_HONOR2,wrg_later3,wrg_absence3,wrg_truancy_t3,wrg_truancy_s3,WrgMarks3,honor3,SE_HONOR3,conduct1,conduct2,conduct3,conduct,mark1,mark2,mark3,mark,ran1,ran2,ran3,ran,total_crs_ncp,voca_cult_avg,voca_cult_avg1,voca_cult_avg2,voca_cult_avg3,voca_prof_avg,voca_prof_avg1,voca_prof_avg2,voca_prof_avg3,voca_cult_mue,voca_prof_mue,SchoolEval1,SchoolEval2,SchoolEval3,volunteer_hr,allpass1,allpass2,allpass3 FROM mrs_stud_conduct where classno='{0}';",
        "SELECT a.stud_c_id,a.stud_ref,a.course_d_id,a.e1,a.t1,a.e2,a.t2,a.e3,a.t3,a.total1,a.total2,a.total3,a.sub_c_p,a.total,a.pk,a.P_X,a.VOCA_MUE,a.eog, coursename,c_t_type,groupid,tab,c_ng_id,rate FROM mrs_stud_course a left join mrs_course_detail b on a.course_d_id=b.course_d_id where a.classno='{0}' and b.classno='{0}' order by a.stud_ref,b.groupid,b.tab;",
        "SELECT stud_ref,activeName,grade1,grade2,grade3,grade,subXF,addXF,bk,act_py FROM mrs_stud_active where classno='{0}';",
        "SELECT stud_ref,GC_Name,grade1,grade2,grade3 FROM mrs_stud_grade_course where classno='{0}' order by cgid"
    ].join("");
    let dt = await getModel().DB_reader(formatString(subsql, classno, classno, classno, classno, classno, classno));
    //console.log(dt.forEach((element,idx) => {console.log(idx); console.log(subtbNs[idx]);console.table(element.slice(0,2))}))
    let ds = [];
    for (let std of std_dt) {
        let row = {
            "std": std.stud_ref,
            "info": std,
            "py": dt[0].filter(r => r.stud_ref == std.stud_ref),
            "cd": dt[1].filter(r => r.stud_ref == std.stud_ref),
            "mk": dt[2].filter(r => r.stud_ref == std.stud_ref),
            "ac": dt[3].filter(r => r.stud_ref == std.stud_ref),
            "gc": dt[4].filter(r => r.stud_ref == std.stud_ref),
        }
        ds.push(row)
    }
    if (calcflag) {
        MarkIterateCalc(ds, ng_dict, iCalc,classno)
        if (updateflag) {
            mk_adpt_Update(ds, "mk");
            cd_adpt_Update(ds, "cd");
        }
    }
    return [std_dt, crs_dt, ng_dict, ds];
}

//////////////////////////
module.exports = {
    HttpGet_pyapi: HttpGet_pyapi,
    HttpGet_pyapi_cb: HttpGet_pyapi_cb,
    Uploadfile: Uploadfile,
    Dowanloadfile: Dowanloadfile,
    GenSummaryTbl: GenSummaryTbl,
    GenSummaryTbl_cb:GenSummaryTbl_cb,
    View_Cross_TotalData:View_Cross_TotalData,
    View_Cross_Data:View_Cross_Data,

}


if (require.main === module) {
    GenSummaryTbl('SC1E', 1);
    (async function () {
      //let classno='SC1E'
      //let data = await GetMrkTblSet(classno, new TMarkCalC_Act(), true, false)
      //fs.writeFileSync('data.txt', JSON.stringify(data));
      //let data_ = JSON.parse(fs.readFileSync('data.txt')); //[std_dt, crs_dt, ng_dict, ds];
      //MarkIterateCalc(data_[3], data_[2], new iMarkCalC_Act(), classno)
      //console.log("====out put=====")
      //console.log(data_[3])
    })();
}



