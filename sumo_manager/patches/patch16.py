# 設計 16:師弟の信頼と部屋の人間関係  v12 -> v13
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:80]))
    s = s.replace(old, new)

# --- 版と保存キー ---
rep('<title>Sumo Manager v12</title>', '<title>Sumo Manager v13</title>')
rep("const SAVE='sumoManager12',SAVE11", "const SAVE='sumoManager13',SAVE12='sumoManager12',SAVE11")
rep('[SAVE11,SAVE10', '[SAVE12,SAVE11,SAVE10')
rep("if(g.v===11){mig12(g);g.v=12;}\n return g.v===12?g:null;}",
    "if(g.v===11){mig12(g);g.v=12;}\n if(g.v===12){mig13(g);g.v=13;}\n return g.v===13?g:null;}")
rep('G={v:12,', "G={v:13,jin:50,meSel:{auto:1,ids:[]},late:[],st16:{join:0,early:0,yame:0,hide:0,ijime:0},")

# --- 部屋の雰囲気:部屋頭は 2 倍の重み ---
rep("function atmo(){const o=own();if(!o.length)return 50;return o.reduce((t,r)=>t+(r.tr==null?50:r.tr),0)/o.length;}",
    "function atmo(){const o=own();if(!o.length)return 50;const top=heyaTop();let s=0,w=0;o.forEach(r=>{const k=(r===top&&o.length>1)?2:1;s+=(r.tr==null?50:r.tr)*k;w+=k;});return s/w;}")

# --- 新しい仕組み本体 ---
CORE = r"""/* v13: 師弟の信頼と部屋の人間関係(設計 16) */
const SHN={褒:'褒める',普:'ふつう',厳:'厳しく'};
function mig13(g){g.jin=g.jin==null?50:g.jin;g.meSel=g.meSel||{auto:1,ids:[]};g.late=g.late||[];g.st16=g.st16||{join:0,early:0,yame:0,hide:0,ijime:0};
 for(const id in g.R){const r=g.R[id];if(r.h===0){if(!r.sh)r.sh='普';r.trl=r.trl||[];}}}
function trAdd(r,d,why){r.tr=cl((r.tr==null?50:r.tr)+d,0,100);if(why&&r.h===0){r.tlog=r.tlog||[];r.tlog.unshift({b:G.bnum,t:why,d:Math.round(d)});if(r.tlog.length>8)r.tlog.length=8;}}
function isNewbie(r){if(r.h!==0||r.ret)return false;if(G.pend.includes(r.id))return true;return (r.join||1)>1&&G.bnum-r.join<12&&r.d>=3;}
function heyaTop(){const o=own();return o.length?o.reduce((a,b)=>(a.pos<=b.pos?a:b)):null;}
function meSlots(){return (G.tmp.away>0||G.post===2)?1:2;}
function neglectWk(){return 12+4*G.staff.filter(s=>s.role==='co').length;}
function meAuto(){return ownAll().map(r=>[r.id,(G.wn-(r.lastMe!=null?r.lastMe:G.wn-8))+(50-(r.tr==null?50:r.tr))*.3+(isNewbie(r)?4:0)]).sort((a,b)=>b[1]-a[1]).map(x=>x[0]);}
function meList(){const S=G.meSel||{auto:1,ids:[]};const n=meSlots();const ok=id=>G.R[id]&&!G.R[id].ret&&G.R[id].h===0;
 let ids=S.auto?[]:(S.ids||[]).filter(ok);ids=ids.filter((x,i)=>ids.indexOf(x)===i);
 if(ids.length<n)ids=ids.concat(meAuto().filter(id=>!ids.includes(id)));return ids.slice(0,n);}
function shF(r){const t=r.tr==null?50:r.tr;let f=t>=70?1.05:t<30?.92:1;
 if(G._me&&G._me.has(r.id))f*=1.05;
 const s=r.sh||'普',p=r.per;
 if(s==='厳')f*=(p==='負けず嫌い'||p==='野心家')?1.08:1.03;
 else if(s==='褒')f*=(p==='おっとり'||p==='繊細')?1.03:.98;
 return f;}
function aniOK(r,a){return !!a&&a!==r&&a.h===0&&!a.ret&&!G.pend.includes(a.id)&&(a.join||1)<(r.join||G.bnum);}
function aniAssign(){const o=ownAll();const cnt={};
 o.forEach(r=>{if(!isNewbie(r)){r.ani=null;return;}const a=r.ani!=null?G.R[r.ani]:null;if(aniOK(r,a))cnt[a.id]=(cnt[a.id]||0)+1;else r.ani=null;});
 o.forEach(r=>{if(!isNewbie(r)||r.ani!=null)return;let best=null,bs=-1e9;
  own().forEach(a=>{if(!aniOK(r,a)||isNewbie(a))return;const c=cnt[a.id]||0;if(c>=2)return;
   const sc=(a.tr==null?50:a.tr)+(a.d>=2?10:0)-c*15+((a.per==='真面目'||a.per==='おっとり')?5:0);if(sc>bs){bs=sc;best=a;}});
  if(best){r.ani=best.id;cnt[best.id]=(cnt[best.id]||0)+1;}});}
function shiteiWeek(){const M=G._me||new Set();const nw=neglectWk();
 ownAll().forEach(r=>{if(r.tr==null)r.tr=50;if(r.lastMe==null)r.lastMe=G.wn;const p=r.per,s=r.sh||'普';let d=0;
  if(M.has(r.id)){r.lastMe=G.wn;d+=p==='繊細'?.45:.3;}
  else if(r.d>=2&&G.wn-r.lastMe>nw)d-=.15;
  if(s==='厳'){d+=(p==='負けず嫌い'||p==='野心家')?.05:(p==='繊細'||p==='気分屋')?-.3:-.1;if(p==='繊細'||p==='気分屋')r.mor=cl(r.mor-.3,0,100);}
  else if(s==='褒')d+=p==='野心家'?.05:.15;
  const a=r.ani!=null?G.R[r.ani]:null;
  if(a&&!a.ret&&a.h===0){d+=((a.tr==null?50:a.tr)-50)*.004+((a.per==='真面目'||a.per==='おっとり')?.05:0);grow(a,pick(MIND),.0015);}
  r.tr=cl(r.tr+d,0,100);});
 G._me=null;}
function v13Basho(sum){const S=G.st16=G.st16||{join:0,early:0,yame:0,hide:0,ijime:0};const a=atmo();
 own().forEach(r=>{r.trl=r.trl||[];r.trl.push(Math.round(r.tr==null?50:r.tr));if(r.trl.length>6)r.trl.shift();
  if(!r.j16){r.j16=1;if((r.join||1)>1&&G.bnum-r.join<=1)S.join++;}});
 // 隠していたけが
 own().forEach(r=>{if(r.inj&&r.inj.hid){r.inj.hid=0;r.inj.wk+=RI(2,4);if(r.inj.s<3&&Math.random()<.3)r.inj.s++;r.inj.t=Math.max(r.inj.t,r.inj.wk);
  addNews(r.n+'は'+r.inj.p+'の痛みを親方に言わずに土俵に上がっていました。けがが悪化しています。');
  if(r.inj.s>=3&&!r.inj.ope&&!r.inj.cons&&!G.ev.some(e=>e.k==='ope'&&e.rid===r.id))G.ev.push({k:'ope',rid:r.id});}});
 // 入門 2 年以内の弟子が辞める
 own().filter(isNewbie).forEach(r=>{if(G.ev.some(e=>(e.k==='yame'||e.k==='retire')&&e.rid===r.id))return;const t=r.tr==null?50:r.tr;const an=r.ani!=null?G.R[r.ani]:null;
  let p=(.022+.02*(50-t)/30+.01*(50-a)/30-(an&&(an.tr==null?50:an.tr)>=60?.004:0))*(G.bnum-(r.join||G.bnum)<6?1.3:.7);
  if(r.per==='繊細')p*=1.3;else if(r.per==='真面目'||r.per==='負けず嫌い')p*=.75;
  p=cl(p,.003,.08);
  if(Math.random()<p){S.trig=(S.trig||0)+1;if(t<28&&Math.random()<.5){S.early++;G.jin=cl((G.jin==null?50:G.jin)-2,0,100);doRetire(r,'部屋を出て、そのまま廃業');}
   else if(!G.ev.some(e=>e.k==='yame'))G.ev.push({k:'yame',rid:r.id});}});
 // 兄弟子の暴力の芽
 if(a<48&&!G.ev.some(e=>e.k==='ijime'||e.k==='scand')){
  const L=own().filter(r=>isNewbie(r)&&r.ani!=null&&G.R[r.ani]&&!G.R[r.ani].ret);
  const okf=G.okami?cl(1-(G.okami.sk.hito-8)*.04,.6,1.3):1;
  for(const r of L){const an=G.R[r.ani];const p=.02*(1+(48-a)/20)*((an.per==='豪快'||an.per==='負けず嫌い')?1.6:1)*((an.tr==null?50:an.tr)<40?1.4:1)*okf;
   if(Math.random()<p){S.ijime++;
    if(Math.random()<.5+(G.okami?G.okami.sk.hito*.02:0))G.ev.push({k:'ijime',rid:r.id,aid:an.id});
    else{G.late.push({b:G.bnum+RI(1,3),rid:an.id,hid:1});trAdd(r,-6,'兄弟子に手を上げられた');}
    break;}}}
 // 後から明るみに出る
 G.late=(G.late||[]).filter(x=>{if(x.b>G.bnum)return true;const an=G.R[x.rid];if(!an||an.ret||an.h!==0)return false;
  if(G.ev.some(e=>e.k==='scand'))return true;G.ev.push({k:'scand',rid:an.id,tp:'bou',hid:x.hid||1});return false;});
 // 親方の評判
 const j=G.jin==null?50:G.jin;G.jin=cl(j+(a-50)*.05+(50-j)*.04,0,100);
 // 相談
 if(Math.random()<.35&&!G.ev.some(e=>e.k==='soudan')){const e={k:'soudan'};if(EVT.soudan.init(e)!==false)G.ev.push(e);}
}
function setMeAuto(v){G.meSel=G.meSel||{auto:1,ids:[]};G.meSel.auto=v?1:0;if(!v&&!(G.meSel.ids||[]).length)G.meSel.ids=meList();save();render();}
function setMe(k,v){G.meSel=G.meSel||{auto:0,ids:[]};G.meSel.ids=G.meSel.ids||[];G.meSel.ids[k]=v===''?null:+v;G.meSel.ids=G.meSel.ids.filter(x=>x!=null);save();render();}
function setAni(id,v){const r=G.R[id];if(!r)return;r.ani=v===''?null:+v;save();render();}
"""
rep('function B_rec(r)', CORE + 'function B_rec(r)')

# --- 週の処理 ---
rep("tkAssign();\n const H0=heyaH(0);", "tkAssign();aniAssign();G._me=new Set(meList());\n const H0=heyaH(0);")
rep("G.pend.forEach(id=>weekR(G.R[id],H0));\n tourEnd();", "G.pend.forEach(id=>weekR(G.R[id],H0));\n shiteiWeek();\n tourEnd();")
rep("gm*=tkF;", "gm*=tkF;if(isOwn)gm*=shF(r);")

# --- 場所後 ---
rep(" v12Basho(sum);", " v12Basho(sum);\n v13Basho(sum);")

# --- 関取からのお礼は信頼で 3〜8% ---
rep("g+=r.inc.tot*.05;", "g+=r.inc.tot*(.03+.05*(r.tr==null?50:r.tr)/100);")

# --- 信頼が低いと、けがを隠して出る ---
rep("if(r.h===0){if(r.injPol==='休')return true;",
    "if(r.h===0){if((r.inj.s===2||(r.inj.s===1&&r.injPol==='休'))&&(r.tr==null?50:r.tr)<35&&G.phase!=='basho'&&Math.random()<(35-r.tr)/35*.6){r.inj.hid=1;if(G.st16)G.st16.hide++;return false;}if(r.injPol==='休')return true;")

# --- 評判は勧誘に効く ---
rep("-p.int*.003+sc+", "-p.int*.003+sc+((G.jin==null?50:G.jin)-50)*.002+")

# --- 引退後の行き先 ---
rep("if(mq&&(!r.fr||r.nat)&&G.staff",
    "if(mq&&(!r.fr||r.nat)&&(r.tr==null?50:r.tr)<35)addNews(r.n+'は親方への信頼が薄く、部屋には残らずに、ほかの部屋で年寄として後進を指導する道を選びました。');\n  else if(mq&&(!r.fr||r.nat)&&G.staff")
rep("price:pr,cash:", "on:(r.tr==null?50:r.tr)>=70?1:0,price:pr,cash:")
rep("が、引退後も部屋付き親方として残り", "が、'+(e.on?'「育ててもらった恩を返したい」と、':'')+'引退後も部屋付き親方として残り")

# --- 引退の相談 ---
rep("c:['引退を認める','もう一場所がんばらせる'],", "c:['引退を認める','もう一場所がんばらせる','引退を認め、第二の人生を一緒に考える(10 万円)'],")
rep("if(i===0){doRetire(r,'本人の希望');return'';}r.stay=true;r.mor=cl(r.mor-8,0,100);",
    "if(i===0){doRetire(r,'本人の希望');return'';}if(i===2){G.money-=10;trAdd(r,10,'');G.jin=cl((G.jin==null?50:G.jin)+2,0,100);own().forEach(x=>{if(x!==r)x.tr=cl(x.tr+1,0,100);});doRetire(r,'本人の希望');return '親方は'+r.n+'と次の仕事について一緒に考えました。その姿を、ほかの弟子たちも見ていました。';}r.stay=true;r.mor=cl(r.mor-8,0,100);if((r.tr==null?50:r.tr)<40)trAdd(r,-4,'引退を引き止められた');")

# --- 不祥事:親方が把握していなかった暴力 ---
rep("(G.post?'(協会の役員でもある親方の対応が注目されています)':'');}",
    "(G.post?'(協会の役員でもある親方の対応が注目されています)':'')+(e.hid===1?'部屋の中で起きていたことに、親方は気づいていませんでした。':e.hid===2?'親方が把握しながら協会に報告していなかったことも問題になっています。':'');}")
rep("const lt=G.post===2?1:0;let m='';",
    "const lt=G.post===2?1:0;let m='';if(e.hid){G.rep=cl(G.rep-(e.hid===2?3:2),0,100);G.jin=cl((G.jin==null?50:G.jin)-3,0,100);}")
rep("if(G.scl.length>40)G.scl.length=40;return m;}}",
    "if(G.scl.length>40)G.scl.length=40;return (e.hid?'(親方の監督責任も問われました)':'')+m;}}")

# --- 新しい出来事 ---
NEWEV = r""" ,yame:{t:'辞めたいという相談',d:e=>{const r=G.R[e.rid];if(!r)return '';return r.n+'('+(r.rkS||'新弟子')+'・入門 '+Math.max(1,G.bnum-(r.join||G.bnum)+1)+' 場所目)が「部屋を辞めたい」と打ち明けてきました。親方への信頼は '+Math.round(r.tr==null?50:r.tr)+' です。';},
  c:()=>['じっくり話を聞いて引き留める','親御さんを呼んで話し合う(10 万円)','本人の決意を尊重して送り出す'],
  ap:(e,i)=>{const r=G.R[e.rid];if(!r||r.ret)return '';const t=r.tr==null?50:r.tr;const S=G.st16;
   const go=m=>{S.early++;S.yame++;doRetire(r,'本人の希望(入門 2 年以内)');return m;};
   if(i===0){if(Math.random()<.35+t/160){trAdd(r,8,'辞めたい気持ちを受け止めてもらった');r.mor=cl(r.mor+4,0,100);return r.n+'は思い直し、もう一度がんばると言いました。';}G.jin=cl(G.jin-1,0,100);return go(r.n+'の決意は固く、部屋を去りました。');}
   if(i===1){if(G.money<10)return go('親御さんを呼ぶ費用がなく、'+r.n+'は部屋を去りました。');G.money-=10;if(Math.random()<.5+t/200){trAdd(r,6,'親を交えて話し合った');r.mor=cl(r.mor+3,0,100);return '親御さんと話し合い、'+r.n+'は続けることにしました。';}return go('親御さんとも話し合いましたが、'+r.n+'は実家に戻ることになりました。');}
   G.jin=cl(G.jin+1,0,100);own().forEach(x=>{if(x!==r)x.tr=cl(x.tr+.5,0,100);});return go(r.n+'の決意を尊重し、送り出しました。誠実な対応は、ほかの弟子や地元にも伝わりました。');}}
 ,ijime:{t:'兄弟子と弟弟子',d:e=>{const r=G.R[e.rid],a=G.R[e.aid];if(!r||!a)return '';return '兄弟子の'+a.n+'('+a.rkS+')が、面倒を見ている'+r.n+'に手を上げているようです。協会は 2018 年の「暴力決別宣言」で、指導の名目でも暴力を許さず、師匠が部屋の暴力を根絶すると定めています。';},
  c:()=>['協会に報告し、部屋でも指導する','部屋の中だけで厳しく指導する','様子を見る'],
  ap:(e,i)=>{const r=G.R[e.rid],a=G.R[e.aid];if(!r||!a||a.ret)return '';
   if(i===0){a.susp=Math.max(a.susp||0,1);G.rep=cl(G.rep-1,0,100);G.jin=cl(G.jin+2,0,100);trAdd(r,6,'暴力から守ってもらった');trAdd(a,-5,'暴力を協会に報告された');own().forEach(x=>{if(x!==r&&x!==a)x.tr=cl(x.tr+1,0,100);});r.ani=null;
    G.scl.unshift({b:G.bnum,n:a.n,t:'後輩への暴力',a:'協会に報告',r:'1 場所の出場停止'});if(G.scl.length>40)G.scl.length=40;return a.n+'は協会から 1 場所の出場停止になりました。'+r.n+'には別の兄弟子を付けます。';}
   if(i===1){trAdd(a,-3,'親方に厳しく叱られた');a.mor=cl(a.mor-4,0,100);trAdd(r,2,'');r.ani=null;if(Math.random()<.35)G.late.push({b:G.bnum+RI(1,3),rid:a.id,hid:2});return '部屋の中で厳しく指導しました。'+r.n+'には別の兄弟子を付けます。';}
   trAdd(r,-10,'暴力を見過ごされた');if(Math.random()<.5)G.late.push({b:G.bnum+RI(1,3),rid:a.id,hid:2});return '様子を見ることにしました。';}}
 ,soudan:{t:'弟子からの相談',d:e=>{const r=G.R[e.rid];if(!r)return '';return r.n+'('+r.rkS+')'+({kazoku:'の実家で、家族が体を悪くしたそうです。顔を見に帰りたいと相談がありました。',oya:'の両親が、稽古を見に部屋を訪ねてきます。',nayami:'が「最近、稽古をしても強くなっている気がしない」と悩んでいます。'})[e.tp];},
  c:e=>({kazoku:['帰省を許す(1 週間)','場所が終わるまで待たせる'],oya:['部屋でもてなす(10 万円)','稽古を見てもらうだけにする'],nayami:['一緒に稽古を見直す','自分で考えさせる']})[e.tp],
  init:e=>{const c=own().filter(r=>!r.inj);if(!c.length)return false;const r=wpick(c.map(x=>[x,1+(x.d>=3?1:0)]));e.rid=r.id;e.tp=wpick([['kazoku',2],['oya',isNewbie(r)?4:1],['nayami',3]]);},
  ap:(e,i)=>{const r=G.R[e.rid];if(!r||r.ret)return '';const p=r.per;
   if(e.tp==='kazoku'){if(i===0){trAdd(r,8,'家族のもとへ帰してもらった');r.mor=cl(r.mor+5,0,100);r.cond=cl(r.cond-6,0,100);return r.n+'は実家に帰り、家族の顔を見て戻ってきました。';}trAdd(r,-6,'帰省を許されなかった');r.mor=cl(r.mor-5,0,100);return r.n+'は稽古を続けていますが、気持ちは晴れないようです。';}
   if(e.tp==='oya'){if(i===0){if(G.money<10)return '資金が足りず、もてなせませんでした。';G.money-=10;trAdd(r,5,'両親を温かく迎えてもらった');G.jin=cl(G.jin+1.5,0,100);return '両親は部屋の様子に安心して帰りました。地元での部屋の評判も上がりそうです。';}trAdd(r,1,'');return '両親は稽古を見て帰りました。';}
   if(i===0){trAdd(r,6,'親方が稽古を一緒に見直してくれた');r.kn=Math.min(100,r.kn+5);grow(r,pick(TECH),.01);return '親方と稽古を見直し、'+r.n+'は手応えをつかんだようです。';}
   if(p==='負けず嫌い'||p==='職人肌'||p==='野心家'){r.mor=cl(r.mor+4,0,100);return r.n+'は自分で工夫を重ね、気持ちを立て直しました。';}
   trAdd(r,-4,'悩みを聞いてもらえなかった');r.mor=cl(r.mor-3,0,100);return r.n+'は一人で抱え込んでいます。';}}
"""
rep(" ,yokoshin:{t:'横綱審議委員会'", NEWEV + " ,yokoshin:{t:'横綱審議委員会'")

# --- 画面 ---
UI = r"""function shiteiPanel(){const o=ownAll();if(!o.length)return '';const S=G.meSel||{auto:1,ids:[]};const n=meSlots();const cur=meList();const nw=neglectWk();
 const opts=[['','(選ぶ)']].concat(o.map(r=>[r.id,(G.pend.includes(r.id)?'新弟子':r.rkS)+' '+r.n]));
 let h='<div class="pn"><h2>師弟<span class="sub">目をかける弟子・接し方・兄弟子</span></h2>';
 h+='<div class="btns" style="margin:4px 0 6px;align-items:center"><span class="kaku">今週目をかける('+n+' 人'+(n<2?'・親方が部屋を空けるため':'')+')</span>'+selH([['1','自動(しばらく見ていない弟子から)'],['0','自分で選ぶ']],S.auto?1:0,'setMeAuto(+this.value)')+(S.auto?'':[0,1].map(k=>selH(opts,(S.ids||[])[k]==null?'':S.ids[k],'setMe('+k+',this.value)')).join(''))+'</div>';
 h+='<p class="kaku" style="font-size:13px;margin:0 0 6px">今週:'+(cur.map(id=>'<b>'+esc(G.R[id].n)+'</b>').join('・')||'—')+'</p>';
 h+='<div style="overflow-x:auto"><table class="tb"><tr><th>番付</th><th>四股名</th><th>信頼</th><th>接し方</th><th>兄弟子</th><th class="hide-s">目をかけた</th></tr>'+o.map(r=>{const t=Math.round(r.tr==null?50:r.tr);const nb=isNewbie(r);const ago=r.lastMe!=null?G.wn-r.lastMe:null;
  return '<tr><td>'+(G.pend.includes(r.id)?'新弟子':esc(r.rkS))+'</td><td class="nm" onclick="showR('+r.id+')" style="cursor:pointer">'+esc(r.n)+'</td><td class="num"><b class="'+(t>=65?'mid':t<40?'shu':'')+'">'+t+'</b></td><td>'+selH(Object.keys(SHN).map(k=>[k,SHN[k]]),r.sh||'普','setR('+r.id+',\'sh\',this.value)')+'</td><td>'+(nb?selH(aniOpts(r),r.ani==null?'':r.ani,'setAni('+r.id+',this.value)'):'<span class="mute">—</span>')+'</td><td class="hide-s" style="white-space:nowrap">'+(ago==null?'—':ago<=0?'今週':ago+' 週前')+(ago!=null&&ago>nw&&r.d>=2?' <span class="tag shu">気にかけて</span>':'')+'</td></tr>';}).join('')+'</table></div>';
 h+='<p class="kaku mute" style="font-size:13px">・目をかけた弟子は、その週の稽古の伸びが 5% 上がり、信頼が少し増えます。幕下以下の弟子を '+nw+' 週より長く見ないでいると、信頼が少しずつ下がります(部屋付き親方が多いほど長く持ちます)。<br>・接し方は性格で効き方が変わります。厳しくすると負けず嫌い・野心家はよく伸びますが、繊細・気分屋は信頼を失います。褒めて伸ばすと信頼が増えますが、伸びは少し控えめです(おっとり・繊細は伸びます)。<br>・信頼が 70 以上だと稽古の伸びが 5% 上がり、30 未満だと 8% 落ちます。信頼の低い弟子は、けがを隠して出場することがあります。<br>・入門 2 年以内の弟子には兄弟子が付きます(1 人の兄弟子に 2 人まで)。兄弟子の信頼と人柄が弟弟子に伝わり、辞めずに続けられるかに効きます。</p></div>';
 return h;}
function aniOpts(r){return [['','(自動)']].concat(own().filter(x=>aniOK(r,x)&&(!isNewbie(x)||x.id===r.ani)).map(x=>[x.id,x.n]));}
function trustBox(r){const L=(r.trl||[]).concat([Math.round(r.tr==null?50:r.tr)]);const lg=r.tlog||[];const a=r.ani!=null?G.R[r.ani]:null;
 return '<div class="kaku" style="font-size:13px;margin:0 0 6px">信頼の推移 '+spark(L,200,34,'#2c3e5c',0,100)+(a&&!a.ret?'<div>兄弟子:'+esc(a.n)+'('+esc(a.rkS)+')</div>':'')+(lg.length?'<div class="mute">最近:'+lg.slice(0,4).map(x=>esc(x.t)+(x.d?'('+(x.d>0?'+':'')+x.d+')':'')).join('/')+'</div>':'')+'</div>';}
"""
rep("function setAll(", UI + "function setAll(")
rep(" h+=bodyPanel();", " h+=shiteiPanel();\n h+=bodyPanel();")
rep("  h+='<h3>能力<span", "  h+=trustBox(r);\n  h+='<h3>能力<span")
rep("'<dt>けがの時</dt>", "'<dt>接し方</dt><dd>'+selH(Object.keys(SHN).map(k=>[k,SHN[k]]),r.sh||'普','setR('+id+',\\'sh\\',this.value)')+'</dd>'+\n  '<dt>けがの時</dt>")
rep("'<dl class=\"kv\" style=\"margin-top:8px\"><dt>部屋の雰囲気</dt>",
    "'<dl class=\"kv\" style=\"margin-top:8px\"><dt>親方の評判</dt><dd>'+Math.round(G.jin==null?50:G.jin)+' / 100(弟子の親や学校の監督のあいだの評判。勧誘に効きます)</dd><dt>部屋の雰囲気</dt>")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
