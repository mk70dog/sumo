# v88 -> v89:一人用と二人用を同じ作りにする(第 1 歩:土台)
# ダルマさん「一人用 2人用 同じにはできない?」→「実装」。
# 「自分の部屋=部屋 0」の決め打ちをやめ、いま受け持っている部屋 ME() と、プレイヤーごとのデータ G.P にする。
# G.P がないとき(今までの一人用)は ME()=0 で、乱数の使い方も含めて v88 と同じ結果になる。
# プレイヤーごとのデータ(お金・スタッフ・施設・出来事・後援会など PKEYS)は、受け持っているプレイヤーの分が G の上に、
# ほかのプレイヤーの分は G.P[i] に入る。pUse(i) で入れかえ、inP(部屋,fn) でその部屋のプレイヤーとして fn を動かす。
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)

# ---- 版の番号 ----
rep('<title>Grand Sumo Manager v88</title>', '<title>Grand Sumo Manager v89</title>')
rep("const APPV=88;\nconst SAVE='sumoManager88',SAVE87", "const APPV=89;\nconst SAVE='sumoManager89',SAVE88='sumoManager88',SAVE87")
rep('[SAVE87,SAVE86,SAVE85', '[SAVE88,SAVE87,SAVE86,SAVE85')
rep(" if(g.v===87){g.v=88;}\n return g.v===88?g:null;}", " if(g.v===87){g.v=88;}\n if(g.v===88){g.v=89;}\n return g.v===89?g:null;}")
rep('G={v:88,', 'G={v:89,')

# ---- 土台 ----
rep("""const me=()=>G.heya[0];
const own=()=>G.order.map(i=>G.R[i]).filter(r=>r.h===0&&!r.ret);""",
"""/* v89:プレイヤーごとのデータ(一人でも二人でも同じ作り)。G.P がなければ今までどおり部屋 0 が受け持ちの部屋 */
const PKEYS=['oshi','supC','chi','bld','yfin','yacc','jin','meSel','late','st16','meal','con','chk','rel','tkPol','post','postT','scl','okamiUsed','okami','yr','intv','myoL','myoM','tourPol','tourTsuki','money','rep','sup','fac','log','ach','pend','staff','market','pros','fin','acc','ev','news','over','overWhy','tmp','mh','capB','supFee','finSc','mePost','wkg','wkgDone','coAs','sp','kpol','yoso','media','popS','_me','_tk','_tr','dok','subX'];
let _PX=0;
function ME(){return G&&G.P?G.P[G.PA||0].h:0;}
function isPH(h){if(!G||!G.P)return h===0;const P=G.P;for(let i=0;i<P.length;i++)if(P[i].h===h)return true;return false;}
function pI(h){if(!G||!G.P)return h===0?0:-1;return G.P.findIndex(p=>p.h===h);}
function pUse(i){const P=G&&G.P;const a=G.PA||0;if(!P||i===a||!P[i])return;const cur=P[a],nx=P[i];const muk=G.tmp?G.tmp.muk:0;
 PKEYS.forEach(k=>{if(k in G){cur[k]=G[k];delete G[k];}else delete cur[k];});
 PKEYS.forEach(k=>{if(k in nx){G[k]=nx[k];delete nx[k];}});
 if(G.tmp)G.tmp.muk=muk;G.PA=i;}
function inP(h,fn){if(!G||!G.P)return fn();const i=pI(h);if(i<0)return fn();const a=G.PA||0;
 if(i!==a)pUse(i);_PX++;try{return fn();}finally{_PX--;if(i!==a)pUse(a);}}
function forP(fn){if(!G||!G.P)return fn(0);const a=G.PA||0;try{for(let i=0;i<G.P.length;i++){pUse(i);_PX++;try{fn(i);}finally{_PX--;}}}finally{pUse(a);}}
function pv(h,k){if(!G||!G.P)return h===0?G[k]:undefined;const i=pI(h);if(i<0)return undefined;return i===(G.PA||0)?G[k]:G.P[i][k];}
function allPK(k){if(!G.P)return G[k]||[];let L=[];G.P.forEach((p,i)=>{const v=i===(G.PA||0)?G[k]:p[k];if(v)L=L.concat(v);});return L;}
function anyEv(){if(G.ev&&G.ev.length)return true;return !!(G.P&&G.P.some((p,i)=>i!==(G.PA||0)&&p.ev&&p.ev.length));}
const me=()=>G.heya[ME()];
const own=()=>{const m=ME();return G.order.map(i=>G.R[i]).filter(r=>r.h===m&&!r.ret);};""")

# お知らせ:プレイヤーの場面の外(世界の出来事)は、全員の日誌に入れる
rep("function addNews(t){G.log.unshift('〔'+bname(G.bnum)+'〕'+t);if(G.log.length>250)G.log.length=250;}",
"function addNews(t){const s='〔'+bname(G.bnum)+'〕'+t;G.log.unshift(s);if(G.log.length>250)G.log.length=250;\n if(G.P&&!_PX)G.P.forEach((p,i)=>{if(i!==(G.PA||0)&&p.log){p.log.unshift(s);if(p.log.length>250)p.log.length=250;}});}")

# ---- 部屋の番号を引数に取るもの ----
rep('heyaH(0)', 'heyaH(ME())', 5)
rep('finScore(0)', 'finScore(ME())')
rep('heyaInfoHTML(0)', 'heyaInfoHTML(ME())')
rep('let _H0=null;function heyaH0(){if(!_H0)_H0=heyaH(ME());return _H0;}',
    'let _H0=null;function heyaH0(){const m=ME();if(!_H0)_H0={};if(!_H0[m])_H0[m]=heyaH(m);return _H0[m];}')
rep("function heyaH(h){\n if(h!==0){", "function heyaH(h){\n if(!isPH(h)){")
rep("(i===0&&me().oyT?0:0)", "(i===ME()&&me().oyT?0:0)")

# ---- ほかの部屋(コンピューターが受け持つ部屋)だけ ----
rep("function openAI(){const L=[];for(let i=1;i<G.heya.length;i++)if(!G.heya[i].closed)L.push(i);return L;}",
    "function openAI(){const L=[];for(let i=1;i<G.heya.length;i++)if(!G.heya[i].closed&&!isPH(i))L.push(i);return L;}")
rep("if(!h||h.closed||i===0)return;", "if(!h||h.closed||isPH(i))return;")
rep("G.order.forEach(add);G.pend.forEach(add);G.aiPend.forEach(add);\n const L=[];for(let h=1;h<G.heya.length;h++)if(!used.has(h)&&!G.heya[h].closed)L.push(h);return L;}",
    "G.order.forEach(add);allPK('pend').forEach(add);G.aiPend.forEach(add);\n const L=[];for(let h=1;h<G.heya.length;h++)if(!used.has(h)&&!G.heya[h].closed&&!isPH(h))L.push(h);return L;}")
rep("const c=G.order.map(id=>G.R[id]).filter(r=>r.h!==0&&!r.ret&&r.d<=3);", "const c=G.order.map(id=>G.R[id]).filter(r=>!isPH(r.h)&&!r.ret&&r.d<=3);")
rep("const L=G.heya.filter((h,i)=>i>0&&!h.closed&&h.ic===ic);", "const L=G.heya.filter((h,i)=>i>0&&!h.closed&&!isPH(i)&&h.ic===ic);")
rep("const L=G.heya.filter((h,i)=>i>0&&!h.closed&&h.ic===me().ic);", "const L=G.heya.filter((h,i)=>i>0&&!h.closed&&!isPH(i)&&h.ic===me().ic);")
rep("let ta=t.ta;\n if(ta==='任'){ta=(r.h!==0&&", "let ta=t.ta;\n if(ta==='任'){ta=(!isPH(r.h)&&") if "let ta=t.ta;\n if(ta==='任'){ta=(r.h!==0&&" in s else rep("if(ta==='任'){ta=(r.h!==0&&", "if(ta==='任'){ta=(!isPH(r.h)&&")
rep("if(r.mKyu===G.bnum&&r.h!==0)return true;", "if(r.mKyu===G.bnum&&!isPH(r.h))return true;")
rep("if(r.mRet&&G.bnum>=r.mRet&&r.h!==0)p=1;", "if(r.mRet&&G.bnum>=r.mRet&&!isPH(r.h))p=1;")
rep("if(r.ret){if(r.h!==0)doRetire(r);out.push(id);return false;}", "if(r.ret){if(!isPH(r.h))doRetire(r);out.push(id);return false;}")
rep("if(L.t==='Y'&&L.h!==0&&day<=12)", "if(L.t==='Y'&&!isPH(L.h)&&day<=12)")
rep("function kenPol(r){return r.h===0?(G.kpol||'nin'):'nin';}", "function kenPol(r){return isPH(r.h)?(pv(r.h,'kpol')||'nin'):'nin';}")
# spinOff:独立のもとが自分の部屋かどうか
rep("const sic=i>0&&src?src.ic:me().ic;let tt=null;if(G.toshi&&i>0&&src){", "const ai=i>0&&!isPH(i);const sic=ai&&src?src.ic:me().ic;let tt=null;if(G.toshi&&ai&&src){")
rep("ic:i>0&&src?src.ic:(me().ic>=0?me().ic:RI(0,4))", "ic:ai&&src?src.ic:(me().ic>=0?me().ic:RI(0,4))")
rep(" if(i>0){const c=G.order.filter(id=>{const r=G.R[id];return r.h===i&&", " if(ai){const c=G.order.filter(id=>{const r=G.R[id];return r.h===i&&")
rep("const k=spinOff(0,{age:s.age,name:s.myo});", "const k=spinOff(ME(),{age:s.age,name:s.myo});")
rep("(ids||[]).forEach(id=>{const r=G.R[id];if(r&&r.h===0&&!r.ret){r.h=k;}});", "(ids||[]).forEach(id=>{const r=G.R[id];if(r&&r.h===ME()&&!r.ret){r.h=k;}});")

# ---- 受け持ちの部屋(いまのプレイヤー)----
for old, new in [
 ("function chkEiy(){const r=G.chk!=null?G.R[G.chk]:null;if(!r||r.ret||r.h!==0)return 4;", "function chkEiy(){const r=G.chk!=null?G.R[G.chk]:null;if(!r||r.ret||r.h!==ME())return 4;"),
 ("function trAdd(r,d,why){r.tr=cl((r.tr==null?50:r.tr)+d,0,100);if(why&&r.h===0){", "function trAdd(r,d,why){r.tr=cl((r.tr==null?50:r.tr)+d,0,100);if(why&&isPH(r.h)){"),
 ("function isNewbie(r){if(r.h!==0||r.ret)return false;", "function isNewbie(r){if(r.h!==ME()||r.ret)return false;"),
 ("const ok=id=>G.R[id]&&!G.R[id].ret&&G.R[id].h===0;", "const ok=id=>G.R[id]&&!G.R[id].ret&&G.R[id].h===ME();"),
 ("function aniOK(r,a){return !!a&&a!==r&&a.h===0&&", "function aniOK(r,a){return !!a&&a!==r&&a.h===ME()&&"),
 ("if(a&&!a.ret&&a.h===0){d+=", "if(a&&!a.ret&&a.h===ME()){d+="),
 ("function wkgRetire(r){if(r.h!==0||", "function wkgRetire(r){if(r.h!==ME()||"),
 ("const an=G.R[x.rid];if(!an||an.ret||an.h!==0)return false;", "const an=G.R[x.rid];if(!an||an.ret||an.h!==ME())return false;"),
 ("*locF(G.heya[0]));}", "*locF(G.heya[ME()]));}"),
 ("if((sum&&sum.yu||[]).some(y=>y.h===0&&y.d<=1))d+=4;", "if((sum&&sum.yu||[]).some(y=>y.h===ME()&&y.d<=1))d+=4;"),
 ("function coMul(r){if(r.h!==0)return 1;", "function coMul(r){if(r.h!==ME())return 1;"),
 ("const r=G.R[a.r];if(!r||r.h!==0||r.ret){delete G.coAs[s.sid];return;}", "const r=G.R[a.r];if(!r||r.h!==ME()||r.ret){delete G.coAs[s.sid];return;}"),
 ("const isOwn=r.h===0;\n const gsel=", "const isOwn=r.h===ME();\n const gsel="),
 ("function hySeeO(r){if(r.h===0)", "function hySeeO(r){if(r.h===ME())"),
 ("(r.h===0?'<div class=\"ms\">'+esc(oyN())", "(r.h===ME()?'<div class=\"ms\">'+esc(oyN())"),
 ("function keyCom(r){if(r.h!==0||!r.cap)return [];", "function keyCom(r){if(r.h!==ME()||!r.cap)return [];"),
 (" if(r.h===0){let d=0;oshiItems(r)", " if(r.h===ME()){let d=0;oshiItems(r)"),
 ("function mAI(){return G.order.map(id=>G.R[id]).filter(r=>r&&!r.ret&&r.h!==0&&G.heya[r.h]);}", "function mAI(){const m=ME();return G.order.map(id=>G.R[id]).filter(r=>r&&!r.ret&&r.h!==m&&G.heya[r.h]);}"),
 ("if(!r||r.ret||r.h!==0)r=heyaTop();return r;}", "if(!r||r.ret||r.h!==ME())r=heyaTop();return r;}"),
 ("const AI=G.order.map(i=>G.R[i]).filter(x=>x&&!x.ret&&x.h>0);", "const AI=G.order.map(i=>G.R[i]).filter(x=>x&&!x.ret&&x.h!==ME());"),
 ("h:0,home:pick(REG[reg].p)", "h:ME(),home:pick(REG[reg].p)"),
 ("h:0,home:a.home", "h:ME(),home:a.home"),
 ("r.h=0;r.join=G.bnum", "r.h=ME();r.join=G.bnum"),
 ("r&&r.h===0);", "r&&r.h===ME());"),
 ("M.forEach(r=>{r.h=0;", "M.forEach(r=>{r.h=ME();"),
]:
    n = 2 if old.startswith('h:0,home:pick') else 1
    rep(old, new, n)
rep("mkNisei(k,0)", "mkNisei(k,ME())", 3)
rep("r&&!r.ret&&r.h!==0", "r&&!r.ret&&r.h!==ME()", 1)

# けが:受け持ちの部屋の力士なら、その部屋のプレイヤーとして
rep("let s=x<.55?1:x<.88?2:3;if(s===3&&r.h===0&&G.con", "let s=x<.55?1:x<.88?2:3;if(s===3&&r.h===ME()&&G.con")
rep(" if(r.h===0&&r.inj.s>=3&&!r.inj.ope&&!r.inj.cons&&!G.ev.some(e=>e.k==='ope'&&e.rid===r.id))G.ev.push({k:'ope',rid:r.id});\n if(r.h===0){addNews(r.n+'が'+src",
    " if(r.h===ME()&&r.inj.s>=3&&!r.inj.ope&&!r.inj.cons&&!G.ev.some(e=>e.k==='ope'&&e.rid===r.id))G.ev.push({k:'ope',rid:r.id});\n if(r.h===ME()){addNews(r.n+'が'+src")
rep("function injure(r,src){\n", "function injure(r,src){return inP(r.h,()=>injure0(r,src));}\nfunction injure0(r,src){\n")
rep("function heal(r){if(!r.inj)return;if(r.inj.s>=2&&!r.inj.ope)r.old[r.inj.p]=(r.old[r.inj.p]||0)+(r.inj.cons?2:1);if(r.h===0)addNews(",
    "function heal(r){if(!r.inj)return;if(r.inj.s>=2&&!r.inj.ope)r.old[r.inj.p]=(r.old[r.inj.p]||0)+(r.inj.cons?2:1);if(isPH(r.h))inP(r.h,()=>addNews(")
rep("のけがが治りました。'+(r.inj.s>=2?'(古傷として残ります)':''));r.inj=null;}", "のけがが治りました。'+(r.inj.s>=2?'(古傷として残ります)':'')));r.inj=null;}")

# 休場の判断
rep("function sitOut(r){if(r.susp>0)return true;", "function sitOut(r){return inP(r.h,()=>sitOut0(r));}\nfunction sitOut0(r){if(r.susp>0)return true;")
rep(" if(r.h===0){if((r.inj.s===2||(r.inj.s===1&&r.injPol==='休'))", " if(r.h===ME()){if((r.inj.s===2||(r.inj.s===1&&r.injPol==='休'))")

# 横綱審議委員会
rep(" if(r.yc===4&&r.h===0)addNews(", " if(r.yc===4&&isPH(r.h))inP(r.h,()=>addNews(")
rep("に「激励」を決議しました。');\n if(r.yc===6)", "に「激励」を決議しました。'));\n if(r.yc===6)")
rep(" if(r.yc>=7){if(r.h===0){if(!G.ev.some(e=>e.k==='yokoshin'))G.ev.push({k:'yokoshin',rid:r.id});return 0;}return .5;}return 0;}",
    " if(r.yc>=7){if(isPH(r.h)){inP(r.h,()=>{if(!G.ev.some(e=>e.k==='yokoshin'))G.ev.push({k:'yokoshin',rid:r.id});});return 0;}return .5;}return 0;}")

# 二世の子・引退
rep("function kidRoll(r){\n if(r.best<42&&G.kids.length<80&&Math.random()<(r.h===0?.25:.08)){\n  G.kids.push({f:r.n,g:r.nisei?{f:r.nisei.f,br:r.nisei.br}:null,own:r.h===0,",
    "function kidRoll(r){\n if(r.best<42&&G.kids.length<80&&Math.random()<(isPH(r.h)?.25:.08)){\n  G.kids.push({f:r.n,g:r.nisei?{f:r.nisei.f,br:r.nisei.br}:null,own:isPH(r.h),oh:r.h,")
rep("  if(r.h===0)addNews(r.n+'には、まだ幼い息子さんがいるそうです。');}}", "  if(isPH(r.h))inP(r.h,()=>addNews(r.n+'には、まだ幼い息子さんがいるそうです。'));}}")
rep("  if(k.own)G.ev.push({k:'nisei',kid:k});", "  if(k.own)inP(k.oh==null?0:k.oh,()=>G.ev.push({k:'nisei',kid:k}));")
rep("function doRetire(r,why){\n", "function doRetire(r,why){return inP(r.h,()=>doRetire0(r,why));}\nfunction doRetire0(r,why){\n")
rep("sansho:r.sansho,kin:r.kin,own:r.h===0};", "sansho:r.sansho,kin:r.kin,own:isPH(r.h),oh:r.h};")
rep(" if(r.h!==0&&myoOK(r)&&(!r.fr||r.nat)){G.myoQ=", " if(!isPH(r.h)&&myoOK(r)&&(!r.fr||r.nat)){G.myoQ=")
rep(" if(r.h===0){\n  let msg=r.n+'('+bestRank(r)+')が引退しました。'", " if(r.h===ME()){\n  let msg=r.n+'('+bestRank(r)+')が引退しました。'")

# 引退の確認:力士ごとに、その部屋のプレイヤーとして
rep(" G.order.forEach(id=>{const r=G.R[id];const rc=B.rec[id];const mk=rc.w<(rc.l+rc.ab);let p=0;\n  if(r.t==='Y'){",
    " G.order.forEach(id=>{const r=G.R[id];inP(r.h,()=>{const rc=B.rec[id];const mk=rc.w<(rc.l+rc.ab);let p=0;\n  if(r.t==='Y'){")
rep(" if(r.h===0){\n   if(r.age>=40)p=1;\n   if(p>=1){doRetire(r,'年齢の限界');return;}\n   if(Math.random()<p*.8&&!r.stay)G.ev.push({k:'retire',rid:r.id});\n   r.stay=false;\n  }else if(Math.random()<p)r.ret=true;\n });\n}",
    " if(r.h===ME()){\n   if(r.age>=40)p=1;\n   if(p>=1){doRetire(r,'年齢の限界');return;}\n   if(Math.random()<p*.8&&!r.stay)G.ev.push({k:'retire',rid:r.id});\n   r.stay=false;\n  }else if(Math.random()<p)r.ret=true;\n });});\n}")

# 大器晩成
rep("function daiki(){G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret||r.daiki||r.d<=1||r.age>24||!r.cap)return;const pt=potOf(r);if(pt>=13.5)return;",
    "function daiki(){G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret||r.daiki||r.d<=1||r.age>24||!r.cap)return;inP(r.h,()=>{const pt=potOf(r);if(pt>=13.5)return;")
rep("*(r.h===0?(.85+.1*((G.fac&&G.fac.keiko)||1)):1)*(pt>=11?.45:1);", "*(r.h===ME()?(.85+.1*((G.fac&&G.fac.keiko)||1)):1)*(pt>=11?.45:1);")
rep(" if(r.h===0){const co=G.staff.find(x=>x.role==='co');addNews((co?co.n+'(部屋付き親方)':me().o.replace(/[((].*$/,'')+'親方')+'「'+r.n+'が稽古で急に力をつけてきた。大器晩成かもしれない」');}});}",
    " if(r.h===ME()){const co=G.staff.find(x=>x.role==='co');addNews((co?co.n+'(部屋付き親方)':me().o.replace(/[((].*$/,'')+'親方')+'「'+r.n+'が稽古で急に力をつけてきた。大器晩成かもしれない」');}});});}")

# ---- 1 週間 ----
rep("""function doWeek(){
 if(G.phase!=='train')return;
 mWeek();oshiWeek();coWeek();
 G._tr=G.wk===TOURWK?tourSet():null;
 tkAssign();aniAssign();G._me=new Set(meList());
 const H0=heyaH(ME());const HA={};
 G.order.forEach(id=>{const r=G.R[id];if(r.h===0)weekR(r,H0);else{if(!HA[r.h])HA[r.h]=heyaH(r.h);weekR(r,HA[r.h]);}});
 G.pend.forEach(id=>weekR(G.R[id],H0));
 shiteiWeek();
 tourEnd();
 scoutWeek(H0);G.tmp.away=0;
 G.wn++;G.wk++;""",
"""function doWeek(){
 if(G.phase!=='train')return;
 const HP={};
 forP(()=>{mWeek();oshiWeek();coWeek();
  G._tr=G.wk===TOURWK?tourSet():null;
  tkAssign();aniAssign();G._me=new Set(meList());
  HP[ME()]=heyaH(ME());});
 const HA={};
 G.order.forEach(id=>{const r=G.R[id];if(HP[r.h])inP(r.h,()=>weekR(r,HP[r.h]));else{if(!HA[r.h])HA[r.h]=heyaH(r.h);weekR(r,HA[r.h]);}});
 forP(()=>{const H0=HP[ME()];
  G.pend.forEach(id=>weekR(G.R[id],H0));
  shiteiWeek();
  tourEnd();
  scoutWeek(H0);G.tmp.away=0;});
 G.wn++;G.wk++;""")
rep(" if(G.wk>WEEKS){G.tmp.chanko=0;startBasho();}\n}", " if(G.wk>WEEKS){forP(()=>{G.tmp.chanko=0;});startBasho();}\n}")

# ---- 本場所の始まり ----
rep("""  if(sitOut(r)){rec.ky=true;days.forEach(x=>rec.res[x-1]={r:'や'});}
  if(r.h===0)peak(r);
  {const u=Math.random();const lh=r.hist&&r.hist.length?r.hist[r.hist.length-1]:null;const pa=lh&&lh.d===0&&lh.w>=10?.15:.06;r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);if(r.h===0&&r.d<=1&&coL('seki').length)r.bfm*=.6;if(r.iki>0){r.bfm+=.015;r.iki--;}}
  {const z=bzCalc(r);r.bzf=z.v;r.bzn=z.note||'';}
  B.rec[id]=rec;});""",
"""  inP(r.h,()=>{
  if(sitOut(r)){rec.ky=true;days.forEach(x=>rec.res[x-1]={r:'や'});}
  if(r.h===ME())peak(r);
  {const u=Math.random();const lh=r.hist&&r.hist.length?r.hist[r.hist.length-1]:null;const pa=lh&&lh.d===0&&lh.w>=10?.15:.06;r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);if(r.h===ME()&&r.d<=1&&coL('seki').length)r.bfm*=.6;if(r.iki>0){r.bfm+=.015;r.iki--;}}
  {const z=bzCalc(r);r.bzf=z.v;r.bzn=z.note||'';}});
  B.rec[id]=rec;});""")
rep(""" const kys=own().filter(r=>B.rec[r.id].ky);
 {const hot=""", """ forP(()=>{const kys=own().filter(r=>B.rec[r.id].ky);
 {const hot=""")
rep(" G.ev.filter(e=>TRAINEV.includes(e.k)).forEach(e=>resolveEv(e.id,e.k==='kaimei'?(EVT.kaimei.c(e).length-1):0));\n}",
    " G.ev.filter(e=>TRAINEV.includes(e.k)).forEach(e=>resolveEv(e.id,e.k==='kaimei'?(EVT.kaimei.c(e).length-1):0));});\n}")

# ---- 一番 ----
rep(" const show=A.h===0||Bq.h===0||(A.d===0", " const show=isPH(A.h)||isPH(Bq.h)||(A.d===0")
rep("tA:A.h===0?B.tac[a]:null,tB:Bq.h===0?B.tac[b]:null", "tA:isPH(A.h)?B.tac[a]:null,tB:isPH(Bq.h)?B.tac[b]:null")
rep("B.kin.push([W.id,L.id,day]);if(W.h===0)achieve('kin','初の金星');}", "B.kin.push([W.id,L.id,day]);if(isPH(W.h))inP(W.h,()=>achieve('kin','初の金星'));}")
rep(" [W,L].forEach(r=>{if(r.h===0||r.d<=1){const o=r===W?L:W;if(r.h===0||o.d<=1){", " [W,L].forEach(r=>{if(isPH(r.h)||r.d<=1){const o=r===W?L:W;if(isPH(r.h)||o.d<=1){")
rep(" if(W.h===0){W.km=W.km||{};", " if(isPH(W.h)){W.km=W.km||{};")
rep(" if(f.hv&&W.h===0&&W.d<=1){G.rep=Math.max(0,G.rep-.4);}", " if(f.hv&&isPH(W.h)&&W.d<=1){inP(W.h,()=>{G.rep=Math.max(0,G.rep-.4);});}")
rep("""(f.hard?1.4:1)*(r.h===0?heyaH0().injMul:1);
  if(r.inj&&Math.random()<.05){r.inj.s=Math.min(3,r.inj.s+1);r.inj.wk+=RI(2,5);if(r.h===0)addNews(r.n+'は'+r.inj.p+'のけがを悪化させました。');if(sitOut(r))goKyujo(r,day);}
  else if(Math.random()<pr){injure(r,day+'日目の取組');if(sitOut(r)){goKyujo(r,day);if(r.h===0)addNews(r.n+'('+r.rk+')は'+(day+1)+'日目から休場します。');}}});""",
"""(f.hard?1.4:1)*(isPH(r.h)?inP(r.h,()=>heyaH0().injMul):1);
  if(r.inj&&Math.random()<.05){r.inj.s=Math.min(3,r.inj.s+1);r.inj.wk+=RI(2,5);if(isPH(r.h))inP(r.h,()=>addNews(r.n+'は'+r.inj.p+'のけがを悪化させました。'));if(sitOut(r))goKyujo(r,day);}
  else if(Math.random()<pr){injure(r,day+'日目の取組');if(sitOut(r)){goKyujo(r,day);if(isPH(r.h))inP(r.h,()=>addNews(r.n+'('+r.rk+')は'+(day+1)+'日目から休場します。'));}}});""")
rep("W.rare[f.k]=(W.rare[f.k]||0)+1;if(W.h===0||(W.d===0&&L.d===0))addNews((W.h===0?'':'幕内で')+W.n+'が珍しい決まり手「'+f.k+'」で'+L.n+'を破りました。館内が大きくどよめきました。');}",
    "W.rare[f.k]=(W.rare[f.k]||0)+1;const rt=W.n+'が珍しい決まり手「'+f.k+'」で'+L.n+'を破りました。館内が大きくどよめきました。';if(isPH(W.h))inP(W.h,()=>addNews(rt));else if(W.d===0&&L.d===0)addNews('幕内で'+rt);}")

# ---- 本場所の終わり ----
rep("G.yusho.push({b:G.bnum,d:d,n:r.n,hn:G.heya[r.h].n,rk:r.rk,w:rc.w,l:rc.l+rc.ab,own:r.h===0});\n  if(r.h===0){achieve('yu'+d,DN[d]+'優勝');addNews('🏆 '+r.n+'が'+DN[d]+'優勝!('+rc.w+'勝'+(rc.l+rc.ab)+'敗)');}",
    "G.yusho.push({b:G.bnum,d:d,n:r.n,hn:G.heya[r.h].n,rk:r.rk,w:rc.w,l:rc.l+rc.ab,own:isPH(r.h),oh:r.h});\n  if(isPH(r.h))inP(r.h,()=>{achieve('yu'+d,DN[d]+'優勝');addNews('🏆 '+r.n+'が'+DN[d]+'優勝!('+rc.w+'勝'+(rc.l+rc.ab)+'敗)');});")
rep("sum.sansho.push({id:id,n:r.n,h:r.h,t:t,rk:r.rk});if(r.h===0){achieve('sansho','三賞受賞');addNews(r.n+'が'+t+'を受賞しました。');}});",
    "sum.sansho.push({id:id,n:r.n,h:r.h,t:t,rk:r.rk});if(isPH(r.h))inP(r.h,()=>{achieve('sansho','三賞受賞');addNews(r.n+'が'+t+'を受賞しました。');});});")
rep("  if(r.hist.length>(r.h===0?150:6))r.hist.shift();", "  if(r.hist.length>(isPH(r.h)?150:6))r.hist.shift();")
rep("  if(r.h===0)sum.own.push({id:id,n:r.n,rk:r.rk,w:rc.w,l:rc.l,ab:rc.ab,kk:kk});", "  if(isPH(r.h))sum.own.push({id:id,n:r.n,rk:r.rk,w:rc.w,l:rc.l,ab:rc.ab,kk:kk,h:r.h});")
rep(" G.pend.forEach(id=>{G.R[id].mz=G.bnum;});\n popUpdate(B,sum);heyaScore(B,sum);sum.fin=finance(B,sum);\n let rg=0;own().forEach(r=>{rg+=[0,0,.6,1.2,2,3,4][rankLv(r)];});\n sum.yu.forEach(y=>{if(y.h===0)rg+=[10,4,2,1,1,1][y.d];});\n sum.sansho.forEach(s=>{if(s.h===0)rg+=2;});\n G.rep=cl(G.rep*.93+rg,0,100);\n G.sup=Math.max(30,Math.round(G.sup+cl((80+G.rep*14-G.sup)*.08,-25,40)+randn()*3));G.sup+=sum.psup||0;\n v7Basho(sum);\n v8Basho(sum);\n payBasho(sum);\n v12Basho(sum);\n v13Basho(sum);\n v14Basho(sum);\n v15Basho(sum);\n amaBasho();\n retireCheck();\n kidsDue();\n genEvents();\n refreshMarket();\n refreshMyo();\n const keep={};G.order.forEach(id=>{const r=G.R[id];if(r.h===0||r.d<=1)keep[id]=B.rec[id];});",
    " forP(()=>{G.pend.forEach(id=>{G.R[id].mz=G.bnum;});\n popUpdate(B,sum);});heyaScore(B,sum);\n forP(()=>{const F=finance(B,sum);if(!G.P||G.PA===0)sum.fin=F;\n let rg=0;own().forEach(r=>{rg+=[0,0,.6,1.2,2,3,4][rankLv(r)];});\n sum.yu.forEach(y=>{if(y.h===ME())rg+=[10,4,2,1,1,1][y.d];});\n sum.sansho.forEach(s=>{if(s.h===ME())rg+=2;});\n G.rep=cl(G.rep*.93+rg,0,100);\n G.sup=Math.max(30,Math.round(G.sup+cl((80+G.rep*14-G.sup)*.08,-25,40)+randn()*3));G.sup+=(G._psup||0);});\n v7Basho(sum);\n v8Basho(sum);\n payBasho(sum);\n v12Basho(sum);\n forP(()=>{v13Basho(sum);\n v14Basho(sum);});\n v15Basho(sum);\n amaBasho();\n retireCheck();\n kidsDue();\n forP(()=>{genEvents();\n refreshMarket();\n refreshMyo();});\n const keep={};G.order.forEach(id=>{const r=G.R[id];if(isPH(r.h)||r.d<=1)keep[id]=B.rec[id];});")
# 人気:プレイヤーごと(後援会の上乗せはそのプレイヤーの分)
rep(" G.popS=mx;sum.psup=Math.round(ps/200);}", " G.popS=mx;G._psup=Math.round(ps/200);if(!G.P||G.PA===0)sum.psup=G._psup;}")
rep("'_tr','dok','subX'];", "'_tr','dok','subX','_psup'];")
# 部屋番付:年間評価はプレイヤーごと
rep("""  const o=hs.yr.map((v,i)=>[i,v]).filter(x=>!G.heya[x[0]].closed).sort((a,b)=>b[1]-a[1]||a[0]-b[0]);const rk=o.findIndex(x=>x[0]===0)+1;
  const gi=rk<=3?0:rk<=10?1:rk<=25?2:3;const gn='SABC'[gi];
  const sub=[300,150,60,0][gi];G.rep=cl(G.rep+[3,1.5,0,-1.5][gi],0,100);
  if(sub){sum.sub=sub;sum.subg=gn;}
  G.yr.push({y:Math.floor((G.bnum-1)/6)+1,rk:rk,g:gn,pts:Math.round(hs.yr[0]),""",
"""  const o=hs.yr.map((v,i)=>[i,v]).filter(x=>!G.heya[x[0]].closed).sort((a,b)=>b[1]-a[1]||a[0]-b[0]);
  forP(()=>{const m=ME();const rk=o.findIndex(x=>x[0]===m)+1;
  const gi=rk<=3?0:rk<=10?1:rk<=25?2:3;const gn='SABC'[gi];
  const sub=[300,150,60,0][gi];G.rep=cl(G.rep+[3,1.5,0,-1.5][gi],0,100);
  G.subX=sub?{b:G.bnum,sub:sub,subg:gn}:null;if(sub&&(!G.P||G.PA===0)){sum.sub=sub;sum.subg=gn;}
  G.yr.push({y:Math.floor((G.bnum-1)/6)+1,rk:rk,g:gn,pts:Math.round(hs.yr[m]),""")
rep("  addNews('年間評価:部屋は '+o.length+' 部屋中 '+rk+' 位(評価 '+gn+')。'+(sub?'協会から助成金 '+man(sub)+'。':''));\n  hs.yr=Array(G.heya.length).fill(0);}}",
    "  addNews('年間評価:部屋は '+o.length+' 部屋中 '+rk+' 位(評価 '+gn+')。'+(sub?'協会から助成金 '+man(sub)+'。':''));});\n  hs.yr=Array(G.heya.length).fill(0);}}")
# 収支:プレイヤーごと
rep(" let yu=0;sum.yu.forEach(y=>{if(y.h===0)yu+=[400,80,20,10,10,10][y.d];});sum.sansho.forEach(s=>{if(s.h===0)yu+=60;});",
    " let yu=0;sum.yu.forEach(y=>{if(y.h===ME())yu+=[400,80,20,10,10,10][y.d];});sum.sansho.forEach(s=>{if(s.h===ME())yu+=60;});")
rep(" if(sum.sub)F.in.push(['協会の助成金(年間評価 '+sum.subg+')',sum.sub]);\n const kinI=sum.kin.filter(k=>G.R[k[0]].h===0).length*30;",
    " {const X=G.subX&&G.subX.b===G.bnum?G.subX:null;if(X)F.in.push(['協会の助成金(年間評価 '+X.subg+')',X.sub]);}\n const kinI=sum.kin.filter(k=>G.R[k[0]].h===ME()).length*30;")
# 信頼・おかみさん・役職・不祥事はプレイヤーごと、ほかの部屋の不祥事は世界で 1 回
rep("function v7Basho(sum){\n const ok=G.okami;", "function v7Basho(sum){forP(()=>v7P(sum));v7W(sum);}\nfunction v7P(sum){\n const ok=G.okami;")
rep("    G.ev.push({k:'scand',rid:r.id,tp:wpick(w)});break;}}}\n // ほかの部屋の不祥事\n", "    G.ev.push({k:'scand',rid:r.id,tp:wpick(w)});break;}}}}\nfunction v7W(sum){\n // ほかの部屋の不祥事\n")
# 親方の世代交代・部屋の閉鎖は世界、自分の部屋の部屋付き親方の独立はプレイヤーごと
rep(" // 自部屋の部屋付き親方の独立\n if(!G.ev.some(e=>e.k==='dokuritsu')){", " // 自部屋の部屋付き親方の独立\n forP(()=>{if(!G.ev.some(e=>e.k==='dokuritsu')){")
rep("G.ev.push({k:'dokuritsu',sid:s.sid,ids:L});break;}}}\n}", "G.ev.push({k:'dokuritsu',sid:s.sid,ids:L});break;}}}});\n}")
# 年寄の名簿:受け持ちの部屋の親方は、その部屋のプレイヤーとして
rep("  if(hi===0){if(t.shi){if((me().gen||1)!==(t.gen0||1)||a>=70){t.shi=0;if(a>=70||Math.random()<.5){t.left=G.bnum;}else t.post='参与';}return;}\n   if(!t.nost&&!G.staff.some(x=>x.tid===k))t.left=G.bnum;else if(t.nost&&a>=70)t.left=G.bnum;return;}\n  if(a>=70&&!(t.shi&&hi>0)){",
    "  if(isPH(hi)){inP(hi,()=>{if(t.shi){if((me().gen||1)!==(t.gen0||1)||a>=70){t.shi=0;if(a>=70||Math.random()<.5){t.left=G.bnum;}else t.post='参与';}return;}\n   if(!t.nost&&!G.staff.some(x=>x.tid===k))t.left=G.bnum;else if(t.nost&&a>=70)t.left=G.bnum;});return;}\n  if(a>=70&&!(t.shi&&hi>0)){")
# 給金:プレイヤーの部屋の力士の分は、その部屋のプレイヤーとして
rep("  if(r.h!==0)return;\n  if(r.kyo>0)r.kyo--;", "  if(!isPH(r.h))return;inP(r.h,()=>{\n  if(r.kyo>0)r.kyo--;")
rep("r.inc={sal:sal,hos:Math.round(hos*10)/10,te:te,kn:kn,tot:Math.round(inc)};});}", "r.inc={sal:sal,hos:Math.round(hos*10)/10,te:te,kn:kn,tot:Math.round(inc)};});});}")
# 角界の出来事:人気・無観客は世界、記者の記事・後援会・海外巡業はプレイヤーごと
rep("function v12Basho(sum){kiNews();", "function v12Basho(sum){forP(()=>kiNews());")
rep(" G.sup=Math.max(30,Math.round(G.sup*(1+(G.boom-1)*.02)));\n", " forP(()=>{G.sup=Math.max(30,Math.round(G.sup*(1+(G.boom-1)*.02)));});\n")
rep(" if(b===4&&Math.random()<.3){const sk=own().filter(r=>r.d<=1);", " if(b===4&&Math.random()<.3)forP(()=>{const sk=own().filter(r=>r.d<=1);")
rep("部屋の関取 '+sk.length+' 人が参加し、相撲の魅力を海外に伝えました。');}}\n}", "部屋の関取 '+sk.length+' 人が参加し、相撲の魅力を海外に伝えました。');}});\n}")
# 名跡:預かっている名跡の返還はプレイヤーごと
rep(" (G.myoL||[]).filter(m=>m.rent).forEach(m=>{if(Math.random()<.02&&!G.ev.some(e=>e.k==='myoBack'))G.ev.push({k:'myoBack',n:m.n});});\n}",
    " forP(()=>{(G.myoL||[]).filter(m=>m.rent).forEach(m=>{if(Math.random()<.02&&!G.ev.some(e=>e.k==='myoBack'))G.ev.push({k:'myoBack',n:m.n});});});\n}")
# アマチュア:大会で注目の選手はプレイヤーごとの候補へ、卒業生は先に声をかけたプレイヤーへ
rep("  sc.slice(0,4).forEach(([a])=>{const last=a.kind==='高'?a.yr>=3:a.kind==='大'?a.yr>=4:true;if(last&&!G.pros.some(p=>p.amaId===a.id)&&G.pros.length<18){const p=prosFromAma(a,'大会で注目');p.amaId=a.id;viewPros(p,6);G.pros.push(p);}});});",
    "  sc.slice(0,4).forEach(([a])=>{const last=a.kind==='高'?a.yr>=3:a.kind==='大'?a.yr>=4:true;forP(()=>{if(last&&!G.pros.some(p=>p.amaId===a.id)&&G.pros.length<18){const p=prosFromAma(a,'大会で注目');p.amaId=a.id;viewPros(p,6);G.pros.push(p);}});});});")
rep("  grad.forEach(a=>{G.ama=G.ama.filter(x=>x!==a);if(G.pros.some(p=>p.amaId===a.id)){mAmaFate(a,'pros');return;}let fate='quit';",
    "  grad.forEach(a=>{G.ama=G.ama.filter(x=>x!==a);if(allPK('pros').some(p=>p.amaId===a.id)){mAmaFate(a,'pros');return;}let fate='quit';")
rep("   if(Math.random()<pro){const p=prosFromAma(a,'卒業後に入門');p.amaId=a.id;\n    if(G.pros.length<18&&((G.rel[a.sch]||0)>=25||Math.random()<.25)){p.src=(G.rel[a.sch]||0)>=25?'監督の紹介':'卒業後に入門';viewPros(p,6);G.pros.push(p);fate='pros';}\n    else{",
    "   if(Math.random()<pro){const p=prosFromAma(a,'卒業後に入門');p.amaId=a.id;\n    forP(()=>{if(fate!=='pros'&&G.pros.length<18&&((G.rel[a.sch]||0)>=25||Math.random()<.25)){p.r.h=ME();p.src=(G.rel[a.sch]||0)>=25?'監督の紹介':'卒業後に入門';viewPros(p,6);G.pros.push(p);fate='pros';}});\n    if(fate!=='pros'){")
rep(" for(const k in G.rel)G.rel[k]=Math.max(0,G.rel[k]-.7);}", " forP(()=>{for(const k in G.rel)G.rel[k]=Math.max(0,G.rel[k]-.7);});}")
# 番付:新弟子の初土俵はプレイヤーごと
rep(" // 新弟子(付出し・前相撲を終えた者)\n const stay=[];\n G.pend.forEach(", " // 新弟子(付出し・前相撲を終えた者)\n forP(()=>{const stay=[];\n G.pend.forEach(")
rep("  else stay.push(id);});\n G.pend=stay;\n", "  else stay.push(id);});\n G.pend=stay;});\n")

# ---- 次の場所へ ----
rep("function nextCycle(){\n if(G.ev.length)return false;", "function nextCycle(){\n if(anyEv())return false;")
rep(""" me().age=(me().age||40)+1/6;G.staff.forEach(s=>{s.age+=1/6;});
 G.staff.filter(s=>s.role==='co'&&s.age>=70).forEach(s=>{if(s.myo){const m=G.myoL.find(x=>x.h===s.sid);if(m)m.h=0;}addNews(s.n+'(部屋付き親方)が 70 歳で退職しました。');});
 G.staff=G.staff.filter(s=>!(s.role==='co'&&s.age>=70));
 const msgs=[];
 own().forEach(r=>{""",
""" G.order.forEach(id=>{const r=G.R[id];const o=old[id];if(o&&r.d<=1&&o.d>1&&!r.sekD){r.sekD=G.bnum;G.sekLog.push({b:G.bnum,s:r.uni||r.hs||'',k:r.fr?'海外':r.uni?'大学':r.hs?'高校':(r.kind||'')});}});if(G.sekLog.length>400)G.sekLog.splice(0,G.sekLog.length-400);if(G.bnum%6===1)schRecalc();
 forP(()=>{
 me().age=(me().age||40)+1/6;G.staff.forEach(s=>{s.age+=1/6;});
 G.staff.filter(s=>s.role==='co'&&s.age>=70).forEach(s=>{if(s.myo){const m=G.myoL.find(x=>x.h===s.sid);if(m)m.h=0;}addNews(s.n+'(部屋付き親方)が 70 歳で退職しました。');});
 G.staff=G.staff.filter(s=>!(s.role==='co'&&s.age>=70));
 const msgs=[];
 own().forEach(r=>{""")
rep(""" G.order.forEach(id=>{const r=G.R[id];const o=old[id];if(o&&r.d<=1&&o.d>1&&!r.sekD){r.sekD=G.bnum;G.sekLog.push({b:G.bnum,s:r.uni||r.hs||'',k:r.fr?'海外':r.uni?'大学':r.hs?'高校':(r.kind||'')});}});if(G.sekLog.length>400)G.sekLog.splice(0,G.sekLog.length-400);if(G.bnum%6===1)schRecalc();
 G.news=msgs;msgs.forEach(m=>addNews(m));
 addNews(bname(G.bnum)+'の番付が発表されました。稽古期間(6 週)に入ります。');
 if(G.money<-2000)G.over=true;
 return true;""",
""" G.news=msgs;msgs.forEach(m=>addNews(m));});
 addNews(bname(G.bnum)+'の番付が発表されました。稽古期間(6 週)に入ります。');
 forP(()=>{if(G.money<-2000)G.over=true;});
 return true;""")
rep(" mCycle(old);\n G.bnum++;", " forP(()=>mCycle(old));\n G.bnum++;")

# ---- プレイヤーを足す(二人相撲の子など。第 2 歩で画面とつなぐ)----
rep("function finInit(g,start){const X=g||G;const hf=HFIN[X.heya[0].n];", "function finInit(g,start){const X=g||G;const hf=HFIN[X.heya[ME()].n];")
rep("const t=X.toshi?X.toshi.find(x=>x.shi&&x.heya===X.heya[0].n):null;const mb=", "const t=X.toshi?X.toshi.find(x=>x.shi&&x.heya===X.heya[ME()].n):null;const mb=")
rep("/* 部屋付き親方として独立する(v43)。", """/* v89:プレイヤーを足す(二人相撲の子など)。ほかの部屋 h を受け持ちの部屋にする。
   始めのお金・施設・後援会・部屋付き親方は、実在の部屋で始めるときと同じ決め方(newGameReal と同じ式) */
function pDef(){return {oshi:null,supC:3,chi:{1:30,3:30,5:30},bld:{k:'rent'},yfin:[],yacc:{i:0,o:0},jin:50,meSel:{auto:1,ids:[]},late:[],st16:{join:0,early:0,yame:0,hide:0,ijime:0},meal:{k:'ソップ',a:1,t:2,ex:0},con:{gym:0,clinic:0,diet:0},chk:null,rel:{},tkPol:'old',post:0,postT:0,scl:[],okamiUsed:false,okami:null,yr:[],intv:[],myoL:[],myoM:[],tourPol:1,tourTsuki:0,money:1500,rep:20,sup:120,fac:{keiko:1,iryo:1,shoku:1,shuku:2},log:[],ach:[],pend:[],staff:[],market:[],pros:[],fin:null,acc:{dek:0,med:0,sc:0,tourIn:0,tourOut:0},ev:[],news:[],over:false,tmp:{chanko:0},mh:[]};}
function addPlayer(h){
 if(!G||!G.heya[h]||G.heya[h].closed)return -1;
 if(!G.P){G.P=[{h:0}];G.PA=0;}
 if(isPH(h))return pI(h);
 const H=G.heya[h];const RH=(typeof REALH!=='undefined')?REALH.find(x=>x[0]===H.n):null;
 const oyT=RH&&OYAB[RH[5]]?RH[5]:pick(Object.keys(OYAB));
 H.player=true;H.oyT=oyT;H.oy=Object.assign({},OYAB[oyT]);
 if(RH&&RH[4]){const b=RH[4]==='Y'?1.5:.8;for(const k in H.oy)H.oy[k]=Math.round(H.oy[k]+b);}
 H.o=H.n+'(元・'+(H.o2||(RH?RH[2]:'')||'')+')';H.pre=RH?RH[6]:H.n.slice(0,1);H.age=H.oa||(RH?RH[3]:50);H.gen=H.gen||1;
 G.P.push({h:h});const k=G.P.length-1;
 inP(h,()=>{Object.assign(G,pDef());
  const o=own();o.forEach(r=>{r.kn=Math.max(r.kn||0,40);r.menu=r.menu||'申';if(r.it==null)r.it=1;if(r.tr==null)r.tr=55;r.sh=r.sh||'普';r.trl=r.trl||[];if(r.pop==null)r.pop=20;
   if(r.cash==null)r.cash=r.d<=1?Math.round(R(300,1500)):Math.round(R(5,60));});
  const sek=o.filter(r=>r.d<=1).length;
  const rf=realFac(H.n,sek,o.length,'B',H.age);G.fac=Object.assign({},rf.f);G.capB=Math.max(0,o.length+3-(4+3*G.fac.shuku));
  G.money=1500+o.length*40;G.sup=100+o.length*12+sek*60;G.supC=Math.round(2+o.length/3+sek*4);G.bld={k:rf.b};
  G.rep=cl(20+sek*5+(o.some(r=>r.t==='Y')?15:0)+(o.some(r=>r.t==='O')?8:0),0,90);
  G.staff.push(mkStaff('sc',8));
  if(G.toshi)G.toshi.forEach((t,j)=>{if(t.left||t.heya!==H.n)return;
   if(t.shi){H.age=ageOf(t.b);t.gen0=H.gen||1;G.post=postLv(t.post);G.mePost=t.post;return;}
   const sf=staffFromToshi(t,j);G.staff.push(sf);G.myoL.push({n:t.n,h:sf.sid});if(G.myo&&G.myo[t.n])G.myo[t.n].st='own';});
  o.forEach(r=>{[r.hs,r.uni].forEach(n=>{if(n&&schOf(n))G.rel[n]=Math.min(80,(G.rel[n]||20)+15);});});
  SCH.slice().sort(()=>Math.random()-.5).slice(0,4).forEach(x=>{if(G.rel[x[0]]==null)G.rel[x[0]]=RI(5,20);});
  if(G.real)finInit(G,true);
  refreshMarket();refreshMyo();G.okami=mkOkami();
  for(let i=0;i<3;i++){const p=mkProspect(-1);viewPros(p,9);G.pros.push(p);}
  addNews(H.n+'部屋を受け持ちます。弟子 '+o.length+' 人(関取 '+sek+' 人)、部屋付き親方 '+G.staff.filter(x=>x.role==='co').length+' 人。資金 '+man(G.money)+'。');});
 return k;}
/* 部屋付き親方として独立する(v43)。""")

# ---- 画面(見ている人の部屋)----
gi = s.find('/* ========== 画面')
head, ui = s[:gi], s[gi:]
mp = ui.find('/* v80:二人相撲')
uiA, uiB = ui[:mp], ui[mp:]
n1 = len(re.findall(r'\.h===0\b', uiA)); n2 = len(re.findall(r'\.h!==0\b', uiA))
uiA = re.sub(r'\.h===0\b', '.h===ME()', uiA); uiA = re.sub(r'\.h!==0\b', '.h!==ME()', uiA)
print('画面の置きかえ', n1, n2)
s = head + uiA + uiB
rep("const rk=o.findIndex(x=>x[0]===0)+1;\n  return '<h3>'+lab+'(自部屋 '+rk+' 位)</h3><table class=\"tb\">'+o.slice(0,10).map((x,j)=>'<tr class=\"'+(x[0]===0?'me':'')+'\">",
    "const m=ME();const rk=o.findIndex(x=>x[0]===m)+1;\n  return '<h3>'+lab+'(自部屋 '+rk+' 位)</h3><table class=\"tb\">'+o.slice(0,10).map((x,j)=>'<tr class=\"'+(x[0]===m?'me':'')+'\">")
rep("esc(G.heya[0].n)+'</td><td class=\"num\">'+Math.round(arr[0])", "esc(G.heya[m].n)+'</td><td class=\"num\">'+Math.round(arr[m])")
rep("'<tr class=\"clk'+(i===0?' me':'')+'\"", "'<tr class=\"clk'+(i===ME()?' me':'')+'\"")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
