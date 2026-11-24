# v165 -> v166:力士の画面のスクロールを減らす(見本 rk3「段ごとにたたむ表」。ダルマさん「実施」→ rk1〜rk3 →「3」)。
#   「付け人」は 1 行の見出しにたたむ(見出しに関取の人数)。
#   「弟子たち」は 1 人 1 行の表(番付・四股名〔年齢・体格・型〕・総合・素質・調子・疲労・人気・前場所。スマホは人気と前場所を省く)にして、
#   「関取/幕下/三段目/序二段・序ノ口・前相撲」の見出しで分ける。最初は関取だけ開いている。行を押すと今までどおり力士の詳しい画面。
#   開け閉めは UI に覚える。作り:render の後処理 rkFold()。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=165;\nconst SAVE='sumoManager165',SAVE164", "const APPV=166;\nconst SAVE='sumoManager166',SAVE165='sumoManager165',SAVE164")
rep('[SAVE164,SAVE163', '[SAVE165,SAVE164,SAVE163')
rep('<title>Grand Sumo Manager v165', '<title>Grand Sumo Manager v166')
BLOCK = r"""<style>
/* v166 力士:段ごとにたたむ表(見本 rk3) */
.rtb{width:100%;border-collapse:collapse}
.rtb th{font-size:12px;color:var(--mute);text-align:left;padding:4px 6px;border-bottom:1px solid var(--line);font-weight:400;white-space:nowrap}
.rtb td{padding:6px;border-bottom:1px solid var(--line);vertical-align:middle;white-space:nowrap}
.rtb tr.rr{cursor:pointer}.rtb tr.rr:hover td{background:rgba(201,162,74,.08)}
.rtb .n{font-weight:700;color:var(--sumi)}.rtb small{display:block;font-size:11px;color:var(--mute);font-weight:400}
.rtb .g{color:var(--midori)}.rtb .r{color:var(--shu)}.rtb .y{color:var(--kin)}
.rtb .tag{font-size:10px;padding:0 4px;margin-left:4px}
.kacc>.rgw{padding:0 10px 8px}
@media (max-width:760px){.rtb .hs{display:none}.rtb td,.rtb th{padding:5px 3px;font-size:13px}.rtb td.n,.rtb small{white-space:normal}}
</style>
<script>
(function(){
UI.rkA=UI.rkA||{sk:true};
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='rikishi')rkFold();}catch(e){console.error(e);}return x;};
function acc(key,title,small){const d=document.createElement('details');d.className='kacc';if(UI.rkA[key])d.open=true;d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=title;d.querySelector('small').textContent=small||'';d.addEventListener('toggle',()=>{UI.rkA[key]=d.open;});return d;}
function rkFold(){
 const H=t=>[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith(t));
 const ht=H('付け人');if(ht){const pn=ht.parentElement;if(!pn.closest('.kacc')){const d=acc('tk','付け人','関取 '+ownAll().filter(r=>r.d<=1).length+' 人の身の回りの世話・付け人の割り当て');pn.parentNode.insertBefore(d,pn);d.appendChild(pn);}}
 const hd=H('弟子たち');if(!hd)return;const cards=hd.parentElement.querySelector(':scope>.cards');if(!cards)return;
 const D=[...cards.children].map(c=>{const id=+(((c.getAttribute('onclick')||'').match(/showR\((\d+)/)||[])[1]);const r=G.R[id];if(!r)return null;
  const s=[...(c.querySelector('.sts')||{children:[]}).children];const val=k=>{const i=s.findIndex(e=>e.textContent===k);return i>=0&&s[i+2]?s[i+2].textContent:'';};
  const inf=c.querySelector('.info');const kids=inf?[...inf.children]:[];
  return {c,r,rk:(inf&&inf.querySelector('.rk')||{}).textContent||'',info:kids.slice(1,3).map(e=>e.textContent).join('・'),sg:val('総合'),so:val('素質'),pop:val('人気'),
   prev:((inf&&inf.querySelector(':scope>.mute'))||{}).textContent||'',tags:[...c.querySelectorAll('.tag')].map(t=>t.outerHTML).join('')};}).filter(Boolean);
 if(!D.length)return;
 const cc=x=>x>=70?'g':x<35?'r':'',fc=x=>x>=70?'r':x>=45?'y':'g';
 const table=L=>{const t=document.createElement('table');t.className='rtb';t.innerHTML='<tr><th>番付</th><th>四股名</th><th>総合</th><th>素質</th><th>調子</th><th>疲労</th><th class="hs">人気</th><th class="hs">前場所</th></tr>';
  L.forEach(d=>{const tr=document.createElement('tr');tr.className='rr';tr.addEventListener('click',()=>showR(d.r.id));const c=Math.round(d.r.cond),f=Math.round(d.r.fat);
   tr.innerHTML='<td></td><td class="n"><span></span>'+d.tags+'<small></small></td><td></td><td class="y"><b></b></td><td class="'+cc(c)+'">'+c+'</td><td class="'+fc(f)+'">'+f+'</td><td class="hs"></td><td class="hs"></td>';
   const td=tr.children;td[0].textContent=d.rk;td[1].querySelector('span').textContent=d.r.n;td[1].querySelector('small').textContent=d.info;td[2].textContent=d.sg;td[3].querySelector('b').textContent=d.so;td[6].textContent=d.pop;td[7].textContent=d.prev.replace(/^前場所\s*/,'');
   t.appendChild(tr);});return t;};
 const GR=[['sk','関取',d=>d.r.d<=1],['ms','幕下',d=>d.r.d===2],['sd','三段目',d=>d.r.d===3],['lo','序二段・序ノ口・前相撲',d=>!(d.r.d<=3)]];
 const W=document.createElement('div');
 GR.forEach(([k,t,f])=>{const L=D.filter(f);if(!L.length)return;const inj=L.filter(d=>d.r.inj).length;const d=acc(k,t,L.length+' 人'+(inj?'・けが '+inj+' 人':''));const w=document.createElement('div');w.className='rgw';w.appendChild(table(L));d.appendChild(w);W.appendChild(d);});
 cards.replaceWith(W);
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
