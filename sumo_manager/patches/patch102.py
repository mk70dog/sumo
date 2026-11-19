# v98 -> v99:①まわり(追い風・向かい風)の判定を直す ②けがを過去 5 年の記録から決める(ダルマさん「どの力士も同じ評価が多い」「関取はそれぞれ違いが欲しい」「けがは 5 年前まで遡り、けがのしやすさ・古傷を反映」→「実施」)
import sys, os, json, re
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v98</title>', '<title>Grand Sumo Manager v99</title>')
rep("const APPV=98;\nconst SAVE='sumoManager98',SAVE97", "const APPV=99;\nconst SAVE='sumoManager99',SAVE98='sumoManager98',SAVE97")
rep('[SAVE97,SAVE96', '[SAVE98,SAVE97,SAVE96')
rep(" if(g.v===97){g.v=98;}\n return g.v===98?g:null;}", " if(g.v===97){g.v=98;}\n if(g.v===98){g.v=99;}\n return g.v===99?g:null;}")
rep('G={v:98,', 'G={v:99,')

# ---------- ② けが ----------
# 実在の関取・幕下の始めの記録:直近 6 場所の休場(data/rec6_2026.txt。sumodb の番付ページ、2026-11-19 に読み取り済み)
rec = {}
for l in open(os.path.join(here, '..', 'data', 'rec6_2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    f = l.strip().split('|')
    if len(f) < 7: continue
    ym, dv, rk, nm, w, lo, ab = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
    try: ab = int(ab)
    except: continue
    if ab > 0:
        full = 7 if dv == 'S' else 15
        rec.setdefault(nm, []).append([int(ym), ab, full])
REC5 = json.dumps(rec, ensure_ascii=False, separators=(',', ':'))
core = """/* v99:けがの履歴。全員のけがを r.ij に残し(直近 30 場所=5 年)、けがしやすさと古傷に反映する。数字はすべて推定 */
const REC5=""" + REC5 + """;
function ijYM(n){const y=(G.y0||2026)+Math.floor((n-1)/6),m=((n-1)%6+6)%6;return y*100+[1,3,5,7,9,11][m];}
function ijLabel(e){const y=e.ym||(G.y0?ijYM(e.b):0);return y?Math.floor(y/100)+'年'+(y%100)+'月':bname(e.b);}
/* けがしやすさ:直近 5 年の重いけが(1)・中くらい(0.5)・軽い(0.15)を、古いほど小さく数えて、確率に掛ける(最大 1.5 倍。全体の数が変わらないよう 1.03 で割る) */
function injSum(r){let t=0;(r.ij||[]).forEach(e=>{const a=(G.bnum||1)-e.b;if(a<0||a>30)return;t+=(e.s===3?1:e.s===2?.5:.15)*(1-a/30)*(e.est?.7:1);});return t;}
function injProne(r){return Math.min(1.5,1+.08*injSum(r))/1.03;}/* 1.03=全体の平均(関取の休場の数を v98 と同じくらいに保つ) */
/* 古傷の効きは年とともに少しずつ弱まる(最大でも半分まで) */
function oldF(r,q){const d=r.oldD&&r.oldD[q];if(!d)return 1;return Math.max(.5,1-((G.bnum||1)-d.b)/60);}
function realInj(r){const L=REC5[r.n];if(!L)return;const b0=G.bnum;r.ij=[];r.oldD=r.oldD||{};
 L.slice().sort((x,y)=>x[0]-y[0]).forEach(([ym,ab,full])=>{const k=Math.round(((2026*12+11)-(Math.floor(ym/100)*12+ym%100))/2);const b=b0-k;const last=r.ij[r.ij.length-1];
  const s=ab>=full?3:ab>=full/2?2:1;if(last&&last.b===b-1){last.s=Math.max(last.s,s);return;}
  let hs=0;for(const c of r.n+ym)hs=(hs*31+c.charCodeAt(0))|0;const u=hhR(hs,3)*100;let acc=0,p=PARTS[0];for(let i=0;i<PARTS.length;i++){acc+=[30,22,16,18,14][i];if(u<acc){p=PARTS[i];break;}}/* 部位は公表されていないので、四股名と場所から決まる推定 */r.ij.push({b:b,ym:ym,p:p,s:s,est:1});});
 r.ij.forEach(e=>{if(e.s>=2){r.old[e.p]=(r.old[e.p]||0)+1;r.oldD[e.p]={b:e.b,ym:e.ym,est:1};}});}
function injHistHTML(r){const old=Object.keys(r.old).filter(k=>r.old[k]).map(k=>{const d=r.oldD&&r.oldD[k];return k+(r.old[k]>1?'×'+r.old[k]:'')+(d?'('+ijLabel(d)+(d.est?'・推定':'')+')':'');});
 const sm=injSum(r),w=sm<.15?'人並み':sm<.6?'やや多い':sm<1.5?'多い':'かなり多い';
 const L=(r.ij||[]).filter(e=>(G.bnum||1)-e.b<=30).slice().sort((a,b)=>b.b-a.b).slice(0,4);
 return '<dt>古傷</dt><dd>'+(old.join('・')||'なし')+'</dd><dt>けがしやすさ</dt><dd>'+w+'<span class="mute" style="font-size:12px"> 過去 5 年</span>'+(L.length?'<br><span class="mute" style="font-size:12px">'+L.map(e=>esc(ijLabel(e))+' '+e.p+'('+['','軽','中','重'][e.s]+(e.est?'・推定':'')+')').join('<br>')+'</span>':'')+'</dd>';}
"""
rep("function injure(r,src){return inP(r.h,()=>injure0(r,src));}", core + "function injure(r,src){return inP(r.h,()=>injure0(r,src));}")
rep("[30,22,16,18,14][PARTS.indexOf(p)]*(1+.6*(r.old[p]||0))]);", "[30,22,16,18,14][PARTS.indexOf(p)]*(1+.6*(r.old[p]||0)*oldF(r,p))]);")
rep(" else r.inj={p:p,s:s,wk:wk,t:wk};\n", " else{r.inj={p:p,s:s,wk:wk,t:wk};r.ij=r.ij||[];r.ij.unshift({b:G.bnum,p:p,s:s});if(r.ij.length>40)r.ij.length=40;}\n")
rep("if(r.inj.s>=2&&!r.inj.ope)r.old[r.inj.p]=(r.old[r.inj.p]||0)+(r.inj.cons?2:1);", "if(r.inj.s>=2&&!r.inj.ope){r.old[r.inj.p]=(r.old[r.inj.p]||0)+(r.inj.cons?2:1);r.oldD=r.oldD||{};r.oldD[r.inj.p]={b:G.bnum};}")
rep("p+=.12*r.old[q];}", "p+=.12*r.old[q]*oldF(r,q);}")
rep("*(r.w>175?1.2:1)*((r.bf||0)>.33?1.15:1)*H.injMul;", "*(r.w>175?1.2:1)*((r.bf||0)>.33?1.15:1)*H.injMul*injProne(r);")
rep("*(f.hard?1.4:1)*(isPH(r.h)?inP(r.h,()=>heyaH0().injMul):1);", "*(f.hard?1.4:1)*injProne(r)*(isPH(r.h)?inP(r.h,()=>heyaH0().injMul):1);")
rep("<dt>古傷</dt><dd>'+(Object.keys(r.old).filter(k=>r.old[k]).map(k=>k+(r.old[k]>1?'×'+r.old[k]:'')).join('・')||'なし')+'</dd></dl>", "'+injHistHTML(r)+'</dl>")
rep("  realAdj(r,X);realFam(r);\n", "  realAdj(r,X);realFam(r);realInj(r);\n")

# ---------- ① まわりの判定 ----------
rep("function oshiItems(r){", "function oshiPopMean(d){const L=G.order.map(i=>G.R[i]).filter(x=>x&&!x.ret&&x.d===d).map(x=>x.pop||20).sort((a,b)=>a-b);return L.length?L[L.length>>1]:20;}\nfunction oshiItems(r){")
# ほかの部屋:関取は多め・少なめの境を高く(つながりが多いのがふつうなので)
rep("const n=hs.size;const v=n>=2?Math.min(60,n*12):(n===0&&r.d<=2?-20:0);", "const n=hs.size;const hi=r.d<=1?12:7,lo=r.d<=1?4:1;const v=n>=hi?Math.min(60,20+(n-hi)*8):n<=lo?(r.d<=2?-20:0):Math.round(5+(n-lo)*2);")
rep("L.push({k:'tsu',lb:'ほかの部屋',v,t:n?'つながり '+n+' 部屋':'つながり少ない',s:", "L.push({k:'tsu',lb:'ほかの部屋',v,t:(n&&v>=0)?'つながり '+n+' 部屋':'つながり少ない'+(n?'('+n+' 部屋)':''),s:")
# 同期:「競い合う」はふつう。同じ段で離されたら向かい風
rep("const mid=df>0&&!far&&r.d!==b.d;const v=far?-30:mid?0:df>0?20:30;", "const mid=df>0&&!far&&r.d!==b.d;const gap=df>0&&!far&&!mid&&df>=(r.d<=1?8:r.d===2?40:70);const v=far?-30:gap?-20:mid?0:df>0?5:(dk.length>=3?30:10);")
rep("t:far?'差をつけられ焦り':mid?'同期が先を行く':df>0?'競い合う':'同期の出世頭',s:mid?", "t:far?'差をつけられ焦り':gap?'同期に離され気味':mid?'同期が先を行く':df>0?'競い合う':'同期の出世頭',s:gap?'同期の '+b.n+'('+G.heya[b.h].n+'・'+b.rkS+')との番付の差が開いてきた。気持ちが焦りがち':mid?")
# 部屋の人望:境を近づける。c は項目ごとに決める
rep("const t=v>=22?'人望あつい':v<=-18?(big?'弟弟子に厳しすぎる':'部屋で浮き気味'):'ふつう';", "const t=v>=16?'人望あつい':v<=-12?(big?'弟弟子に厳しすぎる':'部屋で浮き気味'):'ふつう';")
rep("const s=v>=22?(big?", "const s=v>=16?(big?")
rep(":v<=-18?(big?'稽古場で声を荒らげる", ":v<=-12?(big?'稽古場で声を荒らげる")
rep("L.push({k:'jin',lb:'部屋の人望',v,t,s});", "L.push({k:'jin',lb:'部屋の人望',v,t,s,c:v>=16?'p':v<=-12?'n':'0'});")
rep("L.forEach(x=>{x.v=Math.round(cl(x.v,-100,100));x.c=x.v>=20?'p':x.v<=-18?'n':'0';});return L;}", "L.forEach(x=>{x.v=Math.round(cl(x.v,-100,100));x.c=x.c||(x.v>=20?'p':x.v<=-18?'n':'0');});return L;}")
# 後援会・ファン:同じ段の平均人気と比べる(関取どうしでも差がつく)
rep("let v=mem?25:0;if(mem&&(lastMk>=3||(r.d>=2&&r.d<=3)))v=-25;", "const pm=oshiPopMean(r.d);let v=mem?((r.pop||20)>=pm+6?25:0):0;if(mem&&(lastMk>=3||(r.d>=2&&r.d<=3)))v=-25;")
rep("{const p=r.pop||20;let v=p>=30?30:0;let t=p>=30?'声援 多い':p>=15?'声援 ふつう':'まだ知られていない';", "{const p=r.pop||20;const pm=oshiPopMean(r.d);let v=p>=pm+8?30:(r.d<=1&&p<=pm-6?-20:0);let t=p>=pm+8?'声援 多い':(r.d<=1&&p<=pm-6)?'知名度がいまひとつ':p>=15?'声援 ふつう':'まだ知られていない';")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'REC5 人数', len(rec))
