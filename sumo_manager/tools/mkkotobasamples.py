# 見本 kotoba1〜3(素質を言葉で伝える)と yoso1〜3(取組前の予想印)。v65 に見本用の script を足す(見本なので数値は変えない)
base=open('sumo_manager_v65.html',encoding='utf-8').read()
COMMON=r'''
<style>
.kw{display:inline-block;font-size:13px;padding:1px 8px;border-radius:10px;border:1px solid var(--kin,#a8823c);color:var(--kin,#a8823c);margin-left:4px}
.oyk{display:block;margin:6px 0 2px;padding:7px 11px;border-radius:12px;background:var(--washi2,#efe6d4);font-size:13px;line-height:1.6;color:var(--sumi);position:relative;font-weight:400}
.oyk b{color:var(--shu)}
.oyk .who{font-size:11px;color:var(--mute);display:block}
.yt{width:100%;border-collapse:collapse;font-size:13px;margin-top:5px}.yt td,.yt th{padding:3px 5px;border-bottom:1px dashed var(--line);text-align:center}.yt th{font-weight:400;color:var(--mute);font-size:12px}.yt td:first-child{text-align:left;color:var(--mute);font-size:12px}
.mk{font-size:18px;font-weight:700;font-family:serif}.mk.m0{color:var(--shu)}.mk.m1{color:var(--ai)}.mk.m2{color:#2f7d4a}.mk.m3{color:#8a6d2b}.mk.m4{color:var(--mute);font-size:14px}
.ybar{display:flex;height:16px;border-radius:8px;overflow:hidden;margin:5px 0 2px;font-size:11px;color:#fff;line-height:16px}.ybar i{display:block;text-align:center;font-style:normal}
.yr{font-size:12px;color:var(--mute)}
</style>
<script>
const SMP=__SMP__;
function sd(a,b){let x=Math.sin(a*12.9898+b*78.233)*43758.5453;return x-Math.floor(x);}
/* ---- 素質を言葉で ---- */
const KPH={str:'腰が重い',exp:'立ち合いの踏み込みが鋭い',end:'稽古でなかなかばてない',flx:'体がやわらかい',rec:'疲れが抜けるのが早い',tac:'当たりが強い',tsk:'突き押しに威力がある',mig:'右を差すと強い',hid:'左を差すと強い',yor:'寄りの足がよく出る',nag:'投げのセンスがある',hik:'引き技がうまい',ash:'足技が器用',tgw:'土俵際で粘れる',tos:'負けん気が強い',rei:'取り口が落ち着いている',sho:'勝負どころに強い',ken:'研究熱心',gam:'我慢がきく',pro:'稽古を休まない'};
const KWK={str:'腰の軽さ',exp:'立ち合いの遅さ',end:'スタミナ',flx:'体の硬さ',tac:'当たりの弱さ',tsk:'押しの弱さ',yor:'寄りの足',tgw:'土俵際のもろさ',tos:'おとなしさ',rei:'あわてやすさ',gam:'辛抱のなさ'};
function grW(v){return v>=16?['ひょっとすると、横綱まで行く器かもしれん。','横綱まで行ける器かもしれん。','この子は横綱まで行ける器だ。']:v>=13.5?['三役を狙える素材かもしれん。','三役も狙える素材だと思う。','三役は十分に狙える素材だ。']:v>=11?['関取になれるかどうか、まだ何とも言えん。','関取になれるだけのものは持っている。','稽古しだいで、関取にはなれる。']:v>=8.5?['まだ線が細い。','まだ線が細い。地道にやれば幕下までは行けるかもしれん。','幕下までは行ける。その先は本人しだいだ。']:['まだ何とも言えん。','正直、関取は厳しいかもしれん。','正直、関取は厳しいだろう。'];}
function deg(v){return v>=17?'すごく':v>=15?'かなり':'なかなか';}
function kotoba(r,cert){ // cert 0=まだ分からない 1=だいたい 2=はっきり
 const p=potOf(r);const g=grW(p);
 const ks=Object.keys(KPH).filter(k=>r.cap[k]!=null).sort((a,b)=>r.cap[b]-r.cap[a]);const n=cert===0?1:2;
 const st=ks.slice(0,n).map(k=>deg(r.cap[k])+KPH[k].replace(/^(.*?)(が|に|を)/,'$1$2')).join('。');
 const wk=Object.keys(KWK).filter(k=>r.cap[k]!=null).sort((a,b)=>r.cap[a]-r.cap[b])[0];
 const head=cert===0?'まだよく分からんが、':'';
 return {grade:head+g[cert],st:st+'。',wk:cert>=1?'ただ、'+KWK[wk]+'が課題だな。':'',tag:cert===0?'見立て:まだ':cert===1?'見立て:だいたい':'見立て:はっきり'};}
function who(){const c=G.staff.find(s=>s.role==='co');return c?c.n+'(部屋付き親方)':'親方';}
function kbox(r,cert){const k=kotoba(r,cert);return '<span class="oyk"><span class="who">'+esc(who())+' のひとこと・'+k.tag+'</span>「'+k.grade+k.st+(k.wk?k.wk:'')+'」</span>';}
function knCert(r){const v=r.h===0?r.kn:0;return v>=70?2:v>=35?1:0;}
if(SMP.k){
 const op=potTxt;
 potTxt=function(r){const c=knCert(r);
  if(SMP.k===1)return '<span class="kw">'+['見立て中','だいたい','はっきり'][c]+'</span>'+kbox(r,c);
  if(SMP.k===2)return op(r)+kbox(r,c);
  return (c>=2?op(r):'<span class="kw">見極め '+Math.round(r.kn)+'%(70% で数字が出る)</span>')+kbox(r,c);};
 const os=scoutHTML;scoutHTML=function(){const d=document.createElement('div');d.innerHTML=os();
  d.querySelectorAll('.cards.sc .card').forEach((c,i)=>{const p=G.pros[i];if(!p)return;const cert=p.v>=3?2:p.v>=1?1:0;const divs=[...c.querySelectorAll('.info > div')];
   const a=divs.find(x=>x.textContent.startsWith('今の力'));const b=divs.find(x=>x.textContent.startsWith('素質'));if(!a||!b)return;
   const k=kotoba(p.r,cert);const box='<div class="oyk" style="margin:4px 0"><span class="who">見に行った人のひとこと・'+k.tag+'</span>「'+k.grade+k.st+(k.wk||'')+'」</div>';
   if(SMP.k===1){a.outerHTML=box;b.remove();}
   else if(SMP.k===2){b.insertAdjacentHTML('afterend',box);}
   else{if(cert<2){a.outerHTML=box;b.outerHTML='<div class="mute" style="font-size:12px">3 回見に行くと数字が出ます</div>';}else b.insertAdjacentHTML('afterend',box);}});
  return d.innerHTML;};
}
/* ---- 予想印 ---- */
const PAP=[['相撲日報','番付と力'],['スポーツ角界','調子重視'],['週刊土俵裏','相性・穴狙い']];
const MK=['◎','○','▲','△','―'];
function est(a,o,k){const B=G.B;const ca=B.rec[a.id],co=B.rec[o.id];const hh=(a.h2h&&a.h2h[o.id])||[0,0];
 let d=(ovr(a)-ovr(o))*.9;if(k===0)d+=(o.pos-a.pos)*.004;if(k===1)d+=(a.cond-o.cond)/25+((ca.w-ca.l)-(co.w-co.l))*.06;if(k===2)d+=(hh[0]-hh[1])*.18+(styleName(a)!==styleName(o)?.1:0);
 d+=(sd(a.id*7+o.id,k+1)-.5)*(k===2?1.2:.5);return 1/(1+Math.exp(-d));}
function mk(p){return p>=.68?0:p>=.56?1:p>=.46?2:p>=.36?3:4;}
function mkS(i){return '<span class="mk m'+i+'">'+MK[i]+'</span>';}
function why(a,o){const B=G.B;const hh=(a.h2h&&a.h2h[o.id])||[0,0];const L=[];
 if(ovr(a)-ovr(o)>.8)L.push('力は上');else if(ovr(o)-ovr(a)>.8)L.push('力は相手が上');else L.push('力は互角');
 if(a.cond>=65)L.push('調子よし');else if(a.cond<40)L.push('調子いまひとつ');
 if(hh[0]+hh[1])L.push('対戦 '+hh[0]+'勝'+hh[1]+'敗');
 if(styleName(a)!==styleName(o))L.push(styleName(a)+'対'+styleName(o));return L.join('・');}
if(SMP.y){
 const ob=bashoHTML;bashoHTML=function(){const d=document.createElement('div');d.innerHTML=ob();const B=G.B;if(!B||!B.cur)return d.innerHTML;
  const nx=B.cur.filter(p=>G.R[p[0]].h===0||G.R[p[1]].h===0);{const os=oshiR();if(os){const k=nx.findIndex(p=>p[0]===os.id||p[1]===os.id);if(k>0)nx.unshift(nx.splice(k,1)[0]);}}
  d.querySelectorAll('.nx').forEach((e,i)=>{const p=nx[i];if(!p)return;const a=G.R[p[0]].h===0?G.R[p[0]]:G.R[p[1]],o=a===G.R[p[0]]?G.R[p[1]]:G.R[p[0]];if(B.rec[a.id].ky||B.rec[o.id].ky)return;
   const ps=PAP.map((x,k)=>est(a,o,k));const av=ps.reduce((s,x)=>s+x,0)/3;let h='';
   if(SMP.y===1)h='<table class="yt"><tr><th></th><th>'+esc(a.n)+'</th><th>'+esc(o.n)+'</th></tr>'+PAP.map((x,k)=>'<tr><td>'+x[0]+'<br><span style="font-size:11px">('+x[1]+')</span></td><td>'+mkS(mk(ps[k]))+'</td><td>'+mkS(mk(1-ps[k]))+'</td></tr>').join('')+'</table>';
   else if(SMP.y===2)h='<div style="margin-top:5px;display:flex;gap:8px;align-items:center"><span style="font-size:12px;color:var(--mute)">予想</span>'+mkS(mk(av))+'<span class="yr">'+why(a,o)+'</span></div>';
   else{const w=Math.round(av*100);h='<div class="ybar"><i style="width:'+w+'%;background:var(--shu)">'+(w>=12?w+'%':'')+'</i><i style="width:'+(100-w)+'%;background:var(--ai)">'+(w<=88?(100-w)+'%':'')+'</i></div><div class="yr" style="display:flex;justify-content:space-between"><span>'+esc(a.n)+' の勝つ見込み '+w+'%</span><span>'+esc(o.n)+' '+(100-w)+'%</span></div><div class="yr">新聞の印:'+PAP.map((x,k)=>x[0]+' '+MK[mk(ps[k])]).join('・')+'</div>';}
   const m=e.querySelector('.nxm');if(m)m.insertAdjacentHTML('afterend',h);});
  return d.innerHTML;};
}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 if(SMP.k){const o=own();o.forEach((r,i)=>{r.kn=[20,50,85][i%3];});if(SMP.view==='scout'){G.pros.forEach((p,i)=>{p.v=i%4;});go('scout');}else{const r=o.find(x=>x.d>=2&&x.age<23)||o[0];r.kn=SMP.kn;go('heya');showR(r.id);}}
 else{while(G.phase==='train')doWeek();advanceDay();advanceDay();go('basho');}}catch(e){console.error(e)}},80);});
</script>
'''
NOTE={'kotoba1':'kotoba1:数字をやめて言葉だけ(見極めが進むほど言い方がはっきり)',
 'kotoba2':'kotoba2:数字はそのまま+親方のひとこと',
 'kotoba3':'kotoba3:見極め 70% まで言葉だけ → それから数字も',
 'yoso1':'yoso1:新聞 3 紙の印を表で(紙ごとに見るところが違う)',
 'yoso2':'yoso2:まとめた印 1 つ+理由ひとこと',
 'yoso3':'yoso3:勝つ見込みの棒+新聞の印'}
import json
cfg={'kotoba1':{'k':1,'kn':50},'kotoba2':{'k':2,'kn':50},'kotoba3':{'k':3,'kn':50},'yoso1':{'y':1},'yoso2':{'y':2},'yoso3':{'y':3}}
for n,c in cfg.items():
    for sub in (['','_s'] if 'k' in c else ['']):
        cc=dict(c)
        if sub=='_s':cc['view']='scout'
        s=base.replace('</body>',COMMON.replace('__SMP__',json.dumps(cc))+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[n]+(' (新弟子の画面)' if sub else '')+'</div></body>',1).replace('<title>Sumo Manager v65</title>','<title>見本 %s</title>'%(n+sub),1)
        open('samples/%s%s.html'%(n,sub),'w',encoding='utf-8').write(s)
print('ok')
