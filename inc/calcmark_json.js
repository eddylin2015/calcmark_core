const http = require('http');
const querystring = require('querystring');
const { iMarkCalC_Act, TMarkCalC_Act, MarkIterateCalc,View_cross_tbl,View_cross_tbl_SecTerm } = require("./calcmark_core")
const calcmak_core = require("./calcmark_core")
const { HttpGet_pyapi, Uploadfile, Dowanloadfile } = require("./calcmark_pyapi")
var fs = require('fs');
var path = require('path');


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
            //getModel().DataReaderQuery(sql, [data, r.stud_c_id], (err, results) => {/*console.log(err,results)*/ })
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
                SchoolEval1: "", SchoolEval2: "", SchoolEval3: "",
                SE_HONOR1: 0, SE_HONOR2: 0, SE_HONOR3: 0,
                conduct: ""
            }
            for (let k in data) data[k] = r[k];
            //getModel().DataReaderQuery(sql, [data, r.stud_ref], (err, results) => {/*console.log(err,results)*/ })
        }
    }
}

async function GenSummaryTbl(classno, term, calcflag = true, updateflag = false) {
    let data = await GetMrkTblSet(classno, new TMarkCalC_Act(), true, true)
    if (term == 5) return View_cross_tbl_SecTerm(...data);
    return View_cross_tbl(...data);
}

async function GetMrkTblSet(classno, iCalc = null, calcflag = true, updateflag = false) {
    let [std_dt, crs_dt, ng_dict, ds] = JSON.parse(fs.readFileSync('./secert/data_.txt')); //;
    if (calcflag) {
        MarkIterateCalc(ds, ng_dict, iCalc, classno)
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
    Uploadfile: Uploadfile,
    Dowanloadfile: Dowanloadfile,
    GenSummaryTbl: GenSummaryTbl,
}



if (require.main === module) {
    //GenSummaryTbl('SC1E', 1);
    (async function(){
        let [std_dt, crs_dt, ng_dict, ds]=await GetMrkTblSet('SC1E',new iMarkCalC_Act(),true,false)
        let [cross_, std_dt_, crs]=calcmak_core.View_cross_tbl_Term(std_dt,crs_dt,ng_dict,ds,1)
        console.table(cross_)
        let [cross_TestExam, _, __]=calcmak_core.View_cross_tbl_TermTestExam(std_dt,crs_dt,ng_dict,ds,1)
        console.table(cross_TestExam)
    })()

}


