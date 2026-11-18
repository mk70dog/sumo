# 見本 tekichu1〜3:新聞の予想印の当たり外れの記録(v66 に見本用の script を足す。勝ち負けは変えない)
base=open('sumo_manager_v66.html',encoding='utf-8').read()
JS=r'''
<style>
.tk{width:100%;border-collapse:collapse;font-size:14px}.tk th,.tk td{padding:6px 6px;border-bottom:1px dashed var(--line);text-align:center}.tk th{font-weight:400;font-size:12px;color:var(--mute)}.tk td:first-child{text-align:left}
.tkb{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--line);margin:2px 3px 0 0;white-space:nowrap}
.tkb.ok{border-color:var(--shu);color:var(--shu)}.tkb.ng{color:var(--mute)}.tkb.big{background:var(--shu);color:#fff;border-color:var(--shu)}
.tkc{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}.tkc>div{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper)}
.tkc .pc{font-size:30px;font-weight:700;font-family:serif;color:var(--shu)}.tkc .bar2{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin:4px 0}.tkc .bar2 i{display:block;height:100%;background:var(--shu)}
</style>
<script>
(function(){
const V=__V__;
function Y(){if(!G.yoso)G.yoso={c:{},t:{},big:[],b:G.bnum,log:[]};return G.yoso;}
function z(o,k){if(!o[k])o[k]={n:0,h:0,mn:0,mh:0,an:0,ah:0};return o[k];}
const oa=advanceDay;advanceDay=function(){const B=G.B;let pre=[];
 if(G.phase==='basho'&&B&&B.cur){const y=Y();if(y.b!==G.bnum){y.c={};y.b=G.bnum;}
  pre=B.cur.filter(p=>G.R[p[0]].h===0||G.R[p[1]].h===0).map(p=>{const a=G.R[p[0]].h===0?G.R[p[0]]:G.R[p[1]],o=a===G.R[p[0]]?G.R[p[1]]:G.R[p[0]];if(B.rec[a.id].ky||B.rec[o.id].ky)return null;return {a:a.id,o:o.id,m:PAP.map((x,k)=>mk(est(a,o,k)))};}).filter(Boolean);}
 const day=G.B?G.B.day:0;const bs=oa.apply(this,arguments);
 if(pre.length&&Array.isArray(bs)){const y=Y();pre.forEach(q=>{const b=bs.find(x=>(x.w===q.a&&x.l===q.o)||(x.w===q.o&&x.l===q.a));if(!b||b.fus)return;const win=b.w===q.a;const res=[];
  PAP.forEach((x,k)=>{const m=q.m[k];if(m===2){res.push(0);return;}const pw=m<=1;const hit=pw===win;[z(y.c,k),z(y.t,k)].forEach(s=>{s.n++;if(hit)s.h++;if(m===0||m===4){s.mn++;if(hit)s.mh++;}});
   const ana=(win&&m>=3)||(!win&&m<=1);if(win&&m>=3){[z(y.c,k),z(y.t,k)].forEach(s=>{s.ah++;});y.big.unshift({b:G.bnum,d:day+1,k,a:G.R[q.a].n,o:G.R[q.o].n,m});}
   [z(y.c,k),z(y.t,k)].forEach(s=>{if(m>=3)s.an++;});res.push(hit?1:-1);});
  y.log.unshift({b:G.bnum,d:day+1,a:q.a,o:q.o,m:q.m,win,res});});y.log=y.log.slice(0,300);y.big=y.big.slice(0,30);}
 return bs;};
const pc=(h,n)=>n?Math.round(100*h/n)+'%':'―';
function table(){const y=Y();return '<table class="tk"><tr><th>新聞</th><th>今場所<br>当たり</th><th>◎・― の<br>当たり</th><th>穴(▲△―)が<br>勝った</th><th>通算</th></tr>'+PAP.map((x,k)=>{const c=y.c[k]||{n:0,h:0,mn:0,mh:0,an:0,ah:0},t=y.t[k]||{n:0,h:0};return '<tr><td><b>'+x[0]+'</b><br><span class="mute" style="font-size:11px">'+x[1]+'</span></td><td><b>'+pc(c.h,c.n)+'</b><br><span class="mute" style="font-size:11px">'+c.h+'/'+c.n+'</span></td><td>'+pc(c.mh,c.mn)+'</td><td>'+c.ah+' 回</td><td>'+pc(t.h,t.n)+'</td></tr>';}).join('')+'</table>';}
function bigList(n){const y=Y();if(!y.big.length)return '<p class="mute kaku" style="font-size:13px">まだ大当たりはありません。</p>';return '<ul class="kaku" style="font-size:13px;margin:4px 0 0 1.2em">'+y.big.slice(0,n).map(x=>'<li>'+bname(x.b)+' '+x.d+'日目 '+PAP[x.k][0]+' '+MK[x.m]+' の'+esc(x.a)+'が'+esc(x.o)+'に勝った</li>').join('')+'</ul>';}
function panel(){const note='<p class="mute kaku" style="font-size:12px;margin-top:6px">部屋の力士の取組だけを数えます。▲(互角)は当たり外れに数えません。◎○=勝つ、△―=負けると読んだものとして数えます。</p>';
 if(V===3){const y=Y();return '<div class="pn"><h2>新聞の予想 当たり外れ<span class="sub">'+bname(G.bnum)+'</span></h2><div class="tkc">'+PAP.map((x,k)=>{const c=y.c[k]||{n:0,h:0,mn:0,mh:0,ah:0},t=y.t[k]||{n:0,h:0};const p=c.n?Math.round(100*c.h/c.n):0;return '<div><b>'+x[0]+'</b> <span class="mute" style="font-size:12px">'+x[1]+'</span><div class="pc">'+p+'<span style="font-size:14px">%</span></div><div class="bar2"><i style="width:'+p+'%"></i></div><div class="mute" style="font-size:12px">今場所 '+c.h+'/'+c.n+' 当たり・◎― '+pc(c.mh,c.mn)+'・穴 '+c.ah+' 回・通算 '+pc(t.h,t.n)+'</div></div>';}).join('')+'</div><h3 style="margin-top:10px">大当たり(穴が勝った取組)</h3>'+bigList(6)+note+'</div>';}
 return '<div class="pn"><h2>新聞の予想 当たり外れ<span class="sub">'+bname(G.bnum)+'</span></h2>'+table()+'<h3 style="margin-top:10px">大当たり(穴が勝った取組)</h3>'+bigList(5)+note+'</div>';}
const ok=kirokuHTML;kirokuHTML=function(){const d=document.createElement('div');d.innerHTML=ok();const f=d.querySelector('.pn');const t=document.createElement('div');t.innerHTML=panel();if(f)f.after(...t.childNodes);else d.prepend(...t.childNodes);return d.innerHTML;};
if(V===2){const ob=bashoHTML;bashoHTML=function(){const d=document.createElement('div');d.innerHTML=ob();const y=Y();const day=G.B?G.B.day:0;
 const L=y.log.filter(x=>x.b===G.bnum&&x.d===day);
 L.forEach(x=>{const nm=G.R[x.a].n;const box=[...d.querySelectorAll('.r1')].find(e=>{const b0=e.querySelector('b');return b0&&b0.textContent===nm;});if(!box)return;const tags=PAP.map((p,k)=>{const r=x.res[k];const m=x.m[k];const big=x.win&&m>=3;return '<span class="tkb '+(big?'big':r>0?'ok':r<0?'ng':'')+'">'+p[0].replace('スポーツ','ス')+' '+MK[m]+' '+(big?'大当たり':r>0?'当たり':r<0?'外れ':'')+'</span>';}).join('');if(!box.dataset.tk){box.dataset.tk=1;const bt=box.querySelector('.dhbtn');(bt||box).insertAdjacentHTML(bt?'beforebegin':'beforeend','<div>'+tags+'</div>');}});
 const f=d.querySelectorAll('.pn')[1];if(f){f.insertAdjacentHTML('afterend','<div class="pn"><h2>新聞の予想 今場所の当たり</h2>'+table()+'</div>');}return d.innerHTML;};}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 for(let s=0;s<2;s++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();}
 while(G.phase==='train')doWeek();for(let i=0;i<5;i++)advanceDay();UI.bouts=advanceDay();
 go(V===2?'basho':'kiroku');}catch(e){console.error(e)}},80);});
})();
</script>
'''
NOTE={1:'tekichu1:記録の画面に表(新聞ごとの今場所・通算の当たり、◎の当たり、穴が勝った回数)+大当たりの一覧',
2:'tekichu2:本場所の結果に新聞ごとの「当たり/外れ/大当たり」の札+今場所の表',
3:'tekichu3:記録の画面に新聞ごとのカード(当たりの割合を大きく)+大当たりの一覧'}
for v in (1,2,3):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'</div></body>',1).replace('<title>Sumo Manager v66</title>','<title>見本 tekichu%d</title>'%v,1)
    open('samples/tekichu%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
