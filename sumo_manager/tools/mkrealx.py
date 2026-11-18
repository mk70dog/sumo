# 実在の力士の補正値(v64)を作る:data/rec6_2026.txt・data/rikishi_debut.csv と本体の REALB から
# 出力:patches/realx67.json  {四股名:{dT,rm,fast,iki,old}}
import json,math,re,sys
from datetime import date
html=open(sys.argv[1],encoding='utf-8').read()
i=html.find('const REALB=');j=html.find('];',i);REALB=json.loads(html[i+12:j+1])
Tf=lambda i:4.5+12.5*math.exp(-i/170)
BN=['202511','202601','202603','202605','202607','202609']   # 古い順
rec={}
slots={}
for l in open('data/rec6_2026.txt',encoding='utf-8'):
    if l.startswith('#'):continue
    b,d,rk,nm,w,lo,a=l.strip().split('|')
    slots.setdefault(b,[]).append((nm,d,int(w),int(lo),int(a)))
eq={}   # 四股名 -> [(場所の新しさ k, 力の目安, 重み)]
for b in BN:
    L=slots[b];k=BN[::-1].index(b)
    # 番付の位置(0=横綱の東)。幕内・十両は 1 番 2 枚目ずつ、幕下は付出を最後に
    for idx,(nm,d,w,lo,a) in enumerate(L):
        n=w+lo
        if n==0:continue
        full=15 if d in 'MJ' else 7
        # 1 番の勝ち越し 1 つ = 番付で何人ぶん上の力か(推定):幕内・十両 1 人、幕下 4 人(幕下は 1 勝で 6 枚ほど動く目安の約 3 分の 1)
        per=1.0 if d in 'MJ' else 4.0
        eslot=idx-per*(w-lo)*full/max(n,1)*(n/full)
        eq.setdefault(nm,[]).append((k,Tf(max(0,eslot)),n/full,d))
deb={l.split(',')[0]:l.strip().split(',') for l in open('data/rikishi_debut.csv',encoding='utf-8')}
TIER=lambda t:{'横綱':0,'大関':1,'関脇':2,'小結':2}.get(t,3 if t.startswith('前頭') else 4 if t.startswith('十両') else 5 if t.startswith('幕下') else 6)
def curTier(f0,i):return {'Y':0,'O':1,'S':2,'K':2}.get(f0,3 if i<42 else 4 if i<70 else 5 if i<190 else 6)
def age(b):y,m,d=map(int,b.split('-'));return (date(2026,11,9)-date(y,m,d)).days/365.25
# 出世の速さ:初土俵から今の番付までの場所数を、同じ段の人と比べる
nb={}
for i,l in enumerate(REALB):
    f=l.split('|');nm=f[1]
    if nm in deb:
        y,m=map(int,deb[nm][2].split('-'));nbas=((2026-y)*12+(11-m))//2+1
        nb[nm]=(i,nbas)
def band(i):return 0 if i<10 else 1 if i<42 else 2 if i<70 else 3 if i<130 else 4 if i<190 else 5
med={}
for bd in range(6):
    v=sorted(math.log(x[1]) for nm,x in nb.items() if band(x[0])==bd)
    if v:med[bd]=(v[len(v)//2],(v[int(len(v)*.84)]-v[int(len(v)*.16)])/2 or .5)
out={};rep=[]
for i,l in enumerate(REALB):
    f=l.split('|');nm=f[1];a=age(f[4]);x={}
    T0=Tf(i)+(1.7 if f[0]=='Y' else 1.1 if f[0]=='O' else .4 if f[0] else 0)
    e=eq.get(nm)
    if e and i<190:
        e3=[z for z in e if z[0]<3] or e
        ws=[.6**k*wt for k,t,wt,d in e3];lv=sum(.6**k*wt*t for k,t,wt,d in e3)/sum(ws)
        # 番付の補正(横綱 +1.7 など)の分は、成績の目安にも同じだけ足して比べる
        lv+=T0-Tf(i)
        lim=1.0 if i<70 else .5
        x['dT']=round(max(-lim,min(lim,.5*(lv-T0))),2)
        # 勢い:最近 3 場所と、その前 3 場所の差
        new=[t for k,t,wt,d in e if k<3];old=[t for k,t,wt,d in e if k>=3]
        if new and old:
            mom=sum(new)/len(new)-sum(old)/len(old)
            if a<=25.9 and mom>.6:x['iki']=3;x['rm']=round(min(3,.6*mom),2);x['dT']=max(x['dT'],0)
    if nm in nb and a<26:
        ii,n=nb[nm];m,sd=med[band(ii)];z=(math.log(n)-m)/sd
        x['rm']=round(x.get('rm',0)+max(-1.5,min(2.5,-1.2*z)),2)
        x['rm']=min(3.5,x['rm'])
        if z<-.8:x['fast']=round(min(1.25,1+.1*(-z-.8)+.05),2)
    if nm in deb and a>=28:
        if TIER(deb[nm][3])<=3 and TIER(deb[nm][3])<curTier(f[0],i):x['old']=1
    x={k:v for k,v in x.items() if v}
    if x:out[nm]=x
    rep.append((i,nm,round(a,1),x))
json.dump(out,open('patches/realx67.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for r in rep[:75]:print(r)
print('数',len(out))
