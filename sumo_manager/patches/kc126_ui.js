<script>
/* v126 の画面:稽古タブの上に「誰が決めているか」(親方・部屋付き親方の指導の色)と「親方におまかせ」、力士の札に理由と「口を出す/おまかせに戻す」。
   手で稽古・強さ・午後・場所中の過ごし方を変えた力士は r.kMan(口を出した)。 */
function kcName(){const H=G.heya[ME()]||{};return (H.o||'師匠').replace(/^元・/,'')+'親方';}
function kcCos(){return G.staff.filter(s=>s.role==='co');}
function kcAsTxt(s){const a=coA(s);if(a.t==='one'){const r=G.R[a.r];return r?r.n+'に付きっきり':'付きっきり';}return a.t==='seki'?'関取担当':a.t==='waka'?'若い衆担当':a.t==='sk'?'得意分野':'全体';}
function kcSetMan(ids){(ids||[]).forEach(i=>{const r=G.R[i];if(r)r.kMan=1;});}
function kcBack(id){const r=G.R[id];if(!r)return;delete r.kMan;const p=kcPlan(r);r.menu=p[0];r.it=p[1];r.pm=p[2];r.kWhy=p[3];save();const y=scrollY;render();scrollTo(0,y);}
function kcBackAll(){own().forEach(r=>{delete r.kMan;});kcWeek();save();const y=scrollY;render();scrollTo(0,y);toast('全員を親方におまかせにしました');}
function kcToggle(){G.kAuto=G.kAuto===false?true:false;if(G.kAuto)kcWeek();save();render();}
if(typeof ktSet==='function'){const k0=ktSet;ktSet=function(id,k,v){const ids=id==='all'?ownAll().map(r=>r.id):Array.isArray(id)?id:[id];kcSetMan(ids);return k0.apply(this,arguments);};}
if(typeof bcSetR==='function'){const b0=bcSetR;bcSetR=function(id){kcSetMan([id]);return b0.apply(this,arguments);};
 const b1=bcSetG;bcSetG=function(g){kcSetMan(bcList().filter(r=>bcGrpOf(r)===g).map(r=>r.id));return b1.apply(this,arguments);};
 const b2=bcAuto;bcAuto=function(){kcSetMan(bcList().map(r=>r.id));return b2.apply(this,arguments);};}
function kcHead(){const on=G.kAuto!==false,k=kcOfH(ME()),H=G.heya[ME()]||{},st=KCTRAD[H.n]?KCTRAD[H.n]+'(部屋の型)':kcStyleH(ME());const man=own().filter(r=>r.kMan).length;
 const tag=c=>'<span class="kctag kc-'+c+'">'+KC[c].n+'</span>';
 const rows='<div class="kcrow"><b>'+esc(kcName())+'</b>(師匠)'+tag(k)+'<span class="mute">取り口 '+esc(st)+'・'+esc(KC[k].d)+'</span></div>'+kcCos().map(s=>'<div class="kcrow"><b>'+esc(s.n.replace(/^元・/,''))+'親方</b>('+esc(kcAsTxt(s))+')'+tag(kcOfS(s))+'<span class="mute">取り口 '+esc(kcStyleS(s))+'</span></div>').join('');
 if(UI.kcV===2)return '<div class="kch2">'+(on?'今週の稽古は <b>'+esc(kcName())+'</b>'+tag(k)+(kcCos().length?' と部屋付き親方 '+kcCos().length+' 人':'')+'が決めています。':'<b>親方におまかせ:オフ</b>(稽古は自分で決めます)。')+(man&&on?' <span class="mute">口を出している力士 '+man+' 人</span>':'')+' <button class="btn sm" onclick="kcToggle()">'+(on?'自分で決める':'親方におまかせ')+'</button></div>';
 return '<div class="pn kch1"><h2>稽古を決める人<span class="sub">'+(on?'親方におまかせ(担当の親方が毎週決めます)':'自分で決めています')+'</span></h2>'+rows+
  '<div class="btns" style="margin-top:6px"><button class="btn'+(on?'':' main')+'" onclick="kcToggle()">'+(on?'おまかせをやめて自分で決める':'親方におまかせにする')+'</button>'+(man&&on?'<button class="btn" onclick="kcBackAll()">口を出した '+man+' 人もおまかせに戻す</button>':'')+'</div>'+
  '<p class="mute" style="font-size:12px;margin:4px 0 0">指導の色で伸び方とけがが変わります。入門 3 年までの力士は、担当の親方の取り口(部屋の型)の方へ伸びやすくなります。数字は推定。</p></div>';}
function kcCard(r){if(G.kAuto===false||r.h!==ME())return '';const c=kcCoach(r);
 if(r.d<=1&&!r.inj&&tourWk()&&!r.kMan)return '<div class="kcw"><span class="kctag kc-'+c.kc+'">'+esc(c.co?c.n:'師匠')+'</span> 巡業に同行(巡業の朝稽古)</div>';
 if(r.kMan)return '<div class="kcw man">口を出しています <button class="btn sm" onclick="kcBack('+r.id+')">おまかせに戻す</button></div>';
 return '<div class="kcw"><span class="kctag kc-'+c.kc+'">'+esc(c.co?c.n:'師匠')+'</span> '+esc(r.kWhy||'')+'</div>';}
const kcK0=keikoHTML;keikoHTML=function(){let h=kcK0();if(G.phase!=='train')return h;
 h=h.replace(/(<div class="kch">[\s\S]*?showR\((\d+)\)[\s\S]*?<\/div>)/g,(m,a,id)=>{const r=G.R[id];if(!r)return m;return a+kcCard(r);});
 const x=kcHead();const i=h.indexOf('<div class="pn');return i<0?x+h:h.slice(0,i)+x+h.slice(i);};
/* 初日の見込み:おまかせの力士は、担当の親方がこれから決める稽古で見込む */
const kcPG=pkGuess;pkGuess=function(r){if(G.kAuto===false||r.kMan||r.h!==ME())return kcPG(r);const k=kcCoach(r).kc;
 const L=(r.ld||[]).slice();const done=L.length;for(let w=done+1;w<=WEEKS;w++){const late=w>=WEEKS-1;L.push(r.fat>58?1:late?(k==='mou'?2:1):(k==='mou'?3:2));}
 if(L.length<4)return null;const e=L.slice(0,-2),l=L.slice(-2);const av=a=>a.reduce((x,y)=>x+y,0)/a.length;
 const b=(av(e)>=2.6?3:av(e)>=2?1:0)+(av(l)<=1.5?3:av(l)<=2?0:-2)+(r.fat<25?1:0)-(r.fat>60?6:0);
 const w=b>=7?'仕上がり上々':b>=3?'まずまず':b<=-3?'疲れが残る':'ふつう';const c=b>=7?'#2e7d4f':b>=3?'#5a8f3a':b<=-3?'#b5391f':'#888';
 const t=k==='mou'?'猛稽古派の親方は場所前も量を落としません':r.fat>60?'疲れが多いので、親方が休ませながら整えます':'親方が場所前の 2 週を軽めにして仕上げます';
 return {b:b,w:w,c:c,t:t};};
/* 本場所:過ごし方の札に理由 */
const kcBH=bcHTML;bcHTML=function(){let h=kcBH();if(!h||G.kAuto===false)return h;const L=bcList();const man=L.filter(r=>r.kMan).length;
 return h.replace('<div class="btns" style="margin:0 0 6px">','<p style="font-size:13px;margin:0 0 6px">'+esc(kcName())+'が明日の朝稽古と午後を決めています'+(man?'(口を出している力士 '+man+' 人)':'')+'。ボタンで変えると「口を出す」になります。</p><div class="btns" style="margin:0 0 6px">');};
</script>
<style id="kc126">.kch1 .kcrow{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:4px 0;border-bottom:1px dashed var(--line);font-size:14px}.kch1 .kcrow .mute{font-size:12px}
.kctag{display:inline-block;font:bold 12px sans-serif;padding:1px 8px;border-radius:10px;color:#fff;background:#888}.kc-mou{background:#b5391f}.kc-kiso{background:#5a7a3a}.kc-jis{background:#2f6aa8}.kc-riro{background:#7a5aa8}
.kch2{font:14px sans-serif;background:#fff3cf;color:#1a140c;border-radius:8px;padding:6px 10px;margin:4px 0 8px}
.kcw{font:12px sans-serif;margin:3px 0;padding:2px 6px;border-radius:4px;background:#0000000d}.kcw.man{background:#fff3cf;color:#1a140c}.kcw .btn{margin-left:6px}</style>
