# 見本 mino1〜2:力士の画面の「身のこなし」(体幹の札・隠れた資質)/ ta1〜2:新弟子の候補に「ほかの競技から」/ ken1〜2:運動能力検査
# v70 の本体に、見本用の表示だけを足す(中身の数字は見本の値。ゲームの計算は変えていない)。
base=open('sumo_manager_v70.html',encoding='utf-8').read()

CSS='''<style>
.spt{display:inline-block;font-size:11px;padding:0 6px;border-radius:3px;margin-left:4px;background:#2c3e5c;color:#fff;vertical-align:1px}
.spt.j{background:#2c3e5c}.spt.w{background:#7a4a1e}.spt.b{background:#3d6b4f}
.mn{font-size:12px;line-height:1.5;margin-top:3px}.mn b{color:var(--ai)}
.stars{color:var(--kin);letter-spacing:1px}.stars i{font-style:normal;color:#bbb}
.ktb{width:100%;border-collapse:collapse;font-size:13px;margin:6px 0}.ktb td,.ktb th{padding:3px 6px;border-bottom:1px solid #8884;text-align:left}.ktb td.n{text-align:right}
.ok{color:#2e7d4f;font-weight:bold}.ng{color:var(--shu);font-weight:bold}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}.chips button{border:1px solid #8886;background:transparent;border-radius:14px;padding:3px 10px;font-size:13px}.chips button.on{background:var(--ai);color:#fff}
</style>'''

JS=r'''
<script>
(function(){
const V='__V__';
const star=n=>'<span class="stars">'+'★'.repeat(n)+'<i>'+'★'.repeat(5-n)+'</i></span>';
/* ---- 力士の画面 ---- */
function mino(){
 const r=own().slice().sort((a,b)=>a.pos-b.pos)[0];r.kn=70;go('heya');showR(r.id);
 const rows=[...document.querySelectorAll('.atr')];const kr=rows.find(x=>x.textContent.indexOf('腰の重さ')===0);
 if(kr){const sp=kr.querySelector('span');const em=sp.querySelector('em');
  if(V==='mino1'){em.outerHTML='<em class="atp mi">体格−1.2</em> <em class="atp pu">体幹+1.8</em>';}
 }
 const dls=[...document.querySelectorAll('dl.kv')];const hd=dls.find(d=>[...d.querySelectorAll('dt')].some(t=>t.textContent==='性格'));
 if(hd){
  if(V==='mino1')hd.insertAdjacentHTML('beforeend','<dt>身のこなし<span class="nw" style="font-size:10px;color:var(--shu)">新</span></dt><dd>体幹が強く、運動神経がいい<div class="mute" style="font-size:12px">腰の重さ・瞬発力・柔軟性・土俵際の粘りが少し高い。引き技・足技・逆転が決まりやすい</div></dd>');
  else hd.insertAdjacentHTML('beforeend','<dt>身のこなし<span class="nw" style="font-size:10px;color:var(--shu)">新</span></dt><dd>'+star(4)+' 高い<div class="mute" style="font-size:12px">星 5 つが最高。体幹・瞬発力・柔軟性・土俵際に効く。見極めが進むと星が出ます</div></dd>');
 }
}
/* ---- 新弟子の候補 ---- */
const SP=[
 {s:'柔道',c:'j',k:'大学・21歳',h:'前の競技:柔道(全国学生 3 位・大学柔道部)',f:'投げ・足技・柔軟性が高め。組むのが得意で、突き押しは低め',m:4},
 {s:'レスリング',c:'w',k:'社会人・24歳',h:'前の競技:レスリング(社会人・全日本選手権 5 位)',f:'低い姿勢・体幹・瞬発力が高め。足取りが得意',m:5},
 {s:'柔術',c:'b',k:'社会人・23歳',h:'前の競技:ブラジリアン柔術(茶帯)',f:'柔軟性・土俵際・我慢強さが高め。体は小さめ',m:3}];
function fixHl(){const h=document.querySelector('.hl');if(h)h.innerHTML=h.innerHTML.replace('(身長・体重の基準は 2023 年に撤廃されました)','(身長 167cm・体重 67kg の基準に届かない人は、運動能力検査を受けます)');}
function prospects(){
 go('scout');fixHl();
 const cs=[...document.querySelectorAll('.cards.sc > .card')].slice(0,3);
 cs.forEach((c,i)=>{const d=SP[i];if(!d)return;const info=c.querySelector('.info');
  const rk=info.querySelector('.rk');rk.firstChild.textContent=d.k;
  if(V==='ta1'){rk.insertAdjacentHTML('beforeend','<span class="spt '+d.c+'">'+d.s+'</span>');
   const nm=info.querySelector('.nm');nm.insertAdjacentHTML('afterend','<div class="mn"><b>'+d.h+'</b><br>'+d.f+'(推定)<br>相撲は未経験:立ち合い・突き押しは低めから始まり、最初の 1〜2 年は伸びがゆっくり。身のこなし '+star(d.m)+'</div>');}
  else{rk.insertAdjacentHTML('beforeend','<span class="spt '+d.c+'">'+d.s+'</span>');
   const nm=info.querySelector('.nm');nm.insertAdjacentHTML('afterend','<div class="mute" style="font-size:12px">'+d.h.replace('前の競技:','')+'</div>');}
 });
 if(V==='ta2'){const pn=document.querySelector('.cards.sc');pn.insertAdjacentHTML('beforebegin','<h3>候補をしぼる</h3><div class="chips"><button class="on">すべて</button><button>相撲経験者</button><button>ほかの競技から</button><button>柔道</button><button>レスリング</button><button>柔術・総合</button></div><p class="mute kaku" style="font-size:12px">「ほかの競技から」は、親方の人脈・一門から年に数人ほど入ってきます(推定)。</p>');}
}
/* ---- 運動能力検査 ---- */
function ken(){
 go('scout');fixHl();
 const cs=[...document.querySelectorAll('.cards.sc > .card')].slice(0,3);
 const c=cs[0];if(!c)return;
 const info=c.querySelector('.info');[...info.children].forEach(d=>{if(/^\d+cm・\d+kg/.test(d.textContent.trim()))d.firstChild.textContent='165cm・61kg';});
 info.querySelector('.nm').insertAdjacentHTML('afterend','<div class="shu" style="font-size:12px">身長 165cm・体重 61kg:体格基準(167cm・67kg)に届きません → 運動能力検査を受けます</div>');
 if(V==='ken1'){info.insertAdjacentHTML('beforeend','<div style="font-size:12px">運動能力検査の見込み:<b class="ok">合格しそう</b>(身のこなし・筋力が高め)</div>');}
 else{
  const html='<h2>新弟子検査の結果</h2><p class="kaku">身長 165cm・体重 61kg は体格基準(167cm・67kg)に届かないため、運動能力検査(7 項目)を受けました。</p><table class="ktb"><tr><th>項目</th><th class="n">記録</th><th class="n">基準</th><th></th></tr><tr><td>背筋力</td><td class="n">168 kg</td><td class="n">150 kg</td><td class="ok">○</td></tr><tr><td>握力</td><td class="n">47 kg</td><td class="n">40 kg</td><td class="ok">○</td></tr><tr><td>反復横跳び</td><td class="n">52 回</td><td class="n">45 回</td><td class="ok">○</td></tr><tr><td>(あと 4 項目)</td><td class="n">…</td><td class="n">…</td><td class="ok">○</td></tr></table><p class="kaku"><b class="ok">合格</b>:入門が決まりました。(記録の数字は見本用の仮の値です)</p><button class="btn sm" onclick="closeM()">閉じる</button>';
  const o=document.createElement('div');o.id='kenbox';o.style.cssText='position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:min(520px,92vw);max-height:80vh;overflow:auto;background:var(--bg,#f4efe4);color:var(--fg,#222);border:2px solid var(--ai);border-radius:8px;padding:14px;z-index:9000;box-shadow:0 8px 40px #0008';o.innerHTML=html;document.body.appendChild(o);o.querySelector('button').onclick=()=>o.remove();
 }
}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 if(V.startsWith('mino'))mino();else{while(G.pros.length<4){const p=mkProspect(-1);viewPros(p,9);G.pros.push(p);}G.pros.forEach(p=>{p.v=Math.max(p.v,2)});if(V.startsWith('ta'))prospects();else ken();}
}catch(e){console.error(e)}},400);});
})();
</script>
'''
NOTE={'mino1':'mino1:腰の重さに札 2 つ(体格・体幹)+隠れた資質に「身のこなし」を言葉で','mino2':'mino2:腰の重さの札は今のまま+隠れた資質に「身のこなし」を星 5 つで',
 'ta1':'ta1:候補カードに競技の札・前の競技の経歴・特徴(推定)・身のこなしを全部出す','ta2':'ta2:競技の札だけ小さく+「候補をしぼる」ボタン','ken1':'ken1:体格基準に届かない候補に赤字と検査の見込みを出す','ken2':'ken2:入門のときに運動能力検査の結果の表を出す'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'(数字・名前は見本用)</div></body>',1)
    s=s.replace('<title>Sumo Manager v70</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
