import sympy as sp
import math
import random
import numpy as np
import re
from sympy.parsing.sympy_parser import parse_expr  # 文字字串, 解釋成, Sympy 運算式
from sympy.geometry import Point, Circle, Triangle, Segment, Line, RegularPolygon
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
def Text2St(ans):
    if ans.strip() == "": return "-3.1415926"
    ans = re.sub(r"X", r"x", ans)
    ans = re.sub(r"(\d)x", r"\1*x", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)x", r"\1*x", ans))
    ans=re.sub(r"x[(]", r"x*(", ans)
    ans = re.sub(r"x[ ]*", r"x", ans)
    ans = ans.replace(r"x^", r"x**")
    ans = re.sub(r"Y", r"y", ans)
    ans = re.sub(r"(\d)y", r"\1*y", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)y", r"\1*y", ans))
    ans=re.sub(r"y[(]", r"y*(", ans)
    ans = re.sub(r"y[ ]*", r"y", ans)
    ans = ans.replace(r"y^", r"y**")
    ans=re.sub(r"(\d)[(]", r"\1*(", ans)
    ans=re.sub(r"(\d)J[(]", r"\1*J(", ans)
    ans = ans.replace(r"J(", r"sqrt(")
    return ans

## ----- 產生受限的隨機數 -------
## ----- 範圍(a, b),  受限 (c, d)
# ----- Sw = 0  不受限,  Sw = 1, 受限， [c, d] 內的數不接受 -----
def GetARnd(a , b , e , Sw , c , D ):
    if a > b : x = a; a = b;  b = x                       #若a>b 則 a, b 交換
    if c > D : x = c; c = D;  D = x                       #若c>d 則 c, d 交換
    BL = False
    while True:                                                    # 設置循環
        x = random.randint(a,b)    # 取得 [a, b)範圍內的隨机數  #x = Round(x, e) # 截取 x 的 e 位四舍五入小數
        if Sw == 1 :  BL = x >= c and x <= D       # 若x落在 [c, d] 內，則返回再取 x
        if not BL : break                                      # 若x不在 [c, d] 內，則終止循環
    return x                                                    # 輸出 x

class ALine:
    def __init__(self, a=0,b=0,c=0,Op="≤",St="0*x+y*x" , St1="0*x/1"):
        self.a=a     
        self.b=b     
        self.c=c     
        self.Op=Op  
        self.St=St    
        self.St1 =St1
    def __str__(self):
        return f'ALine(f{self.a} {self.b} {self.c} {self.Op} {self.St} {self.St1})'
class TypeAPSet:
    def __init__(self, Pnt=[], n=0,Cp=[]):
        self.Pnt = Pnt
        self.n = n
        self.Cp = Cp
    def __str__(self):
        return f'TypeAPSet({self.Pnt},{self.n},{self.Cp})'

# ------  選取凸多邊形點集 ------
def GetAPset(n ):
    APset=TypeAPSet([],0,[])
    if n==3:
        APset.Pnt.append(( GetARnd(0, 8, 0, 1, 0, 0), GetARnd(0, 8, 0, 1, 0, 0)))
        APset.Pnt.append(( GetARnd(-8, 0, 0, 1, 0, 0), GetARnd(0, 8, 0, 1, 0, 0)))
        APset.Pnt.append(( GetARnd(-8, 8, 0, 1, 0, 0), GetARnd(-8, 0, 0, 1, 0, 0)))
    elif n==4:
        APset.Pnt.append((GetARnd(4, 8, 0, 0, 0, 0)  , GetARnd(-2, 2, 0, 0, 0, 0) ))
        APset.Pnt.append((GetARnd(-2, 2, 0, 0, 0, 0) , GetARnd(4, 8, 0, 0, 0, 0) ))
        APset.Pnt.append((GetARnd(-8, -4, 0, 0, 0, 0), GetARnd(-2, 2, 0, 0, 0, 0) ))
        APset.Pnt.append((GetARnd(-2, 2, 0, 0, 0, 0),  GetARnd(-8, -4, 0, 0, 0, 0) ))
    elif n==5:
        APset.Pnt.append(( GetARnd(4, 7, 0, 0, 0, 0)  , GetARnd(-1, 2, 0, 0, 0, 0)))
        APset.Pnt.append(( GetARnd(0, 3, 0, 0, 0, 0)  , GetARnd(4, 7, 0, 0, 0, 0)))
        APset.Pnt.append(( GetARnd(-7, -4, 0, 0, 0, 0), GetARnd(1, 4, 0, 0, 0, 0)))
        APset.Pnt.append(( GetARnd(-6, -3, 0, 0, 0, 0), GetARnd(-5, -2, 0, 0, 0, 0)))
        APset.Pnt.append(( GetARnd(0, 3, 0, 0, 0, 0)  , GetARnd(-7, -4, 0, 0, 0, 0)))
    x = 0; y = 0
    for i in range(n):
        Tp=APset.Pnt[i]
        x = x + Tp[0]
        y = y + Tp[1]
    APset.n=n
    APset.Cp.append(x / n)
    APset.Cp.append(y / n)   # 几何中心
    return APset

# ----- 由 2 點建立直線方程 --------
# ----- ax + by = c --------
def MakeAL(Tp1 , Tp2 ):
    Tx= ALine() 
    Tx.a = Tp2[1] - Tp1[1]
    Tx.b = Tp1[0] - Tp2[0]
    Tx.c = Tx.a * Tp1[0] + Tx.b * Tp1[1]
    Tx.c = int(Tx.c + 0.5)
    k = math.gcd(Tx.a, Tx.b); k = math.gcd(k, Tx.c)
    Tx.a = Tx.a / k; Tx.b = Tx.b / k; Tx.c = Tx.c / k
    if Tx.a < 0 : 
        Tx.a = -Tx.a; Tx.b = -Tx.b; Tx.c = -Tx.c
    s1 = ""
    if Tx.a == -1 : s1 = "-x "
    if Tx.a == 1 : s1 = "x "
    if abs(Tx.a) > 1 : s1 = str(Tx.a) + "x "
    s2 = ""
    if Tx.b == -1 : s2 = "-y "
    if Tx.b == 1 : s2 = "y "
    if abs(Tx.b) > 1 : s2 = str(Tx.b) + "y "
    if Tx.b > 0 and Tx.a != 0 : s2 = "+" + s2
    if abs(Tx.b) > 0.01 :
        Tx.St = s1 + s2
    else:
        Tx.St = s1
        Tx.b = 0.01
    Tx.St1 = "(" + str(Tx.c) + "-" + str(Tx.a) + "*x)/" + str(Tx.b)
    return Tx


def Line_PLOT(exprs,Path_):
    """
    fig=Figure()
    fig.set_figheight(3)
    fig.set_figwidth(3)
    ax=fig.subplots()    
    """        
    plt.close('all')
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(5)          
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    ax.grid(axis='both',which='major',color=[166/255,166/255,166/255], linestyle='-', linewidth=1)
    ax.minorticks_on()
    ax.grid(axis='both',which='minor',color=[166/255,166/255,166/255], linestyle=':', linewidth=1)
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    for expr in exprs:
        lam_x = sp.lambdify(x, expr, modules=['numpy'])
        x_vals = np.linspace(-10, 10, 2)
        y_vals = lam_x(x_vals)
        ax.plot(x_vals, y_vals)
        ax.axhline(0, color='black')
        ax.axvline(0, color='black')            
    plt.xlim([-10,10])
    plt.ylim([-10,10])
    plt.show()           
        #fig.savefig(os.getcwd()+"\\static\\"+Path_)
    return Path_
def PF602_Line_PLOT(exprs,Path_,xlim=[-10,10],ylim=[-10,10]):
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
    fig.savefig(os.getcwd()+"\\static\\"+Path_)
    try:
        pass
    except:
        return None
    return Path_
# ------ 建立隨機的線性不等式方程組  3 <=  n <=5 -----
# ------ 不是任意的隨機， 而是可圍成一個封閉的凸多邊形的邊 ------
def GetALset(n ):
    x,y=sp.symbols('x y')
    TL=[]
    Op=["≤","≥"] 
    TPs = GetAPset(n)                                      # 得到隨机的凸n邊形的頂點
    for i in range(n):
        j = i + 1
        if j == n : j = 0
        TL.append( MakeAL(TPs.Pnt[i], TPs.Pnt[j]))   #相鄰的兩點連為直線
        for j in range(-10 , 11):
            s1 = TL[i].St1.replace("x", str(j))
    for i in range(n):
        j = random.randint(1,100)%2
        if j == 0 :
            pass
        else:
            s1 = str(-1*TL[i].c)
            if s1[0] != "-" : s1 = "+" + s1
        expr=parse_expr(Text2St(TL[i].St))
        u = expr.subs({x: TPs.Cp[0],y:TPs.Cp[0] })              # 為使凸多邊形內部成為可行域，
        if u >= TL[i].c :                                    #以凸多邊形的几何中心進行測試，
            TL[i].Op = Op[1]                      # >= 符號
        else:
            TL[i].Op = Op[0]                         #<=符號

    a = GetARnd(-9, 9, 0, 1, -1, 1); b = GetARnd(-9, 9, 0, 1, -1, 1)
    PSt = f"{a}x" + (f"{b}y" if b < 0.1 else f"+{b}y" )
    
    St=[]
    St.append(f"目标:P= {PSt}")
    St.append("條件:  ")
    stt=[]
    expr_arr=[]
    for cc in TL:
        stt.append(f"\\\\{cc.St} {cc.Op} {cc.c}")
        if cc.a>0:
            expr_arr.append(parse_expr(Text2St(cc.St1)))
        else:
            expr_arr.append(parse_expr(Text2St(cc.St1+"+x/1000000")))
    St.append("\\( \\left\{\\begin{array} %s \\end{array}\\right.\\)"%("".join(stt)))            
    j = 1; k = 1
    Min = 99999; Max = -99999
    for i in range(n):
        expr=parse_expr(Text2St(PSt))
        a =expr.subs({x: TPs.Pnt[i][0],y:TPs.Pnt[i][1]})  
        if a > Max :
            Max = a
            j = i             #最大值
        if a < Min :
            Min = a        #最小值
            k = i
    Val=[TPs.Pnt[j][0],TPs.Pnt[j][1],Max,TPs.Pnt[k][0],TPs.Pnt[k][1],Min]    # 最大/小點的點號
    #Line_PLOT(expr_arr,"")
    return [St,Val,expr_arr]

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
            TE=GetTE(Qid,AL[0],AL[1])    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")
            TE["PlainText"]=1
            TE["Tip"]=["x1,y1","Pmax","x2,y2","Pmin"]
            NTE.append(TE) 
            pass
        elif Tx==1:
            AL=PF602_Module.GetALset(4)
            TE=GetTE(Qid,AL[0],AL[1])    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")
            
            TE["PlainText"]=1
            TE["Tip"]=["x1,y1","Pmax","x2,y2","Pmin"]
            NTE.append(TE) 
            pass
        elif Tx==2:
            AL=PF602_Module.GetALset(5)
            TE=GetTE(Qid,AL[0],AL[1])    
            TE["PlotImg"]=PF602_Module.PF602_Line_PLOT(AL[2],"img"+GetKey()+str(Qid)+".png")

            TE["PlainText"]=1
            TE["Tip"]=["x1,y1","Pmax","x2,y2","Pmin"]
            NTE.append(TE) 
            pass
        elif Tx==3:
            if Qid>1 :break
            
            St=tms[idx].split("\n")
            Val=vals[idx]
            TE=GetTE(Qid,St,Val)    
            TE["PlainText"]=1
            TE["Tip"]=tips[idx]
            x,y=sp.symbols("x,y")
            TE["PlotImg"]=PF602_PLOT(exprs[idx],"img"+GetKey()+str(Qid)+".png",xylim[idx],xylim[idx])
            NTE.append(TE) 
            
        
    return NTE