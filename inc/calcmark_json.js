const http = require('http');
const querystring = require('querystring');
const { iMarkCalC_Act, TMarkCalC_Act, MarkIterateCalc } = require("./calcmark_core")
const cm_core = require("./calcmark_core")
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
            //getModel().DataReaderQuery(sql, [data, r.stud_c_id], (err, results) => {/* */ })
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
            //getModel().DataReaderQuery(sql, [data, r.stud_ref], (err, results) => {/**/ })
        }
    }
}

async function GetMrkTblSet(classno, iCalc = null, calcflag = true, updateflag = false) {
    let [std_dt, crs_dt, ng_dict, ds] = JSON.parse(fs.readFileSync('./secert/data_.txt')); //;
    if (calcflag) {
        cm_core.MarkIterateCalc(ds, ng_dict, iCalc, classno)
        if (updateflag) {
            mk_adpt_Update(ds, "mk");
            cd_adpt_Update(ds, "cd");
        }
    }
    return [std_dt, crs_dt, ng_dict, ds];
}

//////////////////////////
module.exports = {
    GetMrkTblSet: GetMrkTblSet,
}



if (require.main === module) {
    (async function(){
        let [std_dt, crs_dt, ng_dict, ds]=await GetMrkTblSet('SC1E',new cm_core.iMarkCalC_Act(),true,false)
        let res={} //TotalMarks TestExam NegaAcadCred
        {
          let [cross_, std, crs]=cm_core.View_Cross_Data(ds,"mk",std_dt,crs_dt,3,ng_dict,(mk)=>[mk.t2,mk.e2,mk.total2]);
          res["TestExam"]=cm_core.MartixWithColuName(cross_,std,crs,[])
        }
        {
           let [cross_, std, crs]=cm_core.View_Cross_TotalData(ds,"mk",std_dt,crs_dt,1,ng_dict,["扣減","mark2","ran2","voca_cult_avg","voca_prof_avg","conduct2","WrgMarks2","honor2"],
            (mk)=>{
               return [mk.total2,0]
                }
           );
           res["TotalMarks"]=cm_core.MartixWithColuName(cross_,std,crs,["扣減","mark2","ran2","voca_cult_avg","voca_prof_avg","conduct2","WrgMarks2","honor2"])
        }
        {
          let [cross_, std, crs]=cm_core.View_Cross_TotalData(ds,"mk",std_dt,crs_dt,1,ng_dict,["扣減"],(mk)=>{
            let m_=Math.round((mk.total2 * 0.3 + mk.total1 * 0.3 - 36) * 6 / 4)
            return [m_,m_]
          });
          res["NegaAcadCred"]=cm_core.MartixWithColuName(cross_,std,crs,["扣減"])
        }
        Object.keys(res).forEach(k => {
            console.log(k)
            console.table(res[k])
        });
            
    })()

}


