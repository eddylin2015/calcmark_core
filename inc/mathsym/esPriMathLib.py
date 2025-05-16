import random  # 亂數
import math  # math 內置數學函數
import numpy as np  # 數字矩陣
import sympy as sp  # sympy 簡易別名 sp
import scipy 
from scipy import optimize as sci_opt
from sympy import I, pi, E
from sympy.parsing.sympy_parser import parse_expr  # 文字字串, 解釋成, Sympy 運算式
from sympy.plotting import plot  # 繪圖表
import json  # JSON 結構化資料
import datetime
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy.solvers.inequalities import reduce_rational_inequalities
from sympy import lambdify
from matplotlib.figure import Figure
import re
import esutils as lib
import os
from sympy.geometry import Point, Circle, Triangle, Segment, Line, RegularPolygon
import matplotlib.pyplot as plt
import base64
from io import BytesIO
"""
小學數學題庫        
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
NTE 多條題目.
NTE=[]; NTE.append(GetTE(Qid,St,Val))
for TE in NTE:  pass
"""

def GetKey(QIID="None"):
    return r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())

def GetTE(Qid, St, Val, Tx=0):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = {}
    #TE["Key"] =r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())
    TE["Id"] = Qid
    TE["Tx"] = Tx
    TE["St"] = St
    TE["Val"] = Val
    TE["Ans"] = ""
    TE["OK"] = 0
    TE["Mark"] = 0
    TE["MxMunites"] = 3
    TE["Minute"]= datetime.datetime.now().strftime("%M:%S")   #"%m-%d-%Y %H:%M:%S"
    TE["Tip"] = ["答題","答題","答題","答題","答題","答題","答題","答題","答題","答題"]
    TE["PotImg"]=None
    TE["PlainText"]=None
    TE["ValFmt"]=None
    TE["ValSt"]=None
    #TE["St_"]=""
    return TE

def GetTE_V2(Qid, St, St_, Val, Tx=0):
    TE=GetTE(Qid, St, Val, Tx=0)
    #TE["St_"]=St_
    return TE
"""
        "PP401.1.除法(整除)",
        "PP402.1.除法(有餘數)",
        "PP403.1.整數四則",
        "PP404.1.混合計算",
        "PP405.1.分數",
        "PP406.1.小數",
        "PP407.1.整除性",
        "PP408.1.對稱圖形",
        "PP409.1.倍數和因數",
        "PP410.1.近似值",
        "PP411.1.垂直線和",
        "PP412.1.平行線",
        "PP501.1.異分母分數加法",
        "PP502.1.異分母分數減法",
        "PP503.1.異分母分數加減混合計算",
        "PP504.1.小數與整數的乘法",
        "PP505.1.小數乘小數",
        "PP506.1.小數除法",
        "PP507.1.積和商的近似值",
        "PP508.1.解方程",
        "PP509.1.分數乘法",
        "PP510.1.分數除法",
        "PP511.1.分數四則混合計算",
        "PP512.1.分數和小數互化",
        "PP513.1.分數和小數混合運算",
        "PP514.1.圖形的面積",
        "PP515.1.四角柱體的表面積",
        "PP516.1.四角柱體的體積",
        "PP601.1.整數四則運算",
        "PP602.1.小數的加減",
        "PP603.1.小數的乘除",
        "PP604.1.小數四則運算",
        "PP605.1.分數的加減",
        "PP606.2.分數的乘除",
        "PP607.1.整數、小數及分數四則",
        "PP608.1.通/約分",
        "PP609.3.解方程",
        "PP610.1.解比例",
        "PP611.1.小數、分數及百分數互化(取至近似值)",
        "PP612.1.分數四則",
        "PP613.1.各數四則混合計算",
"""

PriQList=  [
        "PP421.1.簡便計算",
        "PP422.1.数学广角-龟兔同笼",
        "PP508.1.解方程",
        "PP610.1.解比例"
        ]
"""
算式
"""
def Get_Expr(QIID,QAMT,Tx=-1):
    NTE=None
    if   QIID=="PP401":  NTE=Get_PP401_Expr(QAMT,Tx)
    elif QIID=="PP402":  NTE=Get_PP402_Expr(QAMT,Tx)
    elif QIID=="PP403":  NTE=Get_PP403_Expr(QAMT,Tx)
    elif QIID=="PP404":  NTE=Get_PP404_Expr(QAMT,Tx)
    elif QIID=="PP405":  NTE=Get_PP405_Expr(QAMT,Tx)
    elif QIID=="PP406":  NTE=Get_PP406_Expr(QAMT,Tx)
    elif QIID=="PP407":  NTE=Get_PP407_Expr(QAMT,Tx)
    elif QIID=="PP408":  NTE=Get_PP408_Expr(QAMT,Tx)
    elif QIID=="PP409":  NTE=Get_PP409_Expr(QAMT,Tx)
    elif QIID=="PP410":  NTE=Get_PP410_Expr(QAMT,Tx)
    elif QIID=="PP411":  NTE=Get_PP411_Expr(QAMT,Tx)
    elif QIID=="PP412":  NTE=Get_PP412_Expr(QAMT,Tx)
    elif QIID=="PP501":  NTE=Get_PP501_Expr(QAMT,Tx)
    elif QIID=="PP501":  NTE=Get_PP501_Expr(QAMT,Tx)
    elif QIID=="PP502":  NTE=Get_PP502_Expr(QAMT,Tx)
    elif QIID=="PP503":  NTE=Get_PP503_Expr(QAMT,Tx)
    elif QIID=="PP504":  NTE=Get_PP504_Expr(QAMT,Tx)
    elif QIID=="PP505":  NTE=Get_PP505_Expr(QAMT,Tx)
    elif QIID=="PP506":  NTE=Get_PP506_Expr(QAMT,Tx)
    elif QIID=="PP507":  NTE=Get_PP507_Expr(QAMT,Tx)
    elif QIID=="PP508":  NTE=Get_PP508_Expr(QAMT,Tx)
    elif QIID=="PP509":  NTE=Get_PP509_Expr(QAMT,Tx)
    elif QIID=="PP510":  NTE=Get_PP510_Expr(QAMT,Tx)
    elif QIID=="PP511":  NTE=Get_PP511_Expr(QAMT,Tx)
    elif QIID=="PP512":  NTE=Get_PP512_Expr(QAMT,Tx)
    elif QIID=="PP513":  NTE=Get_PP513_Expr(QAMT,Tx)
    elif QIID=="PP514":  NTE=Get_PP514_Expr(QAMT,Tx)
    elif QIID=="PP515":  NTE=Get_PP515_Expr(QAMT,Tx)
    elif QIID=="PP516":  NTE=Get_PP516_Expr(QAMT,Tx)
    elif QIID=="PP601":  NTE=Get_PP601_Expr(QAMT,Tx)    
    elif QIID=="PP602":  NTE=Get_PP602_Expr(QAMT,Tx)    
    elif QIID=="PP603":  NTE=Get_PP603_Expr(QAMT,Tx)    
    elif QIID=="PP604":  NTE=Get_PP604_Expr(QAMT,Tx)    
    elif QIID=="PP605":  NTE=Get_PP605_Expr(QAMT,Tx)    
    elif QIID=="PP606":  NTE=Get_PP606_Expr(QAMT,Tx)    
    elif QIID=="PP607":  NTE=Get_PP607_Expr(QAMT,Tx)    
    elif QIID=="PP608":  NTE=Get_PP608_Expr(QAMT,Tx)    
    elif QIID=="PP609":  NTE=Get_PP609_Expr(QAMT,Tx)    
    elif QIID=="PP610":  NTE=Get_PP610_Expr(QAMT,Tx)    
    elif QIID=="PP611":  NTE=Get_PP611_Expr(QAMT,Tx)    
    elif QIID=="PP612":  NTE=Get_PP612_Expr(QAMT,Tx)    
    elif QIID=="PP613":  NTE=Get_PP613_Expr(QAMT,Tx)  
    elif QIID=="PP614":  NTE=Get_PP614_Expr(QAMT,Tx)  
    elif QIID=="PP615":  NTE=Get_PP615_Expr(QAMT,Tx)  
    elif QIID=="PP421":  NTE=Get_P302_Expr(QAMT,Tx)  
    elif QIID=="PP422":  NTE=Get_P303_Expr(QAMT,Tx)  
    else:
        return None
    return NTE

def Post_Expr_UpdateAns(ReqForm,NTE,TEid):
    for key in ReqForm.keys():
        if key=="SID": continue
        for value in ReqForm.getlist(key):
            for TE in NTE:
                if int(TE["Id"])==TEid:
                    if int(key)>=1000:
                        if int(TE["Id"])==int(key)-1000:
                            TE["Minute"]=value
                    elif int(TE["Id"])==int(key):
                        if TE["Ans"] != "" :  
                            TE["Ans"]=TE["Ans"]+";"+ value 
                        else:
                            TE["Ans"]=value

def Post_Expr_CheckAns(QIID,NTE,TEid=-1,MxMunites=3):
    for TE in NTE:
        if TEid > 0 and TE["Id"] != TEid:
            continue
        if QIID=="PP601" : Put_Expr_V2(TE)
        elif QIID=="PP602" : Put_Expr_V2(TE)
        elif QIID=="PP603" : Put_Expr_V2(TE)
        elif QIID=="PP609" : Put_PP609_Expr(TE)
        elif QIID=="PP610" : Put_Expr_V6(TE)
        else:  Put_Expr_V1(TE)
        #Get_Expr_CheckAnsMark(QIID,TE)

def Get_Expr_CheckAnsMark(QIID,TE):
    if TE["OK"]==1:
        try:
            MxMunites=TE["MxMunites"]
            stepM = MxMunites / 3 * 60
            m,s=TE["Minute"].split(":")
            m=int(m)
            s=int(s)
            m=m*60+s
            p=1+(stepM-m)/stepM
            k=max(0.2,p)
            k=min(1.8,k)
            k=round(k*10)
            TE["Mark"]=k
        except:
            TE["Mark"]=k

                
def Put_Expr_V1(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Put_Expr_V2(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")

    ans1 = ans[0]
    ans2 = ans[1] if len(ans) > 1 else "3.1415"
    if ans1.strip() == "":
        ans1 = "3.1415"
    if ans2.strip() == "":
        ans2 = "3.1415"
    try:
        if len(Val)==1:
            ans = [ parse_expr(ans1)]
            if ans == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        else:
            ans = [ parse_expr(ans1),  parse_expr(ans2)]
            if ans == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
    except:
        pass    

def Put_Expr_V6(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    ans1=[]
    try:    
        for temp in ans:
            if temp.strip() == "":
                ans1.append(parse_expr(  "3.1415"))
            else:
                ans1.append(parse_expr(lib.Text2St(temp)))
    
        if ans1 == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass    

def Put_Expr_S6(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    TE["OK"] = 0
    try:    
        for i_, temp in enumerate(ans):
            if lib.S6Compare(Val[i_], temp):
                TE["OK"] = 1
            else:
                TE["OK"] = 0
                return
    except:
        pass   

def Put_Expr_InequV1(TE):
    x = sp.symbols('x')
    Val = TE["Val"]
    Flag = False
    ans = TE["Ans"]
    if ans.strip()=="R" and "(-oo < x) & (x < oo)" == str(Val) :
        TE["OK"]=1
        return    
    ans = lib.Text2Inequ(TE["Ans"])
    #ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
    #ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)        
    #if ans == "" or  ans == "R" or ans == "r": ans = "(-oo < x) & (x < oo)"
    a1 = ans.split("|")
    a2 = ans.split("&")
    try:
        if len(a1) > 1:
            a_ = []
            for aa_ in a1:
                a_.append(sp.solve(aa_))
            Flag = (a_[0] | a_[1]) == Val
        elif len(a2) > 1:
            a_ = []
            for aa_ in a2:
                a_.append(sp.parse_expr(aa_))
            Flag = reduce_rational_inequalities([[a_[0], a_[1]]], x) == Val
        elif ans == '空集' or ans == '0'  or ans=='False' or ans=="false":
            if str(Val) == "False":
                Flag = True
        else:
            Flag = sp.solve(ans) == Val
        if Flag:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Put_Expr_X1(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass



def PlotImg(expr):
    x, y, z = sp.symbols('x,y,z')
    try:
        lam_x = lambdify(x, expr, modules=['numpy'])
        x_vals = np.linspace(-5, 5, 10)
        y_vals = lam_x(x_vals)
        fig = Figure()
        fig.set_figheight(3)
        fig.set_figwidth(3)            
        ax = fig.subplots()
        ax.plot(x_vals, y_vals)
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')          
        #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        return base64.b64encode(buf.getbuffer()).decode("ascii")
        #TE["PlotImg"]=f'data:image/png;base64,{data}'
        #return f"<img src='data:image/png;base64,{data}'/>"        
    except Exception as inst:
        print(inst)
        return None
        
"""PP401.1.除法(整除)"""
def Get_PP401_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP402.1.除法(有餘數)"""
def Get_PP402_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP403.1.整數四則"""
def Get_PP403_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP404.1.混合計算"""
def Get_PP404_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP405.1.分數"""
def Get_PP405_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP406.1.小數"""
def Get_PP406_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP407.1.整除性"""
def Get_PP407_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP408.1.對稱圖形"""
def Get_PP408_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP409.1.倍數和因數"""
def Get_PP409_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP410.1.近似值"""
def Get_PP410_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP411.1.垂直線和"""
def Get_PP411_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP412.1.平行線"""
def Get_PP412_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP501.1.異分母分數加法"""
def Get_PP501_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP502.1.異分母分數減法"""
def Get_PP502_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP503.1.異分母分數加減混合計算"""
def Get_PP503_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP504.1.小數與整數的乘法"""
def Get_PP504_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP505.1.小數乘小數"""
def Get_PP505_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP506.1.小數除法"""
def Get_PP506_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP507.1.積和商的近似值"""
def Get_PP507_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP508.1.解方程"""
def Get_PP508_Expr(QN,Tx=-1):
    x,y,z=sp.symbols("x y z")
    NTE = []
    for Qid in range(0,QN):
        p,q=np.random.choice(range(1,20),2)
        p=p if p!=0 else 1;q=q if q!=0 else 1
        if p>q:
            p,q=q,p
        q1=20-q
        k=Qid % 3
        if k==0:
            express_str=f"{p} + x  = {q}" 
            Val=q-p
            TE=GetTE(Qid,express_str,Val)
            NTE.append(TE)
        elif k ==1:
            express_str=f"{q} - x  = {p}" 
            Val=q-p
            TE=GetTE(Qid,express_str.replace("*",r" \times "),Val)
            NTE.append(TE)
        else:
            express_str=f" 2x- {p}  = {q}" 
            Val=parse_expr( f"{p+q}/2")
            TE=GetTE(Qid,express_str.replace("*",r" \times "),Val)
            NTE.append(TE)
        
    return NTE
        
"""PP509.1.分數乘法"""
def Get_PP509_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP510.1.分數除法"""
def Get_PP510_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP511.1.分數四則混合計算"""
def Get_PP511_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP512.1.分數和小數互化"""
def Get_PP512_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP513.1.分數和小數混合運算"""
def Get_PP513_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP514.1.圖形的面積"""
def Get_PP514_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP515.1.四角柱體的表面積"""
def Get_PP515_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP516.1.四角柱體的體積"""
def Get_PP516_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP601.1.整數四則運算"""
def Get_PP601_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP602.1.小數的加減"""
def Get_PP602_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP603.1.小數的乘除"""
def Get_PP603_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP604.1.小數四則運算"""
def Get_PP604_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP605.1.分數的加減"""
def Get_PP605_Expr(QN,Tx=-1):
    sample_list0=list(range(2,10))
    sample_list1=list(range(2,10))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP606.1.分數的乘除"""
def Get_PP606_Expr(QN,Tx=-1):
    sample_list0=list(range(2,10))
    sample_list1=list(range(2,10))
    NTE=[]
    if Tx==0:
        for Qid in range(0,QN):
            a=random.choice(sample_list0)
            b=random.choice(sample_list1)
            c=random.choice(sample_list1)
            qiz=sp.Mul(sp.Rational(a,b),sp.Rational(c,a*b),evaluate=False)
            #St=sp.latex(qiz) 
            St=" %s \\times %s " % (sp.latex(sp.Rational(a,b)),sp.latex(sp.Rational(c,a*b)))
            Val=sp.simplify(qiz)
            TE=GetTE(Qid,St,Val,Tx)
            NTE.append(TE)
        return NTE
    if Tx==1:
        for Qid in range(0,QN):
            a=random.choice(sample_list0)
            b=random.choice(sample_list1)
            c=random.choice(sample_list1)
            qiz=sp.Mul(sp.Rational(a,b),sp.Rational(a*b,c),evaluate=False)
            #St=sp.latex(qiz) 
            St=" %s \\div %s " % (sp.latex(sp.Rational(a,b)),sp.latex(sp.Rational(c,a*b)))
            Val=sp.simplify(qiz)
            TE=GetTE(Qid,St,Val,Tx)
            NTE.append(TE)
        return NTE
        
        
"""PP607.1.整數、小數及分數四則"""
def Get_PP607_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    if Tx==0:
        for Qid in range(0,QN):
            a=random.choice(sample_list0)
            b=random.choice(sample_list1)
            qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
            St=sp.latex(qiz)
            Val=sp.simplify(qiz)
            TE=GetTE(Qid,St,Val,Tx)
            NTE.append(TE)
        return NTE
    if Tx==1:
        for Qid in range(0,QN):
            a=random.choice(sample_list0)
            b=random.choice(sample_list1)
            qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
            St=sp.latex(qiz)
            Val=sp.simplify(qiz)
            TE=GetTE(Qid,St,Val,Tx)
            NTE.append(TE)
        return NTE        
        
"""PP608.1.通/約分"""
def Get_PP608_Expr(QN,Tx=-1):
    sample_list0=list(range(2,10))
    sample_list1=list(range(2,10))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        c=random.choice(sample_list1)
        qiz=sp.Rational(a*c,b*c)#,evaluate=False)
        if Qid % 2==0:
          St=["約分:","\\frac{%s}{%s} " % (a*c,b*c)]
          Val=sp.simplify(qiz)
          TE=GetTE(Qid,St,Val,Tx)
        else:
          St=["通分:","\\frac{%s}{%s} " % (a,b),"分母為%s" % (b*c),"求分子?(\\frac{%s}{%s}=\\frac{?}{%s})"%(a,b,b*c)]
          Val=a*c
          TE=GetTE(Qid,St,Val,Tx)
          TE["Tip"]=["分子"]
        NTE.append(TE)
    return NTE
        
"""PP609.1.解方程"""

def Put_PP609_Expr(TE):
    x, y, z = sp.symbols('x,y,z')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")

    ans1 = ans[0]
    ans2 = ans[1] if len(ans) > 1 else "3.1415"
    if ans1.strip() == "":
        ans1 = "3.1415"
    if ans2.strip() == "":
        ans2 = "3.1415"
    try:
        Val=list(Val.values())
        if len(Val)==1:
            ans = [ parse_expr(ans1)]
            
            if ans == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        else:
            ans = [ parse_expr(ans1),  parse_expr(ans2)]
            if ans == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
    except:
        pass  

def Get_PP609_Expr(QN,Tx=-1):
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    if Tx==0:
        for Qid in range(0, QN):
            #
            a = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=-k1*a+k2
            c2=k1*c+k2*d
            yy=(a*b)+c
            eq1 = sp.Eq(a*x+c,yy)
            eq2 = sp.Eq(c*x+d*y,c2)
            St = [eq1]
            #sp.latex(St)
            Val = sp.solve(St)
            SSt=r" %s " % (sp.latex(eq1))              
            TE = GetTE(Qid, SSt, Val, Tx)
            TE["Tip"] = "x"
            if Val == []:
                pass
            else:
                NTE.append(TE)
            #
    elif Tx==1:
        for Qid in range(0, QN):
            #
            a = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=-k1*a+k2
            c2= k1*c+k2*d
            if c>b: b,c=c,b
            yy=(a*b)-c
            eq1 = sp.Eq(a*x-c,yy)
            St = [eq1]
            #sp.latex(St)
            Val = sp.solve(St)
            SSt=r" %s " % (sp.latex(eq1))              
            TE = GetTE(Qid, SSt, Val, Tx)
            TE["Tip"] = "x"
            if Val == []:
                pass
            else:
                NTE.append(TE)
            #
                        
    elif Tx==2:
        for Qid in range(0, QN):
            #
            a = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=k1+k2
            c2=k1*c+k2*d
            eq1 = sp.Eq(x+y,a+b)
            eq2 = sp.Eq(2*x+4*y,2*a+4*b)
            St = [eq1, eq2]
            Val = (sp.solve(St, [x, y]))
            SSt=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(eq1),sp.latex(eq2))              
            TE = GetTE(Qid, SSt, Val, Tx)
            TE["Tip"] = "xy"
            if Val == []:
                pass
            else:
                NTE.append(TE)
            #
    elif Tx==3:
        for Qid in range(0, QN):       
            #
            a = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([ 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=k1*a+k2*b
            c2=k1*c+k2*d
            eq1 = sp.Eq(a*x+b*y, c1)
            eq2 = sp.Eq(c*x+d*y,c2)
            St = [eq1, eq2]
            Val = (sp.solve(St, [x, y]))
            SSt=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(eq1),sp.latex(eq2))              
            TE = GetTE(Qid, SSt, Val, Tx)
            TE["Tip"] = "xy"
            if Val == []:
                pass
            else:
                NTE.append(TE)
            #
    return NTE
        
"""PP610.1.解比例"""
def Get_PP610_Expr(QN,Tx=-1):
    sample_list0=list(range(1,4))
    sample_list1=list(range(1,4))
    sample_list2=list(range(10,20))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        c=10-a-b
        d=random.choice(sample_list1)*2
        long=(a+b+c)*d*4
        #qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=["用%s cm的鐵絲做一個長方體的框架。"%long,"長、宽、高的比是 %s:%s:%s。 "%(a,b,c),"長、宽、高分別是多少?"]
        Val=[a*d,b*d,c*d]
        
        TE=GetTE(Qid,St,Val,Tx)
        TE["Tip"]=["長","宽","高"]
        NTE.append(TE)
    return NTE
        
        
"""PP611.1.小數、分數及百分數互化(取至近似值)"""
def Get_PP611_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP612.1.分數四則"""
def Get_PP612_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
        
"""PP613.1.各數四則混合計算"""
def Get_PP613_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE

"""PP614.1.圓"""
def Get_PP614_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE


"""PP615.1.百分數"""
def Get_PP615_Expr(QN,Tx=-1):
    sample_list0=list(range(1,100))
    sample_list1=list(range(1,100))
    NTE=[]
    for Qid in range(0,QN):
        a=random.choice(sample_list0)
        b=random.choice(sample_list1)
        qiz=sp.Add(sp.Rational(a,b),sp.Rational(b,a),evaluate=False)
        St=sp.latex(qiz)
        Val=sp.simplify(qiz)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE






"""
P301
""" 
def Get_P301_Expr(QN,Tx=-1):
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            e1=sp.Rational(b, a)
            e2=sp.Rational(c, a)
            if e1+e2 <0:
                e1=e1*-1
                e2=e2*-1
            qiz = sp.Add(e1,e2, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
        elif Tx == 2:
            a = random.choice(range(10,50))  # 亂數a,b,c, 不為零
            b = random.choice(range(10,100))
            qiz = sp.Mul(a,b, evaluate=False)
            St = r" %s \times %s "%(a,b)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
        elif Tx == 3:
            a = random.choice(range(2,10))  # 亂數a,b,c, 不為零
            b = random.choice(range(10,100))
            c = a *b
            St = r" %s \div %s "%(c,a)  # 題目
            Val = sp.S(c)/a
        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            if a+b+c <0 :
                a=a*-1
                b=b*-1
                c=c*-1
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案
        TE = GetTE(Qid, St, Val, Tx)
        NTE.append(TE)
    return NTE
    
    
    
"""
P302
""" 
def Get_P302_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag:Tx = 0 if Qid < (QN//2) else 1  # Tx -半題型1 ,-半題型 2
        Tx=0
        if Tx==0:
            p,q=np.random.choice(range(1,20),2)
            p=p if p!=0 else 1;q=q if q!=0 else 1
            p=p+17
            q1=20-q
            express_str=f"{p} * {q} + {p} * {q1}" 
            St=parse_expr(express_str, evaluate=False) 
            Val=sp.simplify(St)
            TE=GetTE(Qid,express_str.replace("*",r" \times "),Val)
            NTE.append(TE)        
        elif Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)

        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)

    return NTE
    
"""
P303
""" 
def Get_P303_Expr(QN,Tx=-1):
    x,y,z=sp.symbols('x y z')
    NTE = []
    for Qid in range(0, QN):
        ai = np.random.choice(range(4,10), 2)
        if Tx == 0:
            sum_head=ai[0]+ai[1]
            sum_feet=ai[0]*2+ai[1]*4
            St = [f"鷄兔同籠,",f"有{sum_head}個頭,{sum_feet}隻腳,","問鷄兔分別有多少隻?"]
            Val = [ai[0],ai[1]]  # 簡化算式,得出標準答案
        elif Tx == 1:
            times=random.choice([2,3,4])
            ai[0]=ai[1]*times
            sum_head=ai[0]+ai[1]
            sum_feet=ai[0]*2+ai[1]*4
            St =[ f"鷄兔同籠,",f"有{sum_head}個頭,數量鷄是兔{times}倍,"," 問鷄兔分別有多少隻?"]
            Val = [ai[0],ai[1]]  # 簡化算式,得出標準答案
        elif Tx == 2:
            times=random.choice([2,3,4])
            ai[1]=ai[0]*times
            sum_head=ai[0]+ai[1]
            sum_feet=ai[0]*2+ai[1]*4
            St = [f"鷄兔同籠,",f"有{sum_head}個頭,數量兔是鷄{times}倍,"," 問鷄兔分別有多少隻?"]
            Val = [ai[0],ai[1]]  # 簡化算式,得出標準答案
        else:
            sum_head=ai[0]+ai[1]
            sum_feet=ai[0]*2+ai[1]*4
            St = [f"鷄兔同籠,",f"有{sum_head}個頭,{sum_feet}隻腳,"," 問鷄兔分別有多少隻?"]
            Val = [ai[0],ai[1]]  # 簡化算式,得出標準答案
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"]="鷄兔"  ####
        NTE.append(TE)
    return NTE
    
