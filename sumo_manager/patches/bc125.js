<script>
/* v125 の画面:本場所の「場所中の過ごし方」(見本 bc1+bc3 の「おすすめにする」)、稽古タブの「初日の見込み」(見本 bcm)。
   効き目の計算は本体の bcDay(場所中の毎日の終わり)と bcDef(始めの設定)。 */
const BCA={し:'しっかり',軽:'軽め',休:'休む'},BCP={昼:'昼寝',治:'治療',自:'自由時間'};
function bcGrpOf(r){return r.d<=1?'関取':r.d===2?'幕下':'三段目以下';}
function bcList(){const B=G.B;if(!B)return [];return own().filter(r=>B.rec[r.id]&&!B.rec[r.id].ky).sort((a,b)=>a.pos-b.pos);}
function bcSetR(id,k,v){const r=G.R[id];if(!r)return;r[k==='a'?'bca':'bcp']=v;save();bcRe();}
function bcSetG(g,k,v){bcList().filter(r=>bcGrpOf(r)===g).forEach(r=>{r[k==='a'?'bca':'bcp']=v;});save();bcRe();}
function bcAuto(){bcList().forEach(r=>{r.bca=r.fat>60?'休':r.cond<50&&r.fat<40?'し':'軽';r.bcp=r.inj?'治':r.fat>50?'昼':(r.mor<40?'自':'昼');});save();bcRe();toast('疲れの多い力士は休ませ、けが人は治療にしました');}
function bcRe(){const y=scrollY;render();scrollTo(0,y);}
function bcPick(id){const r=G.R[id];if(!r)return;const o=bcDef(r);
 const row=(k,M,cur)=>Object.keys(M).map(x=>'<button class="btn'+(cur===x?' main':'')+'" onclick="bcSetR('+id+',\''+k+'\',\''+x+'\');closeM()">'+M[x]+'</button>').join(' ');
 openM('<h2>'+esc(r.rkS)+' '+esc(r.n)+'</h2><p class="kaku">調子 '+Math.round(r.cond)+'・疲労 '+Math.round(r.fat)+'・気力 '+Math.round(r.mor)+(r.inj?'・<span class="shu">けが('+esc(r.inj.p)+')</span>':'')+'</p><h3>朝稽古</h3><div class="btns">'+row('a',BCA,o.a)+'</div><h3>午後</h3><div class="btns">'+row('p',BCP,o.p)+'</div><div class="btns" style="margin-top:10px"><button class="btn" onclick="closeM()">閉じる</button></div>');}
function bcBar(v,c){return '<span class="bcbar"><i style="width:'+Math.round(cl(v,0,100))+'%;background:'+c+'"></i></span>';}
function bcHTML(){const L=bcList();if(!L.length||!G.B||G.B.day>=15)return '';
 const gs=['関取','幕下','三段目以下'].filter(g=>L.some(r=>bcGrpOf(r)===g));
 const meal=G.meal&&G.meal.k==='ソップ'?'<span class="mute">ちゃんこはソップ(鶏)=勝負メシで気力 +</span>':'';
 return '<div class="pn bcp"><h2>場所中の過ごし方<span class="sub">明日の朝稽古と午後。番付ごとにまとめて決めて、札を押すと 1 人ずつ変えられます</span></h2>'+
  '<div class="btns" style="margin:0 0 6px"><button class="btn main" onclick="bcAuto()">おすすめにする(疲れていたら休ませる)</button> '+meal+'</div>'+
  gs.map(g=>{const R=L.filter(r=>bcGrpOf(r)===g);const same=k=>{const v=bcDef(R[0])[k];return R.every(r=>bcDef(r)[k]===v)?v:'';};
   return '<div class="bcg"><b>'+g+' '+R.length+' 人</b><div class="bcr"><span class="lb">朝稽古</span>'+Object.keys(BCA).map(x=>'<button class="pc'+(same('a')===x?' on':'')+'" onclick="bcSetG(\''+g+'\',\'a\',\''+x+'\')">'+BCA[x]+'</button>').join('')+
   '<span class="lb">午後</span>'+Object.keys(BCP).map(x=>'<button class="pc'+(same('p')===x?' on':'')+'" onclick="bcSetG(\''+g+'\',\'p\',\''+x+'\')">'+BCP[x]+'</button>').join('')+'</div>'+
   '<div class="bcc">'+R.map(r=>{const o=bcDef(r);return '<div class="bck" onclick="bcPick('+r.id+')"><div><span class="mute">'+esc(r.rkS)+'</span> <b class="nm">'+esc(r.n)+'</b>'+(r.inj?' <span class="shu" style="font-size:11px">けが</span>':'')+'</div><div class="mute" style="font-size:11px">調子 '+bcBar(r.cond,'#7aa7d8')+' 疲労 '+bcBar(r.fat,r.fat>60?'#d66':'#8c8')+'</div><div class="bct">'+BCA[o.a]+'・'+BCP[o.p]+'</div></div>';}).join('')+'</div></div>';}).join('')+
  '<p class="mute" style="font-size:12px;margin:4px 0 0">朝稽古:しっかり=四股・すり足・ぶつかり(その日の取組の力 +0.5%・調子 +0.6・疲労 +1/日)/軽め=四股・すり足/休む=疲労 −3/日、その日の取組の力 −0.5%(体が重い)。午後:昼寝=疲労 −1/治療=けがの治りが早い(治療院と契約で大きい)/自由時間=気力 +。数字は推定。</p></div>';}
const bcB0=bashoHTML;bashoHTML=function(){let h=bcB0();let x='';try{x=bcHTML();}catch(e){try{sysLog('場所中の過ごし方',e);}catch(z){}}if(!x)return h;
 const i=h.indexOf('日目の取組');if(i<0)return h+x;const j=h.lastIndexOf('<div class="pn',i);return j<0?h+x:h.slice(0,j)+x+h.slice(j);};
/* 稽古タブ:初日の見込み */
function pkGuess(r){const L=(r.ld||[]).slice();const done=L.length;const rem=Math.max(0,WEEKS-done);const pl=r.inj&&r.inj.s>=2?0:(r.menu==='休'?0:(+r.it||0)+1);
 for(let i=0;i<rem;i++)L.push(pl);if(L.length<4)return null;const e=L.slice(0,-2),l=L.slice(-2);const av=a=>a.reduce((x,y)=>x+y,0)/a.length;
 let b=(av(e)>=2.6?3:av(e)>=2?1:0)+(av(l)<=1.5?3:av(l)<=2?0:-2)+(r.fat<25?1:0)-(r.fat>60?6:0);
 const w=b>=7?'仕上がり上々':b>=3?'まずまず':b<=-3?'疲れが残る':'ふつう';const c=b>=7?'#2e7d4f':b>=3?'#5a8f3a':b<=-3?'#b5391f':'#888';
 let t='';if(r.fat>60)t='疲労 '+Math.round(r.fat)+'。休養か軽めで疲れを抜く';else if(av(l)>1.5&&rem>=1)t='最後の 2 週を軽めにすると上がります';else if(av(e)<2)t='前半の稽古が少なめ';else if(b>=7)t='このままで仕上がります';
 return {b:b,w:w,c:c,t:t};}
const bcK0=keikoHTML;keikoHTML=function(){let h=bcK0();if(G.phase!=='train')return h;
 const cnt={'仕上がり上々':0,'まずまず':0,'ふつう':0,'疲れが残る':0};
 h=h.replace(/(<div class="kch">[\s\S]*?showR\((\d+)\)[\s\S]*?<\/div>)/g,(m,a,id)=>{const r=G.R[id];if(!r||r.h!==ME())return m;const g=pkGuess(r);if(!g)return m;cnt[g.w]++;
  return a+'<div class="pkm" style="border-left:4px solid '+g.c+'"><b style="color:'+g.c+'">初日の見込み:'+g.w+(g.b?'(調子 '+(g.b>0?'+':'−')+Math.abs(Math.round(g.b*1.6))+')':'')+'</b>'+(g.t?'<br><span>'+esc(g.t)+'</span>':'')+'</div>';});
 const n=Object.values(cnt).reduce((x,y)=>x+y,0);if(!n)return h;
 const sum='<div class="pkall">初日の見込み(部屋全体):上々 '+cnt['仕上がり上々']+' 人・まずまず '+cnt['まずまず']+' 人・ふつう '+cnt['ふつう']+' 人・'+(cnt['疲れが残る']?'<b style="color:#b5391f">疲れが残る '+cnt['疲れが残る']+' 人</b>':'疲れが残る 0 人')+' <span class="mute">前半 4 週しっかり → 最後の 2 週を軽めにすると、初日の調子が上がります。いまの稽古の決め方のまま進めたときの見込みです。</span></div>';
 const i=h.indexOf('<div class="pn');return i<0?sum+h:h.slice(0,i)+sum+h.slice(i);};
</script>
<style id="bc125">.bcp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 10px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important}.bcp .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
.bcp .lb{font:bold 13px sans-serif;margin:0 4px 0 8px}.bcg{border:1px solid var(--line);border-radius:8px;padding:8px;margin:6px 0}.bcr{display:flex;align-items:center;flex-wrap:wrap;gap:2px;margin:4px 0}
.bcc{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:6px;margin-top:6px}.bck{border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:13px;cursor:pointer}.bct{font-size:12px;color:var(--ai)}
.bcbar{display:inline-block;width:46px;height:7px;background:#0002;border-radius:4px;overflow:hidden;vertical-align:middle}.bcbar i{display:block;height:100%}
.pkm{font:12px sans-serif;margin:4px 0;padding:2px 8px;background:#fff6;border-radius:4px}.pkall{font:13px sans-serif;background:#fff3cf;color:#1a140c;border-radius:8px;padding:6px 10px;margin:4px 0 8px}</style>
