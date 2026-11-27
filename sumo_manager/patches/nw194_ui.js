<script>/* v194:新弟子タブ・記録タブを開いたとき、前回から新しいものに「新」の印と赤い線を付け、上にまとめる(ダルマさん 見本 nw2) */
(function(MODE){
const st=document.createElement('style');st.textContent=`
.nwt{display:inline-block;background:var(--shu,#b33);color:#fff;font-size:11px;font-weight:700;border-radius:9px;padding:1px 7px;margin-left:6px;vertical-align:middle}
.nwbar{margin:0 0 10px;padding:8px 12px;border:1px solid var(--shu,#b33);border-radius:6px;background:rgba(179,51,51,.12);font-size:14px}
.nwbar b{color:var(--shu,#c44)}
.nwh{grid-column:1/-1;font-weight:700;color:var(--kin);margin:8px 0 2px;font-size:14px;border-bottom:1px dashed var(--line);padding-bottom:3px}
.nr.nwc{border-left:5px solid var(--shu,#b33)}
.mit.nwc{border-left:5px solid var(--shu,#b33)}
.nwf{margin-left:8px}`;document.head.appendChild(st);
const go0=go;go=function(v){if(v==='scout')UI.nwP=new Set(G.pros.filter(p=>!p.seen).map(p=>p.cid));if(v==='kiroku'&&G.media)UI.nwM=G.media.seen||0;return go0(v);};
const R0=render;render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='scout')mkS();if(UI.view==='kiroku')mkK();}catch(e){console.error(e)}return x;};
function bar(n,unit,extra){return '<div class="nwbar">前回見てから <b>新しい'+unit+' '+n+(unit==='候補'?' 人':' 件')+'</b>'+(extra||'')+'</div>';}
function mkS(){const nl=document.querySelector('.nl');if(!nl)return;const S=UI.nwP||new Set();const rows=[...nl.querySelectorAll(':scope>.nr')];if(rows.length!==G.pros.length)return;
 const isN=rows.map((r,i)=>G.pros[i]&&S.has(G.pros[i].cid));const n=isN.filter(Boolean).length;if(!n)return;
 rows.forEach((r,i)=>{if(!isN[i])return;const sp=r.querySelector('.n span');if(sp)sp.insertAdjacentHTML('beforeend','<span class="nwt">新</span>');if(MODE!=='A')r.classList.add('nwc');});
 const fb=MODE==='C'?'<button class="btn sm nwf" onclick="UI.nwOnly=!UI.nwOnly;render()">'+(UI.nwOnly?'ぜんぶ表示':'新しい候補だけ表示')+'</button>':'';
 nl.insertAdjacentHTML('beforebegin',bar(n,'候補',fb));
 if(MODE==='B'){const hN=document.createElement('div');hN.className='nwh';hN.textContent='新しい候補('+n+' 人)';const hO=document.createElement('div');hO.className='nwh';hO.textContent='前からいる候補('+(rows.length-n)+' 人)';
  const nw=rows.filter((r,i)=>isN[i]),od=rows.filter((r,i)=>!isN[i]);nl.appendChild(hN);nw.forEach(r=>{const nx=r.nextElementSibling;nl.appendChild(r);if(nx&&nx.classList.contains('nopen'))nl.appendChild(nx);});nl.appendChild(hO);od.forEach(r=>{const nx=r.nextElementSibling;nl.appendChild(r);if(nx&&nx.classList.contains('nopen'))nl.appendChild(nx);});}
 if(MODE==='C'&&UI.nwOnly)rows.forEach((r,i)=>{if(!isN[i])r.style.display='none';});}
function mkK(){const g=document.querySelector('.mgrid');if(!g)return;const s0=UI.nwM!=null?UI.nwM:(G.media.seen||0);const L=G.media.L.slice(0,UI.mAll?80:12);const its=[...g.querySelectorAll(':scope>.mit')];
 const isN=its.map((e,i)=>L[i]&&L[i].id>s0);const n=G.media.L.filter(x=>x.id>s0).length;if(!n){its.forEach(e=>e.classList.remove('nw'));return;}
 its.forEach((e,i)=>{e.classList.remove('nw');if(!isN[i])return;const mh=e.querySelector('.mh');if(mh)mh.insertAdjacentHTML('beforeend','<span class="nwt">新</span>');if(MODE!=='A')e.classList.add('nwc');});
 const fb=MODE==='C'?'<button class="btn sm nwf" onclick="UI.nwOnlyM=!UI.nwOnlyM;render()">'+(UI.nwOnlyM?'ぜんぶ表示':'新しい記事だけ表示')+'</button>':'';
 g.insertAdjacentHTML('beforebegin',bar(n,'記事',fb));const dt=g.closest('details');if(dt&&n){dt.open=true;const sm=dt.querySelector('summary');if(sm&&!sm.querySelector('.nwt'))sm.insertAdjacentHTML('beforeend','<span class="nwt">新 '+n+'</span>');const top=dt.parentElement;if(top&&top.parentElement)top.parentElement.insertBefore(top,top.parentElement.querySelector('.pn,details,div'));}
 if(MODE==='B'){const hN=document.createElement('div');hN.className='nwh';hN.textContent='新しい記事('+n+' 件)';const hO=document.createElement('div');hO.className='nwh';hO.textContent='前に読んだ記事';
  const nw=its.filter((e,i)=>isN[i]),od=its.filter((e,i)=>!isN[i]);g.appendChild(hN);nw.forEach(e=>g.appendChild(e));g.appendChild(hO);od.forEach(e=>g.appendChild(e));}
 if(MODE==='C'&&UI.nwOnlyM)its.forEach((e,i)=>{if(!isN[i])e.style.display='none';});}
})('B');
</script>
