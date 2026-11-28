<script>/* v203:面白要素(ダルマさん「全て実施」)。A 目標(30 種・進み具合)、B 幕下以下のライバル、C 兄弟子と弟弟子の絆、D 跡継ぎを何年もかけて育てる。数字はすべて推定。 */
/* ---------- B 幕下以下のライバル G.rv2=[{a:自分の部屋,b:ほかの部屋,b0,k}] ---------- */
const RV2K={doki:'同じ場所に入門した同期',near:'同じころに入門し、番付が近い'};
function rv2Of(r){return (G.rv2||[]).find(x=>x.a===r.id);}
function rv2Basho(){G.rv2=G.rv2||[];
 G.rv2=G.rv2.filter(x=>{const a=G.R[x.a],b=G.R[x.b];if(!a||!b||a.ret||b.ret||a.h!==ME()){if(a&&b&&!a.ret&&b.ret&&a.h===ME())addNews(a.n+'のライバルだった'+b.n+'が引退しました。');return false;}
  if(a.d<=1&&!x.sa){x.sa=1;addNews('📣 '+a.n+'が、ライバル '+b.n+'('+G.heya[b.h].n+')'+(b.d<=1?'に続いて':'より先に')+'関取になりました。');a.mor=cl(a.mor+4,0,100);}
  if(b.d<=1&&!x.sb){x.sb=1;if(a.d>1){addNews('📣 '+a.n+'のライバル '+b.n+'('+G.heya[b.h].n+')が、先に関取になりました。'+a.n+'は「負けていられない」と稽古に打ち込んでいます。');a.mor=cl(a.mor+3,0,100);x.boost=G.bnum+6;}}
  if(a.d<=1&&b.d<=1){if(typeof rvPair==='function'&&!rvPair(a,b)){G.rv=G.rv||[];G.rv.push({a:a.id,b:b.id,b0:G.bnum,k:'doki'});addNews('📣 '+a.n+'と'+b.n+'は、関取になってもライバルです。');}return false;}
  return true;});
 own().forEach(r=>{if(r.d<2||rv2Of(r)||G.pend.includes(r.id)||Math.random()>.2)return;
  const C=G.order.map(i=>G.R[i]).filter(o=>o&&!o.ret&&o.h!==ME()&&o.d>=2&&Math.abs((o.join||0)-(r.join||0))<=1&&Math.abs(o.pos-r.pos)<=40&&!(G.rv2||[]).some(x=>x.b===o.id));
  if(!C.length)return;const same=C.filter(o=>o.join===r.join);const o=pick(same.length?same:C);const k=o.join===r.join?'doki':'near';
  G.rv2.push({a:r.id,b:o.id,b0:G.bnum,k:k});addNews('📣 '+r.n+'と'+o.n+'('+G.heya[o.h].n+')が、若い衆のライバルとして競い合うようになりました('+RV2K[k]+')。');
  try{stPush(r,'rv','若い衆のライバル:'+o.n+'('+G.heya[o.h].n+')');}catch(e){}});
 (G.rv2||[]).forEach(x=>{const a=G.R[x.a],b=G.R[x.b];if(!a||!b)return;const ah=(a.hist||[]).slice(-1)[0],bh=(b.hist||[]).slice(-1)[0];if(!ah||!bh||ah.b!==bh.b)return;
  const ak=ah.w>ah.l+(ah.ab||0),bk=bh.w>bh.l+(bh.ab||0);if(ak&&!bk){a.mor=cl(a.mor+2,0,100);}else if(!ak&&bk){a.mor=cl(a.mor-1,0,100);x.boost=Math.max(x.boost||0,G.bnum+1);}});}
/* ---------- C 兄弟子と弟弟子の絆 r.kz={id:兄弟子,v:0〜100} ---------- */
function kzWeek(){own().forEach(r=>{if(r.ani==null)return;const a=G.R[r.ani];if(!a||a.ret)return;if(!r.kz||r.kz.id!==r.ani)r.kz={id:r.ani,v:(r.kz&&r.kz.id===r.ani)?r.kz.v:0};
  r.kz.v=Math.min(100,r.kz.v+1.2+((a.tr==null?50:a.tr)>=60?.6:0)+((r.tr==null?50:r.tr)>=60?.4:0));});}
function kzBasho(){own().forEach(r=>{const z=r.kz;if(!z||z.v<30)return;const a=G.R[z.id];if(!a)return;
  if(a.ret&&!z.rd){z.rd=1;r.mor=cl(r.mor-4,0,100);r.kzB=G.bnum+6;addNews(r.n+'は、世話になった兄弟子 '+a.n+'の引退に涙を見せました。「兄弟子の分まで」と稽古に打ち込んでいます。');try{stPush(r,'kz','兄弟子 '+a.n+'の引退。「兄弟子の分まで」');}catch(e){}return;}
  if(a.ret)return;
  if(a.d<=1&&!z.sk){z.sk=1;r.mor=cl(r.mor+4,0,100);addNews(r.n+'は、兄弟子 '+a.n+'の関取昇進を誰より喜んでいます。');}
  const ah=(a.hist||[]).slice(-1)[0];if(ah&&ah.yu&&ah.b===G.bnum-1&&z.yb!==ah.b){z.yb=ah.b;r.mor=cl(r.mor+3,0,100);addNews(r.n+'は、兄弟子 '+a.n+'の優勝に「次は自分が」と目を輝かせています。');}
  if(r.pos<a.pos&&!z.ov&&r.d<=2){z.ov=1;addNews(r.n+'が、兄弟子 '+a.n+'の番付を追い越しました。'+a.n+'は「うれしいけど悔しい」と笑っています。');a.mor=cl(a.mor+2,0,100);}});}
function kzMul(r){let m=1;if(r.kz&&r.kz.v>=30){const a=G.R[r.kz.id];if(a&&!a.ret)m*=1+Math.min(.04,r.kz.v/2500);}if(r.kzB&&G.bnum<r.kzB)m*=1.05;const x=rv2Of(r);if(x&&x.boost&&G.bnum<x.boost)m*=1.03;return m;}
function kzLv(v){return v>=80?'固い絆':v>=50?'信頼':v>=30?'仲が良い':'まだ浅い';}
/* ---------- D 跡継ぎを育てる G.ato={sid,b0,v:0〜100} ---------- */
function atoCands(){return G.staff.filter(s=>s.role==='co'&&s.myo&&s.age<60);}
function atoSet(sid){sid=+sid;if(!sid){if(G.ato)addNews('跡継ぎの指名を取り消しました。');G.ato=null;save();render();return;}const s=G.staff.find(x=>x.sid===sid);if(!s)return;
 if(G.ato&&G.ato.sid!==sid){addNews('跡継ぎを '+s.n.replace(/^元・/,'')+'親方に変えました。部屋の中に少し動揺があります。');own().forEach(r=>{r.tr=cl((r.tr==null?50:r.tr)-2,0,100);});}
 else addNews(s.n.replace(/^元・/,'')+'親方を、部屋の跡継ぎとして指名しました。');G.ato={sid:sid,b0:G.bnum,v:(G.ato&&G.ato.sid===sid)?G.ato.v:0};save();render();}
function atoBasho(){const A=G.ato;if(!A)return;const s=G.staff.find(x=>x.sid===A.sid);if(!s){addNews('跡継ぎに指名していた親方が部屋を離れました。');G.ato=null;return;}
 A.v=Math.min(100,A.v+5+(s.sk.sei>=14?2:0));if(Math.random()<.18){const ks=['osh','yot','waz','tai','sei','meki'].filter(k=>s.sk[k]<18);if(ks.length){const k=ks.sort((a,b)=>s.sk[a]-s.sk[b])[0];s.sk[k]++;addNews(s.n.replace(/^元・/,'')+'親方は跡継ぎとして親方の仕事を学び、'+SKN[k]+'が '+s.sk[k]+' に上がりました。');}}
 if(A.v>=50&&!A.m50){A.m50=1;addNews('弟子や後援会のあいだで、'+s.n.replace(/^元・/,'')+'親方が次の師匠だという声が定着してきました。');}}
function atoLv(v){return v>=80?'準備万端':v>=50?'周りも認めている':v>=20?'修行中':'指名したばかり';}
/* ---------- A 目標 ---------- */
function raised(){return Object.values(G.R).filter(r=>r.h===ME()&&(r.join||1)>1);}
function cntLv(L,lv){return L.filter(r=>stBest(r)>=lv).length;}
function yuOwn(f){return (G.yusho||[]).filter(y=>y.own&&f(y)).length;}
function gmax(k,v){G.gm=G.gm||{};G.gm[k]=Math.max(G.gm[k]||0,v);return G.gm[k];}
const GOAL=[
 ['j1','育てた弟子から関取を 1 人',()=>[cntLv(raised(),2),1]],['j3','育てた関取 3 人',()=>[cntLv(raised(),2),3]],['j5','育てた関取 5 人',()=>[cntLv(raised(),2),5]],['j10','育てた関取 10 人',()=>[cntLv(raised(),2),10]],
 ['m1','育てた幕内力士 1 人',()=>[cntLv(raised(),3),1]],['m3','育てた幕内力士 3 人',()=>[cntLv(raised(),3),3]],
 ['s1','育てた三役 1 人',()=>[cntLv(raised(),4),1]],['o1','育てた大関 1 人',()=>[cntLv(raised(),5),1]],['y1','育てた横綱 1 人',()=>[cntLv(raised(),6),1]],
 ['cj','中学卒の新弟子から関取',()=>[cntLv(raised().filter(r=>r.kind==='中学'),2),1]],['cs','中学卒の新弟子から三役',()=>[cntLv(raised().filter(r=>r.kind==='中学'),4),1]],
 ['nj','相撲未経験の新弟子から関取',()=>[cntLv(raised().filter(r=>r.kind==='未経験'),2),1]],['fj','海外出身の新弟子から関取',()=>[cntLv(raised().filter(r=>r.kind==='海外'),2),1]],
 ['yu1','幕内優勝 1 回',()=>[yuOwn(y=>y.d===0),1]],['yu3','幕内優勝 3 回',()=>[yuOwn(y=>y.d===0),3]],['yu10','幕内優勝 10 回',()=>[yuOwn(y=>y.d===0),10]],
 ['jy','十両優勝',()=>[yuOwn(y=>y.d===1),1]],['ly5','幕下以下の各段優勝 5 回',()=>[yuOwn(y=>y.d>=2),5]],
 ['sk3','関取が同時に 3 人',()=>[gmax('sk',own().filter(r=>r.d<=1).length),3]],['sk5','関取が同時に 5 人',()=>[gmax('sk',own().filter(r=>r.d<=1).length),5]],
 ['d20','弟子 20 人',()=>[gmax('dn',ownAll().length),20]],['d30','弟子 30 人',()=>[gmax('dn',ownAll().length),30]],
 ['sks','関取が 3 年(18 場所)続けて途切れない',()=>[Math.min(18,(G.skS&&G.skS.m)||0),18]],
 ['ok1','資金 1 億円',()=>[gmax('mo',Math.max(0,Math.round(G.money))),10000]],['sup','後援会 2000 人',()=>[gmax('su',G.sup||0),2000]],
 ['hm1','育てた弟子が部屋付き親方に',()=>[G.staff.filter(s=>s.role==='co'&&s.home).length,1]],
 ['mei','名人の部屋付き親方(能力 17 以上)',()=>[G.staff.filter(s=>s.role==='co'&&Object.values(s.sk).some(v=>v>=17)).length,1]],
 ['ken10','研修に 10 回出す',()=>[G.kenN||0,10]],['oka','おかみさんの能力がすべて 14 以上',()=>[G.okami?Math.min(...Object.values(G.okami.sk).map(v=>Math.min(v,14))):0,14]],
 ['rv2','若い衆のライバルと、そろって関取に',()=>[G.gm&&G.gm.rv2?1:0,1]],['kz','兄弟子と弟弟子が、そろって関取に',()=>[G.gm&&G.gm.kz?1:0,1]],
 ['y10','部屋を 10 年続ける',()=>[Math.floor((G.bnum-1)/6),10]],['y30','部屋を 30 年続ける',()=>[Math.floor((G.bnum-1)/6),30]],
 ['gen2','跡継ぎに部屋を継ぐ',()=>[((me().gen||1)>=2)?1:0,1]]];
function goalBasho(){G.gdone=G.gdone||{};const first=!G.gInit;G.gInit=1;
 own().forEach(r=>{const z=r.kz;if(z&&r.d<=1){const a=G.R[z.id];if(a&&a.d<=1&&!a.ret)gmax('kz',1);}});
 (G.rv2||[]).concat(G.rv||[]).forEach(x=>{const a=G.R[x.a],b=G.R[x.b];if(a&&b&&a.h===ME()&&x.k==='doki'&&a.d<=1&&b.d<=1)gmax('rv2',1);});
 GOAL.forEach(([k,t,f])=>{if(G.gdone[k])return;let v;try{v=f();}catch(e){return;}if(v[0]>=v[1]){if(first){G.gdone[k]=-1;return;}G.gdone[k]=G.bnum;try{achieve('g_'+k,'目標「'+t+'」');}catch(e){}}});}
function goalHTML(){G.gdone=G.gdone||{};const L=GOAL.map(([k,t,f])=>{let v=[0,1];try{v=f();}catch(e){}return {k,t,c:Math.min(v[0],v[1]),g:v[1],d:G.gdone[k]};});const n=L.filter(x=>x.d>0).length,n0=L.filter(x=>x.d<0).length;
 const row=x=>'<div class="gl'+(x.d?' gd':'')+'"><span class="gt">'+(x.d?'★ ':'')+esc(x.t)+'</span><span class="gb"><i style="width:'+Math.round(100*x.c/x.g)+'%"></i></span><span class="gn">'+(x.d?(x.d<0?'はじめから':bname(x.d)):(x.g>=1000?Math.round(100*x.c/x.g)+'%':x.c+' / '+x.g))+'</span></div>';
 const near=L.filter(x=>!x.d).sort((a,b)=>b.c/b.g-a.c/a.g);
 return '<div class="pn"><h2>部屋の目標<span class="sub">'+n+' / '+(L.length-n0)+' 達成'+(n0?'(はじめから '+n0+')':'')+'</span></h2><div class="kaku mute" style="font-size:13px;margin-bottom:6px">あと少しの目標</div>'+near.slice(0,5).map(row).join('')+
  '<details class="gall"><summary>すべての目標を見る</summary>'+L.filter(x=>x.d).map(row).join('')+near.slice(5).map(row).join('')+'</details></div>';}
function rv2HTML(){const L=(G.rv2||[]).map(x=>[G.R[x.a],G.R[x.b],x]).filter(([a,b])=>a&&b);if(!L.length)return '';
 return '<div class="pn"><h2>若い衆のライバル<span class="sub">'+L.length+' 組</span></h2><table class="tb">'+L.map(([a,b,x])=>'<tr><td class="nm">'+esc(a.n)+'<div class="mute" style="font-size:12px">'+esc(a.rkS||'')+'</div></td><td class="mute">vs</td><td class="nm">'+esc(b.n)+'<div class="mute" style="font-size:12px">'+esc(G.heya[b.h].n)+'部屋・'+esc(b.rkS||'')+'</div></td><td class="kaku mute" style="font-size:12px">'+RV2K[x.k]+'</td></tr>').join('')+'</table></div>';}
(function(){
 const dw=doWeek;doWeek=function(){const x=dw.apply(this,arguments);try{kzWeek();}catch(e){}return x;};
 const v7=v7Basho;v7Basho=function(sum){const x=v7.apply(this,arguments);try{forP(()=>{rv2Basho();kzBasho();atoBasho();goalBasho();});}catch(e){}return x;};
 const cm=coMul;coMul=function(r){const m=cm.apply(this,arguments);try{if(r&&r.h===ME())return m*kzMul(r);}catch(e){}return m;};
 if(typeof kenGo==='function'){const kg=kenGo;kenGo=function(id){const had=!!(G.ken&&G.ken[id]);const x=kg.apply(this,arguments);if(!had&&G.ken&&G.ken[id])G.kenN=(G.kenN||0)+1;return x;};}
 const sc=succeed;succeed=function(s,mode){const A=G.ato;const sup0=G.sup;const msg=sc.apply(this,arguments);try{if(A&&mode==='in'&&s.sid===A.sid){const k=Math.min(.08,A.v/1000);G.sup=Math.round(G.sup+sup0*k);own().forEach(r=>{r.tr=cl((r.tr==null?50:r.tr)+Math.round(A.v/20),0,100);});G.ato=null;return msg+'長く跡継ぎとして育ってきたので、弟子も後援会も落ち着いて新しい師匠を迎えました。';}
  if(A){own().forEach(r=>{r.tr=cl((r.tr==null?50:r.tr)-4,0,100);});G.ato=null;return msg+'指名していた跡継ぎとは別の人が継いだため、部屋に少し戸惑いが出ています。';}}catch(e){}return msg;};
 const kh=kirokuHTML;kirokuHTML=function(){let h=kh.apply(this,arguments);try{const g=goalHTML()+rv2HTML();const i=h.indexOf('<div class="pn"><h2>達成</h2>');h=i>=0?h.slice(0,i)+g+h.slice(i):g+h;}catch(e){}return h;};
 const st=staffHTML;staffHTML=function(){let h=st.apply(this,arguments);try{const age=Math.floor(me().age||40);if(age<55&&!G.ato)return h;const C=atoCands();const A=G.ato;const s=A&&G.staff.find(x=>x.sid===A.sid);
  const p='<div class="pn"><h2>跡継ぎ<span class="sub">定年 65 歳まで あと '+Math.max(0,65-age)+' 年</span></h2>'+(s?'<div class="kaku">指名:<b>'+esc(s.n.replace(/^元・/,''))+'親方</b>('+Math.floor(s.age)+'歳・年寄 '+esc(s.myo||'')+')</div><div class="gl"><span class="gt">育ち具合:'+atoLv(A.v)+'</span><span class="gb"><i style="width:'+A.v+'%"></i></span><span class="gn">'+Math.round(A.v)+'</span></div>':'<p class="kaku mute">まだ指名していません。年寄名跡を持つ 60 歳未満の部屋付き親方から選べます。</p>')+
   '<div class="btns" style="margin-top:6px">'+(C.length?selH([[0,'指名しない']].concat(C.map(x=>[x.sid,x.n.replace(/^元・/,'')+'親方('+Math.floor(x.age)+'歳)'])),A?A.sid:0,'atoSet(this.value)'):'<span class="mute kaku">候補になれる部屋付き親方がいません。</span>')+'</div>'+
   '<p class="kaku mute" style="font-size:13px">指名した親方は、場所ごとに親方の仕事を学んで育ち、能力も少しずつ上がります。育ち具合が高いほど、継いだときに弟子の信頼と後援会が落ち着いて引き継がれます。途中で指名を変えたり、指名と違う人が継いだりすると、部屋に動揺が出ます。数字は推定です。</p></div>';
  const i=h.indexOf('<div class="pn"><h2>部屋のスタッフ');h=i>=0?h.slice(0,i)+p+h.slice(i):h+p;}catch(e){}return h;};
 function deco(){try{if(UI.view!=='keiko')return;const h2=[...document.querySelectorAll('.pn>h2')].find(x=>x.firstChild&&x.firstChild.textContent==='師弟');if(!h2)return;const pn=h2.parentElement;if(pn.querySelector('.kzt'))return;
  const L=own().filter(r=>r.kz&&G.R[r.kz.id]).sort((a,b)=>b.kz.v-a.kz.v);if(!L.length)return;
  pn.insertAdjacentHTML('beforeend','<h3 class="kzt">兄弟子と弟弟子の絆</h3><table class="tb">'+L.slice(0,12).map(r=>{const a=G.R[r.kz.id];return '<tr><td class="nm">'+esc(a.n)+(a.ret?' <span class="mute">(引退)</span>':'')+'</td><td class="mute">→</td><td class="nm">'+esc(r.n)+'</td><td style="min-width:120px"><span class="gb"><i style="width:'+Math.round(r.kz.v)+'%"></i></span></td><td class="kaku">'+kzLv(r.kz.v)+'</td></tr>';}).join('')+'</table><p class="kaku mute" style="font-size:13px">兄弟子として面倒を見るうちに絆が育ちます。絆があると弟弟子の伸びが少し良くなり、兄弟子の昇進や引退が弟弟子の心を動かします。</p>');}catch(e){}}
 const R0=render;render=function(){const x=R0.apply(this,arguments);deco();return x;};
})();
</script><style>.gl{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:14px}.gl .gt{flex:1 1 50%}.gb{flex:1 1 30%;display:inline-block;height:8px;border-radius:4px;background:rgba(255,255,255,.12);overflow:hidden;min-width:60px}.gb i{display:block;height:100%;background:var(--kin,#c9a24a)}.gl .gn{flex:0 0 90px;text-align:right;font-size:12px;color:var(--mute,#999)}.gl.gd .gt{color:var(--kin,#c9a24a)}.gl.gd .gb i{background:#b5361f}.gall summary{cursor:pointer;font-size:13px;margin-top:6px;color:var(--mute,#999)}</style>
