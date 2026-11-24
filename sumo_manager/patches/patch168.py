# v164 -> v165:新弟子の画面のスクロールを減らす(見本 ns1「1 人 1 行」。ダルマさん「実施」→ ns1〜ns3 →「1」)。
#   「新弟子集めのしくみ」(長い説明)と「学校とのつきあい」(見出しに紹介してくれる学校の数)を 1 行の見出しにたたむ。
#   候補は 1 人 1 行(出身・名前・経歴・注目の札・素質・今の力・他部屋の関心)。行を押すと今までのカード(会いに行く・勧誘)が開く。
#   他部屋の関心が 60 以上の候補は金の枠。開け閉めは UI に覚える(候補は勧誘のボタンの id で)。作り:render の後処理 nsFold()。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=164;\nconst SAVE='sumoManager164',SAVE163", "const APPV=165;\nconst SAVE='sumoManager165',SAVE164='sumoManager164',SAVE163")
rep('[SAVE163,SAVE162', '[SAVE164,SAVE163,SAVE162')
rep('<title>Grand Sumo Manager v164', '<title>Grand Sumo Manager v165')
BLOCK = r"""<style>
/* v165 新弟子:1 人 1 行(見本 ns1) */
.nl{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:4px;margin-top:6px}
.nr{display:grid;grid-template-columns:44px 1fr auto;gap:2px 8px;align-items:center;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--washi2);cursor:pointer}
.nr .pf{grid-row:1/3;writing-mode:vertical-rl;font-weight:700;color:var(--sumi2);font-size:13px;text-align:center;max-height:4.5em;overflow:hidden}
.nr .n{font-weight:700;color:var(--sumi)}.nr .n small{font-weight:400;font-size:11px;color:var(--mute);margin-left:6px}
.nr .s{font-size:12px;color:var(--mute);grid-column:2/4}.nr .s b{color:var(--kin)}
.nr .x{font-size:11px;color:var(--mute);text-align:right;white-space:nowrap}.nr .x::after{content:'▼'}
.nr.hot{border-color:var(--kin)}
.nr.op{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}.nr.op .x::after{content:'▲'}
.nopen{grid-column:1/-1}.nopen>.card{max-width:none!important;width:auto!important;margin:0 0 6px}
.kacc>.skc>h3{display:none}
@media (max-width:760px){.nl{grid-template-columns:1fr}}
</style>
<script>
(function(){
UI.nsO=UI.nsO||{};UI.nsA=UI.nsA||{};
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='scout')nsFold();}catch(e){console.error(e);}return x;};
function acc(key,el,title,small){const d=document.createElement('details');d.className='kacc';if(UI.nsA[key])d.open=true;d.innerHTML='<summary><b></b><small></small></summary>';d.querySelector('b').textContent=title;d.querySelector('small').textContent=small||'';d.addEventListener('toggle',()=>{UI.nsA[key]=d.open;});el.parentNode.insertBefore(d,el);d.appendChild(el);}
function nsFold(){
 const h2=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith('新弟子'));if(!h2)return;const pn=h2.parentElement;
 const hl=pn.querySelector(':scope>.hl');if(hl)acc('hl',hl,'新弟子集めのしくみ','スカウトの流れ・新弟子検査・入門の条件');
 const skc=pn.querySelector(':scope>.skc');if(skc){const n=skc.querySelectorAll('.st.ok').length;acc('skc',skc,'学校とのつきあい','紹介してくれる学校 '+n+' 校・挨拶や出稽古で関係を深める');}
 pn.querySelectorAll('.cards.sc').forEach(cards=>{const C=[...cards.children].filter(c=>c.classList.contains('card'));if(!C.length)return;const L=document.createElement('div');L.className='nl';
  C.forEach((c,i)=>{const inf=c.querySelector('.info');if(!inf)return;
   const btn=c.querySelector('[onclick*="doTrack("],[onclick*="doOffer("]');const key=btn?((btn.getAttribute('onclick')||'').match(/'([^']+)'/)||[])[1]:'i'+i;
   const rkE=inf.querySelector('.rk');const rk=rkE?[...rkE.childNodes].filter(x=>x.nodeType===3).map(x=>x.textContent).join('').trim():'';
   const tags=rkE?[...rkE.querySelectorAll('.tag')].map(x=>x.textContent).join('・'):'';
   const line=p=>[...inf.children].find(e=>e.textContent.startsWith(p));
   const now=(line('今の力')||{textContent:''}).textContent.replace('今の力:','').trim();
   const so=line('素質');const soB=so?so.querySelector('b'):null;
   const gi=c.querySelector('.sts i');const kw=gi?Math.round(parseFloat(gi.style.width)||0):null;
   const row=document.createElement('div');row.className='nr'+(kw!==null&&kw>=60?' hot':'')+(UI.nsO[key]?' op':'');
   row.innerHTML='<div class="pf"></div><div class="n"><span></span><small></small></div><div class="x"></div><div class="s"></div>';
   row.querySelector('.pf').textContent=(c.querySelector('.fuda')||{}).textContent||'';
   row.querySelector('.n span').textContent=(inf.querySelector('.nm')||{}).textContent||'';
   row.querySelector('.n small').textContent=rk+(tags?' ・'+tags:'');
   const S=row.querySelector('.s');S.append('素質 ');const b=document.createElement('b');b.textContent=soB?soB.textContent:'?';S.append(b,' ・ 今の力 '+now+(kw!==null?' ・ 他部屋の関心 '+kw:''));
   const box=document.createElement('div');box.className='nopen';box.style.display=UI.nsO[key]?'':'none';
   row.addEventListener('click',()=>{UI.nsO[key]=!UI.nsO[key];row.classList.toggle('op',!!UI.nsO[key]);box.style.display=UI.nsO[key]?'':'none';});
   box.appendChild(c);L.appendChild(row);L.appendChild(box);});
  cards.replaceWith(L);
  L.insertAdjacentHTML('beforebegin','<p class="mute kaku" style="font-size:12px;margin:6px 0 2px">1 人 1 行。押すと、会いに行く・勧誘のボタンが開きます。金の枠=ほかの部屋も強く狙っている。</p>');});
}
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
