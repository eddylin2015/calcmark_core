import re
import math
import sympy as sp
import random

def IterateMultiDict(f):
    """
    Iterate requset.form
    """
    #f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            pass #print (key+":"+value)

### math
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)    

### Trim
def StrAllTrim(text):
    text=str(text)
    out=""
    for c in text:
        if c==" ":
            pass
        else:
            out=out+c
    return out

### V6Compare(a,b)
def S6Compare(a,b):
    a=StrAllTrim(a) 
    b=StrAllTrim(b) 
    a=a.replace("°","")
    b=b.replace("°","")    
    return a.lower()==b.lower()


### input ans 

def Text2St(ans,symbols_=["x","y","z","a","b","c"]):
    if ans.strip() == "": return "-3.1415926"
    dictionary = {'X': 'x', 'Y':'y', 'Z': 'z', '^': '**',"\\":"/"}
    transTable = ans.maketrans(dictionary)
    ans = ans.translate(transTable)
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
    ans = ans.replace(r"-(\d+)[*]", r"+-\1*")
    return ans


def Text2StV1(ans,symbols_=["x","y","z","m","n","a","b","c"]):
    if ans.strip() == "": return "-3.1415926"
    dictionary = {'X': 'x', 'Y':'y', 'Z': 'z','M': 'm','N': 'n', '^': '**',"\\":"/"}
    transTable = ans.maketrans(dictionary)
    ans = ans.translate(transTable)
    ans = re.sub(r"[)][(]", r")*(", ans)
    ans = re.sub(r"[)][ ]*[(]", r")*(", ans)
    for idx,s_ in enumerate(symbols_):
        re_expr=r"(\d)[ ]*"+s_
        rep_str=r"\1*"+s_
        ans = re.sub(re_expr, rep_str, ans)
        re_expr=r"[)][ ]*"+s_
        rep_str=r")*"+s_
        ans = re.sub(re_expr, rep_str, ans)
        re_expr=s_+r"[ ]*[(]"
        rep_str=s_+r"*("
        ans = re.sub(re_expr, rep_str, ans)
        if idx<(len(symbols_)-1):
            re_expr=symbols_[idx]+r"[ ]*"+symbols_[idx+1]
            rep_str=symbols_[idx]+r"*"+symbols_[idx+1]
            ans = re.sub(re_expr, rep_str, ans)
    ans = re.sub(r"(\d)[ ]*[(]", r"\1*(", ans)
    ans = re.sub(r"(\d)[ ]*J[(]", r"\1*J(", ans)
    ans = ans.replace('J(','sqrt(',10)
    return ans

### input inequ_ans 

def Text2Inequ(ans):
    ans = re.sub(r",", r"|", ans)
    if ans == "R" : return "(-oo < x) & (x < oo)"  
    r3=re.findall('x[ ]*[≠][ ]*[-]?\d+[ ]*[/]?[ ]*\d*', ans)
    for l_ in r3:
        s_="Ne(%s)" % l_.replace('≠',",")
        ans=ans.replace(l_,s_)
    r3=re.findall('x[ ]*[!][=][ ]*[-]?\d+[ ]*[/]?[ ]*\d*', ans)
    for l_ in r3:
        s_="Ne(%s)" % l_.replace('!=',",")
        ans=ans.replace(l_,s_)
    
    ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
    ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)
    if ans.strip() == "R" or ans.strip() == "r"  : return "(-oo < x) & (x < oo)"
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


def NTE2Table(data):
    return '<table><tr>{}</tr><tr>{}</tr></table>'.format(
           '<th>{}</th>'.format('</th><th>'.join( r for r in  r"編號,題型,題目,答案,作答,檢查,提示".split(","))),
           '</tr><tr>'.join(
               '<td>{}</td>'.format(
                   '</td><td>'.join("$$%s$$" % r[_] if i==2 else "%s" % r[_] for i, _ in enumerate(r))) for r in data)
           )

def TakeARnd(Ta , Tb , Desm=0 , SwIs=0 , Tc=0 , Td=0 ):
    r =0 
    BL = True
    while(BL):
        r = random.randint(Ta,Tb)
        #r = Int(r * 10 ^ Desm + 0.5) / 10 ^ Desm
        if SwIs==0:
            BL = False
        elif SwIs==1:
            BL = (r >= Tc) and (r <= Td)
        else:
            BL = (r == Tc) or (r == Td)
    return r

# ------ 建构一个随机分数,  ---------------
# ----- 分子为(-k , k) 内的整数-------
# ------  分数的SwIs ：0  不允许整数，1 允许整数，2 真分数，3 假分数
# ------ 本课题规定，只取正分数
# k As Single, SwIs As Integer
# As AFrc
def TakeAFrc(k, SwIs ): 
    a=0;b=0;c=0;r=0
    F=sp.Rational(1,2)
    BL = True
    while BL :                                         #
        a = TakeARnd(1, k, 0, 1, 0, 0)            #  分子， 本课题规定，只取正分数
        b = TakeARnd(1, k, 0, 1, 0, 0)             # 分母
        r = math.gcd(a, b)
        a = a / r; b = b / r
        F=sp.Rational(a,b)
        if SwIs== 0:
            BL = b == 1
        elif SwIs== 1:
            BL = False
        elif SwIs== 2:
            BL = abs(a) >= abs(b) or b == 1
        else:
            BL = abs(a) <= abs(b) or b == 1
    #Loop
    return F