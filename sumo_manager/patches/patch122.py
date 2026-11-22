# v119:稽古の見直し(実際の稽古に合わせる)。v118 → v119
#  1 朝の基礎運動(四股・すり足・てっぽう)はどの稽古でも毎日する  2 朝の筋トレを外す(午後とジムだけ)
#  3 出稽古:時期(場所前 2 週)・相手の部屋(同じ一門、関取の数)・小さな部屋ほど効く・費用 1 万円(推定)
#  4 巡業:春 4 週・夏 4 週・秋 3 週・冬 2 週(初場所・夏場所のあとはなし)。ほかの部屋の関取も巡業へ
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=118;\nconst SAVE='sumoManager118',SAVE117", "const APPV=119;\nconst SAVE='sumoManager119',SAVE118='sumoManager118',SAVE117")
rep('[SAVE117,SAVE116', '[SAVE118,SAVE117,SAVE116')
rep('<title>Grand Sumo Manager v118','<title>Grand Sumo Manager v119')
# 稽古の名前・説明
rep(" 基:{n:'四股・てっぽう',"," 基:{n:'基礎だけ(四股・すり足・てっぽう)',")
rep("d:'体の土台。柔軟性・筋力・我慢強さ。けがをしにくい'}","d:'相撲を取らず、基礎運動だけをじっくり。柔軟性・筋力・腰の重さ。けがをしにくい'}")
rep(" 筋:{n:'筋力トレーニング',w:"," 筋:{hide:1,n:'筋力トレーニング',w:")
rep("d:'よその部屋へ。伸びは大きいがけがも多い(1 人 1 週 4 万円)'}","d:'よその部屋へ(同じ一門)。相手の部屋の関取が多いほど伸び、場所前の 2 週がいちばん効く。けがも多い(1 人 1 週 1 万円)'}")
rep("const TOURWK=4;","""const TOURWK=4;
/* v119 巡業の暦:次の場所の月 → [始まりの週, 終わりの週, 名前]。春巡業(3 月末〜4 月下旬)・夏巡業(8 月、28 日間)・秋巡業(10 月)・冬巡業(12 月)。週数は日程からの推定 */
const TOURW={5:[1,4,'春巡業'],9:[1,4,'夏巡業'],11:[1,3,'秋巡業'],1:[1,2,'冬巡業']};
function tourInfo(){return TOURW[MONTH[(G.bnum-1)%6]]||null;}
function tourWk(){const t=tourInfo();return G.phase==='train'&&!!t&&G.wk>=t[0]&&G.wk<=t[1];}
function MKEYS(){return Object['keys'](MENU).filter(k=>!MENU[k].hide);}
/* 出稽古先:同じ一門(一門がなければ全部)のほかの部屋。関取の数が多いほど効く */
function dekList(){const ic=me().ic;const c={};G.order.forEach(id=>{const r=G.R[id];if(r&&!r.ret&&r.d<=1)c[r.h]=(c[r.h]||0)+1;});
 return G.heya.map((h,i)=>({h:i,s:c[i]||0})).filter(x=>x.h!==ME()&&!G.heya[x.h].closed&&(ic<0||G.heya[x.h].ic===ic)).sort((a,b)=>b.s-a.s);}
function dekInfo(){const L=dekList();if(!L.length)return null;let x=G.dekH!=null?L.find(y=>y.h===G.dekH):null;if(!x)x=L[0];return {h:x.h,s:x.s,q:.8+.1*Math.min(5,x.s)};}""")
rep("const GR=.021;","const GR=.0197;")
rep("function aiMenu(r){if(G.wk>=5)return '申';return wpick([['基',25],['申',30],['ぶ',15],['三',15],['筋',15]]);}","function aiMenu(r){if(G.wk>=5)return '申';return wpick([['基',40],['申',30],['ぶ',15],['三',15]]);}")
# 週の処理
rep("  G._tr=G.wk===TOURWK?tourSet():null;","  G._tr=tourWk()?tourSet():null;G._dek=dekInfo();")
rep(" if(isOwn&&G._tr&&G._tr.has(r.id)){mk='巡';it=1;}"," if(mk==='筋')mk='基';\n if(isOwn&&G._tr&&G._tr.has(r.id)){mk='巡';it=1;}\n if(!isOwn&&r.d<=1&&!r.inj&&tourWk()){mk='巡';it=1;}")
rep("if(isOwn&&mk==='出'){if(G.money+G.acc.dek<-1500){mk='申';}else G.acc.dek+=(me().ic>=0?3:4);}","if(isOwn&&mk==='出'){if(G.money+G.acc.dek<-1500||!G._dek){mk='申';}else G.acc.dek+=1;}")
rep(" if(mk==='三')gm*=isOwn?(hasPartner(r)?1.05:.65):.9;"," if(mk==='三')gm*=isOwn?(hasPartner(r)?1.05:.65):.9;\n if(isOwn&&mk==='出'&&G._dek){gm*=G._dek.q*(G.wk>=WEEKS-1?1.1:.95)*(ownAll().length<=10?1.1:1);}")
rep(" if(mk!=='休'&&mk!=='研')AK.forEach(k=>grow(r,k,gm*.12*H.cf[CAT[k]]));\n if(!(M.w&&M.w.kos)&&r.a.kos!=null)r.a.kos=Math.max(1,r.a.kos-.005);",
    " if(mk!=='休'&&mk!=='研')AK.forEach(k=>grow(r,k,gm*.12*H.cf[CAT[k]]));\n const kiso=mk!=='休'&&mk!=='研'&&mk!=='基';/* v119 毎朝の基礎運動 */\n if(kiso)for(const k in MENU['基'].w)grow(r,k,gm*MENU['基'].w[k]*.3*H.cf[CAT[k]]);\n if(!(M.w&&M.w.kos)&&!kiso&&r.a.kos!=null)r.a.kos=Math.max(1,r.a.kos-.005);")
rep("+(isOwn?PM[r.pm||'昼'].f:0),0,100);","+(isOwn?PM[r.pm||'昼'].f:0)+(kiso?2:0)+(isOwn&&mk==='出'&&G.wk<WEEKS-1?3:0),0,100);")
rep(" const ct=50+M.c*5*(it>=1?1:.7)-Math.max(0,r.fat-45)*.9;"," const ct=50+M.c*5*(it>=1?1:.7)-Math.max(0,r.fat-45)*.9+(isOwn&&mk==='出'&&G.wk>=WEEKS-1?4:0);")
rep("if(mk==='出')pa=Math.max(pa,.8);return W.sh*envSh()","if(mk==='出')pa=Math.max(pa,G._dek?Math.min(1,.4+.15*G._dek.s):.8);return W.sh*envSh()")
# 巡業のご祝儀は巡業の最後の週にまとめて(1 回あたり前の 1.5 倍=年 4 回で前の年 6 回と同じくらい)
rep("function tourEnd(){const T=G._tr;G._tr=null;if(!T||!T.size)return;","function tourEnd(){const T=G._tr;G._tr=null;if(!T||!T.size)return;const ti=tourInfo();if(!ti||G.wk!==ti[1])return;")
rep(" inc=Math.round(inc*[1,1.2,1.3][G.post||0]);"," inc=Math.round(inc*1.5*[1,1.2,1.3][G.post||0]);out=Math.round(out*1.5);")
rep("G.rep=cl(G.rep+Math.min(2,.5*sk),0,100);G.sup+=sk*2;","G.rep=cl(G.rep+Math.min(3,.75*sk),0,100);G.sup+=sk*3;")
rep("addNews('巡業に '+T.size+' 人","addNews(ti[2]+'に '+T.size+' 人")
# 巡業の表示
rep("function tourOn(r){return G.phase==='train'&&G.wk===TOURWK&&tourSet().has(r.id);}","function tourOn(r){return tourWk()&&tourSet().has(r.id);}")
rep(" if(G.wk===TOURWK-1)return '<div class=\"hl\">来週は巡業です。同行する関取の稽古は巡業になります(「稽古」で変えられます)。</div>';\n if(G.wk!==TOURWK)return '';const T=tourSet();",
    " const ti=tourInfo();if(!tourWk())return '';const T=tourSet();")
rep("'今週は<b>巡業</b>です。同行:'","'今週は<b>'+ti[2]+'</b>です(第 '+ti[1]+' 週まで)。同行:'")
rep("'<div class=\"pn\"><h2>巡業<span class=\"sub\">稽古の第 '+TOURWK+' 週</span></h2><div class=\"hl\">稽古期間の第 '+TOURWK+' 週は巡業です。同行した関取はご祝儀と評判を得られ、実戦的な稽古で調子が上がります。けがも少しあります。</div>'",
    "(()=>{const ti=tourInfo();return '<div class=\"pn\"><h2>巡業<span class=\"sub\">'+(ti?ti[2]+'・第 '+ti[0]+'〜'+ti[1]+' 週':'この場所の前はなし')+'</span></h2><div class=\"hl\">巡業は年 4 回です。春場所のあと(春巡業・4 週)、名古屋場所のあと(夏巡業・4 週)、秋場所のあと(秋巡業・3 週)、九州場所のあと(冬巡業・2 週)。初場所と夏場所のあとはありません。同行した関取は巡業の朝稽古で調子が上がり、巡業の最後にご祝儀と評判を得られます。けがも少しあります。ほかの部屋の関取も巡業に出るので、部屋の稽古相手は減ります。</div>';})()")
# 画面の稽古の一覧から朝の筋トレを外す
d=__file__.replace('patch122.py','')
rep(open(d+'kt118.js',encoding='utf-8').read(),open(d+'kt119.js',encoding='utf-8').read())
rep("Object.keys(MENU)","MKEYS()",6)
open(dst,'w',encoding='utf-8').write(s)
print('ok')
