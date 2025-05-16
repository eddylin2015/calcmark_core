
/*
* iMarkCalc_Act and SimpleCalc
*/
class iMarkCalC_Act {
    constructor() {
        this.mark1 = 0; this.mark2 = 0; this.mark3 = 0; this.mark = 0; this.total_crs_ncp = 0; this.crs_cnt = 0;
        this.ran1 = 0; this.ran2 = 0; this.ran3 = 0; this.ran = 0; this.allpass1 = 0; this.allpass2 = 0; this.allpass3 = 0;
        this.voca_cult_avg = 0; this.voca_cult_avg1 = 0; this.voca_cult_avg2 = 0; this.voca_cult_avg3 = 0;
        this.voca_prof_avg = 0; this.voca_prof_avg1 = 0; this.voca_prof_avg2 = 0; this.voca_prof_avg3 = 0;
        this.voca_cult_mue = 0; this.voca_cult_cnt = 0;
        this.voca_prof_mue = 0; this.voca_prof_cnt = 0;
        this.allpass1 = 0;
        this.allpass2 = 0;
        this.allpass3 = 0;
        this.pass1_cnt = 0; this.pass2_cnt = 0; this.pass3_cnt = 0;
    }
    /*
    * Clear buffer 
    */
    method_clear() {
        for (let k in this) if (k.indexOf("method_") < 0) this[k] = 0;
    }
    /*
    * Count courses , culture courses, prof courses
    */
    method_inc_count(r) {
        this.crs_cnt++;
        this.voca_cult_cnt += r.c_t_type == '職業文化' ? 1 : 0;
        this.voca_prof_cnt += r.c_t_type == '職業專業' ? 1 : 0;
    }
    /*
    * Calc total  3:3:4 rate forEach term.
    */
    method_total(r, ng_dict, total1, total2, total3, mue) {
        r.total1 = total1
        r.total2 = total2
        r.total3 = total3
        r.total = r.total1 * 0.3 + r.total2 * 0.3 + r.total3 * 0.4
        r.VOCA_MUE = r.total < 60 ? Math.max(r.total, mue) : r.total
        r.sub_c_p = r.total < 60 && r.pk < 60 ? r.sub_c_p = ng_dict[r.c_ng_id] : 0;
        r.P_X = r.total < 60 ? (r.sub_c_p < 0 ? 1 : 2) : 0;
        r.eog = 1;
    }
    /*
    * Accumulate r.total + Agg_.mark-> Agg_.mark 
    */
    method_agg_data(ro) {
        this.pass1_cnt += ro.total1 < 60 ? 0 : 1;
        this.pass2_cnt += ro.total2 < 60 ? 0 : 1;
        this.pass3_cnt += ro.total < 60 ? 0 : 1;
        this.mark1 += ro.total1;
        this.mark2 += ro.total2;
        this.mark3 += ro.total3;
        this.mark += ro.total;
        this.total_crs_ncp += ro.sub_c_p;
    }
    /*
    * Export Agg_data -> dataSet
    */
    method_assignTo(dataSet,cno="") {
        this.mark1 = Math.round(this.mark1 / this.crs_cnt * 100) / 100;
        this.mark2 = Math.round(this.mark2 / this.crs_cnt * 100) / 100;
        this.mark3 = Math.round(this.mark3 / this.crs_cnt * 100) / 100;
        this.mark = Math.round(this.mark / this.crs_cnt * 100) / 100;
        this.allpass1 = this.pass1_cnt == this.crs_cnt ? 1 : 0;
        this.allpass2 = this.pass2_cnt == this.crs_cnt ? 1 : 0;
        this.allpass3 = this.pass3_cnt == this.crs_cnt ? 1 : 0;
        for (let k in this)
            if (k.indexOf("_cnt") < 0 && k.indexOf("method_") < 0) dataSet[k] = this[k];
        let [se1,sh1]=iMarkCalC_Act.GetEval(cno,this.allpass1,this.mark1,dataSet.conduct1,dataSet.wrg_later1,dataSet.wrg_absence1,dataSet.wrg_truancy_t1)
        let [se2,sh2]=iMarkCalC_Act.GetEval(cno,this.allpass2,this.mark2,dataSet.conduct2,dataSet.wrg_later2,dataSet.wrg_absence2,dataSet.wrg_truancy_t2)
        let [se3,sh3]=iMarkCalC_Act.GetEval(cno,this.allpass3,this.mark ,dataSet.conduct3,dataSet.wrg_later3,dataSet.wrg_absence3,dataSet.wrg_truancy_t3)
        dataSet["SchoolEval1"]=se1; 
        dataSet["SchoolEval2"]=se2;
        dataSet["SchoolEval3"]=se3; 
        dataSet["SE_HONOR1"]=sh1;
        dataSet["SE_HONOR2"]=sh2;
        dataSet["SE_HONOR3"]=sh3;
        let totalWrg =  Number(dataSet["WrgMarks1"]) +
                        Number(dataSet["WrgMarks2"]) +
                        Number(dataSet["WrgMarks3"]);
        dataSet["conduct"]= iMarkCalC_Act.CalcAvgConduct(
            dataSet["conduct1"], 
            dataSet["conduct2"], 
            dataSet["conduct3"],
            totalWrg);

    }
    /*
    * Rank
    */
    method_rank(ds) {
        let mark1_rank_map = ds.map(r => r["cd"][0].mark1);
        let mark2_rank_map = ds.map(r => r["cd"][0].mark2);
        let mark3_rank_map = ds.map(r => r["cd"][0].mark3);
        let mark_rank_map = ds.map(r => r["cd"][0].mark);
        mark1_rank_map.sort((a, b) => b - a);
        mark2_rank_map.sort((a, b) => b - a);
        mark3_rank_map.sort((a, b) => b - a);
        mark_rank_map.sort((a, b) => b - a);
        ds.forEach(r => {
            r["cd"][0].ran1 = mark1_rank_map.indexOf(r["cd"][0].mark1) + 1;
            r["cd"][0].ran2 = mark2_rank_map.indexOf(r["cd"][0].mark2) + 1;
            r["cd"][0].ran3 = mark3_rank_map.indexOf(r["cd"][0].mark3) + 1;
            r["cd"][0].ran = mark_rank_map.indexOf(r["cd"][0].mark) + 1;
        })
    }
    /*
    * round 
    */
    method_round_total(r) {
        r.total1 = Math.round(r.total1 * 100) / 100;
        r.total2 = Math.round(r.total2 * 100) / 100;
        r.total3 = Math.round(r.total3 * 100) / 100;
        r.total = Math.round(r.total * 100) / 100;
        // Math.round((num + Number.EPSILON) * 100) / 100
    }
    static NoOfConduct(conduct) {
        let cd = conduct.trim().replace("＋", "+").replace("－", "-").replace("一", "-");
        let rule = "丙-,丙,丙+,乙-,乙,乙+,甲-,甲";
        let ra = rule.split(',');
        for (let i = 0; i < ra.length; i++) {
            if (ra[i]==cd) return i;
        }
        return -1;
    }
    static ConductOfNo(c) {
        if (c < 0) return "";
        let rule = "丙-,丙,丙+,乙-,乙,乙+,甲-,甲";
        let ra = rule.split(',');
        if (c >= ra.length) c = ra.length - 1;
        return ra[c];
    }
    static CalcAvgConduct(conduct1, conduct2, conduct3, wrgMarks=0)
    {
        let c1 = iMarkCalC_Act.NoOfConduct(conduct1);
        let c2 = iMarkCalC_Act.NoOfConduct(conduct2);
        let c3 = iMarkCalC_Act.NoOfConduct(conduct3);
        if (c3 == -1) return "";
        let avgc = (c1 + c2 + c3) / 3;
        /***************************************
         * if (avgc > 5 && wrgMarks > 0) avgc = 5;暫定未执行
         * 日期:2021年7月14日,鄭生申請,按第一二三段操行規定,延伸學年平均操行。
         * logby.eddylin.20210704
         ***************************************/
        if (avgc > 5 && wrgMarks > 0) avgc = 5;
        //console.log(`${wrgMarks},${avgc0}`);
        return iMarkCalC_Act.ConductOfNo(avgc);
    }

    static GetEval(cno, allpass, mark, conduct, later, absence, truancy) {
        let EvalAddHonorInt = 0;
        cno =  cno.toUpperCase();
        let HonorEvalDESC_ARR = ["品學卓越生\n", "品學兼優生\n", "品行優異生\n", "學業優異生\n", "勤學生\n"];
        let SMg = [85, 80, 75];
        let PMg = [101, 85, 75];
        let mg = null;
        if (cno[0] == 'P') { mg = PMg; }
        else if (cno[0] == 'S') { mg = SMg; }
        else { mg = SMg; }
        let res = "";
        let noOfcond = iMarkCalC_Act.NoOfConduct(conduct);
        if (allpass == 1) {
            if (mark >= mg[0] && noOfcond >= 6) {
                res += HonorEvalDESC_ARR[0];
            }
            else if (mark >= mg[1] && noOfcond >= 6) {
                res += HonorEvalDESC_ARR[1];
            }
            else if (noOfcond >= 6) {
                res += HonorEvalDESC_ARR[2];
            }
            else if (mark >= mg[1] && noOfcond >= 4) {
                res += HonorEvalDESC_ARR[3];
            }
            else if (mark >= mg[2] && noOfcond >= 4) {
                res += HonorEvalDESC_ARR[4];
            }
        }
        if (later == 0 && absence == 0 && truancy == 0) {
            res += "全勤生";
        }
        return [res, EvalAddHonorInt];
    }

}
class TMarkCalC_Act extends iMarkCalC_Act {
    constructor() {
        super();
    }
    method_assignTo(dataSet,cno="") {
        if (this.voca_cult_cnt > 0 && this.voca_prof_cnt > 0) {
            this.voca_cult_avg1 = Math.round(this.voca_cult_avg1/this.voca_cult_cnt *100)/100;
            this.voca_cult_avg2 = Math.round(this.voca_cult_avg2/this.voca_cult_cnt *100)/100;
            this.voca_cult_avg3 = Math.round(this.voca_cult_avg3/this.voca_cult_cnt *100)/100;
            this.voca_cult_avg  = Math.round(this.voca_cult_avg /this.voca_cult_cnt *100)/100;
            this.voca_cult_mue  = Math.round(this.voca_cult_mue /this.voca_cult_cnt *100)/100;
            this.voca_prof_avg1 = Math.round(this.voca_prof_avg1/this.voca_prof_cnt *100)/100;
            this.voca_prof_avg2 = Math.round(this.voca_prof_avg2/this.voca_prof_cnt *100)/100;
            this.voca_prof_avg3 = Math.round(this.voca_prof_avg3/this.voca_prof_cnt *100)/100;
            this.voca_prof_avg  = Math.round(this.voca_prof_avg /this.voca_prof_cnt *100)/100;
            this.voca_prof_mue  = Math.round(this.voca_prof_mue /this.voca_prof_cnt *100)/100;
        }
        super.method_assignTo(dataSet,cno)
    }
    method_agg_data(ro) {
        super.method_agg_data(ro);
        if (ro.c_t_type == '職業文化') {
            this.voca_cult_avg1 += ro.total1;
            this.voca_cult_avg2 += ro.total2;
            this.voca_cult_avg3 += ro.total3;
            this.voca_cult_avg += ro.total;
            this.voca_cult_mue += ro.VOCA_MUE;
        }
        if (ro.c_t_type == '職業專業') {
            this.voca_prof_avg1 += ro.total1;
            this.voca_prof_avg2 += ro.total2;
            this.voca_prof_avg3 += ro.total3;
            this.voca_prof_avg += ro.total;
            this.voca_prof_mue += ro.VOCA_MUE;
        }
    }
}

// '職業文化' '職業專業'
function MarkIterateCalc(ds, ng_dict, iCalc = null, cno = "S") {
    let cd_set = iCalc ? iCalc : new TMarkCalC_Act();
    for (let arr_ of ds) {
        cd_set.method_clear();
        let mk = arr_["mk"]
        let cd = arr_["cd"]
        let mk_group = []
        mk.forEach((r, i, self_) => {
            if (r.rate == 100) {
                cd_set.method_total(r, ng_dict,
                    r.t1 * 0.6 + r.e1 * 0.4,
                    r.t2 * 0.6 + r.e2 * 0.4,
                    r.t3 * 0.6 + r.e3 * 0.4,
                    r.pk)
                cd_set.method_round_total(r)
                cd_set.method_inc_count(r)
                cd_set.method_agg_data(r)
            } else if (i < mk.length && r.groupid !== mk[i + 1].groupid) {
                mk_group.push(r)
                let agg_ = mk_group.reduce((sum, ro, idx) => {
                    let tt1 = (ro.t1 * 0.6 + ro.e1 * 0.4) * ro.rate / 100
                    let tt2 = (ro.t2 * 0.6 + ro.e2 * 0.4) * ro.rate / 100
                    let tt3 = (ro.t3 * 0.6 + ro.e3 * 0.4) * ro.rate / 100
                    sum[0] += (ro.t1 * 0.6 + ro.e1 * 0.4) * ro.rate / 100
                    sum[1] += (ro.t2 * 0.6 + ro.e2 * 0.4) * ro.rate / 100
                    sum[2] += (ro.t3 * 0.6 + ro.e3 * 0.4) * ro.rate / 100
                    sum[3] += Math.max(tt1 * 0.3 + tt2 * 0.3 + tt3 * 0.4, r.pk) * ro.rate / 100
                    return sum;
                }, [0, 0, 0, 0])
                cd_set.method_total(r, ng_dict, ...agg_);
                if (r.P_X == 1) {
                    for (let idx = i; idx > i - mk_group.length; idx--) {
                        let t_ = (r.t1 * 0.6 + r.e1 * 0.4 + r.t2 * 0.6 + r.e2 * 0.4) * 0.3 + (r.t3 * 0.6 + r.e3 * 0.4) * 0.4;
                        mk[idx].P_X = t_ < 60 ? (mk[idx].pk < 60 ? 1 : 2) : 0;
                    }
                }
                cd_set.method_round_total(r)
                cd_set.method_inc_count(r)
                cd_set.method_agg_data(r)
                mk_group = []
            } else {
                r.total1=0;
                r.total2=0;
                r.total3=0;
                r.total=0;
                r.sub_c_p=0;
                r.VOCA_MUE=0;
                r.eog=0;
                r.P_X=0;
                mk_group.push(r)
            }
        })
        if (mk_group.length > 0) throw new Error("mk_group is not empty!");
        cd_set.method_assignTo(cd[0],cno)

    }
    cd_set.method_rank(ds)
    console.table(ds[0]["mk"])
    console.log(ds[0]["cd"])
    //console.log(ds[1]["cd"])
}

function View_cross_tbl_SecTerm(std_dt, crs_dt, ng_dict, ds) {
    let crs = []
    let cols_len = crs_dt.length;
    let crs_dict = {};
    let ng_posi = {};
    let ign_cnt = 0;
    crs_dt.forEach((r, i) => {
        if (r.rate == 100
            || (i < cols_len && r.groupid !== crs_dt[i + 1].groupid)) {
            crs_dict[r.course_d_id] = i - ign_cnt;
            ng_posi[i - ign_cnt] = ng_dict[r.c_ng_id];
            crs.push(r.rate == 100 ? r.courseName : r.c_field)
        } else {
            ign_cnt++;
        }
    })
    let cross_ = []
    std_dt.forEach(elm => { cross_.push(Array.from({ length: cols_len + 1 }, (_, i) => null)) })
    std_dt.forEach((elm, i) => {
        ds[i]["mk"].forEach((mk, mi) => {
            if (mk.course_d_id in crs_dict) {
                let m_ = Math.round((mk.total2 * 0.3 + mk.total1 * 0.3 - 36) * 6 / 4);
                cross_[i][crs_dict[mk.course_d_id]] = m_;
                if (m_ < 0) {
                    let ng_ = ng_posi[crs_dict[mk.course_d_id]];
                    cross_[i][cols_len] = cross_[i][cols_len] ?  cross_[i][cols_len] + ng_:ng_;
                }
            }
        })
    });
    crs = [...crs, ...Array.from({ length: ign_cnt + 1 }, (_, i) => "")]
    return [cross_, std_dt, crs];
}

function View_cross_tbl(std_dt, crs_dt, ng_dict, ds) {
    let crs = []
    let cols_len = crs_dt.length;
    let crs_dict = {};
    crs_dt.forEach((r, i) => { crs_dict[r.course_d_id] = i; crs.push(r.courseName) })
    let cross_ = []
    std_dt.forEach(elm => { cross_.push(Array.from({ length: cols_len }, (_, i) => null)) })
    std_dt.forEach((elm, i) => {
        ds[i]["mk"].forEach((mk, mi) => {
            cross_[i][crs_dict[mk.course_d_id]] = mk.total2;
        })
    });
    return [cross_, std_dt, crs];
}

function View_cross_tbl_Term(std_dt, crs_dt, ng_dict, ds, term=0) {
    let crs = []
    let cols_len = crs_dt.length;
    let crs_dict = {};
    crs_dt.forEach((r, i) => { crs_dict[r.course_d_id] = i; crs.push(r.courseName) })
    let cross_ = []
    std_dt.forEach(elm => { cross_.push(Array.from({ length: cols_len }, (_, i) => null)) })
    std_dt.forEach((elm, i) => {
        ds[i]["mk"].forEach((mk, mi) => {
            cross_[i][crs_dict[mk.course_d_id]] = term==1 ? mk.total1: term==2 ? mk.total2: term==3 ? mk.total3:mk.total
        })
    });
    return [cross_, std_dt, crs];
}

function View_cross_tbl_TermTestExam(std_dt, crs_dt, ng_dict, ds, term=0) {
    let crs = []
    let cols_len = crs_dt.length*2;
    let crs_dict = {};
    crs_dt.forEach((r, i) => { crs_dict[r.course_d_id] = i; crs.push(r.courseName+"T");crs.push(r.courseName+"E") })
    let cross_ = []
    std_dt.forEach(elm => { cross_.push(Array.from({ length: cols_len }, (_, i) => null)) })
    std_dt.forEach((elm, i) => {
        ds[i]["mk"].forEach((mk, mi) => {
            cross_[i][crs_dict[mk.course_d_id]*2] = term==1 ? mk.total1: term==2 ? mk.total2: term==3 ? mk.total3:mk.total
            cross_[i][crs_dict[mk.course_d_id]*2+1] = term==1 ? mk.total1: term==2 ? mk.total2: term==3 ? mk.total3:mk.total
        })
    });
    return [cross_, std_dt, crs];
}

module.exports = {
    iMarkCalC_Act: iMarkCalC_Act,
    TMarkCalC_Act: TMarkCalC_Act,
    MarkIterateCalc:MarkIterateCalc,
    View_cross_tbl:View_cross_tbl,
    View_cross_tbl_SecTerm:View_cross_tbl_SecTerm,
    View_cross_tbl_Term:View_cross_tbl_Term,
    View_cross_tbl_TermTestExam:View_cross_tbl_TermTestExam,
}