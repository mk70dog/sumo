# 年寄 103 人・裏方・力士の初土俵と最高位・部屋の資金力と後援会  v17 -> v18
import sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

D = '/home/claude/data/'
TOSHI = [l.split(',') for l in open(D + 'toshiyori2026.csv', encoding='utf-8').read().strip().split('\n')]
assert len(TOSHI) == 103
TOSHI_JS = json.dumps([[r[0], r[1], r[2].replace('部屋', ''), 1 if r[3] == '師匠' else 0, r[4], r[5], r[6], r[7], r[8]] for r in TOSHI], ensure_ascii=False)
URA = [l.split('|') for l in open(D + 'ura2026.txt', encoding='utf-8').read().strip().split('\n')]
URA_JS = json.dumps(URA, ensure_ascii=False)
DEB = {}
for l in open(D + 'rikishi_debut.csv', encoding='utf-8').read().strip().split('\n'):
    f = l.split(',')
    DEB[f[0]] = [f[2], f[3]]
DEB['高安'] = DEB.get('髙安'); DEB['靍林'] = DEB.get('靏林')
DEB_JS = json.dumps(DEB, ensure_ascii=False)
HF = {}
for l in open(D + 'hfin2026.txt', encoding='utf-8').read().strip().split('\n'):
    f = l.split('|')
    HF[f[0]] = [f[1], float(f[2]) if f[2] else None, float(f[3]) if f[3] else None, f[4]]
HF_JS = json.dumps(HF, ensure_ascii=False)

# --- 版 ---
rep('<title>Sumo Manager v17</title>', '<title>Sumo Manager v18</title>')
rep("const SAVE='sumoManager17',SAVE16", "const SAVE='sumoManager18',SAVE17='sumoManager17',SAVE16")
rep('[SAVE16,SAVE15', '[SAVE17,SAVE16,SAVE15')
rep("if(g.v===16){mig17(g);g.v=17;}\n return g.v===17?g:null;}", "if(g.v===16){mig17(g);g.v=17;}\n if(g.v===17){mig18(g);g.v=18;}\n return g.v===18?g:null;}")
rep('G={v:17,', 'G={v:18,')

CORE = r"""/* v18: 年寄・裏方・力士の初土俵・部屋の資金力(実名モード)
   年寄:大相撲のはてなに効く!観戦ガイド「年寄一覧」(2026 年 11 月)。行司・呼出・床山・世話人:日本相撲協会公式サイトの一覧(本名は登録しない)。
   初土俵・最高位:相撲録(sumo6.jp、α版)。後援会の会費:各部屋の公式サイト。 */
const TOSHI=__TOSHI__;
const URA=__URA__;
const DEBUT=__DEB__;
const HFIN=__HF__;
function gDate(X){X=X||G;return (X.y0||2026)+Math.floor(((X.bnum||1)-1)/6)+([1,3,5,7,9,11][((X.bnum||1)-1)%6]-.5)/12;}
function ageOf(b,X){if(!b)return 40;const p=String(b).split('-');return Math.floor(gDate(X)-(+p[0]+((+p[1]||1)-1)/12+((+p[2]||1)-1)/365));}
function rankQ(b){b=String(b||'');return /横綱/.test(b)?14:/大関/.test(b)?13:/関脇/.test(b)?11:/小結/.test(b)?10:/前頭/.test(b)?8.5:/十両/.test(b)?7:6;}
function postLv(p){return p==='理事長'?2:p==='理事'?1:0;}
function tHeya(n){return G.heya.findIndex(h=>!h.closed&&h.n===n);}
function staffFromToshi(t,k){const q=rankQ(t.best);const s={sid:G.sid++,role:'co',n:'元・'+t.mo,mo:t.best,age:ageOf(t.b),own:true,myo:t.n,tid:k,real:1,sk:{}};
 ROLE.co.sk.forEach(x=>s.sk[x]=Math.round(cl(q+randn()*2.5,1,20)));if(t.post==='参与')s.sanyo=true;s.sal=0;return s;}
function toshiInit(g,withStaff){const X=g||G;if(!X.real){X.toshi=null;return;}
 X.toshi=TOSHI.map(r=>({n:r[0],post:r[1],heya:r[2],shi:r[3],mo:r[4],best:r[5],b:r[6],since:r[7],from:r[8]}));
 X.ura=URA.map(r=>({k:r[0],n:r[1],rk:r[2],heya:r[3]}));
 const meN=X.heya[0].n;
 if(withStaff){X.staff.filter(x=>x.role==='co'&&!x.real).forEach(x=>{X.myoL=(X.myoL||[]).filter(m=>m.h!==x.sid);});X.staff=X.staff.filter(x=>!(x.role==='co'&&!x.real));}
 X.toshi.forEach((t,k)=>{const hi=X.heya.findIndex(h=>!h.closed&&h.n===t.heya);
  if(t.shi&&hi>0){X.heya[hi].oa=ageOf(t.b,X);X.heya[hi].o2=t.mo;}
  if(t.shi&&hi===0){X.heya[0].age=ageOf(t.b,X);t.gen0=X.heya[0].gen||1;X.post=postLv(t.post);X.mePost=t.post;}
  if(withStaff&&!t.shi&&t.heya===meN){const sf=staffFromToshi(t,k);X.staff.push(sf);X.myoL=X.myoL||[];X.myoL.push({n:t.n,h:sf.sid});if(X.myo&&X.myo[t.n])X.myo[t.n].st='own';}
  else if(!withStaff&&!t.shi&&t.heya===meN)t.nost=1;});
 for(const id in X.R){const r=X.R[id];const d=DEBUT[r.n];if(!d)continue;r.debut=d[0];r.bestS=d[1];
  if(/^(横綱|大関|関脇|小結)/.test(d[1]))r.san=true;
  const p=d[0].split('-');const idx=(+p[0]-2026)*6+((+p[1])-11)/2;if(isFinite(idx)){r.join=6+Math.round(idx);r.joinReal=1;}}}
function mig18(g){if(g.real){toshiInit(g,false);finInit(g,false);}}
function finScore(i){const h=G.heya[i];if(!h)return 0;const ids=G.order.filter(id=>{const r=G.R[id];return r.h===i&&!r.ret;});
 const sek=ids.filter(id=>G.R[id].d<=1).length;const t=G.toshi?G.toshi.find(x=>x.shi&&x.heya===h.n&&!x.left):null;
 const mb=t?(/横綱/.test(t.best)?5:/大関/.test(t.best)?3:/関脇/.test(t.best)?1:0):(i===0&&me().oyT?0:0);
 const hf=HFIN[h.n];return sek*3+ids.length*.3+mb+(h.est&&h.est<1950?3:h.est&&h.est<1990?1:0)+(hf&&hf[3]?1:0);}
function finRank(v){return v>=25?'S':v>=15?'A':v>=8?'B':v>=4?'C':'D';}
function finInit(g,start){const X=g||G;const hf=HFIN[X.heya[0].n];X.supFee={i:hf&&hf[1]?hf[1]*.7+.6:2.1,c:hf&&hf[2]?hf[2]:20,t:hf?hf[0]:''};
 if(start){const sc=finScore(0);const t=X.toshi?X.toshi.find(x=>x.shi&&x.heya===X.heya[0].n):null;const mb=t?(/横綱/.test(t.best)?200:/大関/.test(t.best)?100:0):0;
  X.money=Math.round(800+sc*110);X.sup=Math.round(X.sup+mb);X.finSc=sc;}}
function toshiBasho(){if(!G.toshi)return;
 G.toshi.forEach((t,k)=>{if(t.left)return;const a=ageOf(t.b);const hi=tHeya(t.heya);
  if(hi===0){if(t.shi){if((me().gen||1)!==(t.gen0||1)||a>=70){t.shi=0;if(a>=70||Math.random()<.5){t.left=G.bnum;}else t.post='参与';}return;}
   if(!t.nost&&!G.staff.some(x=>x.tid===k))t.left=G.bnum;else if(t.nost&&a>=70)t.left=G.bnum;return;}
  if(a>=70&&!(t.shi&&hi>0)){t.left=G.bnum;if(G.myo&&G.myo[t.n]&&G.myo[t.n].st==='ai')G.myo[t.n].st=Math.random()<.5?'izoku':'free';return;}                       // 自分の部屋の親方は部屋の仕組みで扱う
  if(hi<0&&t.shi)return;
  if(t.shi){const h=G.heya[hi];if(h.oa>=65||a>=65){// 師匠の定年:部屋付き親方が継ぐ
    const c=G.toshi.filter(x=>!x.left&&!x.shi&&x.heya===t.heya&&x.post!=='参与'&&ageOf(x.b)<60);
    t.shi=0;if(Math.random()<.6)t.post='参与';else{t.left=G.bnum;G.myo[t.n].st=Math.random()<.5?'izoku':'free';}
    if(c.length){const nx=c.sort((p,q)=>rankQ(q.best)-rankQ(p.best))[0];nx.shi=1;h.o2=nx.mo;h.oa=ageOf(nx.b);hlog(h.n+'部屋は、師匠の定年で元・'+nx.mo+'(年寄 '+nx.n+')が継ぎました。');}
    else h.oa=Math.max(h.oa||0,65);}
   else h.oa=a;return;}
  if(a>=70||(a>=65&&t.post!=='参与'&&Math.random()<.4)){t.left=G.bnum;if(G.myo&&G.myo[t.n])G.myo[t.n].st=Math.random()<.5?'izoku':'free';return;}
  if(a>=65&&t.post!=='参与')t.post='参与';});
 // 閉じた部屋の部屋付き親方は同じ一門の部屋へ
 G.toshi.forEach(t=>{if(t.left||t.shi)return;if(tHeya(t.heya)>=0)return;const ic=(G.heya.find(h=>h.n===t.heya)||{}).ic;
  const L=G.heya.filter((h,i)=>i>0&&!h.closed&&h.ic===ic);if(L.length)t.heya=pick(L).n;else t.left=G.bnum;});}
function toshiOf(n){return G.toshi?G.toshi.filter(t=>!t.left&&t.heya===n):[];}
function uraOf(n){return (G.ura||[]).filter(u=>u.heya===n);}
"""
CORE = CORE.replace('__TOSHI__', TOSHI_JS).replace('__URA__', URA_JS).replace('__DEB__', DEB_JS).replace('__HF__', HF_JS)
rep('function B_rec(r)', CORE + 'function B_rec(r)')

# 開始時(実名モード)
rep("mig11(G);mig12(G);myoInit(G);refreshMyo();heyaInfoInit(G);",
    "mig11(G);mig12(G);myoInit(G);heyaInfoInit(G);toshiInit(G,true);finInit(G,true);refreshMarket();refreshMyo();")
rep("addNews(bname(G.bnum)+'の番付から始めます。'+H[0]+'部屋の弟子は '+o.length+' 人(関取 '+sek+' 人)。資金 '+man(G.money)+'。');",
    "addNews(bname(G.bnum)+'の番付から始めます。'+H[0]+'部屋の弟子は '+o.length+' 人(関取 '+sek+' 人)、部屋付き親方 '+G.staff.filter(x=>x.role==='co').length+' 人。資金 '+man(G.money)+'(資金力 '+finRank(G.finSc||0)+')。');")

# 入門 2 年以内の判定:実在力士は初土俵から
rep("return (r.join||1)>1&&G.bnum-r.join<12&&r.d>=3;}", "return ((r.join||1)>1||r.joinReal)&&G.bnum-r.join<12&&r.d>=3;}")

# 部屋付き親方の給与は協会から(部屋の支出ではない)
rep("const sal=G.staff.reduce((t,s)=>t+s.sal,0);if(sal)F.out.push(['スタッフの給与('+G.staff.length+' 人)',sal]);",
    "const ps=G.staff.filter(s=>s.role!=='co');const sal=ps.reduce((t,s)=>t+s.sal,0);if(sal)F.out.push(['スタッフの給与('+ps.length+' 人)',sal]);")
rep("const ROLE={co:{n:'部屋付き親方',max:3,", "const ROLE={co:{n:'部屋付き親方',max:10,")
rep("s.sal=Math.round((ROLE.co.b+Object.values(s.sk).reduce((t,v)=>t+v,0)/6*ROLE.co.m)*.9);m.h=s.sid;G.staff.push(s);",
    "s.sal=0;m.h=s.sid;G.staff.push(s);if(G.toshi){G.toshi.push({n:m.n,post:'年寄',heya:me().n,shi:0,mo:e.n,best:e.rk,b:((G.y0||2026)+Math.floor((G.bnum-1)/6)-s.age)+'-06-01',since:'',from:''});s.tid=G.toshi.length-1;}")
rep("function fireStaff(sid){const s=G.staff.find(x=>x.sid===sid);if(!s)return;if(s.myo){const m=G.myoL.find(x=>x.h===sid);if(m)m.h=0;}G.money-=s.sal;",
    "function fireStaff(sid){const s=G.staff.find(x=>x.sid===sid);if(!s)return;if(s.role==='co'&&s.tid!=null&&G.toshi&&G.toshi[s.tid]){const t=G.toshi[s.tid];const L=G.heya.filter((h,i)=>i>0&&!h.closed&&h.ic===me().ic);const to=L.length?pick(L):null;G.myoL=G.myoL.filter(x=>x.n!==s.myo);if(G.myo[s.myo])G.myo[s.myo].st='ai';if(to)t.heya=to.n;else t.left=G.bnum;G.staff=G.staff.filter(x=>x.sid!==sid);addNews(s.n+'(年寄 '+s.myo+')は'+(to?to.n+'部屋に移りました。':'協会を離れました。'));return;}if(s.myo){const m=G.myoL.find(x=>x.h===sid);if(m)m.h=0;}G.money-=s.sal;")

# 市場の部屋付き親方:実名モードは同じ一門の実在の親方の移籍
rep("for(let i=0;i<n;i++){const q=Math.random()<.12?R(13,16):R(6,13);G.market.push(mkStaff(pick(roles),q));}\n}",
    "for(let i=0;i<n;i++){const q=Math.random()<.12?R(13,16):R(6,13);G.market.push(mkStaff(pick(roles),q));}\n"
    " if(G.toshi){G.market=G.market.filter(x=>x.role!=='co');const C=G.toshi.map((t,k)=>[t,k]).filter(([t])=>!t.left&&!t.shi&&t.heya!==me().n&&t.post!=='参与'&&ageOf(t.b)<62&&tHeya(t.heya)>0&&G.heya[tHeya(t.heya)].ic===me().ic);\n"
    "  C.sort(()=>Math.random()-.5).slice(0,Math.random()<.5?1:2).forEach(([t,k])=>{const sf=staffFromToshi(t,k);sf.from=t.heya;G.market.push(sf);});}\n}")
rep("G.staff.push(s);G.market=G.market.filter(x=>x.sid!==sid);addNews(ROLE[s.role].n+'として'+s.n+'を迎えました(給与 '+man(s.sal)+'/場所)。');return 'OK';}",
    "if(s.tid!=null&&G.toshi&&G.toshi[s.tid]){const t=G.toshi[s.tid];if(t.left||t.heya!==s.from)return '移籍の話はなくなりました。';t.heya=me().n;G.myo[t.n].st='own';G.myoL.push({n:t.n,h:s.sid});G.staff.push(s);G.market=G.market.filter(x=>x.sid!==sid);addNews(s.n+'(年寄 '+t.n+')が'+s.from+'部屋から移ってきました。給与は協会から出ます。');return 'OK';}\n"
    " G.staff.push(s);G.market=G.market.filter(x=>x.sid!==sid);addNews(ROLE[s.role].n+'として'+s.n+'を迎えました(給与 '+man(s.sal)+'/場所)。');return 'OK';}")

# 独立(AI):元の部屋の部屋付き親方が自分の名跡で部屋を開く
rep("let nm=(o&&o.name&&!used.has(o.name))?[o.name]:G.myo?MYO105.filter(n=>G.myo[n].st==='ai'&&!used.has(n)&&G.myo[n].ic===sic):[];",
    "let tt=null;if(G.toshi&&i>0&&src){const c=G.toshi.filter(t=>!t.left&&!t.shi&&t.heya===src.n&&t.post!=='参与'&&ageOf(t.b)>=35&&ageOf(t.b)<60&&!used.has(t.n));if(!c.length)return -1;tt=pick(c);}\n"
    " let nm=tt?[tt.n]:(o&&o.name&&!used.has(o.name))?[o.name]:G.myo?MYO105.filter(n=>G.myo[n].st==='ai'&&!used.has(n)&&G.myo[n].ic===sic):[];")
rep("h.loc=pick(LOCP);h.est=curYear();h.hist=(src?src.n:me().n)+'部屋から独立して創設。';G.heya.push(h);",
    "h.loc=pick(LOCP);h.est=curYear();h.hist=(src?src.n:me().n)+'部屋から独立して創設。';if(tt){tt.heya=h.n;tt.shi=1;h.o2=tt.mo;h.oa=ageOf(tt.b);if(G.myo&&G.myo[tt.n])G.myo[tt.n].ic=h.ic;}G.heya.push(h);")
rep("const k=spinOff(0,{age:s.age,name:s.myo});if(k<0)return '';",
    "const k=spinOff(0,{age:s.age,name:s.myo});if(k<0)return '';if(G.toshi&&s.tid!=null&&G.toshi[s.tid]){G.toshi[s.tid].heya=G.heya[k].n;G.toshi[s.tid].shi=1;G.heya[k].o2=G.toshi[s.tid].mo;}")

# 引退した関取の襲名を名簿に
rep("G.myoQ.push({n:r.n,rk:bestRank(r),best:r.best});", "G.myoQ.push({n:r.n,rk:bestRank(r),best:r.best,age:Math.floor(r.age),hn:G.heya[r.h]?G.heya[r.h].n:''});")
rep("if(myoCnt('free')>0){const n=myoTake('ai');myoLog('元・'+x.n+'('+x.rk+')が年寄「'+n+'」を襲名しました。');}",
    "if(myoCnt('free')>0){const n=myoTake('ai');myoLog('元・'+x.n+'('+x.rk+')が年寄「'+n+'」を襲名しました。');if(G.toshi)G.toshi.push({n:n,post:'年寄',heya:x.hn,shi:0,mo:x.n,best:x.rk,b:((G.y0||2026)+Math.floor((G.bnum-1)/6)-(x.age||32))+'-06-01',since:'',from:''});}")
rep("else if(myoCnt('izoku')>0&&Math.random()<.6){const n=myoTake('ai','izoku');",
    "else if(myoCnt('izoku')>0&&Math.random()<.6){const n=myoTake('ai','izoku');if(G.toshi)G.toshi.push({n:n,post:'年寄',heya:x.hn,shi:0,mo:x.n,best:x.rk,b:((G.y0||2026)+Math.floor((G.bnum-1)/6)-(x.age||32))+'-06-01',since:'',from:''});")
# 名跡の空き方は名簿があるときは年齢で決める
rep("if(m.st==='ai'&&!hn.has(n)){if(r<.0035)m.st='free';else if(r<.0065)m.st='izoku';}",
    "if(m.st==='ai'&&!hn.has(n)&&!G.toshi){if(r<.0035)m.st='free';else if(r<.0065)m.st='izoku';}")
# 師匠の年齢は名簿から
rep("function v8Basho(sum){", "function v8Basho(sum){\n toshiBasho();")

# 後援会の会費は部屋ごと(わかる部屋は公式サイトの額)
rep("F.in.push(['後援会の年会費・個人('+G.sup+' 人)',Math.round(G.sup*.35)]);if(G.supC)F.in.push(['後援会の年会費・法人('+G.supC+' 社)',Math.round(G.supC*20/6)]);",
    "{const fe=G.supFee||{i:2.1,c:20};F.in.push(['後援会の年会費・個人('+G.sup+' 人)',Math.round(G.sup*fe.i/6)]);if(G.supC)F.in.push(['後援会の年会費・法人('+G.supC+' 社)',Math.round(G.supC*fe.c/6)]);}")
rep("人(年会費 平均 2 万円ほど)</dd>", "人(年会費 平均 '+((G.supFee||{i:2.1}).i).toFixed(1)+' 万円ほど)</dd>'+((G.supFee&&G.supFee.t)?'<dt>会費(公式)</dt><dd>'+esc(G.supFee.t)+'</dd>':'')+'")

# 画面:部屋の詳細に親方・裏方・資金力
rep("return '<dl class=\"kv\"><dt>所在地</dt><dd>'+esc(h.loc||'—')+'</dd>",
    "const TS=toshiOf(h.n).sort((a,b)=>b.shi-a.shi);const U=uraOf(h.n);const hf=HFIN[h.n];const fs=finScore(i);\n"
    " return '<dl class=\"kv\"><dt>資金力</dt><dd>'+finRank(fs)+'(推定。関取・人数・師匠の実績・歴史から)</dd>'+(hf?'<dt>後援会</dt><dd>'+esc(hf[0])+(hf[3]?'。'+esc(hf[3]):'')+'</dd>':'')+"
    "(TS.length?'<dt>親方</dt><dd>'+TS.map(t=>(t.shi?'<b>師匠</b> ':'')+esc(t.n)+'(元・'+esc(t.mo)+'・'+esc(t.best)+'・'+ageOf(t.b)+'歳'+(t.post&&t.post!=='年寄'?'・'+esc(t.post):'')+')').join('<br>')+'</dd>':'')+"
    "(U.length?'<dt>裏方</dt><dd>'+['行司','呼出','床山','世話人'].map(k=>{const L=U.filter(u=>u.k===k);return L.length?k+':'+L.map(u=>esc(u.n)+(u.rk!==k&&u.rk!=='世話人'?'('+esc(u.rk)+')':'')).join('、'):'';}).filter(x=>x).join('<br>')+'</dd>':'')+'<dt>所在地</dt><dd>'+esc(h.loc||'—')+'</dd>")
rep("<th class=\"num\">創設</th><th class=\"num\">力士</th></tr>'+", "<th class=\"num\">創設</th><th class=\"num\">力士</th><th>資金</th></tr>'+")
rep("<td class=\"num\">'+(cnt[i]||0)+'</td></tr>').join('')", "<td class=\"num\">'+(cnt[i]||0)+'</td><td>'+finRank(finScore(i))+'</td></tr>').join('')")
rep("所在地・創設・沿革は 2026 年 10 月時点の実在の部屋のもので、ゲームの途中でできた部屋は架空です。",
    "所在地・創設・沿革は 2026 年 10 月時点の実在の部屋のもので、ゲームの途中でできた部屋は架空です。資金力(S〜D)は推定です。")
# 力士の詳細:初土俵と最高位
rep("'部屋</dd><dt>出身</dt>", "'部屋</dd>'+(r.debut?'<dt>初土俵</dt><dd>'+esc(r.debut.replace('-',' 年 '))+' 月'+(r.bestS?'(最高位 '+esc(r.bestS)+')':'')+'</dd>':'')+'<dt>出身</dt>")
# スタッフ画面:協会の役職と裏方
rep("h+=okamiPanel();h+='<div class=\"pn\"><h2>部屋のスタッフ",
    "if(G.mePost)h=h.replace('定年 65 歳)','定年 65 歳)・協会の役職 '+esc(G.mePost));\n"
    " {const U=uraOf(me().n);if(U.length||G.toshi)h+='<div class=\"pn\"><h2>部屋の裏方<span class=\"sub\">協会に雇われ、この部屋に所属</span></h2>'+(U.length?['行司','呼出','床山','世話人'].map(k=>{const L=U.filter(u=>u.k===k);return L.length?'<div class=\"kaku\" style=\"margin:2px 0\"><b>'+k+'</b> '+L.map(u=>esc(u.n)+(u.rk!==k&&u.rk!=='世話人'?'('+esc(u.rk)+')':'')).join('、')+'</div>':'';}).join(''):'<p class=\"mute kaku\">この部屋に所属する裏方はいません。</p>')+'<p class=\"kaku mute\" style=\"font-size:13px\">行司・呼出・床山・世話人は 2026 年 11 月時点の実在の人(協会の公式一覧から。本名は載せていません)。若者頭は公開の一覧が見つからず、登録していません。</p></div>';}\n"
    " h+=okamiPanel();h+='<div class=\"pn\"><h2>部屋のスタッフ")
rep("<div class=\"btns\"><span class=\"kaku\">給与 '+man(s.sal)+'</span>", "<div class=\"btns\"><span class=\"kaku\">'+(s.role==='co'?'給与は協会から':'給与 '+man(s.sal))+'</span>")

# 最高位:ゲーム開始前の実績も含める
rep("<dt>最高位</dt><dd>'+esc(bestRank(r)||'—')+'</dd>", "<dt>最高位</dt><dd>'+esc(bestRankAll(r)||'—')+'</dd>")
rep("function bestRank(r){", "function bestRankAll(r){const g=bestRank(r);if(!r.bestS)return g;const lv=x=>/横綱/.test(x)?9e6:/大関/.test(x)?8e6:/関脇/.test(x)?7e6:/小結/.test(x)?6e6:/前頭/.test(x)?5e6-(parseInt(x.replace(/[^0-9]/g,''))||1):/十両/.test(x)?4e6-(parseInt(x.replace(/[^0-9]/g,''))||1):/幕下/.test(x)?3e6-(parseInt(x.replace(/[^0-9]/g,''))||1):/三段目/.test(x)?2e6-(parseInt(x.replace(/[^0-9]/g,''))||1):1e6-(parseInt(x.replace(/[^0-9]/g,''))||1);return lv(r.bestS)>lv(g)?r.bestS:g;}\nfunction bestRank(r){")
rep("+' 月'+(r.bestS?'(最高位 '+esc(r.bestS)+')':'')+'</dd>'", "+' 月</dd>'")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
