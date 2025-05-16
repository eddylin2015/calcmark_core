"""
中學數學題庫
"""

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
import PF602_Module 
"""
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
TE  = GetTE(Qid,St,Val)
NTE 多條題目.
NTE = []; 
NTE.append(GetTE(Qid,St,Val))
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


SecQList=  [
        "PS101.1.範例",
        "PS102.1.範例",
        "PS103.1.範例-鸡兔同笼",
        "PS614.1.範例-圓",
        "PS615.1.範例-百分數",
        "PS631.1.範例-負數",
        "PS632.1.範例-百分數(二)",
        "PS633.1.範例-生活和百分數",
        "PS634.1.範例-圓柱和圓錐",
        "PS635.1.範例-自行車里的數學",
        "PS636.1.範例-鴿巢問題",
        
        ]
        
"""
算式
"""
def Get_Expr(QIID,QAMT,Tx=-1):
    NTE=None
    if     QIID=="PS101":  NTE=Get_P301_Expr(QAMT,Tx)
    elif   QIID=="PS102":  NTE=Get_P302_Expr(QAMT,Tx)
    elif   QIID=="PS103":  NTE=Get_P303_Expr(QAMT,Tx)
    elif   QIID=="PS614":  NTE=Get_P614_Expr(QAMT,Tx)
    elif   QIID=="PS615":  NTE=Get_P615_Expr(QAMT,Tx)
    elif   QIID=="PS631":  NTE=Get_P631_Expr(QAMT,Tx)
    elif   QIID=="PS632":  NTE=Get_P632_Expr(QAMT,Tx)
    elif   QIID=="PS633":  NTE=Get_P633_Expr(QAMT,Tx)
    elif   QIID=="PS634":  NTE=Get_P634_Expr(QAMT,Tx)
    elif   QIID=="PS635":  NTE=Get_P635_Expr(QAMT,Tx)
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
        if   QIID=="PS101" : Put_Expr_V1(TE)
        elif QIID=="PS102" : Put_Expr_V1(TE)
        elif QIID=="PS103" : Put_Expr_V2(TE)
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
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案
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
    

"""P614.1.圓"""
def Get_P614_Expr(QN,Tx=-1):
    sample_list0=list(range(1,10))
    sample_list1=list(range(1,10))
    NTE=[]
    Sts=["圓周率為3.14.","圓的半徑擴大2倍,周長和面積擴大2倍.","半徑相等的兩個圓周長相等.","兩個圓的直徑相等,它們的半徑也一定相等.","用4個圓心角為90度的扇形,一定可以拼成一個圓."]
    Vals=[1,0,1,1,0]
    for Qid in range(len(Sts)):
        St=["是非題(對1,錯0)",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE


"""P615.1.百分數"""
def Get_P615_Expr(QN,Tx=-1):
    NTE=[]
    Sts=[r"2400個鸡蛋，有5\%没有孵出来，孵出小鸡有多少只？"]
    Vals=[24000*0.95]
    for Qid in range(len(Sts)):
        St=["",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE


"PS631.1.範例-負數"
def Get_P631_Expr(QN,Tx=-1):
    NTE=[]
    
    Tx=0
    sample_list1 = list(range(5, 15))
    sample_list2 = list(range(-5, -15,-1))
    for Qid in range(10):
        a=random.choice(sample_list1)
        b=random.choice(sample_list2)
        St=["一個人先向東走%d m 記作+%d m,"%(a,a),"再走%d m 是什麼意思?"%b," 問距離出發點有多遠?"      ]
        Val=abs(a+b)
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE

"PS632.1.範例-百分數(二)"
def Get_P632_Expr(QN,Tx=-1):
    NTE=[]
    Sts=[r"2400個鸡蛋，有5\%没有孵出来，孵出小鸡有多少只？"]
    Vals=[24000*0.95]
    for Qid in range(len(Sts)):
        St=["",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE

"PS633.1.範例-生活和百分數"
def Get_P633_Expr(QN,Tx=-1):
    NTE=[]
    Sts=[r"2400個鸡蛋，有5\%没有孵出来，孵出小鸡有多少只？"]
    Vals=[24000*0.95]
    for Qid in range(len(Sts)):
        St=["",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE

"PS634.1.範例-圓柱和圓錐"
def Get_P634_Expr(QN,Tx=-1):
    NTE=[]
    sample_list1 = list(range(1, 10))
    sample_list2 = list(range(-5, -15,-1))
    # a=random.choice(sample_list1)
    
    for Qid in range(10):
        if Qid % 2 == 0:
            r=random.choice(sample_list1)
            h=random.choice(sample_list1)
            St=["圓柱","半徑為%d m"%r,"高為%d m"%h,"表面積?","體積?"]
            Val=[sp.pi*r**2*2+sp.pi*2*r*h,sp.pi*r**2*h]
            TE=GetTE(Qid,St,Val,Tx)
            TE["Tip"]=["面積","體積"]
            NTE.append(TE)
            pass
        else:
            St=["圓錐","半徑為%d m"%r,"高為%d m"%h,"體積?"]
            Val=[sp.pi*r**2*h*1/3]
            TE=GetTE(Qid,St,Val,Tx)
            TE["Tip"]=["體積"]
            NTE.append(TE)
            pass
    return NTE

"PS635.1.範例-自行車里的數學"
def Get_P635_Expr(QN,Tx=-1):
    NTE=[]
    Sts=[r"2400個鸡蛋，有5\%没有孵出来，孵出小鸡有多少只？"]
    Vals=[24000*0.95]
    for Qid in range(len(Sts)):
        St=["",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE

"PS636.1.範例-鴿巢問題"
def Get_P636_Expr(QN,Tx=-1):
    NTE=[]
    Sts=[r"2400個鸡蛋，有5\%没有孵出来，孵出小鸡有多少只？"]
    Vals=[24000*0.95]
    for Qid in range(len(Sts)):
        St=["",Sts[Qid]]
        Val=Vals[Qid]
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)
    return NTE
    
