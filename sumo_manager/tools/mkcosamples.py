# 見本 co1〜3:稽古の画面で部屋付き親方に担当を決める(v61 に見本用の script を足す。選んでも見本なので効き目はない)
base=open('sumo_manager_v61.html',encoding='utf-8').read()
JS=r'''
<style>
.cot{width:100%;border-collapse:collapse;font-size:14px}.cot td{padding:6px 6px;border-bottom:1px dashed var(--line);vertical-align:middle}.cot select{font-size:14px;max-width:100%}
.cog{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:10px}
.coc{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:var(--paper)}
.coc .nm{font-weight:700}.coc .sk{font-size:12px;color:var(--mute)}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}.chip{font-size:13px;padding:3px 9px;border-radius:14px;border:1px solid var(--line);background:transparent;color:var(--sumi);cursor:pointer}.chip.on{background:var(--shu);color:#fff;border-color:var(--shu)}
.coe{font-size:12px;color:var(--mute);margin-top:5px}
.cob{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--ai);color:var(--ai);margin-left:4px;white-space:nowrap}
</style>
<script>
(function(){
const V=__V__;
const T=[['all','全体'],['seki','関取担当'],['waka','若い衆担当'],['one','付きっきり'],['sk','得意分野にしぼる']];
const EFF={all:'得意分野の指導を全員に(今のまま)',seki:'関取の伸び +6%・調子の波が小さく',waka:'幕下以下の伸び +5%・入門2年以内にやめる人 −10%',one:'選んだ弟子の伸び +12%・信頼が上がる',sk:'その種類の稽古の効き +15%(ほかは少し下がる)'};
const SKL=[['osh','押し'],['yot','四つ'],['waz','技'],['tai','体作り'],['sei','心']];
UI.coAs=UI.coAs||{};
window.coSet=(sid,k)=>{UI.coAs[sid]=Object.assign(UI.coAs[sid]||{},{t:k});render();};
window.coOne=(sid,v)=>{UI.coAs[sid]=Object.assign(UI.coAs[sid]||{},{r:v});render();};
window.coSk=(sid,v)=>{UI.coAs[sid]=Object.assign(UI.coAs[sid]||{},{s:v});render();};
const co=()=>G.staff.filter(s=>s.role==='co');
const sub=(s)=>{const a=UI.coAs[s.sid]||{t:'all'};const o=own().slice().sort((x,y)=>x.pos-y.pos);
 if(a.t==='one')return '<select onchange="coOne('+s.sid+',this.value)">'+o.map(r=>'<option value="'+r.id+'"'+(String(a.r)===String(r.id)?' selected':'')+'>'+esc(r.n)+'('+esc(r.rkS)+')</option>').join('')+'</select>';
 if(a.t==='sk')return '<select onchange="coSk('+s.sid+',this.value)">'+SKL.map(([k,n])=>'<option value="'+k+'"'+(a.s===k?' selected':'')+'>'+n+'('+SKN[k]+' '+s.sk[k]+')</option>').join('')+'</select>';
 return '';};
const best=s=>{const L=SKL.slice().sort((x,y)=>s.sk[y[0]]-s.sk[x[0]]);return L.slice(0,2).map(([k,n])=>n+' '+s.sk[k]).join('・');};
function panel(){const L=co();if(!L.length)return '<div class="pn"><h2>部屋付き親方の担当</h2><p class="mute kaku">部屋付き親方がいません。</p></div>';
 const note='<p class="kaku mute" style="font-size:12px;margin-top:6px">見本です(選んでも効き目はありません)。効き目の数字は推定。担当を決めない親方は「全体」のまま。</p>';
 if(V===1)return '<div class="pn"><h2>部屋付き親方の担当<span class="sub">'+L.length+' 人</span></h2><table class="cot">'+L.map(s=>{const a=UI.coAs[s.sid]||{t:'all'};return '<tr><td><b>'+esc(s.n)+'</b><br><span class="mute" style="font-size:12px">得意 '+best(s)+'</span></td><td><select onchange="coSet('+s.sid+',this.value)">'+T.map(([k,n])=>'<option value="'+k+'"'+(a.t===k?' selected':'')+'>'+n+'</option>').join('')+'</select> '+sub(s)+'<div class="coe">'+EFF[a.t]+'</div></td></tr>';}).join('')+'</table>'+note+'</div>';
 if(V===2)return '<div class="pn"><h2>部屋付き親方の担当<span class="sub">ボタンで選ぶ</span></h2><div class="cog">'+L.map(s=>{const a=UI.coAs[s.sid]||{t:'all'};return '<div class="coc"><div class="nm">'+esc(s.n)+'</div><div class="sk">得意 '+best(s)+'</div><div class="chips">'+T.map(([k,n])=>'<button class="chip'+(a.t===k?' on':'')+'" onclick="coSet('+s.sid+',\''+k+'\')">'+n+'</button>').join('')+'</div>'+(sub(s)?'<div style="margin-top:6px">'+sub(s)+'</div>':'')+'<div class="coe">'+EFF[a.t]+'</div></div>';}).join('')+'</div>'+note+'</div>';
 // V3:小さな担当の欄+弟子の一覧に「見る親方」の札
 return '<div class="pn"><h2>部屋付き親方の担当<span class="sub">弟子の一覧に札が出ます</span></h2><div class="chips">'+L.map(s=>{const a=UI.coAs[s.sid]||{t:'all'};return '<span style="display:inline-flex;align-items:center;gap:4px;border:1px solid var(--line);border-radius:8px;padding:3px 6px"><b style="font-size:13px">'+esc(s.n.replace(/^元・/,''))+'</b><select onchange="coSet('+s.sid+',this.value)">'+T.map(([k,n])=>'<option value="'+k+'"'+(a.t===k?' selected':'')+'>'+n+'</option>').join('')+'</select>'+sub(s)+'</span>';}).join('')+'</div>'+note+'</div>';}
function who(r){const L=co().filter(s=>{const a=UI.coAs[s.sid]||{t:'all'};return (a.t==='seki'&&r.d<=1)||(a.t==='waka'&&r.d>=2)||(a.t==='one'&&String(a.r)===String(r.id));});return L.map(s=>'<span class="cob">'+esc(s.n.replace(/^元・/,''))+(((UI.coAs[s.sid]||{}).t==='one')?'(付きっきり)':'')+'</span>').join('');}
const ok=keikoHTML;keikoHTML=function(){let h=ok();const d=document.createElement('div');d.innerHTML=h;
 const first=d.querySelector('.pn');if(first){const t=document.createElement('div');t.innerHTML=panel();first.after(...t.childNodes);}
 if(V===3){d.querySelectorAll('[data-rid],tr').forEach(()=>{});own().forEach(r=>{d.querySelectorAll('td b,td').forEach(e=>{if(e.closest('select'))return;if(e.children.length===0&&e.textContent===r.n&&!e.dataset.cb){e.dataset.cb=1;e.insertAdjacentHTML(e.tagName==='TD'?'beforeend':'afterend',who(r));}});});}
 return d.innerHTML;};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;const L=co();if(L[0])UI.coAs[L[0].sid]={t:'seki'};if(L[1])UI.coAs[L[1].sid]={t:'waka'};{const o=own().filter(r=>r.d>=2);const t=L[2]||L[1];if(t&&L.length>=3)UI.coAs[t.sid]={t:'one',r:o[0]&&o[0].id};}go('keiko');}catch(e){console.error(e)}},80);});
})();
</script>
'''
NOTE={1:'co1:表で選ぶ(1 行 1 人)',2:'co2:親方ごとのカード+ボタン',3:'co3:小さな担当の欄+弟子の名前の横に担当の親方の札'}
for v in (1,2,3):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'</div></body>',1).replace('<title>Sumo Manager v61</title>','<title>見本 co%d</title>'%v,1)
    open('samples/co%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
