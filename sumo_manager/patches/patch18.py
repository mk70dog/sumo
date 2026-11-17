# 設計 18:入門の時期・年寄名跡 105・部屋の名前と一門  v14 -> v15
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:80]))
    s = s.replace(old, new)

NAMES = """雷 境川 藤島 出羽海 春日野 三保ヶ関 武蔵川 木瀬 立浪 伊勢ヶ濱 宮城野 高砂 九重 八角 錦戸 佐渡ヶ嶽 二所ノ関 放駒 片男波 尾上
高田川 時津風 井筒 錣山 陸奥 伊勢ノ海 追手風 玉ノ井 式秀 常盤山 湊 荒汐 鳴戸 大嶽 阿武松 田子ノ浦 西岩 中村 押尾川 二子山
音羽山 安治川 秀ノ山 武隈 浅香山 朝日山 東関 芝田山 峰崎 千賀ノ浦 花籠 大島 友綱 山響 北陣 錦島 出来山 大山 待乳山 甲山
楯山 小野川 熊ヶ谷 竹縄 春日山 間垣 中立 稲川 白玉 君ヶ浜 若藤 浦風 不知火 富士ヶ根 清見潟 千田川 桐山 関ノ戸 振分 立田川
立田山 荒磯 鏡山 粂川 岩友 枝川 勝ノ浦 佐ノ山 谷川 高島 入間川 中川 玉垣 湊川 根岸 浜風 二十山 山分 若松 秩父山
尾車 松ヶ根 高崎 山科 立川""".split()
seen = []
for n in NAMES:
    if n not in seen:
        seen.append(n)
if len(seen) != 105:
    raise SystemExit('名跡の数が 105 ではありません: %d' % len(seen))
NAMES_JS = '[' + ','.join("'%s'" % n for n in seen) + ']'

# --- 版と保存キー ---
rep('<title>Sumo Manager v14</title>', '<title>Sumo Manager v15</title>')
rep("const SAVE='sumoManager14',SAVE13", "const SAVE='sumoManager15',SAVE14='sumoManager14',SAVE13")
rep('[SAVE13,SAVE12', '[SAVE14,SAVE13,SAVE12')
rep("if(g.v===13){mig14(g);g.v=14;}\n return g.v===14?g:null;}",
    "if(g.v===13){mig14(g);g.v=14;}\n if(g.v===14){mig15(g);g.v=15;}\n return g.v===15?g:null;}")
rep('G={v:14,', "G={v:15,myoQ:[],myoLog:[],")

CORE = r"""/* v15: 年寄名跡 105・部屋の名前と一門(設計 18) */
const MYO105=__NAMES__;
const MYOST={ai:'ほかの親方',own:'この部屋',free:'空き(協会が管理)',gen:'現役力士が保有',izoku:'遺族などが保有'};
function myoInit(g){const X=g||G;const M={};const hn={};
 X.heya.forEach((h,i)=>{if(!h.closed&&MYO105.includes(h.n))hn[h.n]=i;});
 MYO105.forEach((n,k)=>{const hi=hn[n];M[n]={st:hi!=null?(hi===0?'own':'ai'):'ai',ic:hi!=null?(hi===0?(X.heya[0].ic>=0?X.heya[0].ic:k%5):X.heya[hi].ic):k%5};});
 // 自部屋の名跡を実在の名前に置き換える
 (X.myoL||[]).forEach(m=>{if(M[m.n]&&M[m.n].st!=='own'&&hn[m.n]==null){M[m.n].st='own';return;}
  const c=MYO105.filter(n=>M[n].st==='ai'&&hn[n]==null);if(!c.length)return;const nn=c[Math.floor(Math.random()*c.length)];
  (X.staff||[]).forEach(s=>{if(s.myo===m.n)s.myo=nn;});m.n=nn;M[nn].st='own';});
 X.myoM=[];
 const pool=()=>MYO105.filter(n=>M[n].st==='ai'&&hn[n]==null);
 const take=(st,k)=>{for(let i=0;i<k;i++){const c=pool();if(!c.length)return;M[c[Math.floor(Math.random()*c.length)]].st=st;}};
 take('free',3);take('gen',6);take('izoku',3);
 X.myo=M;X.myoQ=X.myoQ||[];X.myoLog=X.myoLog||[];}
function mig15(g){myoInit(g);}
function myoCnt(st){return MYO105.filter(n=>G.myo[n].st===st).length;}
function myoFreeL(){return MYO105.filter(n=>G.myo[n].st==='free');}
function myoPrice(){const E=myoCnt('free');return Math.round((1800+12000/(1+E*.9))*R(.85,1.15)/50)*50;}
function myoTake(st,from){const c=MYO105.filter(n=>G.myo[n].st===(from||'free'));if(!c.length)return null;const n=pick(c);G.myo[n].st=st;return n;}
function myoName(g0){const X=g0||G;if(!X.myo)return '年寄'+RI(100,999);const c=MYO105.filter(n=>X.myo[n].st==='free');return c.length?pick(c):'年寄'+RI(100,999);}
function myoLog(t){G.myoLog=G.myoLog||[];G.myoLog.unshift({b:G.bnum,t:t});if(G.myoLog.length>30)G.myoLog.length=30;}
function heyaNames(){return new Set(G.heya.filter(h=>!h.closed).map(h=>h.n));}
function v15Basho(sum){if(!G.myo)myoInit(G);const hn=heyaNames();
 // 引退したほかの部屋の関取が名跡を求める
 const Q=G.myoQ||[];G.myoQ=[];
 Q.forEach(x=>{if(Math.random()>.8)return;
  if(myoCnt('free')>0){const n=myoTake('ai');myoLog('元・'+x.n+'('+x.rk+')が年寄「'+n+'」を襲名しました。');}
  else if(myoCnt('izoku')>0&&Math.random()<.3){const n=myoTake('ai','izoku');myoLog('元・'+x.n+'('+x.rk+')が、遺族の持つ年寄「'+n+'」を預かって親方になりました。');}
  else{myoLog('元・'+x.n+'('+x.rk+')は、空いている年寄名跡がなく、協会を去りました。');if(x.best<30)addNews('元・'+x.n+'('+x.rk+')は年寄名跡が見つからず、協会を退職しました。');}});
 // 定年・退職などで名跡が空く/持ち主が変わる
 MYO105.forEach(n=>{const m=G.myo[n];const r=Math.random();
  if(m.st==='ai'&&!hn.has(n)){if(r<.0065)m.st='free';else if(r<.0075)m.st='izoku';}
  else if(m.st==='gen'&&r<.015)m.st='ai';
  else if(m.st==='izoku'&&r<.01)m.st='free';});
 if(myoCnt('free')>4&&Math.random()<.08)myoTake('gen');
 // 預かっている名跡の返還
 (G.myoL||[]).filter(m=>m.rent).forEach(m=>{if(Math.random()<.02&&!G.ev.some(e=>e.k==='myoBack'))G.ev.push({k:'myoBack',n:m.n});});
}
function myoInfo(){const E=myoCnt('free');return '空き名跡 '+E+'(顧問料の目安 '+man(Math.round((1800+12000/(1+E*.9))/50)*50)+'前後)';}
function shinsa(nm,s){const bad=(G.scl||[]).some(x=>x.n===nm);if(bad){s.keep=G.bnum+60;return '年寄名跡資格審査委員会は、過去の不祥事を踏まえ、10 年間は部屋付き親方として指導に専念することを条件に承認しました。';}return '年寄名跡資格審査委員会で承認されました。';}
"""
CORE = CORE.replace('__NAMES__', NAMES_JS)
rep('function B_rec(r)', CORE + 'function B_rec(r)')

# 旧 myoName を置き換え(上で定義)
old_myoName_start = "function myoName(g0){const X=g0||G;const used=new Set((X.myoL||[]).concat(X.myoM||[]).map(m=>m.n));"
i = s.find(old_myoName_start)
if i < 0: raise SystemExit('myoName が見つかりません')
j = s.find("return '年寄'+RI(100,999);}", i)
s = s[:i] + "function myoNameOld(g0){" + s[j:]

# 売りに出る名跡:空き名跡(顧問料)と遺族の名跡(預かり)
rep("function refreshMyo(){G.myoM=[];const n=Math.random()<.35?0:RI(1,2);\n for(let i=0;i<n;i++){const m={id:Math.random().toString(36).slice(2,8),n:'',pr:Math.round(R(500,1300)/50)*50};m.n=myoName();G.myoM.push(m);}}",
    "function refreshMyo(){if(!G.myo)myoInit(G);G.myoM=[];const F=myoFreeL().sort(()=>Math.random()-.5);const n=Math.min(F.length,Math.random()<.4?0:RI(1,2));"
    "  for(let i=0;i<n;i++)G.myoM.push({id:Math.random().toString(36).slice(2,8),n:F[i],pr:myoPrice()});"
    "  const Z=MYO105.filter(x=>G.myo[x].st==='izoku');if(Z.length&&Math.random()<.4)G.myoM.push({id:Math.random().toString(36).slice(2,8),n:pick(Z),pr:0,rent:1});}")
rep("G.money-=m.pr;G.myoL.push({n:m.n,h:0});G.myoM=G.myoM.filter(x=>x.id!==id);addNews('年寄名跡「'+m.n+'」を取得しました('+man(m.pr)+')。');",
    "if(m.rent){G.myoL.push({n:m.n,h:0,rent:1});G.myo[m.n].st='own';G.myoM=G.myoM.filter(x=>x.id!==id);addNews('遺族が持つ年寄名跡「'+m.n+'」を預かりました(預かり料 年 300 万円)。返してほしいと言われることがあります。');save();render();return;}"
    "G.money-=m.pr;G.myoL.push({n:m.n,h:0});G.myo[m.n].st='own';G.myoM=G.myoM.filter(x=>x.id!==id);addNews('年寄名跡「'+m.n+'」を取得しました(先代側への顧問料 '+man(m.pr)+')。');")
rep("if(G.money<m.pr){alertM('資金が足りません',man(m.pr)+' が必要です。');return;}",
    "if(!m.rent&&G.money<m.pr){alertM('資金が足りません',man(m.pr)+' が必要です。');return;}")
rep("<td class=\"num\">'+man(m.pr)+'</td><td><button class=\"btn sm ai\" onclick=\"doBuyMyo(\\''+m.id+'\\')\">買う</button></td></tr>'",
    "<td class=\"num\">'+(m.rent?'預かり 年 300 万円':man(m.pr))+'</td><td><button class=\"btn sm ai\" onclick=\"doBuyMyo(\\''+m.id+'\\')\">'+(m.rent?'預かる':'取得')+'</button></td></tr>'")
rep("<div class=\"hl\">引退した弟子を部屋付き親方に迎えるには、年寄名跡が必要です。名跡は場所ごとに売りに出ます。空いている名跡は、引退の申し出のときに使われます。</div>",
    "<div class=\"hl\">引退した弟子を部屋付き親方に迎えるには、年寄名跡が必要です。名跡は協会全体で 105 しかありません(今は '+myoInfo()+')。2014 年から売買は禁止されていますが、実際には先代側に「顧問料」を払うのが通例で、空きが少ないほど高くなります。遺族などが持つ名跡を預かることもできますが、返してほしいと言われることがあります。</div>")

# 名跡の預かり料
rep(" if(G.money<0)F.out.push(['借入金の利息',",
    " {const nr=(G.myoL||[]).filter(m=>m.rent).length;if(nr)F.out.push(['年寄名跡の預かり料('+nr+')',nr*50]);}\n if(G.money<0)F.out.push(['借入金の利息',")

# ほかの部屋の関取の引退を記録
rep(" kidRoll(r);\n if(G.retired.length>300)",
    " kidRoll(r);\n if(r.h!==0&&myoOK(r)&&(!r.fr||r.nat)){G.myoQ=G.myoQ||[];G.myoQ.push({n:r.n,rk:bestRank(r),best:r.best});}\n if(G.retired.length>300)")

# 部屋付き親方の申し出
rep("const pr=r.best<9?1200:r.best<30?800:500;G.ev.push({k:'oyakata'",
    "const pr=myoPrice();G.ev.push({k:'oyakata',scl:(G.scl||[]).some(x=>x.n===r.n)?1:0")
rep("(f?'空いている年寄名跡「'+f.n+'」を使えます。':'親方になるには年寄名跡が必要です。名跡の取得には '+man(e.price)+' かかり、本人の貯金から '+man(e.cash||0)+' を充てます。');},",
    "(f?'部屋が持っている年寄名跡「'+f.n+'」を使えます。':myoCnt('free')>0?'親方になるには年寄名跡が必要です。協会の空き名跡を襲名するには、先代側への顧問料が '+man(e.price)+' ほどかかり、本人の貯金から '+man(e.cash||0)+' を充てます。':myoCnt('izoku')>0?'協会に空き名跡がありません。遺族が持つ名跡を預かる道があります(預かり料 年 300 万円、返還を求められることがあります)。':'協会に空き名跡がなく、預かれる名跡もありません。このままでは協会に残れません。');},")
rep("c:e=>G.myoL.find(m=>!m.h)?['部屋付き親方として迎える(名跡を使う)','断る']:['名跡の取得を援助して迎える(部屋の負担 '+man(e.price-(e.cash||0))+')','断る'],",
    "c:e=>G.myoL.find(m=>!m.h)?['部屋付き親方として迎える(名跡を使う)','断る']:myoCnt('free')>0?['名跡の取得を援助して迎える(部屋の負担 '+man(Math.max(0,e.price-(e.cash||0)))+')','断る']:myoCnt('izoku')>0?['遺族の名跡を預かって迎える(年 300 万円)','断る']:['名跡がなく、迎えられない'],")
rep("ap:(e,i)=>{if(i!==0)return e.n+'は角界を去りました。';\n   let m=G.myoL.find(x=>!x.h);\n   if(!m){const pay=e.price-(e.cash||0);if(G.money<pay)return '資金が足りず、年寄名跡を用意できませんでした。'+e.n+'は角界を去りました。';G.money-=pay;m={n:myoName(),h:0};G.myoL.push(m);}",
    "ap:(e,i)=>{let m=G.myoL.find(x=>!x.h);if(!m&&myoCnt('free')===0&&myoCnt('izoku')===0)return '空いている年寄名跡がなく、'+e.n+'は協会を去りました。';if(i!==0)return e.n+'は角界を去りました。';\n"
    "   let note='';if(!m){if(myoCnt('free')>0){const pay=Math.max(0,e.price-(e.cash||0));if(G.money<pay)return '資金が足りず、年寄名跡を用意できませんでした。'+e.n+'は角界を去りました。';G.money-=pay;const n=myoTake('own');m={n:n,h:0};G.myoL.push(m);note='(先代側への顧問料 '+man(e.price)+'、うち部屋の負担 '+man(pay)+')';}\n"
    "    else{const n=myoTake('own','izoku');m={n:n,h:0,rent:1};G.myoL.push(m);note='(遺族の名跡を預かる形。預かり料 年 300 万円)';}}")
rep("s.sal=Math.round((ROLE.co.b+Object.values(s.sk).reduce((t,v)=>t+v,0)/6*ROLE.co.m)*.9);m.h=s.sid;G.staff.push(s);return '元・'+e.n+'が年寄「'+m.n+'」を襲名し、部屋付き親方になりました(給与 '+man(s.sal)+'/場所)。';}}",
    "s.sal=Math.round((ROLE.co.b+Object.values(s.sk).reduce((t,v)=>t+v,0)/6*ROLE.co.m)*.9);m.h=s.sid;G.staff.push(s);const sm=shinsa(e.n,s);return '元・'+e.n+'が年寄「'+m.n+'」を襲名し、部屋付き親方になりました'+note+'。'+sm+'(給与 '+man(s.sal)+'/場所)';}}\n"
    " ,myoBack:{t:'名跡の返還',d:e=>{const m=(G.myoL||[]).find(x=>x.n===e.n);const s=m&&m.h?G.staff.find(x=>x.sid===m.h):null;return '預かっている年寄「'+e.n+'」の持ち主から、名跡を返してほしいと連絡がありました。'+(s?s.n+'が使っています。':'今は誰も使っていません。')+'買い取るには、先代側への顧問料が '+man(e.pr||(e.pr=myoPrice()))+' ほどかかります。';},\n"
    "  c:e=>['顧問料を払って買い取る('+man(e.pr||(e.pr=myoPrice()))+')','名跡を返す'],\n"
    "  ap:(e,i)=>{const m=(G.myoL||[]).find(x=>x.n===e.n);if(!m)return '';if(i===0){if(G.money<e.pr)return '資金が足りません。'+EVT.myoBack.ap(e,1);G.money-=e.pr;m.rent=0;return '年寄「'+e.n+'」を買い取りました。';}\n"
    "   const s=m.h?G.staff.find(x=>x.sid===m.h):null;G.myoL=G.myoL.filter(x=>x!==m);G.myo[e.n].st='ai';\n"
    "   if(s){const f=G.myoL.find(x=>!x.h);if(f){f.h=s.sid;s.myo=f.n;return '名跡を返し、'+s.n+'は部屋が持つ年寄「'+f.n+'」に名前を変えました。';}G.staff=G.staff.filter(x=>x!==s);return '名跡を返しました。ほかに名跡がなく、'+s.n+'は協会を退職しました。';}return '名跡を返しました。';}}")

# --- C:新しい部屋の名前と一門 ---
rep("function spinOff(i,o){const src=G.heya[i];const used=new Set(G.heya.filter(h=>!h.closed).map(h=>h.n));const nm=NEWH.filter(n=>!used.has(n));if(!nm.length)return -1;",
    "function spinOff(i,o){const src=G.heya[i];const used=new Set(G.heya.filter(h=>!h.closed).map(h=>h.n));const sic=i>0&&src?src.ic:me().ic;"
    "let nm=(o&&o.name&&!used.has(o.name))?[o.name]:G.myo?MYO105.filter(n=>G.myo[n].st==='ai'&&!used.has(n)&&G.myo[n].ic===sic):[];"
    "if(!nm.length&&G.myo)nm=MYO105.filter(n=>G.myo[n].st==='ai'&&!used.has(n));if(!nm.length)nm=NEWH.filter(n=>!used.has(n));if(!nm.length)return -1;")
rep("const k=spinOff(0,{age:s.age});if(k<0)return '';",
    "const k=spinOff(0,{age:s.age,name:s.myo});if(k<0)return '';if(G.myo&&G.myo[s.myo]){G.myo[s.myo].st='ai';G.myo[s.myo].ic=me().ic>=0?me().ic:G.myo[s.myo].ic;}")

# --- A:入門の時期(春場所が就職場所) ---
rep("const need=TOTAL-G.order.length+G.pend.length*0;",
    "const need=Math.max(0,TOTAL-25-G.order.length,Math.round((TOTAL-G.order.length)*([.12,1,.3,.2,.25,.1][(G.bnum-1)%6])));")

# --- 場所後に名跡の処理 ---
rep(" v13Basho(sum);\n v14Basho(sum);", " v13Basho(sum);\n v14Basho(sum);\n v15Basho(sum);")

# --- 新しいゲームの初期化 ---
rep("refreshMarket();refreshMyo();G.okami=mkOkami();", "myoInit(G);refreshMarket();refreshMyo();G.okami=mkOkami();")

# --- 序二段・序ノ口の大きさを総数に合わせる ---
rep("function divStart(d){let s=0;for(let i=0;i<d;i++)s+=DIVS[i].sz;return s;}",
    "function divSz(d){if(d!==4)return DIVS[d].sz;const b=DIVS[0].sz+DIVS[1].sz+DIVS[2].sz+DIVS[3].sz;const n=(typeof G!=='undefined'&&G&&G.order)?G.order.length:TOTAL;const rest=Math.max(0,n-b);const jn=Math.max(Math.min(rest,15),Math.min(60,Math.round(rest*.17)));return Math.max(0,rest-jn);}\nfunction divStart(d){let s=0;for(let i=0;i<d;i++)s+=divSz(i);return s;}")
rep("function divEnd(d){return d===5?G.order.length:divStart(d)+DIVS[d].sz;}", "function divEnd(d){return d===5?G.order.length:divStart(d)+divSz(d);}")
rep("function divOfPos(p){let s=0;for(let d=0;d<5;d++){s+=DIVS[d].sz;if(p<s)return d;}return 5;}", "function divOfPos(p){let s=0;for(let d=0;d<5;d++){s+=divSz(d);if(p<s)return d;}return 5;}")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
