/* --- 注目選手のカード(見本 oshi3) --- */
function oshiGoal(r){const h=r.hist&&r.hist.length?r.hist[r.hist.length-1]:null;const ls=h?'(前の場所 '+h.w+'勝'+h.l+'敗'+(h.ab?h.ab+'休':'')+')':'';
 if(r.d===2){const k=r.pos-divStart(2)+1;return k<=15?'十両まで:幕下 '+k+' 枚目。<b>大きく勝ち越せば</b>手が届く'+ls:'次の目標:<b>幕下上位(15 枚目以内)</b>'+ls;}
 if(r.d>=3)return '次の目標:<b>'+DIVS[r.d-1].n+'に上がる</b>'+ls;
 if(r.d===1)return '次の目標:<b>勝ち越し</b>して幕内へ'+ls;
 if(r.t==='Y')return '次の目標:<b>優勝</b>'+ls;
 return '次の目標:<b>'+(r.t?'二桁勝利':'勝ち越し')+'</b>'+ls;}
function oshiHTML(){const r=oshiR();if(!r)return '';const L=oshiItems(r);const n=L.length;
 const pos=L.map((x,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;return [50+40*Math.cos(a),50+40*Math.sin(a)];});
 const col=c=>c==='p'?'var(--shu)':c==='n'?'var(--ai)':'var(--line)';
 const ms=[];const yrs=Math.max(0,G.bnum-(r.join||1));if(r.join>1)ms.push('初土俵から '+yrs+' 場所');if(r.best&&r.best<r.pos)ms.push('自己最高位まであと '+Math.ceil((r.pos-r.best)/2)+' 枚');if(r.daiki)ms.push('大器晩成');
 return '<div class="oc"><h2><span class="st">★</span>注目選手<button class="chg" onclick="oshiPick()">変える</button></h2><div><a class="nm" onclick="showR('+r.id+')">'+esc(r.n)+'</a><span class="rk">'+esc(r.rkS)+'・'+Math.floor(r.age)+' 歳'+(r.home?'・'+esc(r.home):'')+'</span></div><div class="goal">'+oshiGoal(r)+'</div>'+
 '<div class="ow"><div class="ring"><svg>'+pos.map((p,i)=>'<line x1="50%" y1="50%" x2="'+p[0]+'%" y2="'+p[1]+'%" stroke="'+col(L[i].c)+'" stroke-width="'+(L[i].c==='0'?1.5:3)+'"/>').join('')+'</svg><div class="c">'+esc(r.n)+'</div>'+L.map((x,i)=>'<div class="pb s'+x.c+'" style="left:'+pos[i][0]+'%;top:'+pos[i][1]+'%"><b>'+x.lb+'</b>'+esc(x.t)+'</div>').join('')+'</div>'+
 '<ul class="ol">'+L.map(x=>'<li class="s'+x.c+'"><b>'+x.lb+'</b>'+(x.c==='p'?' <span class="ob sp">追い風</span>':x.c==='n'?' <span class="ob sn">向かい風</span>':'')+'<br><span>'+esc(x.s)+'</span></li>').join('')+'</ul></div>'+
 '<div class="ms">'+(ms.length?'節目:'+ms.join('/')+'/':'')+'追い風は気持ちを少し上げ、向かい風は少し下げます。本場所では結果のいちばん上に出ます。</div></div>';}
function oshiPick(){const o=own().slice().sort((a,b)=>a.pos-b.pos);const cur=oshiR();
 openM('<h2>注目選手を選ぶ</h2><p class="kaku mute">部屋を見守るうえで、追いかけたい力士を選びます。成績には影響しません。</p><div class="opl">'+o.map(r=>'<button class="btn'+(cur&&cur.id===r.id?' main':'')+'" onclick="G.oshi='+r.id+';save();closeM();render()">'+esc(r.n)+' <small>'+esc(r.rkS)+'</small></button>').join('')+'</div><div class="row" style="margin-top:10px"><button class="btn" onclick="G.oshi=null;save();closeM();render()">部屋頭にもどす(自動)</button><button class="btn" onclick="closeM()">閉じる</button></div>');}
