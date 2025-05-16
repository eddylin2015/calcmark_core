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
import esPriMathLib as PMath    # 自定義,數學出題庫
import esSecMathLib as SMath    # 自定義,數學出題庫
from flask import  current_app
"""
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
NTE 多條題目.
NTE=[]; NTE.append(GetTE(Qid,St,Val))
for TE in NTE:  pass
"""
def mathPicPath(PlotImg):
    #FilePath=os.getcwd()+"\\static\\"+PlotImg
    FilePath=os.path.join(current_app.config['HW_MATHPIC_FOLDER'], PlotImg)
    return FilePath
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


def GetQList():
    return  [
        "PF101.2.有理數運算",          
        "PF102.6.整數指數冪運算",
        "PF103.4.一元一次方程",
        "PF104.3.整式的加減法練習",    
        "PF105.3.二元一次方程",
        "PF106.4.一元一次不等式",
        "PF107.4.一元一次不等式組",    
        "PF108.5.整式的乘法練習",
        "PF109.3.整式的乘法公式：平方差公式",
        "PF110.4.整式的乘法公式：完全平方公式",
        "PF111.4.十進制度到度°分鐘'秒''角度轉換",
        "PF112.5.有理數的加減運算",     
        "PF201.4.根式的運算",
        "PF203.5.因式分解",
        "PF204.4.分式的乘除",
        "PF205.4.分式的加減",         
        "PF206.4.分式方程",
        "PF207.4.一次函數圖像的性質",
        "PF208.1.三角形的三邊關係：確定第三邊取值範圍",
        "PF209.1.三角形的三邊關係：構成三角形條件",
        "PF210.3.三角形內角和的計算",
        #"PF291.4.一元二次方程式十字相乘法求因式",
        "PF381.2.一元二次方程式根判斷",
        "PF392.4.一元二次方程式求解",
        #"PF293.4.整式的乘法練習",  
        #"PF301.4.一元二次方程式",
        #"PF302.4.解可化為一元二次方程的分式方程",
        #"PF303.4.解二元二次方程組",
        #"PF304.4.二次函數圖像的性質",
        "PF305.5.角度制與弧度制互換",
        "PF306.2.解直角三角形",
        "PF307.3.反比例函數：圖像與性質",
        "PF308.4.反比例函數：函數解析式",
        "PF309.1.函數圖像(一次、二次、正比例、反比例函數)",
        "PF310.6.相似三角形",
        "PF401.3.解一元二次不等式",
        #"PF402.4.等差數列之和",
        #"PF403.4.等比數列之和",
        "PF402.7.等差數列",
        "PF403.7.等比數列",
        "PF404.1.對數與指數關係",
        "PF405.5.對數的基礎運算",   
        "PF407.1.余弦定理",     
        "PF501.1.高次不等式及分式不等式",
        "PF502.3.直線的斜率",
        #"PF503.4.高二二項式定理",
        "PF504.3.多面體-正三棱柱",
        "PF505.4.多面體-直四棱柱",
        "PF506.3.多面體-正六棱柱",
        #"PF601.4.餘式定理",
        ##"PF405.1.高中一元二次方程式",
        ##"PF406.1.高中乘法公式",
        #"PF602.4.高中綫性規劃",
        "PF603.3.高中三角函數同角變換",
        "PF604.3.整式除法(長除法)",
        *PMath.PriQList,
        *SMath.SecQList
        ]
"""
算式
"""
def Get_Expr(QIID,QAMT,Tx=-1):
    NTE=None
    QPF=QIID[0:2]
    
    if   QPF=="PP":  NTE=PMath.Get_Expr(QIID,QAMT,Tx)
    elif QPF=="PS":  NTE=SMath.Get_Expr(QIID,QAMT,Tx)
    elif QIID=="PF101":  NTE=Get_PF101_Expr(QAMT,Tx)
    elif QIID=="PF102" : NTE=Get_PF102_Expr(QAMT,Tx)
    elif QIID=="PF103" : NTE=Get_PF103_Expr(QAMT,Tx)
    elif QIID=="PF104" : NTE=Get_PF104_Expr(QAMT,Tx)
    elif QIID=="PF105" : NTE=Get_PF105_Expr(QAMT,Tx)
    elif QIID=="PF106" : NTE=Get_PF106_Expr(QAMT,Tx)
    elif QIID=="PF107" : NTE=Get_PF107_Expr(QAMT,Tx)
    elif QIID=="PF108" : NTE=Get_PF108_Expr(QAMT,Tx)
    elif QIID=="PF201" : NTE=Get_PF201_Expr(QAMT,Tx)
    elif QIID=="PF109" : NTE=Get_PF109_Expr(QAMT,Tx)
    elif QIID=="PF110" : NTE=Get_PF110_Expr(QAMT,Tx)
    elif QIID=="PF111" : NTE=Get_PF111_Expr(QAMT,Tx)
    elif QIID=="PF112" : NTE=Get_PF112_Expr(QAMT,Tx)
    elif QIID=="PF203" : NTE=Get_PF203_Expr(QAMT,Tx)
    elif QIID=="PF204" : NTE=Get_PF204_Expr(QAMT,Tx)
    elif QIID=="PF205" : NTE=Get_PF205_Expr(QAMT,Tx)
    elif QIID=="PF206" : NTE=Get_PF206_Expr(QAMT,Tx)
    elif QIID=="PF207" : NTE=Get_PF207_Expr(QAMT,Tx)
    elif QIID=="PF208" : NTE=Get_PF208_Expr(QAMT,Tx)
    elif QIID=="PF209" : NTE=Get_PF209_Expr(QAMT,Tx)
    elif QIID=="PF210" : NTE=Get_PF210_Expr(QAMT,Tx)
    elif QIID=="PF381" : NTE=Get_PF381_Expr(QAMT,Tx)
    elif QIID=="PF291" : NTE=Get_PF291_Expr(QAMT,Tx)
    elif QIID=="PF392" : NTE=Get_PF392_Expr(QAMT,Tx)
    elif QIID=="PF293" : NTE=Get_PF293_Expr(QAMT,Tx)
    elif QIID=="PF301" : NTE=Get_PF301_Expr(QAMT,Tx)
    elif QIID=="PF302" : NTE=Get_PF302_Expr(QAMT,Tx)
    elif QIID=="PF303" : NTE=Get_PF303_Expr(QAMT,Tx)
    elif QIID=="PF304" : NTE=Get_PF304_Expr(QAMT,Tx)
    elif QIID=="PF305" : NTE=Get_PF305_Expr(QAMT,Tx)
    elif QIID=="PF306" : NTE=Get_PF306_Expr(QAMT,Tx)
    elif QIID=="PF307" : NTE=Get_PF307_Expr(QAMT,Tx)
    elif QIID=="PF308" : NTE=Get_PF308_Expr(QAMT,Tx)
    elif QIID=="PF309" : NTE=Get_PF309_Expr(QAMT,Tx)
    elif QIID=="PF310" : NTE=Get_PF310_Expr(QAMT,Tx)
    elif QIID=="PF401" : NTE=Get_PF401_Expr(QAMT,Tx)
    elif QIID=="PF402" : NTE=Get_PF402_Expr(QAMT,Tx)
    elif QIID=="PF403" : NTE=Get_PF403_Expr(QAMT,Tx)
    elif QIID=="PF404" : NTE=Get_PF404_Expr(QAMT,Tx)
    elif QIID=="PF405" : NTE=Get_PF405_Expr(QAMT,Tx)
    elif QIID=="PF406" : NTE=Get_PF406_Expr(QAMT,Tx)
    elif QIID=="PF407" : NTE=Get_PF407_Expr(QAMT,Tx)
    elif QIID=="PF501" : NTE=Get_PF501_Expr(QAMT,Tx)
    elif QIID=="PF502" : NTE=Get_PF502_Expr(QAMT,Tx)
    elif QIID=="PF503" : NTE=Get_PF503_Expr(QAMT,Tx)
    elif QIID=="PF504" : NTE=Get_PF504_Expr(QAMT,Tx)
    elif QIID=="PF505" : NTE=Get_PF505_Expr(QAMT,Tx)
    elif QIID=="PF506" : NTE=Get_PF506_Expr(QAMT,Tx)
    elif QIID=="PF601" : NTE=Get_PF601_Expr(QAMT,Tx)
    elif QIID=="PF602" : NTE=Get_PF602_Expr(QAMT,Tx)
    elif QIID=="PF603" : NTE=Get_PF603_Expr(QAMT,Tx)
    elif QIID=="PF604" : NTE=Get_PF604_Expr(QAMT,Tx)
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
        QPF=QIID[0:2]    
        if   QIID=="PF101" : Put_PF101_Expr(TE)
        elif QIID=="PF102" : Put_PF102_Expr(TE)
        elif QIID=="PF103" : Put_PF103_Expr(TE)
        elif QIID=="PF104" : Put_PF104_Expr(TE)
        elif QIID=="PF105" : Put_PF105_Expr(TE)
        elif QIID=="PF106" : Put_PF106_Expr(TE)
        elif QIID=="PF107" : Put_PF107_Expr(TE)
        elif QIID=="PF108" : Put_PF108_Expr(TE)
        elif QIID=="PF201" : Put_PF201_Expr(TE)
        elif QIID=="PF109" : Put_PF109_Expr(TE)
        elif QIID=="PF110" : Put_PF110_Expr(TE)
        elif QIID=="PF111" : Put_Expr_V6(TE)
        elif QIID=="PF112" : Put_PF112_Expr(TE)
        elif QIID=="PF203" : Put_PF203_Expr(TE)
        elif QIID=="PF204" : Put_PF204_Expr(TE)
        elif QIID=="PF205" : Put_PF205_Expr(TE)
        elif QIID=="PF206" : Put_PF206_Expr(TE)
        elif QIID=="PF207" : Put_PF207_Expr(TE)
        elif QIID=="PF208" : Put_Expr_InequV1(TE)
        elif QIID=="PF209" : Put_PF209_Expr(TE)
        elif QIID=="PF210" : Put_PF210_Expr(TE)
        elif QIID=="PF381" : Put_Expr_V2(TE)
        elif QIID=="PF291" : Put_PF291_Expr(TE)
        elif QIID=="PF392" : Put_PF392_Expr(TE)
        elif QIID=="PF293" : Put_PF293_Expr(TE)
        elif QIID=="PF301" : Put_PF301_Expr(TE)
        elif QIID=="PF302" : Put_PF302_Expr(TE)
        elif QIID=="PF303" : Put_PF303_Expr(TE)
        elif QIID=="PF304" : Put_PF304_Expr(TE)
        elif QIID=="PF305" : Put_PF305_Expr(TE)
        elif QIID=="PF306" : Put_Expr_V1(TE)
        elif QIID=="PF307" : Put_PF307_Expr(TE)
        elif QIID=="PF308" : Put_PF308_Expr(TE)
        elif QIID=="PF309" : Put_PF309_Expr(TE)
        elif QIID=="PF310" : Put_PF310_Expr(TE)
        elif QIID=="PF401" : Put_Expr_InequV1(TE)
        elif QIID=="PF402" : Put_PF402_Expr(TE)
        elif QIID=="PF403" : Put_PF403_Expr(TE)
        elif QIID=="PF404" : Put_PF404_Expr(TE)
        elif QIID=="PF405" : Put_PF405_Expr(TE)
        elif QIID=="PF407" : Put_PF407_Expr(TE)
        elif QIID=="PF501" : Put_Expr_InequV1(TE)
        elif QIID=="PF502" : Put_PF502_Expr(TE)
        elif QIID=="PF503" : Put_Expr_X1(TE)
        elif QIID=="PF504" : Put_PF504_Expr(TE)
        elif QIID=="PF505" : Put_PF505_Expr(TE)
        elif QIID=="PF506" : Put_PF506_Expr(TE)
        elif QIID=="PF601" : Put_Expr_X1(TE)
        elif QIID=="PF602" : Put_Expr_V6(TE)
        elif QIID=="PF603" : Put_Expr_S6(TE)
        elif QIID=="PF604" : Put_PF604_Expr(TE)  
        elif QPF=="PP" : PMath.Post_Expr_CheckAns(QIID,NTE,TEid,MxMunites)
        else:  Put_Expr_V1(TE)
        Get_Expr_CheckAnsMark(QIID,TE)

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
PF101有理數運算
"""

def Put_PF101_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Get_PF101_Expr(QN,Tx=-1):
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
PF102整數指數冪運算
"""

def Put_PF102_Expr(TE):
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "-3.1415926"
    try:
        if parse_expr(ans) == Val:
            TE["OK"] = 1
            return True
    except:
        pass
    return False


def Get_PF102_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    a,b,c,x,y,z=sp.symbols("a,b,c,x,y,z")
    NTE=[]
    St_="..."
    for Qid in range(0,QN):
        if TxFlag: Tx=int(Qid % 6)
        if Tx==1:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,2,3,4,5]))
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Mul(a1**b1 , a1**c1, evaluate=False)
            St_=str(St)
            Val=sp.simplify(St)
            St=r" {%s}^{%s} \cdot  {%s}^{%s} " % (a1,b1,a1,c1) #Latex    
        elif Tx==2:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            if op=="Div":
                St=a**b1 / a**c1
                St_=str(St)
                Val=sp.simplify(St)
                St=r" a^{%s} \div  a^{%s} " % (b1,c1) #Latex   \times
            else:
                St=sp.Mul(a**b1 , a**c1, evaluate=False)
                St_=str(St)
                Val=sp.simplify(St)
                St=r" a^{%s} \cdot  a^{%s} " % (b1,c1) #Latex 

        elif Tx==3:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Pow(sp.Mul(b1*a,evaluate=False) , c1, evaluate=False)
            St_=str(St)
            Val=sp.simplify(St)
            St=r" ({%s}*a)^{%s} " % (b1,c1) #Latex 
            #St=sp.latex(St)

        elif Tx==4:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St_=str(St1)
            Val=sp.simplify(St1)
            St=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 

        elif Tx==5:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St11=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St2=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St22=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            op=random.choice(["cdot","div"])
            if op=="div":
                St=St1 / St2
                Val=sp.simplify(St)
                #St=r" {%s} \div  {%s} " % (sp.latex(St1),sp.latex(St2)) #Latex   \times
            else:
                St=sp.Mul(St1 , St2, evaluate=False)
                Val=sp.simplify(St)
            St=r" {%s} \%s  {%s} " % (St11,op,St22) #Latex   \times
        else:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]))
            b1=random.choice([-9,-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9])
            c1=random.choice([-3,-2,-1,2,3])
            St=r" {\large (%s)}^{%s} " % (sp.latex(sp.Rational(a1,b1)),c1) #Latex 
            expr=sp.Pow(sp.Rational(a1,b1), c1 ,evaluate=False)
            Val=sp.simplify(expr) #標準答案 
        #運算方法1:
        #運算方法2:
        #Val=(a / sp.S(b))** c
        TE=GetTE_V2(Qid,St,St_,Val,Tx)
        NTE.append(TE)    
    return NTE


"""
PF103一元一次方程
"""
def Put_PF103_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"]
    if parse_expr(lib.Text2St(ans))==Val[0]:                   #比對答案:
        TE["OK"]=1
        return True
    return False

def Get_PF103_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    x=sp.symbols('x')
    NTE=[]
    St_="..."
    for Qid in range(0,QN):
        if TxFlag:Tx=int(Qid % 4)
        if Tx==1:
            # 2:  ax+b=cx+d a,b,c,d均為-99至99的整数,
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            if c==a : c=int(math.copysign(abs(c)+2,c))
                
            expre=sp.Eq( a * x + b, c * x + d,evaluate=False)
            
            St=sp.latex(expre)
            Val=sp.solve(expre)
        elif Tx==2:
            #3： m(a+bx) + n(c+dx) = p(e+fx) 所有字母均為-9至9整数
            a=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            b=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            c=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            d=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            e=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            f=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            m=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            n=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            expre=sp.Eq(m*(a+b*x)+n*(c+d*x),e+f*x,evaluate=False)
            #St1=sp.latex((m*(a+b*x)+n*(c+d*x))) 
            #St2=sp.latex((e+f*x))
            #St=r"{%s=%s}" %(St1,St2)
            St=r" %s (%s+%sx)+%s(%s+%sx)=%s+%sx "%(m,a,b,n,c,d,e,f)
            Val=sp.solve(expre)
        elif Tx==3:
            #4： (ax+b)/m + (cx+d)/n = (ex+f)/p 字母a,b,c,d,e,f均為-9至9整数;m,n,f均為1至9的整數
            a=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            b=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            c=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            d=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            e=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            f=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            m=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            n=random.choice([-6,-5,-4,-3,-2,2,3,4,5,6])
            p=math.lcm(m,n)
            expre=sp.Eq((a+b*x)/m+(c+d*x)/n,(e+f*x)/p,evaluate=False)
            St=r" \frac{%s+%sx}{%s}+\frac{%s+%sx}{%s}=\frac{%s+%sx}{%s} "%(a,b,m,c,d,n,e,f,p)
            Val=sp.solve(expre)
        else:
            a=random.choice([-6,-5,-4,-3,-2,-1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,2,3,4,5,6])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            express_str=f" {a}*x + {b} "                    # f(x)= ax + b
            QizStat=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            fx=sp.Eq( QizStat, c )                           #sympy.Eq 方程式 f(x)=c ,
            St=r" {%s}={%s} "%(sp.latex(a*x+b),c)
            Val=sp.solve(fx)                                 #sympy.solve求根,得出標準答案
        St=St.replace("+-","-")
        TE=GetTE_V2(Qid, St, St_, Val, Tx)
        NTE.append(TE)    
    return NTE


"""
PF104整式的加減法練習
"""

def Put_PF104_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415"
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
            TE["OK"] = 1
        else:  
            TE["OK"] = 0
    except:
        pass


def Get_PF104_Expr(QN,Tx=-1):
    x,y,z=sp.symbols('x,y,z')
    NTE=[]
    R_list=[]
    for i in range(0,21):
        if i!=10:
            R_list.append(-5+sp.Rational(1,2)*i)
    N_list=R_list[10:]

    for Qid in range(0,QN):
        if Tx==1:
            #( mx2+px)+(nx2+qx) = ax2 + bx  |p|,|q| < 16 整数
            #   p, q = 16以内随机±整数
            #   a=m+n,    b=p∙q 
            j=random.choice(R_list)
            k=random.choice(N_list)
            m=random.choice(R_list) #random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice(R_list) #random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            s=random.choice([2,3,4])
            t=random.choice([2,3])
            u=random.choice([1,2,3,4])
            v=random.choice([1,3,5])                 

            expr1=x**s+x**t + n
            expr2=x**u+x**v + m
            op=random.choice(["-","-","+"])
            if op=="-":
                Val=(expr1)-expr2
            else:
                Val=(expr1)+expr2
            St=r" (%s) %s (%s)"%(  sp.latex(expr1), op,  sp.latex(expr2))
            TE=GetTE(Qid,St,Val,Tx) 
        elif Tx==2:
            #( mx2+px)+(nx2+qx) = ax2 + bx  |p|,|q| < 16 整数
            #   p, q = 16以内随机±整数
            #   a=m+n,    b=p∙q 
            j=random.choice(R_list)
            k=random.choice(N_list)
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) #random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) #random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            s=random.choice([2,3,4])
            t=random.choice([2,3])
            w=random.choice([1,2,3,4])
            expr1=m*x**s+p*x**t + n
            expr2=n*x**s+q*x**w + p
            op=random.choice(["-","-","+"])
            a1=random.choice([-5,-4,-3,-2,2,3,4,5])
            a2=random.choice([-5,-4,-3,-2,2,3,4,5])
            
            if op=="-":
                Val=a1*(expr1) - a2 * expr2
                if a2 <0 :
                    op='+'
                    a2=abs(a2)
                St=r"%s (%s) %s %s (%s)"%( sp.latex(a1), sp.latex(expr1), op, sp.latex(a2), sp.latex(expr2))
            else:
                Val=a1*(expr1) + a2 * expr2
                if a2 <0 :
                    op='-'
                    a2=abs(a2)

                St=r"%s (%s) %s %s (%s)"%( sp.latex(a1), sp.latex(expr1), op, sp.latex(a2), sp.latex(expr2))
            TE=GetTE(Qid,St,Val,Tx) 
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            t=random.choice([2,3,4])

            if p+q!=0:
                b=p+q
            else:
                b=-4
            c=p*q
            

            #express_str=f"{d}*x**{t} + ({b})*x**({t}) + ({c})"      #題型 express_str ax+bx+c
            #St1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
            #Val=sp.simplify(St1)
            Val=0
            expr1=d*x**t
            expr2=b*x**t+c
            Val=expr1+expr2
            if b>=0:
                op='+'
                
            else:
                op='-'
                expr2=abs(b)*x**t+c
            
            St=r" %s %s %s"%(  sp.latex(expr1), op,  sp.latex(expr2))    
            TE=GetTE(Qid,St,Val,Tx) 

            '''
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            t=random.choice([2,3,4])
            b=p+q
            c=p*q
            express_str=f"x**{t} + ({b})*x**({t}) + ({c})"       #題型 express_str ax+bx+c
            St=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
            Val=sp.simplify(St)
            #St=sp.latex(St)
            TE=GetTE(Qid,sp.latex(St),Val,Tx)  
            '''      
        NTE.append(TE)    
    return NTE

"""
PF105二元一次方程
"""

def Put_PF105_Expr(TE):
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
        ans = {x: parse_expr(ans1), y: parse_expr(ans2)}
        if ans == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Get_PF105_Expr(QN,Tx=-1):
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    if Tx==0:
        for Qid in range(0, QN):
            #
            a = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=-k1*a+k2
            c2=k1*c+k2*d
            eq1 = sp.Eq(y,a*x+c1)
            eq2 = sp.Eq(c*x+d*y,c2)
            St = [eq1, eq2]
            #sp.latex(St)
            Val = (sp.solve(St, [x, y]))
            SSt=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(eq1),sp.latex(eq2))              
            TE = GetTE(Qid, SSt, Val, Tx)
            TE["Tip"] = "xy"
            if Val == []:
                pass
            else:
                NTE.append(TE)
            #
    elif Tx==1:
        for Qid in range(0, QN):
            #
            a = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            k1 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            k2 = random.choice([1, 2, 3, 4, 5,6,7,8,9,10])
            if k1==k2 : k2=k2+1
            c1=k1+k2
            c2=k1*c+k2*d
            eq1 = sp.Eq(x+y, c1)
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
    elif Tx==2:
        for Qid in range(0, QN):       
            #
            a = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            b = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            c = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            d = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            m = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
            n = random.choice([-10,-9,-8,-7,-6,-5, -4, -3, -2, -1, 1, 2, 3, 4, 5,6,7,8,9,10])
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

"""
PF106一元一次不等式
"""


"""
def Put_PF106_Expr_InequV1(TE):
    x = sp.symbols('x')
    Val = TE["Val"]
    Flag = False
    ans = TE["Ans"]
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
"""
def Put_PF106_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans=TE["Ans"]
    if ans.strip()=="R" and "(-oo < x) & (x < oo)" == str(Val) :
        TE["OK"]=1
        return
    ans = lib.Text2Inequ(ans)
    if ans == "":
        TE["OK"] = 0
        return
    try:
        if ans.strip() == '空集' or ans == '0'  or ans=='False' or ans=="false":
            if str(Val) == "False":
                TE["OK"] = 1        
        elif sp.solve(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF106_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   

    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
  
        if Tx==1:
            #ax+b<cx+d a,b,c,d均為-99至99的整数,
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">","<"])
            express_str=f" {a}*x + {b} {op} {c}*x+{d}"       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St1=sp.latex((a*x+b))
            St2=sp.latex((c*x+d))
            St=r"%s %s %s" %(St1,op,St2)
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)
 




        elif Tx==2:
            #m(a+bx)+n(c+dx)<p(e+fx)  所有字母均為-9至9整数            
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">","<"])
            express_str=f" {m}*({a}*x + {b})  {op} {p}*({f}*x+{e})  "   
            #express_str=f" {m}*({a}*x + {b})+{n}*({c}*x+{d}) {op} {p}*({f}*x+{e})  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St1=sp.latex((a*x+b))
            St2=sp.latex((f*x+e))
            St=r"%s(%s) %s %s(%s)" %(m,St1,op,p,St2)
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)

            #St1=sp.latex((m*(a*x+b)+n*(c*x+d)))
            #St2=sp.latex((p*(f*x+e)))
            #op=sp.latex((op))
            #St=r"{%s}{%s}{%s}" %(St1,op,St2)
            #Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
            #TE = GetTE(Qid, St, Val,Tx)
            #NTE.append(TE)

        elif Tx==3:
            #(a+bx)/m+(c+dx)/n<(e+fx)/p  所有字母均為-9至9整数
            
            p=random.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6])
            b=p+q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            k=math.lcm(m,n)
            op=random.choice([">","<"])
            express_str=f" ({a}*x+ {b})/{m} +({c}*x+{d})/{n} {op} ({f}*x+{e})/{k}  " 
            #express_str=f" ({a}*x+ {b})/{m} +({c}*x+{d})/{n} {op} ({f}*x+{e})/{p}  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            
            #St1=(a*x+b)
            #St2=(c*x+d)
            #St3=(f*x+e)
            #St4=sp.Rational(sp.latex(a*x+b), m)
            #St5=sp.Rational(sp.latex(c*x+d), n)
            #St6=sp.Rational(sp.latex(f*x+e), k)
            #St=r"%s + %s %s" %(St4,St5,op,St6)
            St=sp.latex(fx)
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)
        else:
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            op=random.choice([">=",">","<=","<"])
            St=a*x +b
            if op==">=":
                St= St >= c
            elif op==">":
                St= St > c
            elif op=="<=":
                St= St <= c
            elif op=="<":
                St= St < c
            Val=solve_univariate_inequality(St,x)      #solve_univariate_inequality 解不等式   
        
            TE = GetTE(Qid, sp.latex(St), Val,Tx)
            NTE.append(TE)
    return NTE


"""
PF107一元一次不等式組
"""
def Put_PF107_Expr(TE):
    x = sp.symbols('x')
    Val = TE["Val"]
    Flag = False
    ans = TE["Ans"]
    ans = lib.Text2Inequ(TE["Ans"])
    ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
    ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)        
    if ans == "": ans = "(-oo < x) & (x < oo)"
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
        elif ans.strip() == '空集' or ans == '0'  or ans=='False' or ans=="false":
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

def Get_PF107_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
        '''
        if Tx==1:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            
            express_str=f" {a}* x+ {b}  {op1} {c}* x+ {d} "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" {e}* x+ {f}   {op2} {g}* x+ {h} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2
        '''
        if Tx==1:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            
            express_str=f" {a}* x+ {b}  {op1} {c}* x+ {d} "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St1=sp.latex((a*x+b))
            St2=sp.latex((c*x+d))
            St_1=r"%s %s %s" %(St1,op1,St2)
            


            express_str=f" {e}* x+ {f}   {op2} {g}* x+ {h} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St3=sp.latex((e*x+f))
            St4=sp.latex((g*x+h))
            St_2=r"%s %s %s" %(St3,op2,St4)

            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(St_1,St_2)  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2

        
        elif Tx==2:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            i=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            j=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            k=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            l=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            r=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            s=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])            
            express_str=f" {m}* ({a}* x+ {b})+{n}* ({c}* x+ {d})   {op1} {p}*({f}* x+ {e}) "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" ({g}* x+ {h})/{q}+ ({i}* x+ {j})/{r}  {op2} ({k}* x+ {l})/{s} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2
            
       
        elif Tx==3:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            if m==n: n=int(math.copysign(abs(n)+5,m))
            if m>n:
                temp=n
                n=m
                m=temp
            expr1=R"\frac{%s x + (%s)}{%s}"%(sp.latex(a),sp.latex(b),sp.latex(c))
            
            if op1==">":
                express_str=f"{n} > {expr1}  > {m} "                    # f(x)= ax + b
                fx1=parse_expr(f"{n} > ({a}* x+ {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x+ {b})/{c} > {m}" , evaluate=False) #字串解釋為可運算式子 expression 
            else:
                express_str=f"{m} < {expr1}  < {n} "                    # f(x)= ax + b
                fx1=parse_expr(f"{m} < ({a}* x + {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x + {b})/{c} < {n}" , evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=express_str
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2            
        else:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            fx1= x > p if op1==">" else x < p
            fx2=  x > q if op2==">" else x < q
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
        TE = GetTE(Qid, St, Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF108整式的乘法練習
"""


def Put_PF108_Expr(TE):
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    ans = lib.Text2StV1(ans,["x","y","z","m","n"])
    try:
        if parse_expr(ans).subs({x: 7,y:7}) == Val.subs({x: 7,y:7}):  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF108_Expr(QN,Tx=-1):
    NTE = []

    for Qid in range(0, QN):
        x,y,z,m,n=sp.symbols('x y z m n')
        
        a=random.choice([2,3,4,5,6,7,8,9])
        b=random.choice([-5,-4,-3,-2,-1,2,3,4,5])
        c=random.choice([2,3,4,5,6,7,8,9])
        d=random.choice([2,3,4])
        e=random.choice([-1,1])
        f=random.choice([-1,1])
        letter=random.choice([m,n])
        base=random.choice([x,y,z])
        fac1=sp.Rational(a,b)
        if Tx==0:
            #print("""同底數冪相乘""")
            ji=a*letter+d
            St=e*base**a*base**d*(f)*base**ji
            '''   
            St_latex=r" {%s} x^{%s}  x^{%s} ({%s}) x^{%s} " %(e,a,d,f,sp.latex(ji))
            if f==1:
                St_latex=r" {%s} x^{%s}  x^{%s}  x^{%s} " %(e,a,d,sp.latex(ji))
            '''
            St_latex=r" %s %s (%s)" %(sp.latex(e*base**a),sp.latex(base**d),sp.latex(f*base**ji))
            if f==1:
                St_latex=r" %s %s %s" %(sp.latex(e*base**a),sp.latex(base**d),sp.latex(base**ji))
            #display(Latex(st_st))
            #val=sp.simplify(st)
            #display(val)
            Val = sp.simplify(St)
            TE = GetTE(Qid, St_latex, Val, Tx)
            NTE.append(TE)

        elif Tx==1:            
            #print("""冪的乘方""")
            ji=a*x+d
            St=(fac1*x**a*y**c)**d
            St_latex=r" (%s)^{%s} " %(sp.latex(fac1*x**a*y**c),d)
            #display(Latex(st_st))
            #val=sp.simplify(st)
            #display(val)
            Val = sp.simplify(St)
            TE = GetTE(Qid, St_latex, Val, Tx)
            NTE.append(TE)

        elif Tx==2:            
            #print("""單項式乘以單項式""")
            b=random.choice([-4,-3,-2,-1,2,3,4])
            d=random.choice([1,2,3])
            e=random.choice([2,3,4])
            f=random.choice([-1,1])
            g=random.choice([-1,1])
            m=random.choice([2,3,4,5,6])
            n=random.choice([2,3,4,5,6])
            fac1=sp.Rational(a,b)
            fac2=sp.Rational(b,a)*d
            St=(fac1*x**m*y**n)**d*(fac2*x**d*y**e)
            if d==1:
                St_latex=r" (%s)(%s) " %(sp.latex(fac1*x**m*y**n),sp.latex(fac2*x**d*y**e))
            else:
                St_latex=r" (%s)^{%s} (%s) " %(sp.latex(fac1*x**m*y**n),d,sp.latex(fac2*x**d*y**e))
            #display(Latex(st_st))
            #val=sp.simplify(st)
            #display(val)
            Val = sp.simplify(St)
            TE = GetTE(Qid, St_latex, Val, Tx)
            NTE.append(TE)

        elif Tx==3:            
            #print("""單項式與多項式的乘法""")
            c=random.choice([2,3,4,5,6,7,8,9])
            g=random.choice([2,3,4,5,6,7,8,9])
            i=random.choice([2,3,4,5,6,7,8,9])
            d=random.choice([2,3,4])
            e=random.choice([-1,1])
            f=random.choice([-1,1])
            h=random.choice([2,3,4,5,6,7,8,9])
            fac1=sp.Rational(a,b)*d
            fac2=sp.Rational(a,b)*a
            fac3=sp.Rational(b,a)
            ji=a*x+d
            St=(fac1*x**a*y**c+fac2*x**g*y**i)*fac3*x**d*y**h
            if fac2>=0:
                St_latex=r"({%s}x^{%s}  y^{%s} + {%s} x^{%s} y^{%s})({%s} x^{%s}  y^{%s})" %(sp.latex(fac1),a,c,sp.latex(fac2),g,i,sp.latex(fac3),d,h)
            else:
                St_latex=r"({%s}x^{%s}  y^{%s} {%s} x^{%s} y^{%s})({%s} x^{%s}  y^{%s})" %(sp.latex(fac1),a,c,sp.latex(fac2),g,i,sp.latex(fac3),d,h)
            #display(Latex(st_st))
            Val=sp.expand(St)
            #Val = sp.simplify(St)
            TE = GetTE(Qid, St_latex, Val, Tx)
            NTE.append(TE)

        elif Tx==4:            
            #print("""多項式的乘法""")
            m=random.choice([-9,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9])
            n=random.choice([-9,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9])
            c=random.choice([2,3,4,5,6,7,8,9,])
            g=random.choice([2,3,4,5,6,7,8,9])
            i=random.choice([2,3,4,5,6,7,8,9])
            d=random.choice([1,2,3])
            k=random.choice([1,2,3])
            e=random.choice([-1,1])
            f=random.choice([-1,1])
            h=random.choice([2,3,4,5,6,7,8,9])
            fac1=sp.Rational(a,b)*d
            fac2=sp.Rational(a,b)*a
            fac3=sp.Rational(b,a)
            ji=a*x+d
            St=(b*x**d+m*y**k)*(n*x**d+a*y**k)
            St1=sp.latex(b*x**d)
            St2=sp.latex(m*y**k)
            St3=sp.latex(n*x**d+a*y**k)
            if m>=0:
                op='+'
                St_latex=r"(%s %s%s)(%s)" %(St1,op,St2,St3)
            else:
                St_latex=r"(%s %s)(%s)" %(St1,St2,St3)


            #display(Latex(st_st))
            Val=sp.expand(St)
            #Val = sp.simplify(St)
            TE = GetTE(Qid, St_latex, Val, Tx)
            NTE.append(TE)
    return NTE


"""
PF201根式的運算
"""


def Put_PF201_Expr(TE):
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

def Get_PF201_Expr(QN,Tx=-1):
    NTE=[]
    for Qid in range(0,QN):
        if Tx==0:  #題型一
            c=random.choice([2,3,6])
            if c==2:
                a=random.choice(range(2,10))
            elif c==3:
                a=random.choice(range(2,6))
            elif c==6:
                a=random.choice(range(2,4))
            b=random.choice(range(2,10))
            st1=b*sp.sqrt(c**a)
            St=st1
            Stt=r" %s\sqrt{%s} "%(b,c**a)
            Val=sp.simplify(St)
            TE = GetTE(Qid, Stt, Val, Tx)
            NTE.append(TE)
        if Tx==1: #分母有理化二
            e=random.choice([2,3,6])
            if e==2:
                a=random.choice(range(2,10))
            elif e==3:
                a=random.choice(range(2,6))
            elif e==6:
                a=random.choice(range(2,4))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            f=e**a
            St=r"\frac{%s}{%s \sqrt{%s}}"%(b,c,f)
            Val=b/(c*sp.sqrt(f))            
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        elif Tx==2: #分母有理化三
            e=random.choice([2,3,6])
            if e==2:
                a=random.choice(range(2,8))
            elif e==3:
                a=random.choice(range(2,6))
            elif e==6:
                a=random.choice(range(2,4))
            f=e**a
            b=random.choice(range(2,5))
            c=random.choice(range(2,5))
            St=r"\frac{%s}{%s + \sqrt{%s}}"%(b,c,f)
            Val=b/( sp.sqrt(f)+c)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        elif Tx==3:  #題型四
            Tid=random.choice(range(0,3))
            a=random.choice([2,4,8,12,16,18,20,24,28,32,36,3,9,27,48,75,108,147])
            b,c,d=np.random.choice([2,4,8,12,16,18,20,24,28,32,36,3,9,27,48,75,108,147],3)
            st1=sp.sqrt(a)
            st2=sp.sqrt(b)
            st3=sp.sqrt(c)
            if Tid==0:
                St=st1+st2-st3
                Stt=r" \sqrt{%s} + \sqrt{%s} - \sqrt{%s} "%(a,b,c)
            elif Tid==1:
                St=(st1+st2)*(st1-st2)
                Stt=r" (\sqrt{%s} +\sqrt{%s})(\sqrt{%s}-\sqrt{%s}) "%(a,b,a,b)
            elif Tid==2:
                St=(st1+st2)**2
                Stt=r" (\sqrt{%s} + \sqrt{%s})^2 "%(a,b)        
            Val=sp.simplify(St)
            TE = GetTE(Qid, Stt, Val, Tx)
            NTE.append(TE)

    return NTE

"""
PF109整式的乘法公式平方差
"""


def Put_PF109_Expr(TE):
    x,y,z=sp.symbols('x y z')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2StV1(ans)
    if ans.strip()=="":ans="3.1415"
    try:
        if parse_expr(ans).subs({x:71,y:71,z:71})==Val.subs({x:71,y:71,z:71}):  #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF109_Expr(QN,Tx=-1):
    x,y,z=sp.symbols("x y z")
    sample_list0= list(range(-39,29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1= list(range(-19,19))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            a = random.choice(sample_list1)
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10])
            letter=random.choice([x,y,z])
            St=(p*letter +a) * (p*letter - a)
            #express_str=f"({p}*x +({a})) * ({p}*x - ({a}))  "  #題型 express_str ax+bx+c
            #St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
            Val = sp.expand(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)

        elif Tx==1:
            a =random.choice(sample_list1) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10])
            q=random.choice([sp.Rational(1,2),sp.Rational(2,3),sp.Rational(3,4),2,3,4])
            letter=random.choice([x,y,z])
            St=(p*letter**q +a) * (p*letter**q - a)    #題型 express_str ax+bx+c
            Val=sp.expand(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
        elif Tx==2:            
            a =random.choice(sample_list1) 
            p=random.choice([1,2,3,4,5])
            q=random.choice([sp.Rational(1,2),sp.Rational(2,3),2,3,4])
            St=(p*x**q * y**p + z**p ) * (p * x**q * y**p - z**p)  
            Val=sp.expand(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
        else:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
            St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
            Val = sp.expand(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
    return NTE

def Put_PF110_Expr(TE):
    x,y,z=sp.symbols('x y z')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2StV1(ans)
    if ans.strip()=="":ans="3.1415"
    try:
        if parse_expr(ans).subs({x:71,y:71,z:71})==Val.subs({x:71,y:71,z:71}):  #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

"整式的乘法完全平方公式"
def Get_PF110_Expr(QN,Tx=-1):
    x,y,z=sp.symbols("x y z")
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            p,q=np.random.choice(range(-16,16),2)
            p=p if p!=0 else 1;q=q if q!=0 else 1
            Tidx=Qid % 3
            if Tidx==0:
                express_str=f"(x+({q})) ** 2" 
                St=parse_expr(express_str, evaluate=False) 
                Stt=sp.latex(St)
            elif Tidx==1:
                Stt=f"({p}+y)^2"
                St=(p+y)**2
            elif Tidx==2:
                Stt=f"({p}-y)^2"
                St=(p-y)**2
            Val=sp.expand(St)
            TE=GetTE(Qid,Stt,Val,Tx)        
            NTE.append(TE)    
        elif Tx==1:
            p,q=np.random.choice(range(-16,16),2)
            p=p if p!=0 else 1;q=q if q!=0 else 1
            Tidx=Qid % 3
            if Tidx==0:
                #express_str=f"({p}*x+({q})) ** 2" 
                #St=parse_expr(express_str, evaluate=False) 
                St=( p * x + q) **2
            elif Tidx==1:
                St=(p+q*y)**2
            elif Tidx==2:
                St=(p*x+q*y)**2
                
            Stt=sp.latex(St)
            Val=sp.expand(St)
            TE=GetTE(Qid,Stt,Val,Tx)           
            NTE.append(TE)    
        elif Tx==2:
            p,q=np.random.choice(range(-16,16),2)
            #r=random.choice(["(1/3)","(2/3)","(1/4)",2,3,4,5])
            #s=random.choice(["(1/3)","(2/3)","(1/4)",2,3,4,5])
            r=random.choice([sp.S(1)/3,sp.S(2)/3,sp.S(1)/4,2,3,4,5])
            s=random.choice([sp.S(1)/3,sp.S(2)/3,sp.S(1)/4,2,3,4,5])
            p=p if p!=0 else 1;q=q if q!=0 else 1
            Tidx=Qid % 2
            
            if Tidx==0:
                expr1=p*x**s
                expr2=r*y**r
                #express_str=f"({p}*x**{s}+ ({r})*y**{r}) ** 2" 
                #St=parse_expr(express_str, evaluate=False) 
                St=(expr1+expr2)**2
                Stt=sp.latex(St)
            elif Tidx==1:
                expr1=p* x**r
                expr2=r* y**r
                #express_str=f"({p}*x**{r} - ({r})*y**{r}) ** 2" 
                #St=parse_expr(express_str, evaluate=False) 
                St=(expr1-expr2)**2
                Stt=sp.latex(St)            
            Val=sp.expand(St)
            TE=GetTE(Qid,Stt,Val,Tx)         
            NTE.append(TE)    
        elif Tx==3:
            p,q=np.random.choice(range(-5,5),2)
            r=random.choice(["(1/3)","(2/3)","(1/4)",2,3,4,5])
            s=random.choice(["(1/3)","(2/3)","(1/4)",2,3,4,5])
            p=p if p!=0 else 1;q=q if q!=0 else 1
            p=p*sp.Rational(1,2)
            q=q*sp.Rational(1,2)
            exp1=p*x+q
            exp2=p*x-q
            exp3=(p*x)**2 - q**2
            St=exp1 * exp2 * exp3
            #express_str=f"(({p}*x)**2-({q})**2) *({p}*x**{q} +({q})) * ({p}*x**{q} - ({q}))" 
            #St=parse_expr(express_str, evaluate=False) 
            Stt=sp.latex(St)            
            Val=sp.expand(St)
            TE=GetTE(Qid,Stt,Val,Tx)          
            NTE.append(TE)                


    return NTE


"""
度分秒進制轉換
"""
def Get_PF111_Expr(QN,Tx=-1):
    NTE = []
    for Qid in range(0, QN):
        a,b,c=np.random.choice(range(0,10),3)
        d=a*100+b*10+c
        d=d/100
        b=b*6
        c=c*36
        while c>=60:
          c=c-60
          b=b+1
        if Tx==0:
            Stt=f"{a}°{b}'{c}''"
            Val=d
            TE=GetTE(Qid,Stt,Val,Tx)    
            TE["Tip"] = ["十進制度°"]
            pass
        elif Tx==1:
            Stt=f"{d}。"
            Val=[a,b,c]
            TE=GetTE(Qid,Stt,Val,Tx)    
            TE["Tip"] = ["度°","分'","秒\""]
            pass
        elif Tx==2:
            b1,c1,b2,c2=np.random.choice(range(0,60),4)
            a1,a2=np.random.choice(range(0,180),2)
            a3=a1+a2
            b3=b1+b2
            c3=c1+c2
            while c3>=60:
                c3=c3-60
                b3=b3+1
            while b3>=60:
                b3=b3-60
                a3=a3+1
            Stt=f"{a1}°{b1}'{c1}''+{a2}°{b2}'{c2}''"
            Val=[a3,b3,c3]
            TE=GetTE(Qid,Stt,Val,Tx)    
            TE["Tip"] = ["度°","分'","秒\""]

        elif Tx==3:
            b1,c1,=np.random.choice(range(0,60),2)
            a1=np.random.choice(range(0,180))
            d=np.random.choice(range(0,10))
            a3=a1*d
            b3=b1*d
            c3=c1*d
            while c3>=60:
                c3=c3-60
                b3=b3+1
            while b3>=60:
                b3=b3-60
                a3=a3+1
            
            Stt=f"{a1}°{b1}'{c1}''×{d}"
            Val=[a3,b3,c3]
            TE=GetTE(Qid,Stt,Val,Tx)    
            TE["Tip"] = ["度°","分'","秒\""]


            
        NTE.append(TE)
    return NTE    


"""
PF112有理數四則運算
"""

def Put_PF112_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF112_Expr(QN,Tx=-1):
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(range(1,20))
            b=random.choice(range(1,20))
            c=random.choice(range(1,20))
            d=random.choice(range(1,20))
            e=random.choice(range(1,20))
            f=random.choice(range(1,20))
            g=0
            if a>b: m=sp.Rational(b,a)
            else: m=sp.Rational(a,b)
            if c>d: n=sp.Rational(d,c)
            else: n=sp.Rational(c,d)
            if g==0:
                St=r"%s+%s(答案以假分數作答)"  %(sp.latex(m),sp.latex(n))
                Val=m+n
            else:
                if m>n:
                    St=r"%s-%s" %(sp.latex(m),sp.latex(n))
                    Val=m-n
                else:
                    St=r"%s-%s" %(sp.latex(n),sp.latex(m))
                    Val=n-m
        elif Tx==1:
            a=random.choice(range(1,20))
            b=random.choice(range(1,20))
            c=random.choice(range(1,20))
            d=random.choice(range(1,20))
            e=random.choice(range(1,20))
            f=random.choice(range(1,20))
            g=1
            if a>b: m=sp.Rational(b,a)
            else: m=sp.Rational(a,b)
            if c>d: n=sp.Rational(d,c)
            else: n=sp.Rational(c,d)
            if g==0:
                St=r"%s+%s(答案以假分數作答)"  %(sp.latex(m),sp.latex(n))
                Val=m+n
            else:
                if m>n:
                    St=r"%s-%s(答案以假分數作答)" %(sp.latex(m),sp.latex(n))
                    Val=m-n
                else:
                    St=r"%s-%s(答案以假分數作答)" %(sp.latex(n),sp.latex(m))
                    Val=n-m       
        elif Tx==2:
            a=random.choice(range(1,10))
            b=random.choice(range(1,10))
            c=random.choice(range(1,10))
            d=random.choice(range(1,10))
            e=random.choice(range(1,9))
            f=random.choice(range(1,9))
            g=random.choice([0,1])
            if e<f:
                h=e
                e=f
                f=h
            while a==b:
                a=random.choice(range(1,10))
                b=random.choice(range(1,10))
            while c==d:
                c=random.choice(range(1,10))
                d=random.choice(range(1,10))
            if a>b: m=sp.Rational(b,a)
            else: m=sp.Rational(a,b)
            if c>d: n=sp.Rational(d,c)
            else: n=sp.Rational(c,d)
            if g==0:
                St=r"%s%s+%s%s(答案以假分數作答)"  %(e,sp.latex(m),f,sp.latex(n))
                Val=m+n+e+f
            else:
                if m>n:
                    St=r"%s%s-%s%s(答案以假分數作答)" %(e,sp.latex(m),f,sp.latex(n))
                    Val=m-n+e-f
                else:
                    St=r"%s%s-%s%s(答案以假分數作答)" %(e,sp.latex(n),f,sp.latex(m))
                    Val=n-m+e-f  
        elif Tx==3:
            a=random.choice(range(1,10))
            b=random.choice(range(1,10))
            c=random.choice(range(1,10))
            d=random.choice(range(1,10))
            e=random.choice(range(1,9))
            f=random.choice(range(1,9))
            g=1
            while e==f:
                e=random.choice(range(1,9))
                f=random.choice(range(1,9))
            if e<f:
                h=e
                e=f
                f=h
            while a==b:
                a=random.choice(range(1,10))
                b=random.choice(range(1,10))
            while c==d:
                c=random.choice(range(1,10))
                d=random.choice(range(1,10))
            if a>b: m=sp.Rational(b,a)
            else: m=sp.Rational(a,b)
            if c>d: n=sp.Rational(d,c)
            else: n=sp.Rational(c,d)
            if g==0:
                St=r"%s%s+%s%s(答案以假分數作答)"  %(e,sp.latex(m),f,sp.latex(n))
                Val=m+n+e+f
            else:
                
                St=r"%s%s-%s%s(答案以假分數作答)" %(e,sp.latex(m),f,sp.latex(n))
                Val=m-n+e-f
        elif Tx==9:
            a=random.choice(range(1,20))
            b=random.choice(range(1,20))
            c=random.choice(range(2,9))
            d=random.choice([1,2,3,4,5,6,7,8,9,10])
            e=random.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1])
            f=random.choice(range(1,20))
            #St1=sp.Mul(sp.Rational(a,b),c,evaluate=False)
            St=r"%s×%s+%s%s" %(sp.latex(sp.Rational(a,b)),sp.latex(b*c),sp.latex(d),sp.latex(e))
            Val=sp.Rational(a,b)*b*c+d+e

            while  sp.Rational(a,b)*c+d+e <0:
                
                while sp.Rational(a,b)*c+d <0:
                    a=random.choice(range(1,20))
                    b=random.choice(range(1,20))
                    c=random.choice(range(2,9))
                    d=random.choice([1,2,3,4,5,6,7,8,9,10])
                    e=random.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1])
                    f=random.choice(range(1,20))
                    #St1=sp.Mul(sp.Rational(a,b),c,evaluate=False)
                    St=r"%s×%s+%s%s" %(sp.latex(sp.Rational(a,b)),sp.latex(b*c),sp.latex(d),sp.latex(e))
                    Val=sp.Rational(a,b)*b*c+d+e
        elif Tx==4:
            a=random.choice(range(1,10))
            b=random.choice(range(1,10))
            c=random.choice(range(1,10))
            d=random.choice(range(1,10))
            e=random.choice(range(1,9))
            f=random.choice(range(1,9))
            aa=random.choice(range(1,10))
            bb=random.choice(range(1,10))
            ff=random.choice(range(1,9))
            g=random.choice([0,1])
            m=sp.Rational(a,b)
            n=sp.Rational(c,d)
            o=sp.Rational(aa,bb)
            while e==f:
                e=random.choice(range(1,9))
                f=random.choice(range(1,9))
            if e<f:
                h=e
                e=f
                f=h
            while a==b:
                a=random.choice(range(1,10))
                b=random.choice(range(1,10))
            while c==d:
                c=random.choice(range(1,10))
                d=random.choice(range(1,10))
            while aa==bb:
                aa=random.choice(range(1,10))
                bb=random.choice(range(1,10))
            if a>b: m=sp.Rational(b,a)
            else: m=sp.Rational(a,b)
            if c>d: n=sp.Rational(d,c)
            else: n=sp.Rational(c,d)
            if aa>bb: o=sp.Rational(bb,aa)
            else: o=sp.Rational(aa,bb)
            if g==0:
                St=r"%s%s+%s%s+%s%s(答案以假分數作答)" %(e,sp.latex(m),f,sp.latex(n),ff,sp.latex(o))
                Val=m+n+o+e+f+ff
            elif g==1:
                if m>n:
                    St=r"%s%s-%s%s+%s%s(答案以假分數作答)" %(e,sp.latex(m),f,sp.latex(n),ff,sp.latex(o))
                    Val=m-n+o+e-f+ff
                else:
                    St=r"%s%s-%s%s+%s%s(答案以假分數作答)" %(e,sp.latex(n),f,sp.latex(m),ff,sp.latex(o))
                    Val=n-m+o+e-f+ff
                  
        TE=GetTE(i,St,Val,Tx)        
        NTE.append(TE)    
    return NTE






"""
PF203因式分解提公因式
"""


def Put_PF203_Expr(TE):
    x,y,z,m,n=sp.symbols('x y z m n',real=True)
    Val = TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2StV1(ans)
    if ans.strip()=="": ans="3.1415"
    subsV={x:7,y:11,z:17,m:23,n:29}
    try:
        if parse_expr(ans).subs(subsV)==Val.subs(subsV):                   #比對答案:
            TE["OK"]=1
    except:
        pass
    #TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF203_Expr(QN,Tx=-1):
    x,y,z,m,n=sp.symbols('x y z m n',real=True)
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            #x,y,z,m,n=sp.symbols('x y z m n')
            letter=random.choice([x,y,z,m,n])
            a,b,c,d =  np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],4)
            ab=a*b;ac=a*c; ad=a*d
            p=random.choice([2,3,4,5])
            q=random.choice([1,2,3])
            u=random.choice([1,2,3,4,5])
            v=random.choice([1,2])
            expr1=a*b*letter**p
            expr2=b*c*letter**q
            expr3=a*b*c*d*letter**v
            St=expr1+expr2+expr3
            Val=sp.factor(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
        
        
        elif Tx==1:
            
            a,b,c,d = np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],4)
            ab=a*b; ac=a*c; ad=a*d
            p=1;u=1;q=2;v=2
            while p==u and q==v:
                p,q,u,v = np.random.choice([1,2,3,4],4)
            express_str=f"{ab} * x**{p} * y**{q}  + {ac} * x**{u}*y**{v}  "  #題型 express_str ax+bx+c
            St=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
            Val=sp.factor(St)
            
            st01=ab*(x**p)*(y**q)
            st02=ac*(x**u)*(y**v)
            if ac>=0:
                op='+'
            else:
                op='-'
                st02=abs(ac)*(x**u)*(y**v) 

            St=r"%s  %s %s "%( sp.latex(st01), op, sp.latex(st02)) 

            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        
        elif Tx==2:
            #x,y,z,m,n=sp.symbols('x y z m n')
            letter=random.choice([x,y,z,m,n])
            p,q=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],2)
            b=p+q; c=p*q
            St=letter**2+b*letter+c
            #express_str=f"x**2 + {b}*x +  {c} "  
            #St=parse_expr(express_str, evaluate=False)     #字串解釋為可運算式子 expression
            Val=sp.factor(St)                              #因式分解,得出標準答案
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
        elif Tx==3:
            #x,y,z,m,n=sp.symbols('x y z m n')
            letter=random.choice([x,y,z,m,n])
            a,b,c,d=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],4)
            expr1=a*c*letter**2
            expr2=(a*d+b*c)*letter
            expr3=b*d
            St=expr1+expr2+expr3
            Val=sp.factor(St)                              #因式分解,得出標準答案
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
        
        elif Tx==4:
            math.gcd(4,5)
            a=2;b=4;c=2;d=4

            #x,y,z,m,n=sp.symbols('x y z m n')

            while math.gcd(a,b)!=1:
                a,b=np.random.choice([1,2,3,4,5,6,7,8,9],2)

            while math.gcd(c,d)!=1:
                c,d=np.random.choice([1,2,3,4,5,6,7,8,9],2)
            op=random.choice([1,-1])

            letter=random.sample([x,y,z,m,n],4)
            st1=c*letter[0]+d*letter[1]
            if op==1:
                express_str=f"{a*letter[2]} *({c*letter[0]}+{d*letter[1]})+{b*letter[3]}*({c*letter[0]}+{d*letter[1]}) "
                St=r"%s(%s)%s%s(%s)"%(sp.latex(a*letter[2]),sp.latex(st1),'+', sp.latex(b*letter[3]),sp.latex(st1))
            else :
                express_str=f"{a*letter[2]} *({c*letter[0]}+{d*letter[1]})-{b*letter[3]}*({c*letter[0]}+{d*letter[1]}) "
                St=r"%s(%s)%s%s(%s)"%(sp.latex(a*letter[2]),sp.latex(st1),'-', sp.latex(b*letter[3]),sp.latex(st1))
            St_ans=parse_expr(express_str, evaluate=False)
            Val=sp.factor(St_ans)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
    return NTE


"""
PF204分式的乘除
"""


def Put_PF204_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    #TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF204_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x, y, z, m, n = sp.symbols('x,y,z,m,n')
    op_list = ["*", "/"]
    sample_list0 = list(range(1, 17))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    if Tx==0:
        for Qid in range(0, QN):
            op=  random.choice(op_list) 
            a = random.choice(sample_list0) 
            b = random.choice(sample_list0) 
            c = random.choice(sample_list0) 
            d = random.choice(sample_list0) 
            p = random.choice(sample_list0) 
            q = random.choice(sample_list0) 
            r = random.choice(sample_list0) 
            u = random.choice(sample_list0) 
            v = random.choice(sample_list0) 
            p1 = random.choice(sample_list0) 
            q1 = random.choice(sample_list0) 
            r1 = random.choice(sample_list0) 
            u1 = random.choice(sample_list0)
            v1 = random.choice(sample_list0)
            k1 = random.choice([1, 2, 3, 4, 5])
            k2 = random.choice([1, 2, 3, 4, 5])
            fx1=a*x**p*y**q*z**r
            fx2=k1*a*x**p1*y**q1*z**r1
            St=fx1/fx2
            #St=sp.Mul(fx1,fx2,evaluate=False)
            fx1latex=sp.latex(fx1)
            fx2latex=sp.latex(fx2)        
            StLatex= r"\frac {%s}{%s}"% (fx1latex,fx2latex)
            Val=sp.simplify(St)
            TE=GetTE(len(NTE),StLatex,Val)        
            TE["ValLatex"]=sp.latex(Val)
            NTE.append(TE)    
            
            pass
    elif Tx==1:
        for Qid in range(0, QN):
            op=  random.choice(op_list) 
            a = random.choice(sample_list0) 
            b = random.choice(sample_list0) 
            c = random.choice(sample_list0) 
            d = random.choice(sample_list0) 
            p = random.choice(sample_list0) 
            q = random.choice(sample_list0) 
            r = random.choice(sample_list0) 
            u = random.choice(sample_list0) 
            v = random.choice(sample_list0) 
            p1 = random.choice(sample_list0) 
            q1 = random.choice(sample_list0) 
            r1 = random.choice(sample_list0) 
            u1 = random.choice(sample_list0)
            v1 = random.choice(sample_list0)
            ffx=x+a
            fx1=(x+b)*ffx
            fx2=(x+c)*ffx
            St=fx1/fx2
            #St=sp.Mul(fx1,fx2,evaluate=False)
            fx1latex=sp.latex(fx1.expand())
            fx2latex=sp.latex(fx2.expand())        
            StLatex= r"\frac {%s}{%s}"% (fx1latex,fx2latex)
            Val=sp.simplify(St)
            TE=GetTE(len(NTE),StLatex,Val)        
            TE["ValLatex"]=sp.latex(Val)
            NTE.append(TE)    
            pass
    elif Tx==2:
        for Qid in range(0, QN):
            op=  random.choice(op_list) 
            a = random.choice(sample_list0) 
            b = random.choice(sample_list0) 
            c = random.choice(sample_list0) 
            d = random.choice(sample_list0) 
            p = random.choice(sample_list0) 
            q = random.choice(sample_list0) 
            r = random.choice(sample_list0) 
            u = random.choice(sample_list0) 
            v = random.choice(sample_list0) 
            p1 = random.choice(sample_list0) 
            q1 = random.choice(sample_list0) 
            r1 = random.choice(sample_list0) 
            u1 = random.choice(sample_list0)
            v1 = random.choice(sample_list0)
            fx1=(a*x**p*y**q*z**r)/(b*m**u*n**v)
            fx2=(d*m**u1*n**v1)/(c*x**p1*y**q1*z**r1)
            fx1latex=sp.latex(fx1)
            fx2latex=sp.latex(fx2)
            StLatex=""
            if op=="*":
                St=sp.Mul(fx1,fx2,evaluate=False)
                Val=sp.simplify(St)
                StLatex=f" {fx1latex} \cdot {fx2latex}"
            elif op=="/":
                St=fx1/fx2
                StLatex= f" {fx1latex} \div {fx2latex}"
                Val=sp.simplify(St)
            TE=GetTE(len(NTE),StLatex,Val)        
            TE["ValLatex"]=sp.latex(Val)
            NTE.append(TE)                
            pass
    elif Tx==3:
        for Qid in range(0, QN):
            op=  random.choice(op_list) 
            a = random.choice(sample_list0) 
            b = random.choice(sample_list0) 
            c = random.choice(sample_list0) 
            d = random.choice(sample_list0) 
            e = random.choice(sample_list0) 
            p = random.choice(sample_list0) 
            q = random.choice(sample_list0) 
            r = random.choice(sample_list0) 
            u = random.choice(sample_list0) 
            v = random.choice(sample_list0) 
            p1 = random.choice(sample_list0) 
            q1 = random.choice(sample_list0) 
            r1 = random.choice(sample_list0) 
            u1 = random.choice(sample_list0)
            v1 = random.choice(sample_list0)
            ffx=x+a
            fx1=(x+b)*ffx
            fx2=(x+c)*ffx
            fx3=(x-a)*ffx
            fx4=(x-b)*ffx
            fx1latex=sp.latex(fx1.expand())
            fx2latex=sp.latex(fx2.expand())        
            fx3latex=sp.latex(fx3.expand())        
            fx4latex=sp.latex(fx4.expand())        
            if op=="*":
                St=fx1/fx2 *( fx3/fx4)
                StLatex= r"\frac {%s}{%s} \cdot  \frac {%s}{%s}"% (fx1latex,fx2latex,fx3latex,fx4latex)
            elif op=="/":
                St=fx1/fx2 /(fx3/fx4)
                #St=sp.Mul(fx1,fx2,evaluate=False)
                StLatex= r"\frac {%s}{%s} \div  \frac {%s}{%s}"% (fx1latex,fx2latex,fx3latex,fx4latex)
            Val=sp.simplify(St)
            TE=GetTE(len(NTE),StLatex,Val)        
            TE["ValLatex"]=sp.latex(Val)
            NTE.append(TE)    
    return NTE


"""
PF205分式的加減
"""


def Put_PF205_Expr(TE):
    x, y, z = sp.symbols('x,y,z')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    #TE["Val"] = r"\(%s\)" % sp.latex(Val)


def Get_PF205_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    op_list = ["+", "-"]
    sample_list0 = list(range(1, 16))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 11))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag : Tx= 0
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        h = random.choice(sample_list1)
        k = random.choice(sample_list1)
        h1 = random.choice(sample_list1)
        k1 = random.choice(sample_list1)
        e = lib.lcm(a, b)
        f = lib.lcm(a, b) // a
        g = lib.lcm(a, b) // b
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        if p+q==0: q=int(math.copysign((abs(q)+2),q))
        b = p+q
        c = p*q
        fx1 = c / (a*x**h*y**k)
        fx2 = d / (b*x**h1*y**k1)
        St = sp.S(0)
        if op == "+":
            St = sp.Add(fx1, fx2)
        if op == "-":
            St = fx1-fx2
        Val = sp.simplify(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF206分式方程
"""


def Put_PF206_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans=lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val[0].subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF206_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x = sp.Symbol('x')
    sample_list0 = list(range(1, 8))     # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 10))
    sample_list2 = list(range(-10, 10))  # sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list0)
        a1 = random.choice(sample_list0)
        c = random.choice(sample_list1)
        c1 = random.choice(sample_list1)
        ac1 = a*c1
        a1c = a1*c
        aclcm = lib.lcm(ac1, a1c)
        c1 = aclcm//a
        c = aclcm//a1
        b = random.choice(sample_list2)
        b1 = random.choice(sample_list2)
        d = random.choice(sample_list2)
        d1 = random.choice(sample_list2)
        expr1 = (c * x+d)/(a*x+b)
        expr2 = (c1 * x+d1)/(a1*x+b1)
        St = sp.Eq(expr1, expr2)  # f1(x)=f2(x)
        Val = sp.solve(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF207一次函數圖像的性質
"""


def Put_PF207_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"].lower().strip()
    #ans=lib.Text2St(ans)
    try:
        #if parse_expr(ans)==Val:                   #比對答案:
        if ans==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF207_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        k = random.choice(sample_list1)
        b = random.choice(sample_list0)
        St = sp.Eq(y, k*x+b)  
        Val = "a"
        if k < 0:
            Val = "b"
        TE = GetTE(Qid, ["根據方程式及右圖, 判斷函數圖像的性質:",sp.latex(St),"選擇題:", "a. y隨x的增大而增大。","b. y隨x的增大而減少。"], Val, Tx)
        
        try:
            TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
            expr= k*x+b
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
            fig.savefig(mathPicPath(TE["PlotImg"]))

            # Save it to a temporary buffer.
            #buf = BytesIO()
            #fig.savefig(buf, format="png")
            #data = base64.b64encode(buf.getbuffer()).decode("ascii")
            #TE["PlotImg"]=f'data:image/png;base64,{data}'
            #return f"<img src='data:image/png;base64,{data}'/>"        
        except Exception as inst:
            #print(inst)
            TE["PlotImg"]=None
        NTE.append(TE)

    return NTE

def Get_PF381_Expr(QN,Tx=-1):
    x, y, z = sp.symbols('x,y,z')
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    if Tx==0:
        for Qid in range(0, QN):
            a,b,c = np.random.choice(sample_list1,3)
            St = sp.Eq(a*x*x+b*x+c)  
            Val = [sp.Rational(-b,a),sp.Rational(c,a)]
            TE = GetTE(Qid, ["求兩根之和，兩根之積:",sp.latex(St)], Val, Tx)
            TE["Tip"] = ["x1+x2", "x1*x2"]
            NTE.append(TE)
    elif Tx==1:
        for Qid in range(0, QN):
            a,b,c = np.random.choice(sample_list1,3)
            St = sp.Eq(a*x*x+b*x+c)  
            e=b*b-4*a*c
            Val=3 if e < 0 else  1 if  e> 0 else 2
            Val=[Val]
            TE = GetTE(Qid, ["求方程式根的判斷:",sp.latex(St),"(1)不相同實數根","(2)相同實數根","(3)無解"], Val, Tx)
            TE["Tip"] = ["1 or 2  or 3"]
            NTE.append(TE)
    return NTE    


"""
PF208 三角形的三邊關係
"""

def Get_PF208_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   

    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        
        if Tx==0:
            a,b=np.random.randint(1,30,2)
    
            fx1=parse_expr(f'x>{abs(a-b)}', evaluate=False) 
            fx2=parse_expr(f'x<{a+b}', evaluate=False) 
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and

            situation=random.choice([1,2,3])
            if situation==1:
                St=r"已知三角形三邊長分別為%s,%s,%s，求%s的取值範圍"%(a,b,sp.latex(x),sp.latex(x))
            elif situation==2:
                St=r"已知三角形三邊長分別為%s,%s,%s，求%s的取值範圍"%(a,sp.latex(x),b,sp.latex(x))
            else:
                St=r"已知三角形三邊長分別為%s,%s,%s，求%s的取值範圍"%(sp.latex(x),a,b,sp.latex(x))
            #Val=fx      #solve_univariate_inequality 解不等式   
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)       
    return NTE

def Put_PF209_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"].upper().strip()
    #ans=lib.Text2St(ans)
    try:
        #if parse_expr(ans)==Val:                   #比對答案:
        if ans==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

"""
PF209 三角形的三邊關係:確定三角形
"""

def Get_PF209_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   

    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        
        if Tx==0:
            choice=[]
            a,b=np.random.randint(1,30,2)
            c=np.random.randint(abs(a-b)+1,a+b)
            choice.append(f'{a},{b},{c}')
            for i in range(3):
                a,b=np.random.randint(1,30,2)
                c=np.random.randint(a+b,a+b+5)
                number=[a,b,c]
                random.shuffle(number)
                number=list(map(str,number))
                Str = ",".join(number)
                choice.append(Str)

            answer=random.choice([0,1,2,3])
            if answer==0:
                St=['下列長度的三條線段，能構成三角形的是()【填字母】',f'【A】{choice[0]}',f'【B】{choice[1]}',f'【C】{choice[2]}',f'【D】{choice[3]}']
                Val='A'
            elif answer==1:
                St=['下列長度的三條線段，能構成三角形的是()【填字母】',f'【A】{choice[1]}',f'【B】{choice[0]}',f'【C】{choice[2]}',f'【D】{choice[3]}']
                Val='B'
            elif answer==2:
                St=['下列長度的三條線段，能構成三角形的是()【填字母】',f'【A】{choice[1]}',f'【B】{choice[2]}',f'【C】{choice[0]}',f'【D】{choice[3]}']
                Val='C'
            elif answer==3:
                St=['下列長度的三條線段，能構成三角形的是()【填字母】',f'【A】{choice[1]}',f'【B】{choice[2]}',f'【C】{choice[3]}',f'【D】{choice[0]}']
                Val='D'

            TE = GetTE(Qid, St, Val,Tx)
            TE["Tip"] = ["填字母"]
            NTE.append(TE)

    return NTE


"""
PF210 三角形內角和
"""

def Put_PF210_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Get_PF210_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   

    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        
        if Tx==0:
            a,b,c=random.sample(['A','B','C','P','Q','R','D','E','F'],3)
            angle=[x for x in range(5, 90,5)]
            d,e=np.random.choice(angle,2)
            f=180-d-e
            Val= f
            St=r"在\triangle %s%s%s中, \angle %s = {%s}^o,\angle %s = {%s}^o, 則\angle %s =(    )^o"%(a,b,c,a,d,b,e,c)
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)

        elif Tx==1:
            a,b,c=random.sample(['A','B','C','P','Q','R','D','E','F'],3)
            angle=[x for x in range(1, 90,1)]
            d,e=np.random.choice(angle,2)
            f=180-d-e
            Val= f    
            St=r"在\triangle %s%s%s中, \angle %s = {%s}^o,\angle %s = {%s}^o, 則\angle %s =(    )^o"%(a,b,c,a,d,b,e,c)       
            TE = GetTE(Qid, St, Val,Tx)
            NTE.append(TE)

        elif Tx==2:
            a,b,c=random.sample(['A','B','C','P','Q','R','D','E','F'],3)

            Val=random.choice([1,2,3])
            if Val==1:
                f=np.random.randint(91,178)
                e=np.random.randint(1,180-f)
                d=180-f-e
            elif Val==2:
                d=1;e=1
                while d+e<=90:
                    d,e=np.random.randint(1,89,2)
                f=180-d-e
            else:
                d=np.random.randint(1,89)
                e=90-d
                f=180-d-e

               
            St1=r"在\triangle %s%s%s中, \angle %s = {%s}^o,\angle %s = {%s}^o ,則這個三角形是：    【填序號】"%(a,b,c,a,d,b,e)      
            St3=r"【1】鈍角三角形"
            St4=r"【2】銳角三角形"
            St5=r"【3】直角三角形"
            St=[St1,St3,St4,St5]
            TE = GetTE(Qid, St, Val,Tx)
            TE["Tip"] = ["填序號"]
            NTE.append(TE) 

    return NTE



"""
PF291一元二次方程式十字相乘法求因式
"""


def Put_PF291_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

def Get_PF291_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF392一元二次方程式求解
"""


def Put_PF392_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    try:
        cnt=0
        for idx in ans_:
            if idx.strip()=="無解":
                if Val[0]=="無解": 
                    TE["OK"]=1
                else:
                    TE["OK"]=0
                return    
            for v_ in Val:
                if parse_expr(lib.Text2St(idx))==v_ : cnt+=1
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
        


def Get_PF392_Expr(QN,Tx=-1):
    x=sp.Symbol('x',real=True)
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            p,q=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],2)
            b=p+q
            c=p*q
            express_str=f"x**2 + {b}*x +  {c} "  
            St=parse_expr(express_str, evaluate=False)     #字串解釋為可運算式子 expression
            St=sp.Eq(St,0)                              #f(x)=0

            St1=x**2+b*x+c
            St_latex=r" %s = %s" %(sp.latex(St1),sp.latex(0))
            Val=sp.solve(St)                              #因式分解,得出標準答案
            TE = GetTE(Qid, St_latex, Val, Tx)
            TE["Tip"] = ["x1", "x2"]
            NTE.append(TE)
        elif Tx==1:
            a,b,c,d=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],4)
            expr1=a*c*x**2
            expr2=(a*d+b*c)*x
            St=expr1+expr2+b*d
            St=sp.Eq(St,0)                              #f(x)=0
            Val=sp.solve(St)                              #因式分解,得出標準答案
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            TE["Tip"] = ["x1", "x2"]
            NTE.append(TE)
        elif Tx==2:
            a,b,c,d=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],4)
            expr1=a*c*(x+a)**2
            expr2=sp.Mul((a*d+b*c),(x+a),evaluate=False)
            St=sp.Add(expr1,expr2,b*d,evaluate=False)
            St=sp.Eq(St,0)                              #f(x)=0
            Val=sp.solve(St)                              #因式分解,得出標準答案
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            TE["Tip"] = ["x1", "x2"]
            NTE.append(TE)
        elif Tx==3:
            a,b,c=np.random.choice([-5,-4,-3,-2,-1,1,2,3,4,5],3)
            expr1=a*x**2
            expr2=b*x
            St=expr1+expr2+c
            St=sp.Eq(St,0)                    #f(x)=0
            Val=sp.solve(St,x)         #因式分解,得出標準答案
            if Val==[]: Val=["無解"]
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            TE["Tip"] = ["x1", "x2"]
            NTE.append(TE)
    return NTE


"""
PF293整式的乘法練習
"""


def Put_PF293_Expr(TE):
    x=sp.Symbol('x')
    Val=TE["Val"]
    ans=TE["Ans"]
    ans = lib.Text2StV1(ans)
    try:
        if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass
    

def Get_PF293_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = {}
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF301一元二次方程式
"""
def Put_PF301_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    ans=[]
    ans_idx=[]
    try:
        cnt=0
        for value in ans_:
            ans.append(parse_expr(value))
        
        for idx, a_ in enumerate(ans):
            for vidx, v_ in enumerate(Val):
                if a_==v_ : 
                    if vidx in ans_idx:
                        pass
                    else:
                        cnt+=1
                        ans_idx.append(vidx)
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF301_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = 1
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        if Tx == 2:
            p = random.choice(range(-15, 15))
            q = random.choice(range(-15, 15))
            b = p+q
            c = p*q
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass

        St = sp.Add(a*x**2, b*x, c, evaluate=False)
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        
                

        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF302解可化為一元二次方程的分式方程
"""


def Put_PF302_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    ans=[]
    ans_idx=[]
    try:
        cnt=0
        for value in ans_:
            ans.append(parse_expr(lib.Text2St(value)))
        
        for idx, a_ in enumerate(ans):
            for vidx, v_ in enumerate(Val):
                if a_==v_ : 
                    if vidx in ans_idx:
                        pass
                    else:
                        cnt+=1
                        ans_idx.append(vidx)
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass

    


def Get_PF302_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = random.choice(sample_list1)
        b = random.choice(sample_list1)
        b = sp.Integer(math.copysign(b, a))
        fx1 = a / (x**2)
        St = sp.Eq(fx1, b)  # f(x)=0
        if Tx == 2:
            if a*a+4*b >= 0:
                fx1 = a / x
                fx2 = b / (x**2)
                fx = sp.Add(fx1, fx2, evaluate=False)
                St = sp.Eq(fx, sp.Integer(1))  # f(x)=0
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF303解二元二次方程組
"""


def Put_PF303_Expr(TE):
    Val=TE["Val"]
    ans_=TE["Ans"].split(";")
    try:
        cnt=0
        for idx in ans_:
            for v_ in Val:
                if parse_expr(idx)==v_ : cnt+=1
        if cnt==len(Val):                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF303_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y = sp.symbols('x,y')
    NTE = []
    for Qid in range(0, QN):
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        f = p*q
        l = (p+q)
        eq1 = sp.Eq(x+y, b)
        eq2 = sp.Eq(x*y, c)
        St = [eq1, eq2]
        Val = sp.solve([eq1, eq2], x, y)
        #Val=sp.solve([x+y+f,x*y+l],x,y)
        #St = [sp.latex(eq1), sp.latex(eq2)]  # 題目
        St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(eq1),sp.latex(eq2))  
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = ["x1,y1","x2,y2"]
        NTE.append(TE)
    return NTE


"""
PF304二次函數圖像的性質
"""


def Put_PF304_Expr(NTE):
    Val=TE["Val"]
    ans=TE["Ans"].split(";")
    anss=[]
    try:
        for idx in ans:
            if idx=="" : idx="0"
            anss.append(parse_expr(lib.Text2St(idx)))
        Flag=0
        for v_ in Val:
            for a_ in ans:
                if(v_==a_): Flag+=1
        if Flag>1:                   #比對答案:
            TE["OK"]=1
        else:                                           #不則
            TE["OK"]=0
    except:
        pass

def Get_PF304_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list1)
        h = random.choice(sample_list0)
        k = random.choice(sample_list0)
        St = sp.Eq(y, a*(x-h)**2+k)  # , evaluate=False) #字串解釋為可運算式子 expression
        Val = [h, k]
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "xy"
        #TE["Plot"]=a*(x-h)**2+k
        NTE.append(TE)
    return NTE


"""
PF305解直角三角形    
"""


def sjstr(a, d, e):
    triang_fnc = ["", "sin", "cos", "tan"]
    str = triang_fnc[a]
    if e == 2:
        str += "^2"
    ang_degree = ["", "0^o", "30^o", "45^o", "60^o", "90^o"]
    return str+ang_degree[d]


def ang_expre(a, d, e):
    ad = [sp.pi, sp.pi*0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2]
    f = sp.S(1)
    if a == 1:
        f = sp.sin(ad[d])
    elif a == 2:
        f = sp.cos(ad[d])
    elif a == 3:
        f = sp.tan(ad[d])
    elif a == 4:
        f = sp.atan(ad[d])
    if e == 2:
        f = f**2
    return f
############################################################################


def Put_PF305_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

    

def Put_PF305_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    Tx = TE["Tx"]
    if Tx == 0 or Tx ==1 :
        if ans.strip() == "": ans = "3.1415926"
        try:
            if parse_expr(ans) == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass
    elif Tx==2:
        ans = ans.split(";")
        try:
            if parse_expr(ans[0].replace("^","**")) == Val[0]:  # 比對答案:
                if parse_expr(ans[1]) == Val[1]:
                    TE["OK"] = 1
                else:
                    TE["OK"] = 0
            else:  # 不則
                TE["OK"] = 0 
        except:
            pass
        
    
def Get_PF305_Expr(QN,Tx=-1):
    sp.init_printing("mathjax")
    x = sp.symbols('x')
    pp =[sp.Rational(1,6),sp.Rational(1,4),sp.Rational(1,3),sp.Rational(1,2),sp.Rational(2,3),sp.Rational(3,4),sp.Rational(5,6),1,sp.Rational(7,6),sp.Rational(5,4),sp.Rational(4,3),sp.Rational(3,2),sp.Rational(5,3),sp.Rational(7,3),sp.Rational(11,6)]
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            mode = random.choice([1,2])
            
            p = random.choice(pp)
            ra = p*180
            if mode==1:
                St=r"{%s}°=A{%s},求A的值" %(ra,chr(960))
                Val = p
                TE = GetTE(Qid, St, Val)
                TE["Tip"]= "A"
            elif mode ==2:
                St=r"{%s}=A°,求A的值" %(chr(960))
                Val = ra
                TE = GetTE(Qid, sp.latex(p)+St, Val)
                TE["Tip"]= "A"
                TE["Tx"]=0
        elif Tx==1:
            mode = random.choice([1,2])
            pp= range(5,3600,5)
            #p = random.choice(pp)
            #ra = p*180
            ra = random.choice(pp)
            p = sp.Mul(ra,sp.Rational(1,180),evaluate=False)
            if mode==1:
                St=r"{%s}°=A{%s},求A的值" %(ra,chr(960))
                Val = p
                TE = GetTE(Qid, St, Val)
                TE["Tip"]= ["A"]
            elif mode ==2:
                St=r"{%s}=A°,求A的值" %(chr(960))
                Val = ra
                p = sp.Mul(ra,sp.Rational(1,180),evaluate=True)
                TE = GetTE(Qid, sp.latex(p)+St, Val)
                TE["Tip"]= ["A"]
            TE["Tx"]=1
        elif Tx==2:
            mode = random.choice([1,2])
            pp= range(-3600,3600,5)
            #p = random.choice(pp)
            #ra = p*180
            ra = random.choice(pp)
            p = sp.Mul(ra,sp.Rational(1,180),evaluate=False)
            if mode==1:
                St=r"{%s}°=A{%s},求A的值" %(ra,chr(960))
                Val = p
                TE = GetTE(Qid, St, Val)
                TE["Tip"]= ["A"]
            elif mode ==2:
                St=r"{%s}=A°,求A的值" %(chr(960))
                Val = ra
                p = sp.Mul(ra,sp.Rational(1,180),evaluate=True)
                TE = GetTE(Qid, sp.latex(p)+St, Val)
                TE["Tip"]= ["A"]
            TE["Tx"]=1
        elif Tx==3:
            p= range(10,350,10)
            pp= range(-3600,3600,360)
            #p = random.choice(pp)
            #ra = p*180
            ra1 = random.choice(p)
            ra2 = random.choice(pp)
            while ra2==0:
                ra2 = random.choice(pp)
            ra3 = ra1 + ra2
            St=r"A={%s}°,求A的最小正角" %(ra3)
            Val = ra1
            TE = GetTE(Qid, St, Val)
            TE["Tip"]= ["A"]
            TE["Tx"]=1
        elif Tx==4:
            mode = random.choice([1,2])
            #Val = [1,1]
            Val = 0
            pp= range(5,3600,5)
            #p = random.choice(pp)
            #ra = p*180
            ra = random.choice(pp)
            p = sp.Mul(ra,sp.Rational(1,180),evaluate=False)
            ra2 = ra % 360
            if ra2<=90:
                Val = 1
            elif ra2 <=180:
                Val = 2
            elif ra2 <=270:
                Val = 3
            elif ra2 <=360:
                Val = 4
            
            if mode==1:
                #St=r"{%s}°=A{%s},求A的值,並說明所成角在第幾象限" %(ra,chr(960))
                St=r"A={%s}°,求A在第幾象限" %(ra)
                #Val[0] = p
                TE = GetTE(Qid, St, Val)
                #TE["Tip"]= ["A","象限(填1,2,3,4)"]
                TE["Tip"]= ["象限(填1,2,3,4)"]
            elif mode ==2:
                #St=r"{%s}=A°,求A的值,並說明所成角在第幾象限" %(chr(960))
                St=r"{%s}=A,求A在第幾象限" %(chr(960))
                #Val[0] = ra
                p = sp.Mul(ra,sp.Rational(1,180),evaluate=True)
                TE = GetTE(Qid, sp.latex(p)+St, Val)
                #TE["Tip"]= ["A","象限(填1,2,3,4)"]
                TE["Tip"]= ["象限(填1,2,3,4)"]
            TE["Tx"]=1
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


#######################


def plotTriangle(t,BAngle,li,Path_):
    B, C, A = t.vertices #頂点
    AB, BC, CA = Segment(A, B), Segment(B, C), Segment(C, A) #辺の設定 右辺は ABC.sidesと同等
    a, b, c = BC.length, CA.length, AB.length #辺の長さ
    opposides = { #頂点に対する対辺(opposite side)
        A: BC,
        B: CA,
        C: AB
    } #print(AB,BC,CA ,*t.sides)    
    # Figure and Axes
    fig=Figure()
    fig.set_figheight(3)
    fig.set_figwidth(3)
    ax=fig.subplots()    
    #plt.close('all')
    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')      #ax.grid()
    ax.set_axis_off() #軸の非表示
    ax.add_patch(plt.Polygon(t.vertices, fill=False))  
    ax.plot(*zip(*t.vertices), 'o') #'ro'
    ax.text(*B, '$\mathrm{B}$', ha='right', va='top') 
    ax.text(*C, '$\mathrm{C}$', ha='left', va='top')
    ax.text(*A, '$\mathrm{A}$', ha='left', va='bottom')
    squar_side_len=(a / 10)
    c1=Point(C[0],C[1]+squar_side_len)
    c2=Point(C[0]-squar_side_len,C[1]+squar_side_len)
    c3=Point(C[0]-squar_side_len,C[1])
    ax.add_patch(plt.Polygon([C,c1,c2,c3], fill=False))
    if "a" in li:
        ax.text(*BC.midpoint, r'$\mathrm{a}=%s$'%sp.latex(a), ha='right', va='top')
    else:
        ax.text(*BC.midpoint, '$\mathrm{a } $', ha='right', va='top')
    if "b" in li:    
        ax.text(*CA.midpoint, r'$\mathrm{b }=%s $'%sp.latex(b), ha='left', va='top')
    else:
        ax.text(*CA.midpoint, '$\mathrm{b } $', ha='left', va='top')
    if "c" in li:
        ax.text(*AB.midpoint, r'$\mathrm{c }=%s $'%sp.latex(c), ha='left', va='bottom')      
    else:
        ax.text(*AB.midpoint, '$\mathrm{c } $', ha='left', va='bottom')  
    #Arc Plot
    if BAngle != None:
        d=np.arange(start=0,stop=BAngle,step=1)
        rad=np.deg2rad(d)
        r=(a/10)
        xc = r*np.cos(rad)
        yc = r*np.sin(rad)
        ax.plot(xc,yc,color=[20/255,20/255,20/255],linestyle='-')   
        ax.text(B[0]+r,B[1]+0.04,r'$%s^o$' % BAngle)
    #plt.show()
    #fig.savefig(os.getcwd()+"\\static\\"+Path_) 
    fig.savefig(mathPicPath(Path_))
    return Path_       

def Get_PF306_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            op = random.choice([" + "])
            e = random.choice([1, 2])
            a = random.choice([1, 2, 3])
            b = random.choice([1, 2, 3])
            d1 = random.choice([1, 2, 3, 4, 5])
            d2 = random.choice([1, 2, 3, 4, 5])

            if a == 3 and d1 == 5:
                d1 = 4
            if b == 3 and d2 == 5:
                d2 = 4
            St = sjstr(a, d1, e) 
            if op == " / ":
                St = sjstr(a, d1, e) 
            Val = sp.S(0)

            if op == " + ":
                Val = ang_expre(a, d1, e)
            TE = GetTE(Qid, St, Val, Tx)
            TE["Tip"]=["答案(若無解請輸入zoo)"]

        elif Tx==1:
            op = random.choice([" + ", " - ", " * ", " / "])
            e = random.choice([1, 2])
            a = random.choice([1, 2, 3])
            b = random.choice([1, 2, 3])
            d1 = random.choice([1, 2, 3, 4, 5])
            d2 = random.choice([1, 2, 3, 4, 5])

            if a == 3 and d1 == 5:
                d1 = 4
            if b == 3 and d2 == 5:
                d2 = 4
            St = sjstr(a, d1, e) + op + sjstr(b, d2, 1)
            if op == " / ":
                St = sjstr(a, d1, e) + "\div " + sjstr(b, d2, 1) + "(若無解請輸入zoo)"
            Val = sp.S(0)

            if op == " + ":
                Val = ang_expre(a, d1, e) + ang_expre(b, d2, 1)
            elif op == " - ":
                Val = ang_expre(a, d1, e) - ang_expre(b, d2, 1)
            elif op == " * ":
                Val = ang_expre(a, d1, e) * ang_expre(b, d2, 1)
            elif op == " / ":
                Val = ang_expre(a, d1, e) / ang_expre(b, d2, 1)
            TE = GetTE(Qid, St, Val, Tx)
            #TE["Tip"] = ["log(a,b)","c"]
            TE["Tip"]=["答案(若無解請輸入zoo)"]
        NTE.append(TE)
    return NTE

##############################################################

def Get_PF306666_Expr(QN,Tx=-1):
    NTE = []
    for Qid in range(0, QN):
        x=random.choice([2,3,4,5])
        theta = random.choice([30,45,60,37,53])
        gamma=90-theta
        if theta==30:
            A=x*sp.sqrt(3)
            O=sp.S(x)
            H=sp.S(2*x)
        elif theta==45:
            A=sp.S(x)
            O=sp.S(x)
            H=x*sp.sqrt(2)
        elif theta==60:
            A=sp.S(x)
            O=x*sp.sqrt(3)
            H=sp.S(2*x)
        elif theta==37:
            A=sp.S(4*x)
            O=sp.S(3*x)
            H=sp.S(5*x)
        elif theta==53:
            A=sp.S(3*x)
            O=sp.S(4*x)
            H=sp.S(5*x)        
        if Tx == 1:
            b_f=["a","b","c"]
            b_v=[A,O,H]
            b_idx=random.choice([0,1,2])
            b_a=(random.choice([1,2])+b_idx)% 3
            St=[r"如下圖, 在Rt\triangle ABC中, \angle C = 90^o,", r"\angle B =%s^o, %s=%s,  求 %s  = ?"%(theta, b_f[b_idx],sp.latex(b_v[b_idx]),b_f[b_a])]
            if theta==53 or theta==37:
                anglesfilter=""
                St=[r"如下圖, 在Rt\triangle ABC中, \angle C = 90^o,"]
                for b_ in range(0,3):
                    if b_f[b_] != b_f[b_a]:
                        anglesfilter+=r" %s  = %s ,"% (b_f[b_],sp.latex(b_v[b_]))
                St.append(   anglesfilter)     
                St.append(r"求 %s  = ?"% (b_f[b_a]))
            Val = b_v[b_a]
            TE = GetTE(Qid, St, Val, Tx)
            if theta==53 or theta==37:
                t = Triangle(sss=(A, O,H)) #sss, sas, or asa
                anglesfilter=""
                for b_ in b_f:
                    if b_ != b_f[b_a]:
                        anglesfilter+=b_
                TE["PlotImg"]=plotTriangle(t,None,anglesfilter,"img"+GetKey()+str(Qid)+".png")
            else:
                t = Triangle(sas=(H, theta ,A)) #sss, sas, or asa
                TE["PlotImg"]=plotTriangle(t,theta,b_f[b_idx],"img"+GetKey()+str(Qid)+".png")

            
            NTE.append(TE)
            
        else:
            angle_=["A","B"]
            trig_=["sin","cos","tan"]
            trig=random.choice(trig_)
            ang=random.choice(angle_)
            #St=["設直角三角形:", r"a=%s,b=%s,c=%s, 求 %s \%s = ?"%(A,O,sp.latex(H) , trig,ang)]
            St=[r"如下圖, 在Rt\triangle ABC中, \angle C = 90^o,", r"a=%s, b=%s, 求 %s (%s) = ?"%(sp.latex(A),sp.latex(O), trig,ang)]
            Val = 1
            if trig=="sin":
                if ang=="A":             
                    Val=O/H
                if ang=="B":             
                    Val=A/H
            if trig=="cos":
                if ang=="A":             
                    Val=A/H
                if ang=="B":             
                    Val=O/H
            if trig=="tan":
                if ang=="A":             
                    Val=sp.S(O)/A
                if ang=="B":             
                    Val=sp.S(A)/O
            
            TE = GetTE(Qid, St, Val, Tx)
            t = Triangle(sss=(A, O,H)) #sss, sas, or asa
            TE["PlotImg"]=plotTriangle(t,None,"ab","img"+GetKey()+str(Qid)+".png")
            NTE.append(TE)

    return NTE

"""
PF307反比例函數的圖像與性質
"""

def Put_PF307_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"].lower().strip()
    #ans=lib.Text2St(ans)
    try:
        #if parse_expr(ans)==Val:                   #比對答案:
        if ans==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF307_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-15, 15))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list0.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            k=sp.symbols('k')
            t = random.choice(sample_list0)

            St = sp.Eq(y, k/x)  
            Val = "a"
            if t < 0:
                Val = "b"
            
            TE = GetTE(Qid, ["根據右圖作出判斷:",sp.latex(St),"選擇題:","a. k>0","b. k<0"], Val, Tx)
            
            try:
                TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
                expr= t/x
                lam_x = lambdify(x, expr, modules=['numpy'])
                x_vals = np.linspace(0.2, 5, 100)
                y_vals = lam_x(x_vals)
                fig = Figure()
                fig.set_figheight(3)
                fig.set_figwidth(3)
                color=random.choice(['#FFA042','#5A5AAD','#FF8000','#4A4AFF','#00BB00','#FF359A'])        
                ax = fig.subplots()
                ax.plot(x_vals, y_vals,color=color)
                ax.plot(-x_vals, -y_vals,color=color)
                ax.axhline(0, color='black')
                ax.axvline(0, color='black')          
                #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
                fig.savefig(mathPicPath(TE["PlotImg"]))

                # Save it to a temporary buffer.
                #buf = BytesIO()
                #fig.savefig(buf, format="png")
                #data = base64.b64encode(buf.getbuffer()).decode("ascii")
                #TE["PlotImg"]=f'data:image/png;base64,{data}'
                #return f"<img src='data:image/png;base64,{data}'/>"        
            except Exception as inst:
                #print(inst)
                TE["PlotImg"]=None
            NTE.append(TE)

        elif Tx==1:
            k = random.choice(sample_list0)

            St = sp.Eq(y, k/x)  
            Val = "減少"
            if k < 0:
                Val = "增大"
            TE = GetTE(Qid, ["根據函數解析式及右圖, 判斷函數圖像的性質:",sp.latex(St),"填充題:","y隨x的增大而........。","(填增大/減少)"], Val, Tx)
            
            try:
                TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
                expr= k/x
                lam_x = lambdify(x, expr, modules=['numpy'])
                x_vals = np.linspace(0.2, 5, 100)
                y_vals = lam_x(x_vals)
                fig = Figure()
                fig.set_figheight(3)
                fig.set_figwidth(3)
                color=random.choice(['#FFA042','#5A5AAD','#FF8000','#4A4AFF','#00BB00','#FF359A'])        
                ax = fig.subplots()
                ax.plot(x_vals, y_vals,color=color)
                ax.plot(-x_vals, -y_vals,color=color)
                ax.axhline(0, color='black')
                ax.axvline(0, color='black')          
                #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
                fig.savefig(mathPicPath(TE["PlotImg"]))
                # Save it to a temporary buffer.
                #buf = BytesIO()
                #fig.savefig(buf, format="png")
                #data = base64.b64encode(buf.getbuffer()).decode("ascii")
                #TE["PlotImg"]=f'data:image/png;base64,{data}'
                #return f"<img src='data:image/png;base64,{data}'/>"        
            except Exception as inst:
                #print(inst)
                TE["PlotImg"]=None
            NTE.append(TE)
        
        elif Tx==2:
            k = random.choice(sample_list0)

            St = sp.Eq(y, k/x)  
            Val = "減少"
            if k < 0:
                Val = "增大"
            TE = GetTE(Qid, ["根據函數解析式, 判斷函數圖像的性質:",sp.latex(St),"填充題:","y隨x的增大而........。","(填增大/減少)"], Val, Tx)
            
            NTE.append(TE)

    return NTE

"""
PF308反比例函數：解析式
"""
def Put_PF308_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"].upper().strip()
    #ans=lib.Text2St(ans)
    try:
        #if parse_expr(ans)==Val:                   #比對答案:
        if ans==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF308_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    NTE = []
    for Qid in range(0, QN):
        x, y, z ,k,b,a= sp.symbols('x,y,z,k,b,a')
        
        if Tx==0:
            x1=random.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9])
            k1=x1*random.choice([1,2,3,4,5,6,-1,-2,-3,-4,-5,-6])
            
            situation=random.choice([1,1,2,2,2])
            letter=random.choice(['P','Q','R','S','T'])
            if situation==1:
                y1=int(k1/x1)
                Val='在'
            elif situation==2:
                y1=int(round((k1/x1)*random.choice([-1,2,3,4,-2,-3,-4]),0))
                Val='不在'
            
            St=r"判斷：點%s(%s,%s)是否在%s上【填 在 / 不在】"%(letter,x1,y1,sp.latex(sp.Eq(y,k1/x)))
            
            TE = GetTE(Qid, St, Val, Tx) 
            NTE.append(TE)
        
        elif Tx==1:
            x1=random.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9])
            k1=x1*random.choice([1,2,3,4,5,6,-1,-2,-3,-4,-5,-6])
            y1=int(k1/x1)
            letter=random.choice(['P','Q','R','S','T'])
            Val=str(k1) 
            St=r"點%s(%s,%s)在%s上，求k的值"%(letter,x1,y1,sp.latex(sp.Eq(y,k/x)))
            
            TE = GetTE(Qid, St, Val, Tx) 
            NTE.append(TE)
        
        elif Tx==2:
            x1=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6])
            
            c=random.choice([1,1,1,1,2,2,2,3,3,3])
            d=random.choice([1,2,3,4,5,-1,2,-3,-4,-5,0])

            f=random.choice([1,2,3,4,5,-1,2,-3,-4,-5])
            letter=random.choice(['P','Q','R','S','T'])
            if c==1:
                k1=(x1+d)*f
                y1=f
                St=r"點%s(%s,%s)在%s上，求k的值"%(letter,x1,y1,sp.latex(sp.Eq(y,k/(x+d))))
            elif c==2:
                k1=(x1**2+d)*f
                y1=f
                St=r"點%s(%s,%s)在%s上，求k的值"%(letter,x1,y1,sp.latex(sp.Eq(y,k/(x**2+d))))
            elif c==3:
                k1=((x1+d)**2)*f
                y1=f
                St=r"點%s(%s,%s)在%s上，求k的值"%(letter,x1,y1,sp.latex(sp.Eq(y,k/(x+d)**2)))

            Val=str(k1) 
                    
            TE = GetTE(Qid, St, Val, Tx) 
            NTE.append(TE)
        
        elif Tx==3:
            x1=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5,6])
            
            f=random.choice([1,2,3,4,5,-1,2,-3,-4,-5])

            a1=random.choice([1,2,3,4,5,6])
            b1=random.choice([1,2,3,4,5,-1,2,-3,-4,-5,0])
            c1=random.choice([1,2,3,4,5,-1,2,-3,-4,-5,0])
            d1=random.choice([1,2,3,4,5,-1,2,-3,-4,-5,0])

         
            k1=(a1*x1**2+b1*x1+c1)*f
            y1=f-d1
            St1=y+d1
            St2=a1*x**2+b1*x+c1
            Sta=r"已知：%s與%s成反比例，"%(sp.latex(St1),sp.latex(St2))
            Stb=r"當x=%s時，y=%s"%(x1,y1)
            Stc=r"求反比例式的比例系數"


            Val=str(k1)
            TE = GetTE(Qid,[Sta,Stb,Stc], Val, Tx) 
            NTE.append(TE)
        

    return NTE




"""
PF309函數圖像的綜合練習(一次、二次、正比例、反比例函數)
"""

def Put_PF309_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"].upper().strip()
    #ans=lib.Text2St(ans)
    try:
        #if parse_expr(ans)==Val:                   #比對答案:
        if ans==Val:                   #比對答案:
            TE["OK"]=1
        else:                                      #不則
            TE["OK"]=0
    except:
        pass


def Get_PF309_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            x, y, z ,k,b,a,c= sp.symbols('x,y,z,k,b,a,c')
            sample_list0 = list(range(-15, 15))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
            sample_list0.remove(0)    # 非零數列
            sample_list1 = list(range(-15, 15))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
            sample_list1.remove(0) 
            sample_list2 = list(range(-3, 3))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
            sample_list2.remove(0)
            sample_list3 = list(range(-3, 3))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
            sample_list4 = list(range(-3, 3))   # [-5,-4,-3,-2,-1,1,2,3,4,5]

            species=random.choice([0,1,1,2,2,3,3])
       

            k1=random.choice(sample_list0)
            b1=random.choice(sample_list1)
            a2=random.choice(sample_list2)
            b2=random.choice(sample_list3)
            c2=random.choice(sample_list4)

            if species==0:
                St = sp.Eq(y, k1*x)
                expr= k1*x
                if k1>0: Val="A"
                else: Val="B"
            elif species==1:
                St = sp.Eq(y, k1*x+b1)
                expr= k1*x+b1
                if k1>0:
                    if b1>0: Val="C"
                    else: Val="D"
                else:
                    if b1>0: Val="E"
                    else: Val="F"
            elif species==2:
                St = sp.Eq(y, k1/x)
                expr= k1/x
                if k1>0: Val="G"
                else: Val="H"
            elif species==3:
                St = sp.Eq(y, a2*x**2+b2*x+c2)
                expr= a2*x**2+b2*x+c2
                if a2>0: Val="I"
                else: Val="J"

            
            St1=r"【 A 】 %s (%s) 【 B 】 %s(%s) "%(sp.latex(sp.Eq(y, k*x)),sp.latex(k>0),sp.latex(sp.Eq(y, k*x)),sp.latex(k<0))  
            St2=r"【 C 】 y=kx+b(k>0,b>0)【 D 】 y=kx+b(k>0,b<0) "
            St3=r"【 E 】 y=kx+b(k<0,b>0)【 F 】 y=kx+b(k<0,b<0) "
            St4=r"【 G 】 %s (%s) 【 H 】 %s(%s) "%(sp.latex(sp.Eq(y, k/x)),sp.latex(k>0),sp.latex(sp.Eq(y, k/x)),sp.latex(k<0)) 
            St5=r"【 I 】 %s (%s) "%(sp.latex(sp.Eq(y, a*x**2+b*x+c)),sp.latex(a>0)) 
            St6=r"【 J 】 %s (%s) "%(sp.latex(sp.Eq(y, a*x**2+b*x+c)),sp.latex(a<0)) 
            TE = GetTE(Qid, ["根據右圖，選取合適的解析式:【填字母】",St1,St2,St3,St4,St5,St6
        
                
                ], Val, Tx)
            
            try:
                TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
                
                
                lam_x = lambdify(x, expr, modules=['numpy'])
                if species==2:
                    x_vals = np.linspace(0.2, 5, 100)
                    y_vals = lam_x(x_vals)
                    fig = Figure()
                    fig.set_figheight(3)
                    fig.set_figwidth(3)
                    color=random.choice(['#FFA042','#5A5AAD','#FF8000','#4A4AFF','#00BB00','#FF359A'])        
                    ax = fig.subplots()
                    ax.plot(x_vals, y_vals,color=color)
                    ax.plot(-x_vals, -y_vals,color=color)
                    ax.axhline(0, color='black')
                    ax.axvline(0, color='black')          
                    #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
                    fig.savefig(mathPicPath(TE["PlotImg"]))
                elif species==3:
                    vertex=-b2/(2*a2)
                    x_vals = np.linspace(vertex-5, vertex+5, 999)
                    y_vals = lam_x(x_vals)
                    fig = Figure()
                    #fig.set_figheight(3)
                    #fig.set_figwidth(3)
                    color=random.choice(['#FFA042','#5A5AAD','#FF8000','#4A4AFF','#00BB00','#FF359A'])        
                    ax = fig.subplots()
                    ax.axhline(0, color='black')
                    ax.axvline(0, color='black')  
                    ax.axes.set(xlim=(vertex-5, vertex+5))       
                    ax.plot(x_vals, y_vals,color=color) 
                    #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
                    fig.savefig(mathPicPath(TE["PlotImg"]))

                else:
                    x_vals = np.linspace(-5, 5, 100)
                    y_vals = lam_x(x_vals)
                    fig = Figure()
                    fig.set_figheight(3)
                    fig.set_figwidth(3)
                    color=random.choice(['#FFA042','#5A5AAD','#FF8000','#4A4AFF','#00BB00','#FF359A'])        
                    ax = fig.subplots()
                    ax.plot(x_vals, y_vals,color=color)
                    ax.axhline(0, color='black')
                    ax.axvline(0, color='black')          
                    #fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
                    fig.savefig(mathPicPath(TE["PlotImg"]))

                # Save it to a temporary buffer.
                #buf = BytesIO()
                #fig.savefig(buf, format="png")
                #data = base64.b64encode(buf.getbuffer()).decode("ascii")
                #TE["PlotImg"]=f'data:image/png;base64,{data}'
                #return f"<img src='data:image/png;base64,{data}'/>"        
            except Exception as inst:
                #print(inst)
                TE["PlotImg"]=None
            NTE.append(TE)

    return NTE


"""
PF310相似三角形
"""

def Put_PF310_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Get_PF310_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    
    
    NTE = []
    Val=1
    for Qid in range(0, QN):
        letters=random.sample(['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V'],6)
        St1a='△'+letters[0]+letters[1]+letters[2]
        St1b='△'+letters[3]+letters[4]+letters[5]
        indexs=random.sample([0,1,2],3)
        side1a=letters[indexs[0]]+letters[indexs[1]]
        side1b=letters[indexs[0]+3]+letters[indexs[1]+3]

        ratio1=2;ratio2=4
        while math.gcd(ratio1,ratio2)!=1:
            ratio1,ratio2=np.random.choice([1,2,3,4,5,6,7,8,9],2)
        
        
        if Tx == 0:
            situation=random.choice([0,1])
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            if situation==1:
                side2a_length=random.choice([1,2,3,4,5,6,7,8,9,10,11])*ratio1
                Val=sp.Rational(side2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，則%s=......"%(side2a,side2a_length,side2b)
            else:
                side2b_length=random.choice([1,2,3,4,5,6,7,8,9,10,11])*ratio2
                Val=sp.Rational(side2b_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，則%s=......"%(side2b,side2b_length,side2a)
            TE = GetTE(Qid,[St1,St2], Val, Tx)
        
        elif Tx == 1:
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            side3a=letters[indexs[2]]+letters[indexs[0]]
            side3b=letters[indexs[2]+3]+letters[indexs[0]+3]
            situation=random.choice([0,1])
            if situation==0:
                C2a_length=np.random.randint(1,30)*ratio1
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1a,C2a_length,St1b)
                St3=''
            elif situation==1:
                C2b_length=np.random.randint(1,30)*ratio2
                Val=sp.Rational(C2b_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1b,C2b_length,St1a)
                St3=''
            TE = GetTE(Qid,[St1,St2,St3], Val, Tx)
        
        elif Tx == 2:
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            side3a=letters[indexs[2]]+letters[indexs[0]]
            side3b=letters[indexs[2]+3]+letters[indexs[0]+3]
            situation=random.choice([2,3])
            if situation==2:
                side1,side2,side3=np.random.randint(1,30,3)*ratio1
                C2a_length=side1+side2+side3
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s"%(side1a,side1,side2a,side2,side3a,side3)
                St3=r"則%s的周長是=......"%(St1b)
            elif situation==3:
                side1,side2,side3=np.random.randint(1,30,3)*ratio2
                C1a_length=side1+side2+side3
                Val=sp.Rational(C1a_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s，"%(side1b,side1,side2b,side2,side3b,side3)
                St3=r"則%s的周長是=......"%(St1a)
            TE = GetTE(Qid,[St1,St2,St3], Val, Tx)
        
        elif Tx == 3:
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            side3a=letters[indexs[2]]+letters[indexs[0]]
            side3b=letters[indexs[2]+3]+letters[indexs[0]+3]
            situation=random.choice([0,1,2,3])
            if situation==0:
                C2a_length=np.random.randint(1,30)*ratio1
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1a,C2a_length,St1b)
                St3=''
            elif situation==1:
                C2b_length=np.random.randint(1,30)*ratio2
                Val=sp.Rational(C2b_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1b,C2b_length,St1a)
                St3=''
            elif situation==2:
                side1,side2,side3=np.random.randint(1,30,3)*ratio1
                C2a_length=side1+side2+side3
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s"%(side1a,side1,side2a,side2,side3a,side3)
                St3=r"則%s的周長是=......"%(St1b)
            elif situation==3:
                side1,side2,side3=np.random.randint(1,30,3)*ratio2
                C1a_length=side1+side2+side3
                Val=sp.Rational(C1a_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s，"%(side1b,side1,side2b,side2,side3b,side3)
                St3=r"則%s的周長是=......"%(St1a)
            TE = GetTE(Qid,[St1,St2,St3], Val, Tx)
         
        elif Tx == 4:
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            side3a=letters[indexs[2]]+letters[indexs[0]]
            side3b=letters[indexs[2]+3]+letters[indexs[0]+3]
            situation=random.choice([0,1])
            if situation==0:
                S2a_length=np.random.randint(1,6)*ratio1**2
                Val=sp.Rational(S2a_length*ratio2**2,ratio1**2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的面積是%s，則%s的面積是=......"%(St1a,S2a_length,St1b)
                St3=''
            elif situation==1:
                S2b_length=np.random.randint(1,6)*ratio2**2
                Val=sp.Rational(S2b_length*ratio1**2,ratio2**2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的面積是%s，則%s的面積是=......"%(St1b,S2b_length,St1a)
                St3=''
            TE = GetTE(Qid,[St1,St2,St3], Val, Tx)
        
        elif Tx == 5:
            side2a=letters[indexs[1]]+letters[indexs[2]]
            side2b=letters[indexs[1]+3]+letters[indexs[2]+3]
            side3a=letters[indexs[2]]+letters[indexs[0]]
            side3b=letters[indexs[2]+3]+letters[indexs[0]+3]
            situation=random.choice([0,1,2,3,4,4,4,5,5,5,5])
            if situation==0:
                C2a_length=np.random.randint(1,30)*ratio1
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1a,C2a_length,St1b)
                St3=''
            elif situation==1:
                C2b_length=np.random.randint(1,30)*ratio2
                Val=sp.Rational(C2b_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的周長是%s，則%s的周長是=......"%(St1b,C2b_length,St1a)
                St3=''
            elif situation==2:
                side1,side2,side3=np.random.randint(1,30,3)*ratio1
                C2a_length=side1+side2+side3
                Val=sp.Rational(C2a_length*ratio2,ratio1)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s"%(side1a,side1,side2a,side2,side3a,side3)
                St3=r"則%s的周長是=......"%(St1b)
            elif situation==3:
                side1,side2,side3=np.random.randint(1,30,3)*ratio2
                C1a_length=side1+side2+side3
                Val=sp.Rational(C1a_length*ratio1,ratio2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s=%s，%s=%s，%s=%s，"%(side1b,side1,side2b,side2,side3b,side3)
                St3=r"則%s的周長是=......"%(St1a)
            elif situation==4:
                S2a_length=np.random.randint(1,6)*ratio1**2
                Val=sp.Rational(S2a_length*ratio2**2,ratio1**2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的面積是%s，則%s的面積是=......"%(St1a,S2a_length,St1b)
                St3=''
            elif situation==5:
                S2b_length=np.random.randint(1,6)*ratio2**2
                Val=sp.Rational(S2b_length*ratio1**2,ratio2**2)
                St1=r"已知：%s∽%s，%s : %s=%s:%s "%(St1a,St1b,side1a,side1b,ratio1,ratio2) 
                St2=r"若%s的面積是%s，則%s的面積是=......"%(St1b,S2b_length,St1a)
                St3=''
            TE = GetTE(Qid,[St1,St2,St3], Val, Tx)     
        
                
        NTE.append(TE)
    return NTE



def Get_PF401_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    NTE=[]
    for i in range(0,QN):
        ai=np.random.choice(range(-7,7),4)
        for i_, a_ in enumerate(ai):
            if a_ ==0 : ai[i_]=1            
        if Tx==0:
            op=random.choice([">","<"])
            express_str=f" ({ai[0]}*x + {ai[1]})*  ({ai[2]}*x + {ai[3]}) {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==1:
            op=random.choice([">","<"])
            express_str=f" {ai[0]}*x**2 + {ai[1]} {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==2:
            op=random.choice([">","<"])
            express_str=f" ({ai[0]}*x + {ai[1]})*  ({ai[2]}*x + {ai[3]}) "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=True) #字串解釋為可運算式子 expression 
            St=fx.apart() 
            if op==">":
                St=St>0
                Val=solve_univariate_inequality(fx > 0, x)      #solve_univariate_inequality 解不等式   
            else:
                St=St<0
                Val=solve_univariate_inequality(fx < 0, x)      #solve_univariate_inequality 解不等式   
                
        elif Tx==3:
            op=random.choice([">","<"])
            express_str=f" {ai[0]}*x**2 + {ai[1]}*x+{ai[2]} {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        else:
            op=random.choice([">","<"])
            express_str=f" {ai[0]}*x**2 + {ai[1]} {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        
        TE=GetTE(i,sp.latex(St),Val,Tx)        
        NTE.append(TE)    
    return NTE

"""
PF402等差數列之和
"""

def Put_PF402_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Get_PF402_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    n= sp.symbols('n')
    NTE=[]
    a1=random.sample(range(-9,10), k=10)
    for i in range(0,QN):
        if Tx==0:
            a2=1 
            a3=(a2+random.choice(range(4,7)) )% 11 ;a3=a3 if a3>0 else 1;
            d=random.choice(range(-9,10))
            a1=random.choice(range(-9,10))
            St=r"己知 a_{%s}={%s},d=%s,求a_{%s}"%(a2,a1,d,a3)
            Val=a1+(a3-1)*d
        elif Tx==1:
            a2=random.choice(range(2,10))
            a3=a2+random.choice(range(4,9))
            d=random.choice(range(-9,10))
            a1=random.choice(range(-9,10))
            St=r"己知 a_{%s}={%s},d=%s,求a_{%s}"%(a2,a1,d,a3)
            Val=a1+(a3-a2)*d
        elif Tx==2:
            a2=random.randrange(10) +1 
            a3=(a2+random.choice(range(4,7)) )% 11 ;a3=a3 if a3>0 else 1;
            d=a1[i]; d= d if d!=0 else 1
            expre= n*d
            expr_func= sp.lambdify(n,expre)
            a=expr_func(np.arange(12))
            St=r"己知 a_{%s}={%s},d=%s,求a_{%s}"%(a2,a[a2],d,a3)
            Val=a[a3]
        elif Tx==3:
            a2=random.randrange(10) +1 
            a3=(a2+random.choice(range(4,7)) )% 11 ;a3=a3 if a3>0 else 1;
            d=a1[i]; d= d if d!=0 else 1
            expre= n*d
            expr_func= sp.lambdify(n,expre)
            a=expr_func(np.arange(21))
            St=r"己知 a_{%s}=%s,a_{%s}=%s,求d"%(a2,a[a2],a3,a[a3])
            Val=d

            pass
        elif Tx==4:
            a2=random.randrange(6) + 6 
            a3=(a2+random.choice(range(4,7)) )% 11 ;a3=a3 if a3>0 else 1;
            d=a1[i]; d= d if d!=0 else 1
            expre= n*d
            expr_func= sp.lambdify(n,expre)
            a=expr_func(np.arange(18))
            print(a)
            tem_=""
            for i_,a_ in enumerate(a):
                if i_>0 and i_<4  :
                    tem_ = tem_+str(sp.latex(a_))+"、"
            St=r'己知等差數列的前%s項為 %s...、%s, 求S_{%s}'%(sp.latex(a2),tem_,sp.latex(a[a2]),sp.latex(a2))
            Val=sp.summation(expre, (n, 1, a2))
            pass
        elif Tx==5:
            a2=random.randrange(6) + 6 
            a3=(a2+random.choice(range(4,7)) )% 11 ;a3=a3 if a3>0 else 1;
            d=a1[i]; d= d if d!=0 else 1
            expre= n*d
            expr_func= sp.lambdify(n,expre)
            a=expr_func(np.arange(18))
            St=r'己知 a_{1}=%s,d=%s, 求S_{%s} '%(a[1],d,a2)
            Val=sp.summation(expre, (n, 1, a2))
            pass
        elif Tx==6:
            a2=random.choice(range(2,10))
            a3=a2+random.choice(range(4,9))
            d=random.choice(range(-9,10))
            a22=random.choice(range(-9,10))
            a33=a22+(a3-a2)*d
            s=random.randrange(6) + 6 
            a1=a22-(a2-1)*d
            St=r"己知 a_{%s}={%s},a_{%s}={%s}, 求S_{%s}"%(a2,a22,a3,a33,s)
            Val=(2*a1+(s-1)*d)*s/2
            pass
        
        TE=GetTE(i,St,Val,Tx)        
        NTE.append(TE)    
    return NTE



"""
PF403等比數列之和
"""

def Put_PF403_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Get_PF403_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    n= sp.symbols('n')
    NTE=[]
    a1=random.sample([sp.S(-4),-3,-2,sp.Rational(-1,2),sp.Rational(-1,3),sp.Rational(-1,4),1,2,3,4], k=10)
    for i in range(0,QN):
        if Tx==0:
            a2=random.choice([-3,-2,sp.Rational(-1,2),sp.Rational(-1,3),sp.Rational(-1,4),2,3,4,5,6,7,8,9])
            a3=1+random.choice([2,3,4,5])
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            St=r"己知 a_{%s}={%s},q=%s,求a_{%s}" % (1,a2,q,a3)
            Val=a2*(q**(a3-1))
        elif Tx==1:
            a2=random.randrange(3) +1 
            a3=(a2+random.choice(range(2,5)) )% 8 ;a3=a3 if a3>0 else 1;
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            expre= q**n
            a=[]
            for j in range(12):
                a.append(expre.subs(n,j))
            St=r"己知 a_{%s}={%s},q=%s,求a_{%s}" % (a2,a[a2],q,a3)
            Val=a[a3]
        elif Tx==2:
            a2=random.choice([-3,-2,sp.Rational(-1,2),sp.Rational(-1,3),sp.Rational(-1,4),2,3,4,5,6,7,8,9])
            a22=random.choice([2,3,4,5])
            a3=a22+random.choice([2,3,4,5])
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            ch=random.choice([1,2])
            if ch==1:
                St=r"己知 a_{%s}={%s},q=%s,求a_{%s}" % (a22,a2,q,a3)
                Val=a2*(q**(a3-a22))
            elif ch==2:
                St=r"己知 a_{%s}={%s},q=%s,求a_{%s}" % (a3,a2*(q**(a3-a22)),q,a22)
                Val=a2
        elif Tx==3:
            a2=random.randrange(3) +1 
            a3=(a2+random.choice(range(2,5)) )% 8 ;a3=a3 if a3>0 else 1;
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            if q<0  :q=-q
            expre= q**n
            a=[]
            for j in range(12):
                a.append(expre.subs(n,j))
            St=r"己知 a_{%s}=%s,a_{%s}=%s,求q, 其中q>0" %(a2,a[a2],a3,a[a3])
            Val=q
        elif Tx==4:
            a2=random.randrange(3) +5
            a3=(a2+random.choice(range(2,5)) )% 8 ;a3=a3 if a3>0 else 1;
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            expre= q**n
            a=[]
            for j in range(12):
                a.append(expre.subs(n,j))
            tem_=""
            for i_,a_ in enumerate(a):
                if i_>0 and i_<4  :
                    tem_ = tem_+str(sp.latex(a_))+"、"     
            St=r'己知 %s...、%s, 求S_{%s} '%(tem_,sp.latex(a[a2]),sp.latex(a2))            
            Val=sp.summation(expre, (n, 1, a2))
            pass
        elif Tx==5:
            a2=random.randrange(3) +4 
            a3=(a2+random.choice(range(2,5)) )% 8 ;a3=a3 if a3>0 else 1;
            q=a1[i]; 
            if q==0 :q=2
            if q==1 :q=2
            expre= q**n
            a=[]
            for j in range(12):
                a.append(expre.subs(n,j))
            St=r'己知 a_1={},q={}, 求S_{} '.format(a[1],q,a2)
            Val=sp.summation(expre, (n, 1, a2))
            pass
        elif Tx==6:
            a11=random.choice([sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,4),2,3,4,5,6,7,8,9])
            a22=random.choice([2,3,4,5])
            a3=a22+random.choice([2,3,4,5])
            q=random.choice([sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,4),2,3,4])
            s=3+random.choice([1,2,3,4])
            if q==0 :q=2
            if q==1 :q=2
            St=r"己知 a_{%s}={%s},a_{%s}={%s},求S_{%s}" % (a22,a11*(q**(a22-1)),a3,a11*(q**(a3-1)),s)
            Val=a11*(1-q**s)/(1-q)
            pass
        TE=GetTE(i,St,Val,Tx)        
        NTE.append(TE)    
    return NTE


"""
PF404對數與指數關係
"""

def Put_PF404_Expr(TE):
    x = sp.symbols('x')
    ans = TE["Ans"]
    Val = TE["Val"]
    ans = ans.split(";")
    #lib.Text2St(TE["Ans"])
    try:
        
        if parse_expr(lib.Text2St(ans[0])) == Val[0]:  # 比對答案:
            if parse_expr(lib.Text2St(ans[1])) == Val[1]:
                TE["OK"] = 1
            else:
                TE["OK"] = 0
        else:  # 不則
            TE["OK"] = 0
    except:
        pass

def Get_PF404_Expr(QN,Tx=-1):
    sp.init_printing("mathjax")
    x = sp.symbols('x')
    base_=[2,3,5,9,10,12,15,18,20]
    val_=[11,13,17,23,31,37,41,43,47]
    NTE = []
    for Qid in range(0, QN):
        if Tx==0:
            mode=random.choice([1,2,3,4,5,6])
            #mode=1
            if mode==1:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  \log_{%s}{%s} = {%s}  化成  a^b = c  的形式" %(b,x,c)
              ##  display(Latex(f"$   {St} = {c} $" ))
                eq1=b**c
                eq2=x
                d=r"{%s}" %(c)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["a**b","c"]
              ##  display(Latex(f"$   {b}^{d} = {eq2} $" ))
            elif mode ==2:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  \log_{%s}{%s} = {%s}  化成  a^b = c  的形式" %(x,b,c)
               ## display(Latex(f"$   {St} = {c} $" ))
               ## eq1=sp.latex(x**c)
                eq1=x**c
                eq2=b
                d=r"{%s}" %(c)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["a**b","c"]
              ##  Val[0] = eq2
               ## Val[1] = eq2
                ##display(Latex(f"$   {x}^{d} = {eq2} $" ))
              ##  display(Latex(f"$   {eq1} = {eq2} $" ))
            elif mode ==3:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  \log_{%s}{%s} = {%s}  化成  a^b = c  的形式" %(b,c,x)
               ## display(Latex(f"$   {St} = {x} $" ))     
                eq1=b**x
                eq2=c
                d=r"{%s}" %(x)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["a**b","c"]
               ## display(Latex(f"$   {b}^{x} = {eq2} $" ))
            elif mode ==4:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  {%s}^{%s} = {%s}  化成  \log_ba = c  的形式" %(b,x,c)
              ##  display(Latex(f"$   {St} = {c} $" ))
                eq1=sp.log(c,b)
                eq2=x
                d=r"\log_{%s}{%s}" %(b,c)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["log(a,b)","c"]
              ##  display(Latex(f"$   {d} = {eq2} $" ))
            elif mode ==5:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  {%s}^{%s} = {%s}  化成  \log_ba = c  的形式" %(x,b,c)
              ##  display(Latex(f"$   {St} = {c} $" ))
                eq1=sp.log(c,x)
                eq2=b
                d=r"\log_{%s}{%s}" %(x,c)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["log(a,b)","c"]
               ## display(Latex(f"$   {d} = {eq2} $" ))
            elif mode ==6:
                b=random.choice(base_)
                c=random.choice(val_)
                St=r"請將  {%s}^{%s} = {%s}  化成  \log_ba = c  的形式" %(b,c,x)
             ##   display(Latex(f"$   {St} = {x} $" ))
           
                eq1=sp.log(x,b)
                eq2=c
                d=r"\log_{%s}{%s}" %(b,x)
                Val = [1,1]
                Val[0] = eq1
                Val[1] = eq2
                TE = GetTE(Qid, St, Val)
                TE["Tip"] = ["log(a,b)","c"]
             ##   display(Latex(f"$   {d} = {eq2} $" ))
            if Val == []:
                pass
            else:
                NTE.append(TE)
    return NTE



"""
PF405對數的基礎運算
"""

def Put_PF405_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF405_Expr(QN,Tx=-1):
    base_=[2,3,5,10]
    val_=[2,3,4,5,sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,4),sp.Rational(1,5)]
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            b=random.choice(base_)
            c=random.choice(val_)
            d=b**c
            St=r"\log_{%s}{%s}" %(b,sp.latex(d))
            Val=c
            SSt=sp.log(d,b)  
        elif Tx==1:
            val_=[2,3,5,6,7,11,13]
            base=random.choice(base_)
            c=random.choice(val_)
            d=random.choice(val_)
            while c==d:
                d=random.choice(val_)
            e=c*d
            St=r"\log_{%s}{%s} + \log_{%s}{%s}" %(base,c,base,d)  #Val=c1+sp.log(c2,b)+sp.log(c3,b)
            SSt=sp.log(d,base)  # display(SSt)
            Val=sp.log(e,base)     #display(sp.logcombine(SSt,force=True))
        elif Tx==2:
            val_=[2,3,5,6,7,11,13]
            base=random.choice(base_)
            c=random.choice(val_)
            d=random.choice(val_)
            while c==d:
                d=random.choice(val_)
            e=c*d
            St=r"\log_{%s}{%s} - \log_{%s}{%s}" %(base,e,base,c)  #Val=c1+sp.log(c2,b)+sp.log(c3,b)
            SSt=sp.log(d,base)  # display(SSt)
            Val=sp.log(d,base)     #display(sp.logcombine(SSt,force=True))
            
        elif Tx==3:
            val__=[2,3,4,5,6,7,8]
            b=random.choice(base_)
            c1=random.choice([1,2,3])
            c2=random.choice(val__)
            c3=random.choice(val__)
            d=b**c1*c2*c3
            St=r"\log_{%s}{%s}" %(b,d)  #Val=c1+sp.log(c2,b)+sp.log(c3,b)
            SSt=sp.log(d,b)  # display(SSt)
            Val=sp.expand_log(SSt,force=True)     #display(sp.logcombine(SSt,force=True))
            
        elif Tx==4:
            choose=[0,1]
            n=random.choice(choose)
            if n==0:
                b=random.choice(base_)
                c=random.choice(val_)
                d=b**c
                St=r"把\log_{x}{%s}簡化成a\log_{x}{%s}時, a的值為多少？" %(sp.latex(d),b)
                Val=c 
            elif n==1:
                b=random.choice(base_)
                c=random.choice(val_)
                d=b**c
                St=r"把\log_{%s}{x}簡化成a\log_{%s}{x}時, a的值為多少？" %(sp.latex(d),b)
                Val=sp.Rational(1,c)
           

        elif Tx==5:
            logNum=[]
            logNum_s=[]
            b=random.choice(base_)
            val__=[2,3,4]
            for j in range(3):
                c1=random.choice([1,2,3])
                c2=random.choice(val__)
                c3=random.choice(val__)
                d=b**c1*c2*c3
                logNum.append(sp.log(d,b))
                logNum_s.append(r"\log_{%s}{%s}" %(b,d))
            St=logNum_s[0]
            SSt=logNum[0]
            for j in range(1):
                op=random.choice(["-","+"])
                St=St+op+logNum_s[j+1]
                if op=="-":
                    SSt=SSt-logNum[j+1]
                else:
                    SSt=SSt+logNum[j+1]
            Val=sp.expand_log(SSt,force=True)     #display(sp.logcombine(SSt,force=True))            

        elif Tx==6:
            logNum=[]
            logNum_s=[]
            b=random.choice(base_)
            val__=[2,3,4]
            for j in range(3):
                c1=random.choice([1,2,3])
                c2=random.choice(val__)
                c3=random.choice(val__)
                d=b**c1*c2*c3
                logNum.append(sp.log(d,b))
                logNum_s.append(r"\log_{%s}{%s}" %(b,d))
            St=logNum_s[0]
            SSt=logNum[0]
            for j in range(2):
                op=random.choice(["-","+"])
                St=St+op+logNum_s[j+1]
                if op=="-":
                    SSt=SSt-logNum[j+1]
                else:
                    SSt=SSt+logNum[j+1]
            Val=sp.expand_log(SSt,force=True)     #display(sp.logcombine(SSt,force=True))
        TE=GetTE(i,St,Val,Tx)        
        NTE.append(TE)    
    return NTE

def Put_PF407_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF407_Expr(QN,Tx=-1):
    point_=[1,2,3,4,5,6,7,8,9]
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(point_)
            b=random.choice(point_)
            c=random.choice(point_)
            d=random.choice(point_)
            while (a+b<=c) or (a+c<=b)  or (b+c<=a):
                a=random.choice(point_)
                b=random.choice(point_)
                c=random.choice(point_)
                d=random.choice(point_)
            St=f"已知三角形三邊分別為a=%s, b=%s, c=%s, 求cosA的值" %(a,b,c)
            Val=sp.Rational(b*b+c*c-a*a,2*b*c)
       
        TE=GetTE(i,St,Val,Tx) 
        NTE.append(TE)
    return NTE



def Get_PF501_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    NTE=[]
    for i in range(0,QN):
        bi=[]
        for i_ in range(0,6):
            r=random.choice([1,2,3])
            if r==1 :
                 bi.append("")
            else:
                 bi.append(f"**{r}")
        ai=np.random.choice(range(-4,4),12)
        for i_, a_ in enumerate(ai):
            if a_ ==0 : ai[i_]=1        
        if Tx==0:
            op=random.choice([">","<"])
            express_str=f" ({ai[0]}*x + {ai[1]}) * ({ai[2]}*x + {ai[3]}) * ({ai[4]}*x + {ai[5]}) {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==1:
            op=random.choice([">","<"])
            
            express_str=f" ({ai[0]}*x + {ai[1]}){bi[1]} * ({ai[2]}*x + {ai[3]}){bi[2]}  * ({ai[4]}*x + {ai[5]}){bi[3]}  * ({ai[6]}*x + {ai[7]}) {bi[4]} {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==2:
            op=random.choice([">","<"])
            express_str=f" ((x + {ai[0]})*( x + {ai[1]}) ) / ( (x+ {ai[2]})*(x + {ai[3]})) "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=True) #字串解釋為可運算式子 expression 
            St=fx #.apart() 
            if op==">":
                St=St>0
                Val=solve_univariate_inequality(fx > 0, x)      #solve_univariate_inequality 解不等式   
            else:
                St=St<0
                Val=solve_univariate_inequality(fx < 0, x)      #solve_univariate_inequality 解不等式   
                
        elif Tx==3:
            op=random.choice([">","<"])
            express_str=f" ((x + {ai[0]})*( x + {ai[1]}) ) / ( (x+ {ai[2]})*(x + {ai[3]})) "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=True) #字串解釋為可運算式子 expression 
            St=fx #.apart() 
            if op==">":
                St=St>0
                Val=solve_univariate_inequality(fx > ai[4], x)      #solve_univariate_inequality 解不等式   
            else:
                St=St<0
                Val=solve_univariate_inequality(fx <  ai[4], x)      #solve_univariate_inequality 解不等式   
        else:
            op=random.choice([">","<"])
            express_str=f" {ai[0]}*x**2 + {ai[1]} {op} 0 "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        
        TE=GetTE(i,sp.latex(St),Val,Tx)        
        NTE.append(TE)    
    return NTE


"""
PF502直線的斜率
"""

def Put_PF502_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF502_Expr(QN,Tx=-1):
    point_=[-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(point_)
            b=random.choice(point_)
            c=random.choice(point_)
            d=random.choice(point_)
            St=f"已知兩點A(%s, %s)、B(%s, %s), 求直線AB的斜率(若斜率不存在, 請輸入999)" %(a,b,c,d)
            if a==c: Val=999
            else : Val = sp.Rational((b-d),(a-c)) 
        elif Tx==1:
            point_=[-9,-8,-7,-6,-5,-4,-3,-2,-1,2,3,4,5,6,7,8,9]
            a=random.choice(point_)
            b=random.choice(point_)
            c=random.choice([11,13,19,17])
            if b>0:St=f"已知直線方程%sx+%sy+%s=0, 求直線的斜率" %(a,b,c)
            else : St=f"已知直線方程%sx%sy+%s=0, 求直線的斜率" %(a,b,c)
            Val = sp.Rational(-a,b)
        
        elif Tx==2:
            point_=[-9,-8,-7,-6,-5,-4,-3,-2,-1,2,3,4,5,6,7,8,9]
            mode=random.choice([1,2])
            if mode ==1 :
                a=random.choice(point_)
                b=random.choice(point_)
                c=random.choice([11,13,19,17])
                if b>0:St=f"已知直線方程%sx+%sy+%s=0, 求直線的斜率" %(a,b,c)
                else : St=f"已知直線方程%sx%sy+%s=0, 求直線的斜率" %(a,b,c)
                Val = sp.Rational(-a,b)
            else:
                a=random.choice(point_)
                b=random.choice(point_)
                c=random.choice([11,13,19,17])
                if b>0:St=f"已知直線方程%sy+%sx+%s=0, 求直線的斜率" %(a,b,c)
                else : St=f"已知直線方程%sy%sx+%s=0, 求直線的斜率" %(a,b,c)
                Val = sp.Rational(-b,a)
        TE=GetTE(i,St,Val,Tx) 
        NTE.append(TE)
    return NTE


def Get_PF503_Expr(QN,Tx=-1):
    a,b = sp.symbols('a b', real=True)
    x,y = sp.symbols('x y')
    n,k = sp.symbols('n k', integer=True, nonnegative=True)
    General_Term=sp.binomial(n, k)  *  a**(n-k)  *   b**(k)
    a_v ="-1/2,1/2,1,-1,2,-2".split(",")
    a_v=[sp.S(i_) for i_ in a_v ]
    b_v ="-1/3,1/3,-1/2,1/2,1,-1,3/2,-3/2,2,-2,-5/2,5/2,-3,3".split(",")
    b_v=[sp.S(i_) for i_ in b_v ]
    NTE=[]
    for Qid in range(0,QN):
        if Tx == 0:
            a_=random.choice(a_v)
            b_=random.choice(b_v)
            c_=3 if Qid<6 else 4;
            a_=x**a_
            St= (a_ + b_) **c_
            Val=sp.expand(St)
            op="" if str(b_)[0]=="-" else "+"
            St=f"\\left( {sp.latex(a_)} {op} {sp.latex(b_)} \\right) ^{c_}" 
            
            Val_Terms=[ General_Term.subs({ a:a_,  b: b_,  n: c_,  k:K } ) for K in range( c_ + 1)]
            ValSt=[]
            for i_, term_ in enumerate(Val_Terms):
                if not (str(term_)[0]=='-' or i_==0):
                    ValSt.append("+")
                ValSt.append(str(term_))
            ValSt="".join(ValSt)
            TE = GetTE(Qid, St, Val, Tx)
            TE["ValFmt"]=r"HTML"
            TE["ValSt"]=ValSt
            NTE.append(TE)
        elif Tx == 1:
            a_1,a_2=np.random.choice(b_v,2)
            b_1,b_2=np.random.choice(a_v,2)
            if b_1==b_2:b_1=b_1*b_1
            c_=3 if Qid<6 else 4;
            a_=a_1 * x**b_1
            b_=a_2 * x**b_2
            St= (a_ + b_) **c_
            Val=sp.expand(St)
            op="" if str(b_)[0]=="-" else "+"
            St=f"\\left( {sp.latex(a_)} {op} {sp.latex(b_)} \\right) ^{c_}" 
            
            Val_Terms=[ General_Term.subs({ a:a_,  b: b_,  n: c_,  k:K } ) for K in range( c_ + 1)]
            ValSt=[]
            for i_, term_ in enumerate(Val_Terms):
                if not (str(term_)[0]=='-' or i_==0):
                    ValSt.append("+")
                ValSt.append(str(term_))
            ValSt="".join(ValSt)
            TE = GetTE(Qid, St, Val, Tx)
            TE["ValFmt"]=r"HTML"
            TE["ValSt"]=ValSt
            NTE.append(TE)
        elif Tx == 2:
            a_=random.choice(a_v)
            b_=random.choice(b_v)
            c_=3 if Qid<6 else 4;
            a_=x**a_
            St= (a_ + b_) **c_
            Val=sp.expand(St)
            op="" if str(b_)[0]=="-" else "+"
            St=f"\\left( {sp.latex(a_)} {op} {sp.latex(b_)} \\right) ^{c_}" 
            ch=random.randint(1,c_+1)
            St=[St, f"求第{ch}項。"]
            Val= General_Term.subs({ a:a_,  b: b_,  n: c_,  k:ch-1 })
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        elif Tx == 3:
            a_=random.choice(a_v)
            b_=random.choice(b_v)
            c_=3 if Qid<6 else 4;
            a_=x**a_
            St= (a_ + b_) **c_
            Val=sp.expand(St)
            op="" if str(b_)[0]=="-" else "+"
            St=f"\\left( {sp.latex(a_)} {op} {sp.latex(b_)} \\right) ^{c_}" 
            ch=random.randint(1,c_)
            St=[St, f"求含有{sp.latex(a_**ch)}的項。"]
            Val= General_Term.subs({ a:a_,  b: b_,  n: c_,  k:c_ - ch })
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)

        else:
            a_=random.choice(a_v)
            b_=random.choice(b_v)
            c_=3 if Qid<6 else 4;
            a_=x**a_
            St= (a_ + b_) **c_
            Val=sp.expand(St)
            op="" if str(b_)[0]=="-" else "+"
            St=f"\\left( {sp.latex(a_)} {op} {sp.latex(b_)} \\right) ^{c_}" 
            Val= sp.expand(St)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)


    return NTE



"""
PF504 三棱柱
"""

def Put_PF504_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF504_Expr(QN,Tx=-1):
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知正三棱柱,高是%s,底面邊長%s,求這個正三棱柱的側面積" %(a,b)
            Val=a*b*3
        elif Tx==1:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知正三棱柱,高是%s,底面邊長%s,求這個正三棱柱的表面積 (√3請輸入3**0.5)" %(a,b)
            Val=a*b*3+0.25*b*b*(3**0.5)
          
        
        elif Tx==2:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知正三棱柱,高是%s,底面邊長%s,求這個正三棱柱的體積 (√3請輸入3**0.5)" %(a,b)
            Val=a*0.25*b*b*(3**0.5)
            
        TE=GetTE(i,St,Val,Tx) 
        NTE.append(TE)
    return NTE


"""
PF505 直四棱柱
"""

def Put_PF505_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF505_Expr(QN,Tx=-1):
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知直四棱柱,它的側棱長是%s, 它的底面是一個長是%s、闊是%s的長方形,求這個直四棱柱的側面積" %(a,b,c)
            Val=(b+b+c+c)*a
        elif Tx==1:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知直四棱柱,它的側棱長是%s, 它的底面是一個長是%s、闊是%s的長方形,求這個直四棱柱的表面積" %(a,b,c)
            Val=(b+b+c+c)*a+b*c*2
          
        
        elif Tx==2:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知直四棱柱,它的側棱長是%s, 它的底面是一個長是%s、闊是%s的長方形,求這個直四棱柱的體積" %(a,b,c)
            Val=a*b*c
            
        elif Tx==3:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知直四棱柱,它的側棱長是%s, 它的底面是一個長是%s、闊是%s的長方形,求這個正三棱柱的對角線長(二次方根請使用**0.5)" %(a,b)
            Val=(a*a+b*b+c*c)**0.5
          
        TE=GetTE(i,St,Val,Tx) 
        NTE.append(TE)
    return NTE


"""
PF506 正六棱柱
"""

def Put_PF506_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF506_Expr(QN,Tx=-1):
    NTE=[]
    for i in range(0,QN):
        if Tx==0:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知一個正六棱柱的底邊長是%s, 高是%s, 求這個正六棱柱的側面積 (√3請輸入3**0.5)" %(a,b)
            Val=a*b*6
        elif Tx==1:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知一個正六棱柱的底邊長是%s, 高是%s, 求這個正六棱柱的表面積 (√3請輸入3**0.5)" %(a,b)
            Val=a*b*6+0.25*a*a*(3**0.5)*6
          
        
        elif Tx==2:
            a=random.choice(range(2,10))
            b=random.choice(range(2,10))
            c=random.choice(range(2,10))
            
            St=f"已知一個正六棱柱的底邊長是%s, 高是%s, 求這個正六棱柱的體積 (√3請輸入3**0.5)" %(a,b)
            Val=a*0.25*a*b*(3**0.5)*6
            
        TE=GetTE(i,St,Val,Tx) 
        NTE.append(TE)
    return NTE



def Get_PF601_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    NTE=[]
    for i in range(0,QN):
        ai = np.random.choice(range(-6,7), 5)
        for i_, a_ in enumerate(ai):
            if a_ ==0 : ai[i_]=1           
        a= random.choice(range(-3,4))
        if a==0 : a=1
        b= random.choice(range(-8,9))
        c= random.choice(range(-3,4))
        d= random.choice(range(-6,7))  
        try:      
            if Tx==0:
                express_str=f" {ai[0]}+{ai[1]}*x + {ai[2]}*x**2 +  {ai[3]}*x**3 " # f(x)= ax + b > c
                f1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
                f2=parse_expr(f"{a}*x+{b}", evaluate=False) #字串解釋為可運算式子 expression 
                St=[r"多項式%s"%sp.latex(f1),r" 除以  %s  之餘式" %(sp.latex(f2))]
                Val=sp.rem(f1,f2,domain=sp.QQ)     #solve_univariate_inequality 解不等式   
            elif Tx==1:
                express_str=f" {ai[0]}+{ai[1]}*x + {ai[2]}* x**2 +  {ai[3]}* x**3  +  {ai[4]}* x**4" # f(x)= ax + b > c
                f1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
                f2=parse_expr(f"{a}*x+{b}", evaluate=False) #字串解釋為可運算式子 expression 
                St=[r"多項式%s"%sp.latex(f1),r" 除以  %s  之餘式" %(sp.latex(f2))]
                Val=sp.rem(f1,f2,domain=sp.QQ)     #solve_univariate_inequality 解不等式        elif Tx==3:
            elif Tx==2:
                b= random.choice(range(-6,7))
                express_str=f" {ai[0]}+{ai[1]}*x + {ai[2]}* x**2 +  {ai[3]}* x**3 " # f(x)= ax + b > c
                f1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
                f2=parse_expr(f"(x+{a})*(x+{b})", evaluate=False) #字串解釋為可運算式子 expression 
                St=[r"多項式%s"%sp.latex(f1),r" 除以  %s  之餘式" %(sp.latex(f2))]
                Val=sp.rem(f1,f2,domain=sp.QQ)     #solve_univariate_inequality 解不等式        else:
            else:
                ai = np.random.choice(range(-4,5), 5)
                a= random.choice(range(-2,3))
                if a==0 : a=1
                b= random.choice(range(-4,5))
                c= random.choice(range(-2,3))
                d= random.choice(range(-4,5))        
                express_str=f" {ai[0]}+{ai[1]}*x + {ai[2]}* x**2 +  {ai[3]}* x**3 +  {ai[4]}* x**4" # f(x)= ax + b > c
                f1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
                f2=parse_expr(f"({a}*x+{b})*({c}*x+{d})", evaluate=False) #字串解釋為可運算式子 expression 
                St=[r"多項式%s"%sp.latex(f1),r" 除以  %s  之餘式" %(sp.latex(f2))]
                Val=sp.rem(f1,f2,domain=sp.QQ)     #solve_univariate_inequality 解不等式
            TE=GetTE(i,St,Val,Tx)    
            TE["PlainText"]=1
            NTE.append(TE)    
        except:
            pass
    return NTE

def PF602_PLOT(exprs,Path_,xlim=[-1,10],ylim=[-1,10]):
    x=sp.Symbol('x')
    fig=Figure()
    fig.set_figheight(5)
    fig.set_figwidth(5)
    ax=fig.subplots()    
    """        
    plt.close('all')
    fig = plt.figure()
    fig.set_figheight(3)
    fig.set_figwidth(3)            
    ax = fig.add_subplot(1, 1, 1)
    """        
    ax.set_aspect('equal')
    ax.grid(axis='both',which='major',color=[166/255,166/255,166/255], linestyle='-', linewidth=1)
    ax.minorticks_on()
    ax.grid(axis='both',which='minor',color=[166/255,166/255,166/255], linestyle=':', linewidth=1)
    for expr in exprs:
        lam_x = sp.lambdify(x, expr, modules=['numpy'])
        x_vals = np.linspace(xlim[0], xlim[1], 5)
        y_vals = lam_x(x_vals)
        ax.plot(x_vals, y_vals)
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')    
    ax.set_xlim(xlim[0],xlim[1])            
    ax.set_ylim(ylim[0],ylim[1])            
    #plt.xlim([-1,10])
    #plt.ylim([-1,10])
    #plt.show()        
    #fig.savefig(os.getcwd()+"\\static\\"+Path_)
    fig.savefig(mathPicPath(Path_))
    try:
        pass
    except:
        print
        return None
    return Path_

def Get_PF602_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    #example
    tms=["""範例1. 設有甲、乙二紙廠生產三種紙類，機器每運轉一日:
        甲廠生產 1 噸 A 級紙、1 噸 B 級紙、5  噸 C 級紙, 開銷4 萬元；
        乙廠生產 3 噸 A 級紙、1 噸 B 級紙、2  噸 C 級紙, 開銷3 萬元；；
        今有訂單 9 噸 A 級紙、7 噸 B 級紙、20 噸 C 級紙。 
        問需如何運轉才能使開銷最低，又最低 的開銷為多少元？,
        |目標 \\( Pmin=4x+5y  \\) ; 註: 甲廠運轉x日;乙廠y日; x,y∈N
        |條件 \\( \\left\{\\begin{array}\\\\x+3y ≥ 9 \\\\x+y ≥ 7\\\\5x+2y ≥20\\\\x ≥ 0,y ≥ 0  \\end{array}\\right.\\)"""
        ,
        """範例2.有一工廠生產兩種不同產品(A,B),需4個部門,是各部門年最大產能:<table><tr><td><td>Product A<td>Product B</tr><tr><td>Moulding<td>25000<td>35000</tr><tr><td>Painting<td>33000<td>17000</tr><tr><td>Assembly A<td>22500<td>0</tr><tr><td>Assembly B<td>0<td>15000</tr><tr><td>Net profit pre unit<td>300<td>250</tr></table>
        |目標 \\( P=300x+250y  \\) ; 註: x = 產品(A)數量單位; y = 產品(B);x,y∈R
        |條件 \\( \\left\{\\begin{array}\\\\1.4x+y ≤ 35000\\\\0.51x+y ≤ 17000\\\\x ≤ 22500\\\\y ≤ 15000\\\\x ≥ 0, y ≥ 0  \\end{array}\\right.\\) """
        ]
    vals=[{"x":2,"y":5,"Pmin":23},{"x1":20224.72,"y1":6685.39,"Pmax":7738764}]    
    tips=[["X1=","Y1=","Pmin="],["X1=","Y1=","Pmax="]]
    exprs=[ [(9-x)/3 ,7-x,(20-5*x) /2],[35000-1.4*x,17000-0.51*x,(22500-x)*1000  ,15000- x*0.0001 ] ]
    xylim=[[-1,10],[-1,30000]]
    NTE=[]
    for Qid in range(0,10):
        idx=Qid
        if Tx==0:
            AL=PF602_Module.GetALset(3)
            TE=GetTE(Qid,AL[0],AL[1],Tx)    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")
            TE["PlainText"]=1
            TE["Tip"]=["x1","y1","Pmax","x2","y2","Pmin"]
            #print(TE)
            NTE.append(TE) 
            pass
        elif Tx==1:
            AL=PF602_Module.GetALset(4)
            TE=GetTE(Qid,AL[0],AL[1],Tx)    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")
            
            TE["PlainText"]=1
            TE["Tip"]=["x1","y1","Pmax","x2","y2","Pmin"]
            NTE.append(TE) 
            pass
        elif Tx==2:
            AL=PF602_Module.GetALset(5)
            TE=GetTE(Qid,AL[0],AL[1],Tx)    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")
            TE["PlainText"]=1
            TE["Tip"]=["x1","y1","Pmax","x2","y2","Pmin"]
            NTE.append(TE) 
            pass
        elif Tx==3:
            if Qid>1 :break
            
            St=tms[idx].split("\n")
            Val=vals[idx]
            TE=GetTE(Qid,St,Val,Tx)    
            TE["PlainText"]=1
            TE["Tip"]=tips[idx]
            x,y=sp.symbols("x,y")
            TE["PlotImg"]=PF602_PLOT(exprs[idx],"img"+GetKey()+str(Qid)+".png",xylim[idx],xylim[idx])
            NTE.append(TE) 
            
        
    return NTE


def Get_PF603_Expr(QN,Tx=-1):
    tips=["分子","分母"]
    Sheet02Cells=[
    ["已知==>",	"sin",	"cos",	"tan",	"cot",	"sec",	"csc",	"I",	"II",	"III",	"IV",	"0",	"30",	"45",	"60",	"90",	"120",	"135",	"150",	"180",	"210",	"125",	"240",	"270",	"300",	"315",	"330",	"360"],
    ["sin",	"k",	"J(1-k^2)",	"k/J(1+k^2)",	"1/J(1+k^2)",	"J(k^2-1)/k",	"1/k",	"1",	"1",	"-1",	"-1",	"0",	"1/2",	"J(2)/2",	"J(3)/2",	"1",	"J(3)/2",	"J(2)/2",	"1/2",	"0",	"-1/2",	"-J(2)/2",	"-J(3)/2",	"-1",	"-J(3)/2",	"-J(2)/2",	"-1/2",	"0"],
    ["cos",	"J(1-k^2)",	"k",	"1/J(1+k^2)",	"k/J(1+k^2)",	"1/k",	"J(k^2-1)/k",	"1",	"-1",	"-1",	"1",	"1",	"J(3)/2",	"J(2)/2",	"1/2",	"0",	"-1/2",	"-J(2)/2",	"-J(3)/2",	"-1",	"-J(3)/2",	"-J(2)/2",	"-1/2",	"0",	"1/2",	"J(2)/2",	"J(3)/2",	"1"],
    ["tan",	"k/J(1-k^2)",	"J(1-k^2)/k",	"k",	"1/k",	"J(k^2-1)",	"1/J(k^2-1)",	"1",	"-1",	"1",	"-1",	"0",	"J(3)/3",	"1",	"J(3)",	"**",	"-J(3)",	"-1",	"-J(3)/3",	"0",	"J(3)/3",	"1",	"J(3)",	"**",	"-J(3)",	"-1",	"-J(3)/3",	"0"],
    ["cot",	"J(1-k^2)/k",	"k/J(1-k^2)",	"1/k",	"k",	"1/J(k^2-1)",	"J(k^2-1)",	"1",	"-1",	"1",	"-1",	"**",	"J(3)",	"1",	"J(3)/3",	"0",	"-J(3)/3",	"-1",	"-J(3)",	"**",	"J(3)",	"1",	"J(3)/3",	"0",	"-J(3)/3",	"-1",	"-J(3)",	"**"],
    ["sec",	"1/J(1-k^2)",	"1/k",	"J(1+k^2)",	"J(1+k^2)/k",	"k",	"k/J(k^2-1)",	"1",	"-1",	"-1",	"1",	"1",	"2J(3)/3",	"J(2)",	"2",	"**",	"-2",	"-J(2)",	"-2J(3)/3",	"-1",	"-2J(3)/3",	"-J(2)",	"-2",	"**",	"2",	"J(2)",	"2J(3)/3",	"1"],
    ["csc",	"1/k",	"1/J(1-k^2)",	"J(1+k^2)/k",	"J(1+k^2)",	"k/J(k^2-1)",	"k",	"1",	"1",	"-1",	"-1",	"**",	"2",	"J(2)",	"2J(3)/3",	"1",	"2J(3)/3",	"J(2)",	"2",	"**",	"-2",	"-J(2)",	"-2J(3)/3",	"-1",	"-2J(3)/3",	"-J(2)",	"-2",	"**"]
    ]
    NTE=[]
    for Qid in range(0,QN  ):
        
        Ss1 = ["sin", "cos", "tan", "cot", "sec", "csc"]
        Ss3 = ["I", "II", "III", "IV"]
        i = lib.TakeARnd(1, 6, 0, 0, 0, 0)
        j = lib.TakeARnd(1, 6, 0, 1, i, i)
        s1 = Ss1[i - 1]; s2 = Ss1[j - 1]                           #   '已知s1, 求 s2
        St = Sheet02Cells[j ][i ]                           #  '答案的公式
        if Tx == 2 or  Tx == 1 :
            if Tx == 1 :
                St = St.replace( "k^2", s1 + "^2x")
                St = St.replace( "k", s1 + " x")
            else:
                St = St.replace( "k", "A")
            k = St.split("/")
            if len(k) == 1 :
                Ts1 = St
                Ts2 = ""
            else:
                Ts1 = k[0]
                Ts2 = k[1]
            if Tx == 20 :
                s1 = s1 + " x"
                s2 = s2 + " x"
            else:
                s1 = s1 + " x = A"
                s2 = s2 + " x"
            Xx = Ss3[0]
            St=[f"已知 {s1}, 求 {s2} ?  x∈{Xx}象限"]
            Val=[Ts1, Ts2]

            TE=GetTE(Qid,St,Val,Tx)
            TE["ValFmt"]=r"HTML"
            TE["ValSt"]=r"<table><tr><td>%s<tr><td>%s</table>"%(Ts1,Ts2)
            TE["Tip"]=["分子","分母"]
        elif Tx == 3 :               #给定函数值，指定象限
            if i < 3 :
                x = lib.TakeAFrc(9, 2)                                     # sin,cos 取真分数
            elif i < 5 :
                x = lib.TakeAFrc(9, 1)                                     # tan,coe, 不限
            else:
                x = lib.TakeAFrc(9, 3)                                     # sec,csc 取假分数
            k = random.randint(0,100) % 4
            Xx = Ss3[k]
            r = Sheet02Cells[i][ 7 + k]
            if r == -1 :
                x = -1 * x
            s1 = f"{s1}  x = {x}"                                     # 其值的正负要跟象限而定
            s2 = f"{s2}  x"
            St_=f"已知 {s1}, 求 {s2} ?  x∈{Xx}象限"
            # ---- 答案计算，化简
            Val=[]
            temp_=St.split("/")
            ValSt="<table>"
            for temp__ in temp_:
                tt_=temp__.replace("k",f"({x})")
                ValSt=f"{ValSt}<tr><td>{tt_}"
                Val.append(tt_)
            
            St=[St_]
            TE=GetTE(Qid,St,Val,Tx)
            TE["ValFmt"]=r"HTML"
            TE["ValSt"]=ValSt+"</table>"
            TE["Tip"]=["分子","分母"]
        elif Tx == 0 :       #特殊角，例 sin A = J(3)/2   A∈ II, ==> A=? tanA =?         
            Tip=["A=", f"{s2} A="]
            s5 = "**"
            while s5 == "**":
                r = lib.TakeARnd(1, 16, 0, 0, 0, 0)                      # 角
                s5 = Sheet02Cells[i][ 10 + r]
            s1 = f"{s1} A = {s5} "
            s2 = f"A,   {s2} A"
            a = Sheet02Cells[0][10 + r]
            Ts1 = f"{a}°"
            Ts2 = Sheet02Cells[j][ 10 + r]
            k = int(int(a) / 91)
            Xx = Ss3[k]      
            St_=f"已知 {s1}, 求 {s2} ?  A∈{Xx}象限, 若無意義請輸入**"
            # ---- 答案计算，化简
            Val=[Ts1,Ts2]
            St=[St_]
            TE=GetTE(Qid,St,Val,Tx)
            TE["ValFmt"]=r"HTML"
            TE["ValSt"]=r"<table><tr><td>%s<tr><td>%s</table>"%(Ts1,Ts2)
            TE["Tip"]=Tip

        TE["PlainText"]=1
        TE["PlotImg"]="//mail.mbc.edu.mo/ckeditorimages/worknote_210_2_triangle_same_angle_translate.png"
        NTE.append(TE)   
    return NTE     


def Put_PF604_Expr(TE):
    x = sp.Symbol('x')
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "3.1415926"
    
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1
        else:  # 不則
            TE["OK"] = 0
    except:
        pass


def Get_PF604_Expr(QN,Tx=-1):
    NTE = []
    for Qid in range(0, QN):
        x=sp.Symbol('x')
        if Tx==0:
            a = 1
            b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            e = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            f = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            St1=sp.latex(((a*d)*x**3+(a*e+b*d)*x**2+(b*e+c*d)*x+c*e+f))
            St2=sp.latex((d*x+e))
            St=r"求{%s}除以{%s}的餘數" %(St1,St2)
            St_latex=r"({%s} x^3 +{%s} x^2 +{%s} x +{%s})/({%s} x +{%s})" %(a*d, a*e+b*d,b*e+c*d,c*e+f,d,e)
            #display(Latex(st_st))
            Val=f
            #Val = sp.simplify(St)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        elif Tx==1:
            a = 1
            b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            e = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            f = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            g = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            h = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            i = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            
            St1=sp.latex(((a*d)*x**4+(a*e+b*d)*x**3+(b*e+c*d+a*f)*x**2+(b*f+e*c+g)*x+c*f+h))
            St2=sp.latex((d*x**2+e*x+f))
            St=r"求{%s}除以{%s}的餘式" %(St1,St2)
            St_latex=r"({%s} x^3 +{%s} x^2 +{%s} x +{%s})/({%s} x +{%s})" %(a*d, a*e+b*d,b*e+c*d,c*e+f,d,e)
            #display(Latex(st_st))
            Val=g*x+h
            #Val = sp.simplify(St)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
        elif Tx==2:
            a = random.choice([ 1, 2, 3, 4])
            b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            e = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            f = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            g = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            h = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            i = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            
            St1=sp.latex(((a*d)*x**4+(a*e+b*d)*x**3+(b*e+c*d+a*f)*x**2+(b*f+e*c+g)*x+c*f+h))
            St2=sp.latex((d*x**2+e*x+f))
            St=r"求{%s}除以{%s}的餘式" %(St1,St2)
            St_latex=r"({%s} x^3 +{%s} x^2 +{%s} x +{%s})/({%s} x +{%s})" %(a*d, a*e+b*d,b*e+c*d,c*e+f,d,e)
            #display(Latex(st_st))
            Val=g*x+h
            #Val = sp.simplify(St)
            TE = GetTE(Qid, St, Val, Tx)
            NTE.append(TE)
     
        else:
            a = 1
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            u = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            r = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({b}))* ( x + ({c}))  "  # 題型 express_str ax+bx+c
            St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
            Val = sp.expand(St)
            TE = GetTE(Qid, sp.latex(St), Val, Tx)
            NTE.append(TE)
    return NTE






def Get_PF405xxxx_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    #example
    tms=["""\\(  5x^2+kx-92=0  \\)
        己知 \\( x_{1} = -4 \\) 
        求另一根 \\( x_{2} \\) 和參數K
        <br><br><br><br><br><br>
        """]
    vals=[["23/5",-3]]    
    tips=[["x2","k"]]
    NTE=[]
    for Qid in range(0,QN):
        idx=0
        St=tms[idx].split("\n")
        Val=vals[idx]
        TE=GetTE(Qid,St,Val,Tx)    
        TE["PlainText"]=1
        TE["Tip"]=tips[idx]
        NTE.append(TE) 
        break;   
    return NTE

def Get_PF406_Expr(QN,Tx=-1):
    x=sp.symbols('x')
    #example
    tms=[""" \\( (y+8x)(y-8x) \\)
        """]
    vals=[["y^2-64*x^2"]]    
    tips=[[""]]
    
    NTE=[]
    for Qid in range(0,QN):
        idx=0
        St=tms[idx].split("\n")
        Val=vals[idx]
        TE=GetTE(Qid,St,Val,Tx)    
        TE["PlainText"]=1
        TE["Tip"]=tips[idx]
        x,y=sp.symbols("x,y")
        NTE.append(TE) 
        break;   
    return NTE
