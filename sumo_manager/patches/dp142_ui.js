<style>
#dpx{position:fixed;inset:0;z-index:60;background:rgba(20,16,12,.72);display:flex;align-items:flex-end;justify-content:center;padding:0 10px calc(10px + env(safe-area-inset-bottom))}
#dpx .in{width:100%;max-width:760px;box-sizing:border-box;background:#fffaf0;color:#1d1a16;border:2px solid #c9a24a;border-radius:10px 10px 6px 6px;box-shadow:0 -6px 24px rgba(0,0,0,.5);padding:14px 16px;max-height:88vh;overflow:auto;font-family:var(--kaku)}
#dpx h2{margin:0 0 4px;font-size:19px;display:flex;align-items:center;gap:8px}#dpx h2 .st{font-size:12px;font-weight:400;color:#7d7365;margin-left:auto}
.dpstep{display:flex;gap:4px;margin:0 0 10px}.dpstep i{flex:1;height:5px;border-radius:3px;background:#e4d8bf}.dpstep i.on{background:#b3261e}
.dpsay{display:flex;gap:10px;align-items:flex-start;margin:8px 0}.dpsay>img{width:84px;flex:none;border-radius:6px;border:3px solid #c9a24a}
.dpff{writing-mode:vertical-rl;background:linear-gradient(90deg,#d9c39a,#e9d8b4 40%,#d4bd92);border:1px solid #8e7347;font-weight:800;font-size:20px;text-align:center;padding:8px 0;min-height:110px;width:44px;flex:none;border-radius:3px;letter-spacing:.1em}
.dpsay .bb{position:relative;flex:1;min-width:0;background:#fff;border:1px solid #c9b48a;border-radius:8px;padding:8px 11px;font-size:15px;line-height:1.6}
.dpsay .bb:before{content:'';position:absolute;left:-8px;top:18px;border:8px solid transparent;border-left:0;border-right-color:#c9b48a}
.dpsay .bb b.who{display:block;font-size:12px;color:#7d7365;font-weight:400}
.dpsay.r{flex-direction:row-reverse}.dpsay.r .bb:before{left:auto;right:-8px;border-right:0;border-left:8px solid #c9b48a}
.dpnote{font-size:13px;color:#5a5044;background:#f3ead6;border-radius:6px;padding:6px 10px;margin:6px 0}
.dpbtn{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.dpbtn button{flex:1;min-width:140px;padding:9px 8px;font:15px var(--kaku);color:#1d1a16;border:1px solid #8e7347;background:#f3ead6;border-radius:6px;cursor:pointer}.dpbtn button.ai{background:#b3261e;color:#fff;border-color:#b3261e}
.dpbtn button small{display:block;font-size:11px;opacity:.8}
.dptg{display:inline-block;font-size:11px;background:#c9a24a33;border:1px solid #c9a24a88;border-radius:9px;padding:0 6px;margin:2px 3px 0 0}
.dprow{display:flex;gap:8px;align-items:center;border-bottom:1px dashed #d8c9a8;padding:6px 0}.dprow>img{width:46px;border-radius:4px;border:2px solid #c9a24a;flex:none}
.dprow .dpff{font-size:13px;min-height:62px;width:26px;padding:4px 0}
.dprow .dpnm{font:800 15px var(--kaku);min-width:4.5em}.dprow .ans{flex:1;font-size:14px}.dprow button{font:13px var(--kaku);padding:5px 8px;border:1px solid #8e7347;background:#f3ead6;border-radius:5px;color:#1d1a16}
.dpok{color:#1d6b3a;font-weight:800}.dpng{color:#b3261e;font-weight:800}.dpmg{color:#a06a00;font-weight:800}
.dpbig{display:flex;gap:14px;align-items:flex-start}.dpbig>img{width:150px;flex:none;border-radius:8px;border:3px solid #c9a24a}.dpbig>.dpff{min-height:180px;width:60px;font-size:26px}
@media (max-width:560px){.dpbig>img{width:104px}.dpsay>img{width:70px}}
.dpkan{border:3px double #b3261e;color:#b3261e;border-radius:6px;padding:10px;text-align:center;font-size:17px;font-weight:800;margin:6px 0;background:#fff}
.dpkan small{display:block;font-size:12px;font-weight:400;color:#5a5044}
.dpteam{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:8px 0}.dpteam>div{text-align:center;font-weight:800}.dpteam img{width:86px;border-radius:6px;border:3px solid #c9a24a;display:block;margin:0 auto 2px}.dpteam .dpff{margin:0 auto 2px;min-height:96px}
</style>
<script>
/* v142:独立の段取りの画面。数字と判定は dp142_core.js(dpStart・dpAns・dpMay・dpSum・dpPer・dpFin)。 */
function dpImg(a){for(const k of a){if(k&&typeof PIMG!=='undefined'&&PIMG[k])return PIMG[k];if(k&&typeof PIMGO!=='undefined'&&PIMGO[k])return PIMGO[k];}return null;}
function dpFace(keys,lab){const s=dpImg(keys);return s?'<img src="'+s+'" alt="">':'<div class="dpff">'+esc(lab)+'</div>';}
function dpSay(keys,lab,who,t,r){return '<div class="dpsay'+(r?' r':'')+'">'+dpFace(keys,lab)+'<div class="bb"><b class="who">'+esc(who)+'</b>'+esc(t)+'</div></div>';}
function dpMs(d,t){return dpSay([d.ms],d.ms||d.par,'師匠 '+d.par+'親方',t);}
function dpMe(d,t,who){return dpSay([d.n,d.sh],d.n,who||'あなた('+d.n+'親方)',t,1);}
function dpAnsTx(w){return w.fin==='go'?'<span class="dpok">ついて来る</span>':w.fin==='stay'?'<span class="dpng">残ります</span>':w.fin==='wait'?'<span class="dpmg">返事待ち</span>':'<span class="dpmg">迷っています</span>';}
function dpShow(){const d=UI.dp;let el=document.getElementById('dpx');if(!d){if(el)el.remove();return;}
 if(!el){el=document.createElement('div');el.id='dpx';document.body.appendChild(el);}
 const sn=d.st<=1?1:d.st<=3?2:d.st===4?3:4;
 let h='<h2>'+esc(d.n)+'部屋を興す<span class="st">'+['','① 師匠に打ち明ける','② 弟子に声をかける','③ 理事会','④ 門出'][sn]+'</span></h2><div class="dpstep">'+[1,2,3,4].map(i=>'<i class="'+(i<=sn?'on':'')+'"></i>').join('')+'</div>';
 if(d.st===1){h+=dpMs(d,d.sb?'……急な話だな。止めはせんが、うちの部屋にも稽古相手は要る。連れて行く者のことは、よく考えてくれ。':'そうか、部屋を持つか。……連れて行きたい者がいるなら、本人とよく話せ。送り出すからには、立派な部屋にしてもらわんとな。')+
  dpMe(d,d.sb?'わかりました。一人ずつ、きちんと話をさせてください。':'ありがとうございます。弟子たちと、一人ずつ話をさせてください。')+
  '<div class="dpnote">'+(d.sb?'師匠は<b>少し渋っています</b>。ついて来る見込みが少し下がり、元の部屋との関係も少し冷えた状態で始まります。':'師匠は<b>快く送り出してくれました</b>。元の部屋との関係も良いままです。')+'</div><div class="dpbtn"><button class="ai" onclick="dpGo(2)">弟子に声をかけに行く</button></div>';}
 else if(d.st===2){const w=d.L[d.i];
  h+='<div style="font-size:13px;color:#7d7365">声をかけるのは '+d.L.length+' 人。'+(d.i+1)+' 人目</div><div class="dpbig">'+dpFace([w.n],w.n)+'<div style="flex:1;min-width:0"><div style="font-size:20px;font-weight:800">'+esc(w.n)+' <span style="font-size:13px;font-weight:400">'+esc(w.rk||'')+(w.age?'・'+w.age+'歳':'')+'</span></div>'+w.tg.map(t=>'<span class="dptg">'+esc(t)+'</span>').join('')+
   '<div class="dpsay" style="margin-top:6px"><div class="bb"><b class="who">'+esc(w.n)+(w.how?'(親方が'+esc(w.how)+'あと)':'')+'</b>'+esc(w.ln)+'</div></div></div></div>';
  if(w.ans==='mayo'&&!w.fin)h+='<div class="dpnote"><span class="dpmg">迷っています</span>。どう話しますか。</div><div class="dpbtn"><button onclick="dpM(0)">稽古の方針を語る<small>同じ大学の後輩や内弟子に効きやすい</small></button><button onclick="dpM(1)">親御さんに会いに行く<small>同郷・同じ高校に効きやすい</small></button><button onclick="dpM(2)">答えを待つ<small>門出の前に返事が来る</small></button></div>';
  else h+='<div class="dpnote">'+dpAnsTx(w)+'</div><div class="dpbtn"><button class="ai" onclick="dpNext()">'+(d.i+1<d.L.length?'次の人へ':'返事をまとめる')+'</button></div>';}
 else if(d.st===3){h+=dpMe(d,'声をかけた '+d.L.length+' 人の返事がそろった。')+d.L.map(w=>'<div class="dprow">'+dpFace([w.n],w.n)+'<span class="dpnm">'+esc(w.n)+'<br><small style="font-weight:400">'+esc(w.rk||'')+'</small></span><span class="ans">'+dpAnsTx(w)+' 「'+esc(w.ln)+'」</span>'+(w.fin==='stay'&&!w.per?'<button onclick="dpP(\''+w.n+'\')">もう一度説得</button>':'')+'</div>').join('');
  const s=d.L.filter(w=>w.fin==='stay'&&!w.per);
  if(s.length)h+='<div class="dpnote">残ると言った力士には、もう一度だけ説得できます(見込み:'+s.map(w=>esc(w.n)+' '+(dpPerP(w,d.sb)>=.5?'五分以上':dpPerP(w,d.sb)>=.35?'やや低め':'低い')).join('、')+')。断られると、元の部屋との関係が少し冷えます。</div>';
  h+='<div class="dpbtn"><button class="ai" onclick="dpGo(4)">'+(s.length?'本人の気持ちを尊重して次へ':'理事会へ')+'</button></div>';}
 else if(d.st===4){const g=dpGoN(d);h+='<div class="dpkan">日本相撲協会 理事会<br>'+esc(d.n)+'部屋の新設を承認<small>'+esc(d.par)+'部屋から独立。力士 '+g.length+' 人とともに出発</small></div>'+
  dpMs(d,d.cool>0?'承認が下りたか。……まあ、しっかりやれ。':'承認が下りたな。これからは師匠同士だ。土俵では手加減せんぞ。')+'<div class="dpbtn"><button class="ai" onclick="dpGo(5)">門出へ</button></div>';}
 else {const g=d.L.filter(w=>w.fin==='go'),s=dpStayN(d);h+=dpMe(d,'今日から'+d.n+'部屋だ。人数は少ないが、そのぶん一人ひとりをしっかり見る。まずは全員で関取を目指そう。','新しい師匠 '+d.n+'親方')+
  '<div class="dpteam">'+g.map(w=>'<div>'+dpFace([w.n],w.n)+esc(w.n)+'</div>').join('')+'</div>'+(s.length?'<div class="dpnote">元の部屋に残った力士:'+s.map(esc).join('・')+'</div>':'')+'<div class="dpbtn"><button class="ai" onclick="dpEnd()">新しい部屋を始める</button></div>';}
 el.innerHTML='<div class="in">'+h+'</div>';el.querySelector('.in').scrollTop=0;}
function dpGo(st){const d=UI.dp;if(!d)return;if(st===2){d.i=0;dpAns(d,0);}if(st===4)dpSum(d);d.st=st;dpShow();}
function dpNext(){const d=UI.dp;if(!d)return;if(d.i+1<d.L.length){d.i++;dpAns(d,d.i);d.st=2;}else{dpSum(d);d.st=3;}dpShow();}
function dpM(k){const d=UI.dp;if(!d)return;dpMay(d,d.i,k);dpShow();}
function dpP(n){const d=UI.dp;if(!d)return;dpPer(d,n);dpShow();}
function dpEnd(){const d=UI.dp;if(!d)return;UI.dp=null;dpShow();UI.start=null;UI.title=false;dpFin(d);save();UI.view='home';render();}
const dpDS0=doStartDok;doStartDok=function(n){if(typeof mpDkOn==='function'&&mpDkOn())return dpDS0(n);/* 二人相撲の親は今まで通り */const ws=[...document.querySelectorAll('.dkw input:checked')].map(e=>e.value);if(!ws.length)return;const x=dokList().find(y=>y.n===n);if(!x)return;
 UI.dp=dpStart(x,ws,$('#r_t').value);if(!UI.dp.L.length){UI.dp=null;return;}try{heyaClose();}catch(z){}dpShow();};
</script>
