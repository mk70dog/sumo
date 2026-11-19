# 見本 hyo1〜3:能力を「数字で見える(測れるもの)」と「人の評価」に分ける / ken3:対戦相手の研究と助言
# v71 の本体に見本用の表示だけを足す(評価は見本用の作り。ゲームの計算は変えていない)。
base=open('sumo_manager_v71.html',encoding='utf-8').read()
CSS='''<style>
.hy{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px}
.hy .bx{border:1px solid var(--line);border-radius:6px;padding:6px 8px;background:#fff8}
.hy .bx h4{margin:0 0 4px;font-size:14px;color:var(--ai)}
.hr{display:flex;justify-content:space-between;font-size:13px;padding:1px 0}
.w5{font-weight:bold}.w5.s{color:var(--shu)}.w5.g{color:#b5651d}.w5.n{color:var(--fg,#333)}.w5.m{color:#2c6a8c}.w5.k{color:#556}
.evb{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}.evb button{border:1px solid var(--line);background:transparent;border-radius:14px;padding:3px 10px;font-size:13px}.evb button.on{background:var(--ai);color:#fff}
.who{font-size:12px;color:var(--mute);margin:2px 0 6px}
.ms{font-size:13px;margin:4px 0}.ms b{font-size:16px;color:var(--ai)}
.ht{width:100%;border-collapse:collapse;font-size:12.5px}.ht th,.ht td{border-bottom:1px solid #8883;padding:3px 4px;text-align:center}.ht td:first-child,.ht th:first-child{text-align:left}
.ht tr.split td{background:#f3d9c955}.ht .q{color:#bbb}
.rg{position:relative;height:12px;background:var(--line);border-radius:2px;margin:2px 0 5px}.rg u{position:absolute;top:0;bottom:0;background:var(--ai);opacity:.6;border-radius:2px}.rg i{position:absolute;top:-2px;width:2px;height:16px;background:var(--shu)}
.cm{background:#f1e8d4;border-radius:8px;padding:6px 10px;margin:4px 0;font-size:13px}.cm .wh{font-size:11px;color:var(--mute)}
.kk{border:2px solid var(--ai);border-radius:8px;padding:10px;margin:8px 0;background:#fffc}
.kk h3{margin:0 0 6px}
</style>'''
JS=r'''
<script>
(function(){
const V='__V__';
let MU=12;const W=v=>{const d=v-MU;return d>=2.5?['すばらしい','s']:d>=1?['良い','g']:d>=-1?['ふつう','n']:d>=-2.5?['物足りない','m']:['課題','k'];};
const wh=v=>{const w=W(v);return '<span class="w5 '+w[1]+'">'+w[0]+'</span>';};
const GR=[['体',['str','exp','end','flx','rec','kos']],['押し',['tac','tsk','mae','hik']],['四つ',['mig','hid','yor']],['技',['nag','ash','tgw']],['心',['tos','rei','sho','gam']]];
const NM={};AT.forEach(x=>NM[x[0]]=x[1]);
function ev(r){const sh=G.staff.find(s=>s.role==='co');
 return [
 {k:'oy',n:'師匠',d:'木瀬親方。弟子は甘めに見がち',f:(k,v,i)=>v+.8+(hhR(r.id,10+i)-.5)*2.4},
 {k:'co',n:'部屋付き親方',d:(sh?sh.n:'部屋付き親方')+'。四つの目は確か、押しは見立てが粗い',f:(k,v,i)=>(['mig','hid','yor','nag'].includes(k)?v+(hhR(r.id,30+i)-.5)*.8:v+(hhR(r.id,30+i)-.5)*4)},
 {k:'tr',n:'トレーナー',d:'外部契約のジム。体の項目だけ測定(数字)',f:(k,v,i)=>['str','exp','end','flx','rec'].includes(k)?Math.round(v):null,num:1},
 {k:'ic',n:'一門の親方',d:'連合稽古で 3 回肌を合わせた',f:(k,v,i)=>['tac','tsk','mig','hid','yor','kos','tos'].includes(k)?v+(hhR(r.id,50+i)-.5)*2:null},
 {k:'ki',n:'記者',d:'相撲担当の記者。最近の成績と人気に引っぱられる',f:(k,v,i)=>null}];}
let AVG={};function setAvg(r){const L=Object.values(G.R).filter(x=>!x.ret&&x.d===r.d&&x.a);AK.forEach(k=>{AVG[k]=L.reduce((a,x)=>a+(k==='kos'||k==='mae'?atTot(x,k):x.a[k]),0)/L.length;});}
function val(r,k){MU=AVG[k]||12;return k==='kos'||k==='mae'?atTot(r,k):r.a[k];}
function summary(r){const o=ovr(r),p=potOf(r);
 return '<div class="ms">総合の見立て:師匠 <b>'+gradeOf(o+.8)+'</b>「三役でも十分やれる」・記者 <b>'+gradeOf(o-.6)+'</b>「上位には分が悪い」</div>'+
  '<div class="ms">素質の見立て:師匠 <b>'+gradeOf(p+.8)+'</b>・部屋付き親方 <b>'+gradeOf(p)+'</b>・記者 <b>'+gradeOf(p-1)+'</b><span class="mute" style="font-size:12px">(本当の素質はだれにも分かりません)</span></div>'+
  '<div class="ms">数字で分かること:'+Math.round(r.ht)+'cm・'+Math.round(r.w)+'kg・体脂肪 '+Math.round(r.bfp||24)+'%・背筋力 '+Math.round(150+r.a.str*7)+'kg・握力 '+Math.round(40+r.a.str*2)+'kg(トレーナーの測定)</div>';}
function tabs(r,sel){const E=ev(r);const e=E.find(x=>x.k===sel)||E[0];
 let h='<div class="evb">'+E.map(x=>'<button class="'+(x.k===e.k?'on':'')+'" onclick="window.__hy(\''+x.k+'\')">'+x.n+'</button>').join('')+'</div><div class="who">'+e.d+'</div>';
 if(e.k==='ki')return h+'<div class="cm"><div class="wh">記者の記事(九州場所の前)</div>「好調を保つ。立ち合いの鋭さは幕内でも上位。ただ四つに組まれると苦しい場面が目立つ」</div><div class="cm"><div class="wh">解説者</div>「押し相撲らしい押し相撲。素質は大関級でしょう」</div>';
 h+='<div class="hy">'+GR.map(([g,ks])=>'<div class="bx"><h4>'+g+'</h4>'+ks.map((k,i)=>{const x=e.f(k,val(r,k),AK.indexOf(k));return '<div class="hr"><span>'+NM[k]+'</span>'+(x==null?'<span class="q">―</span>':e.num?'<b>'+x+'</b>':wh(x))+'</div>';}).join('')+'</div>').join('')+'</div>';
 return h;}
function table(r){const E=ev(r).filter(x=>x.k!=='ki');
 let h='<p class="mute kaku" style="font-size:12px">色の付いた行は、見る人によって評価が割れている項目です。「―」はその人には分からない項目。</p><table class="ht"><tr><th>項目</th>'+E.map(e=>'<th>'+e.n+'</th>').join('')+'</tr>';
 GR.forEach(([g,ks])=>{h+='<tr><td colspan="'+(E.length+1)+'" style="font-weight:bold;color:var(--ai);padding-top:6px">'+g+'</td></tr>';
  ks.forEach(k=>{const xs=E.map(e=>e.f(k,val(r,k),AK.indexOf(k)));const ws=xs.filter(x=>x!=null&&!0).map(x=>W(x)[0]);const sp=new Set(xs.map((x,i)=>x==null||E[i].num?null:W(x)[0]).filter(x=>x)).size>1;
   h+='<tr class="'+(sp?'split':'')+'"><td>'+NM[k]+'</td>'+xs.map((x,i)=>'<td>'+(x==null?'<span class="q">―</span>':E[i].num?'<b>'+x+'</b>':wh(x))+'</td>').join('')+'</tr>';});});
 return h+'</table><div class="cm"><div class="wh">記者</div>「立ち合いの鋭さは幕内でも上位。ただ四つに組まれると苦しい」</div>';}
function ranges(r){const E=ev(r).filter(x=>x.k!=='ki');
 return '<p class="mute kaku" style="font-size:12px">棒の幅=見る人たちの見立ての幅(狭いほど確か)。赤い線=いちばん信用できる人の見立て。</p><div class="hy">'+GR.map(([g,ks])=>'<div class="bx"><h4>'+g+'</h4>'+ks.map(k=>{const xs=E.map(e=>e.f(k,val(r,k),AK.indexOf(k))).filter(x=>x!=null);const lo=Math.min(...xs),hi=Math.max(...xs),be=xs[xs.length>2?1:0];
  return '<div class="hr"><span>'+NM[k]+'</span>'+wh(be)+'</div><div class="rg"><u style="left:'+(lo/20*100)+'%;width:'+Math.max(2,(hi-lo)/20*100)+'%"></u><i style="left:'+(be/20*100)+'%"></i></div>';}).join('')+'</div>').join('')+'</div>'+
  '<div class="cm"><div class="wh">いちばん信用できる人</div>体=トレーナー・四つと技=部屋付き親方・押しと心=師匠(目利きと接した回数で決まります)</div>';}
function rikishi(){const r=own().slice().sort((a,b)=>a.pos-b.pos)[0];r.kn=70;setAvg(r);go('heya');showR(r.id);
 const m=document.querySelector('.atw5');if(!m)return;const head=m.previousElementSibling;
 const draw=sel=>{const h='<div id="hyo">'+summary(r)+(V==='hyo1'?tabs(r,sel):V==='hyo2'?table(r):ranges(r))+'</div>';const o=document.getElementById('hyo');if(o)o.outerHTML=h;else m.outerHTML=h;};
 window.__hy=draw;draw('oy');
 if(head&&head.tagName==='H3')head.innerHTML='能力の見立て<span class="mute kaku" style="font-size:13px;margin-left:8px">数字は測れるものだけ。ほかは人の評価(同じ地位の力士とくらべて)です</span>';}
function kenkyu(){go('home');const pn=document.querySelector('.pn');const r=own().slice().sort((a,b)=>a.pos-b.pos)[0];
 const op=Object.values(G.R).filter(x=>x.h!==0&&x.d===r.d&&!x.ret).sort((a,b)=>Math.abs(a.pos-r.pos)-Math.abs(b.pos-r.pos))[0];
 const h='<div class="kk"><h3>明日の取組:'+esc(r.n)+' − '+esc(op.n)+'('+esc(G.heya[op.h].n)+')</h3>'+
 '<div class="ms">対戦成績 2 勝 3 敗・相手の取り口:'+styleName(op)+'</div>'+
 '<div class="cm"><div class="wh">本人('+esc(r.n)+')・研究熱心:よく研究する</div>「映像で見ました。右から張って左を差しに来る。左を固めて、先に右をおっつけます」<br><span class="mute" style="font-size:12px">→ 相手の立ち合いへの備え(少し有利)</span></div>'+
 '<div class="cm"><div class="wh">兄弟子(先場所 '+esc(op.n)+'に勝った)</div>「土俵際の逆転があるから、最後まで足を止めるな」<br><span class="mute" style="font-size:12px">→ 土俵際で少し有利</span></div>'+
 '<div class="cm"><div class="wh">部屋付き親方</div>「現役のころ、あの部屋とはよく出稽古をした。組んだら下手を切れ」</div>'+
 '<div class="btns" style="margin-top:6px"><span class="kaku" style="font-size:13px">親方の方針:</span><select><option>本人に任せる</option><option selected>映像でいっしょに研究する</option><option>研究より稽古で覚えさせる</option></select></div>'+
 '<p class="mute kaku" style="font-size:12px">苦手意識:この相手には 5 回中 3 敗。4 敗になると「苦手」がつき、その相手にだけ力が少し落ちます(勝つと消えます)。</p></div>';
 pn.insertAdjacentHTML('beforebegin',h);}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;if(V==='ken3')kenkyu();else rikishi();}catch(e){console.error(e)}},400);});
})();
</script>
'''
NOTE={'hyo1':'hyo1:評価する人をボタンで切りかえ。人ごとに言葉の評価(トレーナーは体だけ数字)','hyo2':'hyo2:項目×評価する人の一覧表。評価が割れている項目に色',
 'hyo3':'hyo3:見立ての幅を棒で。いちばん信用できる人の見立てに赤い線','ken3':'ken3:取組の前に、本人の研究・兄弟子と部屋付き親方の助言・親方の方針・苦手意識'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'(言葉・数字は見本用)</div></body>',1)
    s=s.replace('<title>Sumo Manager v71</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
