<style>
/* v153:部屋の会話(見本 cv1+cv3) */
.cvbub{position:absolute;z-index:40;display:flex;flex-direction:column;gap:8px;top:10px;pointer-events:none}
.cvb{display:flex;gap:8px;align-items:flex-start;pointer-events:auto;cursor:pointer;animation:cvin .35s ease-out}
.cvb.r{flex-direction:row-reverse}
.cvb img{width:50px;height:64px;object-fit:cover;border-radius:4px;border:2px solid #e9d39a;flex:none;box-shadow:0 2px 8px rgba(0,0,0,.45)}
.cvb .dpff{min-height:64px;width:28px;font-size:13px;flex:none}
.cvb .bb{background:rgba(251,246,234,.97);color:#1d1a16;border:1px solid #8e7347;border-radius:12px;padding:7px 11px;font-size:15px;line-height:1.55;box-shadow:0 3px 10px rgba(0,0,0,.4);text-shadow:none}
.cvb .bb b{display:block;font-size:11px;color:#7d7365;font-weight:400}
.cvb.old{opacity:.7}
.cvctl{display:flex;gap:6px;justify-content:flex-end;pointer-events:auto}
.cvctl button{font:700 13px var(--kaku,serif);padding:5px 12px;border-radius:6px;border:1px solid #c9a24a;background:#1d1a16;color:#e9d39a}
@keyframes cvin{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (max-width:760px){.cvb .bb{font-size:14px}.cvb.old{display:none}}
.cvov{position:fixed;inset:0;background:rgba(10,8,6,.55);z-index:900;display:flex;align-items:center;justify-content:center;padding:14px}
.cvbox{background:#fbf6ea;color:#1d1a16;border:3px double #8e7347;border-radius:10px;max-width:720px;width:100%;max-height:88vh;overflow:auto;padding:14px 16px;box-shadow:0 10px 40px rgba(0,0,0,.5);text-shadow:none}
.cvbox h2{margin:0 0 4px;font:800 20px var(--kaku,serif);display:flex;justify-content:space-between;align-items:baseline;gap:8px;color:#1d1a16}
.cvbox h2 small{font-size:13px;color:#7d7365;font-weight:400}
.cvbox .dpsay .bb{background:#fff;border:1px solid #d8c9a8;border-radius:10px;padding:8px 10px;font-size:15px;line-height:1.6;color:#1d1a16}
.cvbox .dpsay.r{flex-direction:row-reverse}.cvbox .dpsay.r .bb{background:#f1e6cc}
.cvbox .dpsay img{width:64px;height:84px;object-fit:cover;border-radius:4px;border:1px solid #8e7347;flex:none}
.cvbox .who{display:block;font-size:12px;color:#7d7365}
.cvbtn{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
.cvbtn button{font:700 15px var(--kaku,serif);padding:8px 16px;border-radius:6px;border:1px solid #8e7347;background:#fff;color:#1d1a16}
.cvbtn button.ai{background:#1d1a16;color:#e9d39a;border-color:#c9a24a}
.cvdots{display:flex;gap:4px;margin:2px 0 8px}.cvdots i{width:18px;height:4px;background:#d8c9a8;border-radius:2px}.cvdots i.on{background:#b5361f}
.cvre{display:block;width:100%;font:700 12px var(--kaku,serif);margin:2px 0 6px;padding:3px 8px;border-radius:9px;border:1px solid rgba(154,43,29,.45);background:rgba(154,43,29,.07);color:#9a2b1d;text-align:left}
</style>
<script>
/* v153:部屋の会話(ダルマさん「ホームの画面に親方をはじめ色々な方面から会話形式のコメントをポップアップで表示。独立モード時のはじめのやり取りのような会話形式」→ 見本 cv1&3)。
   ふだんの週=部屋の絵の上に 2〜4 人の吹き出し(cv3)。番付発表のあと・初日の前・千秋楽のあと=中央の会話の窓(cv1)。
   中身は今の数値から作る(koePeople の話+親方の返し)。見せ方だけで、数値は変わらない。 */
function cvSp(k,lb,who,t,r){return {k:k,lb:lb,who:who,t:t,r:r?1:0};}
function cvOya(){const h=me();return {k:[h.o2],lb:h.n+'親方',who:h.n+'親方'};}
function cvOk(){return G.okami?{k:[],lb:G.okami.n,who:G.okami.n+'(おかみさん)'}:null;}
function cvR(r,tag){return {k:[r.n,r.kk],lb:r.n,who:r.n+'('+(r.rkS||'')+(tag?'・'+tag:'')+')'};}
function cvS(p,t,r){return cvSp(p.k,p.lb,p.who,t,r);}
function cvPick(a,s){return a.length?a[Math.abs(s)%a.length]:null;}
/* ふだんの週:部屋の声から 1〜2 人+親方の返し */
function cvWeek(){if(!G||G.over||typeof koePeople!=='function')return [];const K=koePeople();if(!K.length)return [];
 const sd=G.bnum*7+G.wk;const L=[];const oy=cvOya();const shi=K.find(p=>p.role==='師匠');
 const others=K.filter(p=>p.role!=='師匠');
 if(shi&&shi.lines.length)L.push(cvS(oy,cvPick(shi.lines,sd)));
 const a=cvPick(others,sd);if(a){const ln=cvPick(a.lines,sd+1);const r=own().find(x=>x.n===a.who);
  L.push(cvSp(r?[r.n,r.kk]:[],a.who,a.who+'('+a.role+')',ln,1));
  const rep=/痛|けが/.test(ln)?'焦るな。治してからが勝負だ。':/新弟子/.test(ln)?'いい子がいたら、まず会ってみよう。':/疲れ/.test(ln)?'少し軽めにするか。体が資本だからな。':/雰囲気|元気/.test(ln)?'稽古場の空気は、上の者が作るものだ。':/調子|好調|動け/.test(ln)?'その調子だ。気を抜くなよ。':'わかった。頼むぞ。';
  L.push(cvS(oy,rep));}
 const b=cvPick(others.filter(p=>p!==a),sd+3);if(b&&L.length<4)L.push(cvSp([],b.who,b.who+'('+b.role+')',cvPick(b.lines,sd+2),1));
 return L.slice(0,4);}
/* 大事な場面 */
function cvScene(){if(!G||G.over)return null;const o=own().filter(r=>!r.ret);if(!o.length)return null;const oy=cvOya(),ok=cvOk();const top=heyaTop();const L=[];let t='';
 const last=r=>(r.hist&&r.hist.length)?r.hist[r.hist.length-1]:null;
 if(G.phase==='post'){t='千秋楽を終えて';const rc=r=>{const x=B_rec(r);return x?x.w-x.l-x.ab:-99;};const s=o.filter(r=>B_rec(r)).sort((a,b)=>rc(b)-rc(a));if(!s.length)return null;
  const best=s[0],worst=s[s.length-1],bx=B_rec(best),wx=B_rec(worst);
  L.push(cvS(oy,'みんな、15 日間ご苦労だった。'+(bx.yu?best.n+'、よくやった。優勝だ。':best.n+'は '+bx.w+' 勝。よく踏ん張った。')));
  L.push(cvS(cvR(best),bx.w>bx.l+bx.ab?'ありがとうございます。来場所はもっと上を目指します。':'まだまだです。稽古をやり直します。',1));
  if(worst!==best&&wx.w<wx.l+wx.ab){L.push(cvS(oy,worst.n+'は '+wx.w+' 勝 '+(wx.l+wx.ab)+' 敗か。'+(wx.ab?'まず体を治せ。':'下を向くな。')));L.push(cvS(cvR(worst),wx.ab?'はい…。早く治して戻ります。':'悔しいです。次は勝ち越します。',1));}
  if(ok)L.push(cvS(ok,'今夜はちゃんこを多めに作りますね。みんな、ゆっくり休んで。',1));}
 else if(G.phase==='train'&&G.wk===1){t='番付発表を受けて';const ch=o.map(r=>{const h=last(r);return {r,d:h&&h.pos!=null?h.pos-r.pos:0,h};}).filter(x=>x.h);
  const up=ch.filter(x=>x.d>0).sort((a,b)=>b.d-a.d)[0],dn=ch.filter(x=>x.d<0).sort((a,b)=>a.d-b.d)[0];
  L.push(cvS(oy,'新しい番付が出た。'+(top?top.n+'は'+top.rk+'だ。':'')));
  if(up){L.push(cvS(oy,up.r.n+'、'+(up.h.rk||'')+'から'+up.r.rk+'へ上がったな。'));L.push(cvS(cvR(up.r),'はい。番付に名前が大きく載って、身が引き締まります。',1));}
  if(dn){L.push(cvS(oy,dn.r.n+'は'+dn.r.rk+'に下がった。ここからだぞ。'));L.push(cvS(cvR(dn.r),'わかっています。すぐに取り戻します。',1));}
  if(ok)L.push(cvS(ok,'後援会の皆さんにも、新しい番付をお知らせしておきます。',1));}
 else if(G.phase==='train'&&G.wk===WEEKS){t='初日を前に';const inj=o.filter(r=>r.inj&&r.inj.s>=2);
  L.push(cvS(oy,'いよいよ初日だ。'+(top?top.n+'、部屋頭として頼むぞ。':'')));
  if(top)L.push(cvS(cvR(top,'部屋頭'),(top.cond||50)>=60?'体はよく動いています。いい場所にします。':'少し体が重いですが、やるだけです。',1));
  if(inj.length)L.push(cvS(oy,inj.map(r=>r.n).join('・')+'は無理をするな。'));
  if(ok)L.push(cvS(ok,'場所中は勝負メシを用意しておきますね。',1));}
 else return null;
 return L.length>=2?{key:G.bnum+'-'+G.phase+'-'+G.wk,t:t,L:L}:null;}
function cvKey(){return G.bnum+'-'+G.phase+'-'+G.wk;}
function cvOn(){return !!(G&&!G.over&&UI.view==='home'&&!(typeof MPG!=='undefined'&&UI.mpGuest)&&!UI.cvOff);}
function cvBubHTML(){if(!cvOn())return '';const k=cvKey();if((G.cvW||'')===k)return '';const L=cvWeek();if(!L.length)return '';
 const n=Math.min(L.length,UI.cvN&&UI.cvK===k?UI.cvN:1);
 return '<div class="cvbub">'+L.slice(0,n).map((x,i)=>'<div class="cvb'+(x.r?' r':'')+(i<n-1?' old':'')+'" onclick="cvNext()">'+dpFace(x.k,x.lb)+'<div class="bb"><b>'+esc(x.who)+'</b>'+esc(x.t)+'</div></div>').join('')+
  '<div class="cvctl">'+(n<L.length?'<button onclick="cvNext()">▶ 次へ '+n+'/'+L.length+'</button>':'')+'<button onclick="cvClose()">閉じる</button></div></div>';}
function cvNext(){const k=cvKey();if(UI.cvK!==k){UI.cvK=k;UI.cvN=1;}UI.cvN++;const L=cvWeek();if(UI.cvN>L.length){cvClose();return;}render();}
function cvClose(){G.cvW=cvKey();UI.cvN=1;save();render();}
function cvModalHTML(){if(!cvOn())return '';const S=cvScene();if(!S)return '';if((G.cvS||'')===S.key&&!UI.cvRe)return '';
 const n=Math.min(S.L.length,UI.cvM||2);
 return '<div class="cvov"><div class="cvbox"><h2>'+esc(S.t)+'<small>'+esc(bname(G.bnum))+' ・ 部屋の会話 '+n+'/'+S.L.length+'</small></h2><div class="cvdots">'+S.L.map((x,i)=>'<i class="'+(i<n?'on':'')+'"></i>').join('')+'</div>'+
  S.L.slice(0,n).map(x=>dpSay(x.k,x.lb,x.who,x.t,x.r)).join('')+'<div class="cvbtn"><button onclick="cvMDone()">'+(n<S.L.length?'あとで読む':'閉じる')+'</button>'+(n<S.L.length?'<button class="ai" onclick="UI.cvM='+(n+1)+';render()">次へ</button>':'')+'</div></div></div>';}
function cvMDone(){const S=cvScene();if(S)G.cvS=S.key;UI.cvM=2;UI.cvRe=0;save();render();}
function cvReopen(){UI.cvRe=1;UI.cvM=2;G.cvW='';render();}
/* 部屋の絵(hbStage、描いたあとに差し込まれる)に吹き出しと「会話」ボタン、部屋の画面(homeHTML)に会話の窓 */
function cvPlace(){const old=document.getElementById('cvbub');if(old)old.remove();const st=document.querySelector('.hbs');if(!st)return;const b=cvBubHTML();if(!b)return;
 const R=st.getBoundingClientRect();const nar=innerWidth<760;const d=document.createElement('div');d.id='cvbub';d.innerHTML=b;const c=d.firstChild;
 c.style.position='absolute';c.style.top=(R.top+scrollY+8)+'px';c.style.left=(R.left+scrollX+R.width*(nar?.03:.21))+'px';c.style.width=(R.width*(nar?.94:.52))+'px';
 document.body.appendChild(d);}
const cvRen0=render;render=function(){const o=document.getElementById('cvbub');if(o)o.remove();return cvRen0.apply(this,arguments);};
const cvFit0=hbFit;hbFit=function(){cvFit0.apply(this,arguments);cvPlace();};
const cvSt0=hbStage;hbStage=function(){let h=cvSt0();
 return h.replace('<div class="hbk">部屋の声<small>押すと話が聞けます</small></div>','<div class="hbk">部屋の声<small>押すと話が聞けます</small></div><button class="cvre" onclick="cvReopen()">💬 今週の会話を聞く</button>');};
const cvHome0=homeHTML;homeHTML=function(){return cvHome0()+cvModalHTML();};
</script>
