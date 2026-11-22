# 見本 bc1〜bc3:本場所中の過ごし方(朝稽古・午後)の欄、bcm:稽古タブの「初日の見込み」(v124 の本体に見本用の表示を足す。押しても効き目はない)
# 使い方:cd sumo_manager; python3 tools/mkbcsamples.py
base=open('sumo_manager_v124.html',encoding='utf-8').read()
COMMON=r'''
const BA={し:'しっかり',軽:'軽め',休:'休む'},BP={昼:'昼寝',治:'治療',自:'自由時間'};
const BAD={し:'四股・すり足・ぶつかり。調子 +・疲れ +',軽:'四股・すり足だけ。いつもどおり',休:'稽古場に下りない。疲れが抜ける・調子 −'};
window.__bc={};
function bcOf(r){return window.__bc[r.id]||(window.__bc[r.id]={a:r.d<=1?'軽':'し',p:r.inj?'治':'昼'});}
function bcSet(id,k,v){bcOf(G.R[id])[k]=v;bcMount();}
function bcGrp(g,k,v){bcL().filter(r=>bcG(r)===g).forEach(r=>bcOf(r)[k]=v);bcMount();}
function bcG(r){return r.d<=1?'関取':r.d===2?'幕下':'三段目以下';}
function bcL(){return own().filter(r=>G.B&&G.B.rec[r.id]&&!G.B.rec[r.id].ky).sort((a,b)=>a.pos-b.pos);}
function bar(v,c){return '<span class="bcbar"><i style="width:'+Math.round(v)+'%;background:'+c+'"></i></span>';}
function chips(id,k,M,cur){return Object.keys(M).map(x=>'<button class="pc'+(cur===x?' on':'')+'" onclick="bcSet('+id+',\''+k+'\',\''+x+'\')">'+M[x]+'</button>').join('');}
function bcNote(){return '<p class="mute" style="font-size:12px;margin:4px 0 0">朝稽古:しっかり=四股・すり足・ぶつかり(調子 +0.4・疲れ +3/日)/軽め=四股・すり足(いつもどおり)/休む=疲れ −3・調子 −0.3。午後:昼寝=疲れ −1/治療=けがの治り +(治療院と契約で大きい)/自由時間=気力 +。場所中のちゃんこがソップ(鶏)なら気力 +(縁起)。数字は推定。</p>';}
'''
V={
'bc1':('案1:番付ごとにまとめて決める行+力士ごとの小さな札(押すと個別に変えられる)',r'''
function bcHTML(){const L=bcL();const G3=['関取','幕下','三段目以下'].filter(g=>L.some(r=>bcG(r)===g));
 return '<div class="pn bcp"><h2>場所中の過ごし方<span class="sub">明日の朝稽古と午後。番付ごとにまとめて決めて、力士ごとに変えられます</span></h2>'+
 G3.map(g=>{const R=L.filter(r=>bcG(r)===g);const a=R.every(r=>bcOf(r).a===R[0]&&0)?'':'';const same=k=>R.every(r=>bcOf(r)[k]===bcOf(R[0])[k])?bcOf(R[0])[k]:'';
  return '<div class="bcg"><b>'+g+' '+R.length+' 人</b><div class="bcr"><span class="lb">朝稽古</span>'+Object.keys(BA).map(x=>'<button class="pc'+(same('a')===x?' on':'')+'" onclick="bcGrp(\''+g+'\',\'a\',\''+x+'\')">'+BA[x]+'</button>').join('')+'<span class="lb">午後</span>'+Object.keys(BP).map(x=>'<button class="pc'+(same('p')===x?' on':'')+'" onclick="bcGrp(\''+g+'\',\'p\',\''+x+'\')">'+BP[x]+'</button>').join('')+'</div>'+
  '<div class="bcc">'+R.map(r=>{const o=bcOf(r);return '<div class="bck"><div><span class="mute">'+esc(r.rkS)+'</span> <b class="nm">'+esc(r.n)+'</b></div><div class="mute" style="font-size:11px">調子 '+bar(r.cond,'#7aa7d8')+' 疲労 '+bar(r.fat,r.fat>60?'#d66':'#8c8')+'</div><div class="bct">'+BA[o.a]+'・'+BP[o.p]+'</div></div>';}).join('')+'</div></div>';}).join('')+bcNote()+'</div>';}
''',''),
'bc2':('案2:表で 1 人 1 行(調子・疲労・きのうの結果・朝稽古・午後)',r'''
function bcHTML(){const L=bcL();
 return '<div class="pn bcp"><h2>場所中の過ごし方<span class="sub">明日の朝稽古と午後</span></h2><div style="overflow-x:auto"><table class="tb bct2"><tr><th>番付</th><th>四股名</th><th>調子</th><th>疲労</th><th>成績</th><th>朝稽古</th><th>午後</th></tr>'+
 L.map(r=>{const o=bcOf(r),c=G.B.rec[r.id];return '<tr><td>'+esc(r.rkS)+'</td><td class="nm">'+esc(r.n)+'</td><td>'+bar(r.cond,'#7aa7d8')+'</td><td>'+bar(r.fat,r.fat>60?'#d66':'#8c8')+'</td><td>'+c.w+'勝'+c.l+'敗</td><td>'+chips(r.id,'a',BA,o.a)+'</td><td>'+chips(r.id,'p',BP,o.p)+'</td></tr>';}).join('')+'</table></div>'+bcNote()+'</div>';}
''',''),
'bc3':('案3:力士ごとの大きめの札(調子・疲労の棒と、朝稽古・午後のボタン)。おすすめ「疲れていたら休ませる」ボタン',r'''
function bcAuto(){bcL().forEach(r=>{const o=bcOf(r);o.a=r.fat>60?'休':r.cond<45?'し':'軽';o.p=r.inj?'治':r.fat>50?'昼':'自';});bcMount();}
function bcHTML(){const L=bcL();
 return '<div class="pn bcp"><h2>場所中の過ごし方<span class="sub">明日の朝稽古と午後</span></h2><div class="btns" style="margin:0 0 8px"><button class="btn main" onclick="bcAuto()">おすすめにする(疲れていたら休ませる)</button></div><div class="bcc3">'+
 L.map(r=>{const o=bcOf(r),c=G.B.rec[r.id];return '<div class="bk3'+(r.d<=1?' sk':'')+'"><div><span class="mute">'+esc(r.rkS)+'</span> <b class="nm">'+esc(r.n)+'</b> <span class="mute">'+c.w+'勝'+c.l+'敗</span></div><div class="mute" style="font-size:12px">調子 '+bar(r.cond,'#7aa7d8')+' '+Math.round(r.cond)+'　疲労 '+bar(r.fat,r.fat>60?'#d66':'#8c8')+' '+Math.round(r.fat)+'</div><div class="bcr"><span class="lb">朝稽古</span>'+chips(r.id,'a',BA,o.a)+'</div><div class="bcr"><span class="lb">午後</span>'+chips(r.id,'p',BP,o.p)+'</div></div>';}).join('')+'</div>'+bcNote()+'</div>';}
''','''.bcc3{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:8px}.bk3{border:1px solid var(--line);border-radius:8px;padding:8px}.bk3.sk{border-color:#c9a24a;border-width:2px}'''),
}
CSS='''.bcp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 10px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important}.bcp .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
.bcp .lb{font:bold 13px sans-serif;margin:0 4px 0 8px}.bcg{border:1px solid var(--line);border-radius:8px;padding:8px;margin:6px 0}.bcr{display:flex;align-items:center;flex-wrap:wrap;gap:2px;margin:4px 0}
.bcc{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:6px;margin-top:6px}.bck{border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:13px;cursor:pointer}.bct{font-size:12px;color:#7a1d10}
.bcbar{display:inline-block;width:46px;height:7px;background:#0002;border-radius:4px;overflow:hidden;vertical-align:middle}.bcbar i{display:block;height:100%}
.bct2 td{vertical-align:middle;white-space:nowrap}'''
MOUNT=r'''
function bcMount(){document.querySelectorAll('.bcp').forEach(e=>e.remove());const h=[...document.querySelectorAll('#app .pn')].find(p=>/日目の取組/.test((p.querySelector('h2')||{}).textContent||''));if(h)h.insertAdjacentHTML('beforebegin',bcHTML());}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;let g=0;while(G.phase==='train'&&g++<20)doWeek();for(let d=0;d<3;d++)UI.bouts=advanceDay();own().forEach((r,i)=>{r.fat=[20,35,72,48,15,62,30][i%7];r.cond=[70,55,40,62,80,45,58][i%7];});go('basho');bcMount();}catch(e){console.error(e)}},500);});
'''
for k,(note,js,css) in V.items():
    inj='<script>'+COMMON+js+MOUNT+'</script><style>'+CSS+css+'</style><div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 '+k+':'+note+'(押しても効き目はありません)</div>'
    s=base.replace('</body>\n</html>',inj+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v124</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
# 稽古タブの「初日の見込み」
BCM=r'''<script>
function pkGuess(r){const L=(r.ld||[]).slice();const wk=G.wk||1;return wk;}
const kt0=keikoHTML;keikoHTML=function(){let h=kt0();return h;};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;for(let i=0;i<4;i++)doWeek();go('keiko');
 const W=['仕上がり上々(調子 +11)','まずまず(調子 +5)','ふつう','疲れが残る(調子 −8)'],C=['#2e7d4f','#5a8f3a','#888','#b5391f'],T=['このまま最後の 2 週を軽めに','最後の 2 週を軽めにすると上々に','前半の稽古がやや少ない','疲労 68。休養か軽めを'];
 document.querySelectorAll('#app .nm').forEach((e,i)=>{const card=e.closest('div[class]');if(!card||card.querySelector('.pkm'))return;const k=i%4;e.insertAdjacentHTML('afterend','<div class="pkm" style="border-left:4px solid '+C[k]+'"><b style="color:'+C[k]+'">初日の見込み:'+W[k]+'</b><br><span>'+T[k]+'</span></div>');});
 const pn=document.querySelector('#app .pn');pn.insertAdjacentHTML('afterbegin','<div class="pkall">初日の見込み(部屋全体):上々 4 人・まずまず 9 人・ふつう 5 人・<b style="color:#b5391f">疲れが残る 2 人</b>　<span class="mute">前半 4 週しっかり → 最後の 2 週を軽めにすると、初日の調子が上がります</span></div>');
}catch(e){console.error(e)}},500);});
</script><style>.pkm{font:12px sans-serif;margin:4px 0;padding:2px 8px;background:#fff8;border-radius:4px}.pkall{font:13px sans-serif;background:#fff3cf;border-radius:8px;padding:6px 10px;margin:4px 0 8px}</style>
<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 bcm:稽古タブの力士の札と上に「初日の見込み」(どの案でも同じ。中身は見本用)</div>'''
s=base.replace('</body>\n</html>',BCM+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v124</title>','<title>見本 bcm</title>',1)
open('samples/bcm.html','w',encoding='utf-8').write(s)
print('ok')
