# 見本 nou1〜2:能力 20 項目の見直し(前さばき・腰の重さを足し、研究熱心・プロ意識を隠れた資質へ、大一番は勝負強さにまとめる)。見本の新しい値は今の能力からの仮の計算
base=open('sumo_manager_v68.html',encoding='utf-8').read()
JS=r'''
<style>.atw5{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.nw{font-size:10px;color:var(--shu);margin-left:3px}</style>
<script>
(function(){
const V=__V__;
const NA=[['str','筋力','体'],['exp','瞬発力','体'],['end','持久力','体'],['flx','柔軟性','体'],['rec','回復力','体'],['kos','腰の重さ','体',1],
 ['tac','立ち合い','押'],['tsk','突き押し','押'],['mae','前さばき','押',1],['hik','引き・いなし','押'],
 ['mig','右四つ','四'],['hid','左四つ','四'],['yor','寄り','四'],
 ['nag','投げ','技'],['ash','足技','技'],['tgw','土俵際','技'],
 ['tos','闘志','心'],['rei','冷静さ','心'],['sho','勝負強さ','心'],['gam','我慢強さ','心']];
function val(r,k){if(k==='kos')return (r.a.str*.5+r.a.gam*.25+r.a.end*.25)+(r.wT>170?1:0);if(k==='mae')return r.a.tac*.4+r.a.yor*.3+Math.max(r.a.mig,r.a.hid)*.3;return r.a[k];}
function box(r,g,lab){return '<div class="atc"><div class="atg">'+lab+'</div>'+NA.filter(x=>x[2]===g).map(x=>{const v=val(r,x[0]);return '<div class="atr"><span>'+x[1]+(x[3]?'<span class="nw">新</span>':'')+'</span><b class="'+ac(v)+'">'+Math.round(v)+'</b><i></i></div>';}).join('')+'</div>';}
function panel(r){if(V===1){const tech=NA.filter(x=>'押四技'.includes(x[2]));return '<div class="atw">'+box(r,'体','体')+'<div class="atc"><div class="atg">技</div>'+tech.map(x=>{const v=val(r,x[0]);return '<div class="atr"><span>'+x[1]+(x[3]?'<span class="nw">新</span>':'')+'</span><b class="'+ac(v)+'">'+Math.round(v)+'</b><i></i></div>';}).join('')+'</div>'+box(r,'心','心')+'</div>';}
 return '<div class="atw5">'+box(r,'体','体')+box(r,'押','押し')+box(r,'四','四つ')+box(r,'技','技')+box(r,'心','心')+'</div>';}
const os=showR;showR=function(id){os(id);const r=G.R[id];const m=document.querySelector('.atw');if(!m||!r)return;m.outerHTML=panel(r);
 const dl=[...document.querySelectorAll('dl.kv')].find(d=>[...d.querySelectorAll('dt')].some(t=>t.textContent==='性格'));if(dl){[...dl.querySelectorAll('dt')].forEach(dt=>{if(dt.textContent==='大一番'){dt.nextElementSibling.remove();dt.remove();}});
  const kn=r.kn||0;const w=(v,a,b)=>v>=14?a:v<=6?b:'ふつう';
  dl.insertAdjacentHTML('beforeend','<dt>研究熱心<span class="nw">移</span></dt><dd>'+(kn>=45?w(r.a.ken,'よく研究する(技の伸びが良い)','研究しない'):'<span class="mute">?(見極め中)</span>')+'</dd><dt>プロ意識<span class="nw">移</span></dt><dd>'+(kn>=45?w(r.a.pro,'自己管理が行き届く(けが・体重)','自己管理が甘い'):'<span class="mute">?(見極め中)</span>')+'</dd>');}};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;const r=own().slice().sort((a,b)=>a.pos-b.pos)[0];r.kn=60;go('heya');showR(r.id);}catch(e){console.error(e)}},80);});
})();
</script>
'''
NOTE={1:'nou1:20 項目の中身を入れかえ(体 6・技 10・心 4)。並びは今と同じ 3 つの箱',2:'nou2:同じ 20 項目を 5 つの箱(体・押し・四つ・技・心)に分けて並べる'}
for v in (1,2):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'(「新」=新しい項目、「移」=隠れた資質へ移した項目)</div></body>',1).replace('<title>Sumo Manager v68</title>','<title>見本 nou%d</title>'%v,1)
    open('samples/nou%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
