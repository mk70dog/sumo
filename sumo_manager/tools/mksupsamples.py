# 見本 sup1〜3:部屋を支える人(後援会長・タニマチ・かかりつけ医・師匠の家族)  v59 の本体に見本用の script を足す
base=open('sumo_manager_v59.html',encoding='utf-8').read()
JS=r'''
<style>
.spg{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;margin-top:6px}
.spc{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:var(--paper)}
.spc .t{font-weight:700;font-size:16px}.spc .w{font-size:13px;margin:2px 0}.spc .e{font-size:12px;color:var(--mute)}
.bar{display:inline-block;width:70px;height:7px;border-radius:4px;background:rgba(0,0,0,.1);vertical-align:1px;margin:0 4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--shu)}
.lb{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--ai);color:var(--ai);margin-left:4px}
.lb.w{border-color:#b8860b;color:#b8860b}
.sw3{display:grid;grid-template-columns:1fr 2.2fr 1fr;gap:10px;align-items:start}
@media(max-width:760px){.sw3{grid-template-columns:1fr}}
.side .spc{margin-bottom:8px}
.ring3{position:relative;width:min(560px,100%);aspect-ratio:1/1;margin:0 auto}
.ring3 svg{position:absolute;inset:0;width:100%;height:100%}
.ring3 .n{position:absolute;transform:translate(-50%,-50%);background:var(--paper);border:1.5px solid var(--sumi);border-radius:8px;padding:3px 7px;font-size:12px;text-align:center;line-height:1.3;white-space:nowrap}
@media(max-width:500px){.ring3 .n{font-size:10px;padding:2px 4px}.ring3 .n.c{font-size:12px;padding:5px 7px}}
.ring3 .n.o{border-color:#b8860b}.ring3 .n.c{font-size:15px;font-weight:700;padding:8px 12px}
</style>
<script>
(function(){
const V=__V__;
const S=[
 {k:'kai',t:'後援会長',w:'松岡 源一郎(地元の建設会社 会長・72歳)',n:78,e:'顔の広さ 15。後援会員の増え方 +、地方の激励会、法人の後援',tag:'退任まで約 3 年'},
 {k:'tm1',t:'タニマチ',w:'高槻 清(運送会社 会長)',n:84,e:'化粧廻しを贈る・祝賀会のご祝儀が大きい',tag:'宴席に誘いがち',warn:1},
 {k:'tm2',t:'タニマチ',w:'三好 和代(料亭の女将)',n:61,e:'ちゃんこの差し入れ・関取の食事'},
 {k:'tm3',t:'タニマチ',w:'野々村 誠一(病院の院長)',n:45,e:'新弟子の紹介(地元の高校)・けが人の相談'},
 {k:'doc',t:'かかりつけ医',w:'すみだ整形クリニック(月 15 万円)',n:null,e:'けが・病気を早く見つける。手術の判断がよくなる。協会の相撲診療所(内科・整形外科)はいつでも使える'},
 {k:'fam',t:'師匠の家族',w:'長男 17 歳(高校相撲部)・長女 14 歳',n:null,e:'長男は入門を考えている(二世力士の候補)'}];
const nb=x=>x.n==null?'':'<div class="w">親しさ<span class="bar"><i style="width:'+x.n+'%"></i></span>'+x.n+'</div>';
const card=x=>'<div class="spc"><div class="t">'+x.t+(x.tag?'<span class="lb'+(x.warn?' w':'')+'">'+x.tag+'</span>':'')+'</div><div class="w">'+x.w+'</div>'+nb(x)+'<div class="e">'+x.e+'</div></div>';
const note='<p class="kaku mute" style="font-size:13px;margin-top:6px">見本です。名前・会社はすべて架空。数字は推定。タニマチの宴席の誘いは、断ると親しさが下がり、行かせると不祥事の芽になることがあります。</p>';
const oo=orgHTML;
orgHTML=function(){const h=oo();
 if(V===1)return h+'<div class="pn"><h2>部屋を支える人<span class="sub">部屋の外から</span></h2><div class="spg">'+S.map(card).join('')+'</div>'+note+'</div>';
 if(V===2){const d=document.createElement('div');d.innerHTML=h;const org=d.querySelector('.org');const L=S.filter(x=>['kai','tm1','tm2','tm3'].includes(x.k)),R=S.filter(x=>['doc','fam'].includes(x.k));
  const w=document.createElement('div');w.className='sw3';w.innerHTML='<div class="side"><div class="kaku" style="font-weight:700;margin-bottom:4px">後援する人</div>'+L.map(card).join('')+'</div><div class="mid"></div><div class="side"><div class="kaku" style="font-weight:700;margin-bottom:4px">医師・家族</div>'+R.map(card).join('')+'</div>';
  org.replaceWith(w);w.querySelector('.mid').appendChild(org);return d.innerHTML.replace('</div>','</div>');}
 if(V===3){const inner=[['部屋付き親方',''],['おかみさん',''],['マネージャー',''],['若者頭',''],['世話人',''],['行司・呼出・床山','']];const outer=S;
  const pt=(i,n,r)=>{const a=-Math.PI/2+i*2*Math.PI/n;return [50+r*Math.cos(a),50+r*Math.sin(a)];};
  let svg='<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="24" fill="none" stroke="var(--line)" stroke-dasharray="1 1"/><circle cx="50" cy="50" r="38" fill="none" stroke="var(--line)" stroke-dasharray="1 1"/>'+outer.map((x,i)=>{const p=pt(i+.5,outer.length,38);return '<line x1="50" y1="50" x2="'+p[0]+'" y2="'+p[1]+'" stroke="'+(x.warn?'#b8860b':'var(--line)')+'" stroke-width="'+(x.n?x.n/60:.6)+'"/>';}).join('')+'</svg>';
  let ns='<div class="n c">'+esc(me().n)+'部屋<br><span style="font-size:11px;font-weight:400">師匠 '+esc(me().o)+'</span></div>';
  ns=ns.replace('class="n c"','class="n c" style="left:50%;top:50%"');
  ns+=inner.map((x,i)=>{const p=pt(i,inner.length,24);return '<div class="n" style="left:'+p[0]+'%;top:'+p[1]+'%">'+x[0]+'</div>';}).join('');
  ns+=outer.map((x,i)=>{const p=pt(i+.5,outer.length,38);return '<div class="n o" style="left:'+p[0]+'%;top:'+p[1]+'%"><b>'+x.t+'</b><br>'+x.w.split('(')[0]+(x.n!=null?'<br>親しさ '+x.n:'')+'</div>';}).join('');
  return '<div class="pn"><h2>部屋のまわりの人<span class="sub">内側=部屋の中・外側=部屋を支える人(線の太さ=親しさ)</span></h2><div class="ring3">'+svg+ns+'</div><div class="spg" style="margin-top:10px">'+S.map(card).join('')+'</div>'+note+'</div>'+h;}
 return h;};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('春日野');UI.title=0;UI.start=0;go('staff');}catch(e){console.error(e)}},50);});
})();
</script>
'''
for v in (1,2,3):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'</body>',1).replace('<title>Sumo Manager v59</title>','<title>見本 sup%d</title>'%v,1)
    open('samples/sup%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
