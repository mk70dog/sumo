# v160 -> v161:稽古の画面のスクロールを減らす(見本 kk5「たためる見出し」。ダルマさん「kk2は少しわかりにくい」→ kk4・kk5 →「お任せします」)。
#   「稽古」の上の部分(週を過ごす・おすすめ・稽古日・出稽古・育つ環境・番付ごとにまとめて決める)は今までどおり開いたまま。
#   「ひとりずつ決める」は 1 人 1 行の一覧(番付・四股名・調子と疲労の点・今週の稽古)にして、見出しでたたむ。行を押すとその人のカードが開く。
#   下の「部屋付き親方の担当・師弟・ちゃんこと体作り・巡業・稽古の種類・部屋の指導力」も 1 行の見出しにたたむ。
#   開け閉めは UI に覚える(ボタンを押して画面が描き直されても閉じない)。描き直しのあとに DOM を組み替える(render の後処理)。
#   ついでに直す:「初日の見込み」(.pkm)の地が白っぽい半透明で、暗い色の組だと緑の字が読めなかった → 地を灰色の薄い色に。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=160;\nconst SAVE='sumoManager160',SAVE159", "const APPV=161;\nconst SAVE='sumoManager161',SAVE160='sumoManager160',SAVE159")
rep('[SAVE159,SAVE158', '[SAVE160,SAVE159,SAVE158')
rep('<title>Grand Sumo Manager v160', '<title>Grand Sumo Manager v161')
rep('.pkm{font:12px sans-serif;margin:4px 0;padding:2px 8px;background:#fff6;border-radius:4px}', '.pkm{font:12px sans-serif;margin:4px 0;padding:2px 8px;background:rgba(127,127,127,.14);border-radius:4px}')
BLOCK = r"""<style>
/* v161 稽古の画面:たためる見出し(見本 kk5) */
.kacc{border:1px solid var(--line);border-radius:8px;background:var(--paper);margin:8px 0}
.kacc>summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.kacc>summary::-webkit-details-marker{display:none}
.kacc>summary b{font-size:16px;color:var(--sumi)}.kacc>summary small{color:var(--mute);font-size:12px}
.kacc>summary::after{content:'▼ ひらく';margin-left:auto;font-size:12px;color:var(--mute)}
.kacc[open]>summary::after{content:'▲ たたむ'}
.kacc>.pn{margin:0;border:none;box-shadow:none}
.kacc>.pn>h2{display:none}
.kacc>.kl{padding:0 10px 10px}
.kl{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:4px}
.kr{display:grid;grid-template-columns:62px 1fr auto;gap:2px 6px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.kr .rk{font-size:11px;color:var(--mute)}.kr .n{font-weight:700;color:var(--sumi)}.kr .w{font-size:12px;color:var(--mute);grid-column:2/4}
.kr .st{font-size:11px;color:var(--mute);white-space:nowrap;text-align:right}
.kr .st::after{content:' ▼'}.kr.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}.kr.op .st::after{content:' ▲'}
.kr.warn{border-color:var(--shu)}
.kopen{grid-column:1/-1}.kopen>.kc{margin:0 0 6px}
.kdot{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 2px 0 6px;background:#888}.kdot.g{background:var(--midori)}.kdot.y{background:var(--kin)}.kdot.r{background:var(--shu)}
@media (max-width:760px){.kl{grid-template-columns:1fr}}
</style>
<script>
(function(){
UI.kkO=UI.kkO||{};UI.kkA=UI.kkA||{};
const R0=render;
render=function(){const r=R0.apply(this,arguments);try{if(UI.view==='keiko')kkFold();}catch(e){console.error(e);}return r;};
function acc(key,title,small){const d=document.createElement('details');d.className='kacc';if(UI.kkA[key])d.open=true;d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=title;d.querySelector('small').textContent=small||'';d.addEventListener('toggle',()=>{UI.kkA[key]=d.open;});return d;}
function kkFold(){
 const h3=[...document.querySelectorAll('h3')].find(e=>e.textContent.trim()==='ひとりずつ決める');
 const pn=h3?h3.closest('.pn'):null;
 if(h3){const kcs=h3.nextElementSibling;if(kcs&&kcs.classList.contains('kcs')){
  const cards=[...kcs.children];const L=document.createElement('div');L.className='kl';
  cards.forEach(c=>{const a=c.querySelector('[onclick^="showR("]');const id=a?+(a.getAttribute('onclick').match(/\d+/)||[0])[0]:0;const r=G.R[id];if(!r)return;
   const on=[...c.querySelectorAll('.krow')].map(x=>(x.querySelector('button.on')||{}).textContent).filter(Boolean);
   const w0=c.querySelector('.kcw');const w=w0?w0.cloneNode(true):null;if(w)w.querySelectorAll('button,.kctag').forEach(x=>x.remove());let wt=(w?w.textContent:'').replace(/\s+/g,' ').trim();if(/口を出しています/.test(wt))wt='自分で決めた';
   const ca=r.cond>=70?'g':r.cond<35?'r':'',fa=r.fat>=70?'r':r.fat>=45?'y':'g';
   const row=document.createElement('div');row.className='kr'+(UI.kkO[id]?' op':'')+((r.inj||r.fat>=70||r.cond<35)?' warn':'');
   row.innerHTML='<span class="rk"></span><span class="n"></span><span class="st"><span class="kdot '+ca+'"></span>調子 '+Math.round(r.cond)+'<span class="kdot '+fa+'"></span>疲労 '+Math.round(r.fat)+'</span><span class="w"></span>';
   row.querySelector('.rk').textContent=c.querySelector('.wsr')?c.querySelector('.wsr').textContent:'';row.querySelector('.n').textContent=r.n;
   row.querySelector('.w').textContent=[wt].concat(on).filter(Boolean).join('・')+(r.inj?'(けが)':'');
   const box=document.createElement('div');box.className='kopen';box.style.display=UI.kkO[id]?'':'none';box.appendChild(c);
   row.addEventListener('click',()=>{UI.kkO[id]=!UI.kkO[id];row.classList.toggle('op',!!UI.kkO[id]);box.style.display=UI.kkO[id]?'':'none';});
   L.appendChild(row);L.appendChild(box);});
  const d=acc('one','ひとりずつ決める',cards.length+' 人・行を押すと、その人の稽古を細かく決められます(目標・型・初日の見込みも)');
  h3.replaceWith(d);kcs.replaceWith(document.createComment(''));d.appendChild(L);}}
 [...document.querySelectorAll('.pn')].filter(e=>e!==pn&&!e.parentElement.closest('.pn')&&!e.closest('.kacc')).forEach(e=>{const h=e.querySelector(':scope>h2');if(!h)return;
  const t=(h.childNodes[0]&&h.childNodes[0].nodeType===3?h.childNodes[0].textContent:h.textContent).trim();if(!t||/稽古を決める人/.test(t))return;
  const sm=(h.querySelector('.sub')||{}).textContent||'';const d=acc('p:'+t,t,sm);e.parentNode.insertBefore(d,e);d.appendChild(e);});
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
