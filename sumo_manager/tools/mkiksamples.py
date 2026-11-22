# 見本 ik1〜ik3:一人相撲の記録の画面に「育成の成績」欄(v122 の本体に見本用の表示を足す。数字は見本用の作り物)
# 使い方:cd sumo_manager; python3 tools/mkiksamples.py
base=open('sumo_manager_v122.html',encoding='utf-8').read()
COMMON=r'''
const IKY=[{y:2027,p:11,rk:21},{y:2028,p:19,rk:12},{y:2029,p:26,rk:8},{y:2030,p:34,rk:5},{y:2031,p:28,rk:6}];
const IKTOP=[['木瀬の若','新入幕・三役',41],['肥後ノ龍','新十両・十両優勝',18],['一元','新十両',9]];
const IKRANK=[['伊勢ヶ濱',52],['二所ノ関',47],['追手風',41],['佐渡ヶ嶽',36],['高田川',33],['木瀬',28],['九重',26],['玉ノ井',22],['藤島',21],['春日野',19]];
const IKB=[['新幕下',9],['新十両',4],['新入幕',2],['三役以上',1],['優勝',1],['三賞',2]];
function ikHead(){return '<h2>育成の成績<span class="sub">始めたときに幕下以下だった力士と、そのあと入った力士の点(推定の点数)</span></h2>';}
'''
V={
'ik1':('案1:大きな数字(通算・今年)と順位、内訳の札、年ごとの表、点の多い力士 3 人',r'''
function ikHTML(){const L=IKY[IKY.length-1];
 return '<div class="pn ikp">'+ikHead()+'<div class="ikg"><div class="ikb"><small>通算の育成点</small><b>118</b><span>5 年</span></div><div class="ikb"><small>今年(2031 年)</small><b>'+L.p+'</b><span>点</span></div><div class="ikb hl"><small>育成番付(今年)</small><b>'+L.rk+' 位</b><span>45 部屋中・去年 5 位</span></div></div>'+
 '<div class="ikc">'+IKB.map(x=>'<span>'+x[0]+' <b>'+x[1]+'</b></span>').join('')+'</div>'+
 '<div class="grid2"><div><h4>年ごとの成績</h4><table class="tb"><tr><th>年</th><th>育成点</th><th>育成番付</th></tr>'+IKY.slice().reverse().map(x=>'<tr><td>'+x.y+'年</td><td class="num">'+x.p+'</td><td class="num">'+x.rk+' 位</td></tr>').join('')+'</table></div>'+
 '<div><h4>点の多い力士</h4><table class="tb"><tr><th>四股名</th><th>おもな手柄</th><th>点</th></tr>'+IKTOP.map(x=>'<tr><td class="nm">'+x[0]+'</td><td>'+x[1]+'</td><td class="num">'+x[2]+'</td></tr>').join('')+'</table></div></div></div>';}
''',''),
'ik2':('案2:育成番付の表(上位 10 部屋+この部屋の行に色)が主役。上に今年の点と順位のひとこと',r'''
function ikHTML(){return '<div class="pn ikp">'+ikHead()+'<p class="ik1l">今年の育成点 <b>28 点</b>・<b>45 部屋中 6 位</b>(去年 5 位)。通算 118 点。</p>'+
 '<table class="tb"><tr><th>順位</th><th>部屋</th><th>今年の育成点</th></tr>'+IKRANK.map((x,i)=>'<tr class="'+(x[0]==='木瀬'?'me':'')+'"><td class="num">'+(i+1)+'</td><td>'+x[0]+'部屋</td><td class="num">'+x[1]+'</td></tr>').join('')+'</table>'+
 '<p class="mute" style="font-size:12px">内訳(通算):'+IKB.map(x=>x[0]+' '+x[1]).join('・')+'。点の多い力士:'+IKTOP.map(x=>x[0]+' '+x[2]+' 点').join('・')+'</p></div>';}
''',''),
'ik3':('案3:育成番付の順位の移り変わり(折れ線)と年ごとの点(棒)。横に内訳と点の多い力士',r'''
function ikHTML(){const w=520,h=170,px=34,n=IKY.length,X=i=>px+(w-px-14)*i/(n-1),Yr=r=>14+(r-1)/(45-1)*(h-40),mx=40,Yb=v=>h-22-(h-40)*v/mx;
 let g='';[1,10,20,30,45].forEach(r=>{g+='<line x1="'+px+'" x2="'+(w-10)+'" y1="'+Yr(r)+'" y2="'+Yr(r)+'" stroke="#e5dcc6"/><text x="'+(px-4)+'" y="'+(Yr(r)+4)+'" font-size="10" text-anchor="end" fill="#888">'+r+'位</text>';});
 IKY.forEach((x,i)=>{g+='<rect x="'+(X(i)-12)+'" y="'+Yb(x.p)+'" width="24" height="'+(h-22-Yb(x.p))+'" fill="#c9a24a55"/><text x="'+X(i)+'" y="'+(h-6)+'" font-size="10" text-anchor="middle" fill="#888">'+x.y+'</text>';});
 g+='<polyline points="'+IKY.map((x,i)=>X(i)+','+Yr(x.rk)).join(' ')+'" fill="none" stroke="#b5391f" stroke-width="2.5"/>'+IKY.map((x,i)=>'<circle cx="'+X(i)+'" cy="'+Yr(x.rk)+'" r="4" fill="#b5391f"/><text x="'+X(i)+'" y="'+(Yr(x.rk)-8)+'" font-size="11" text-anchor="middle" fill="#b5391f">'+x.rk+'位</text>').join('');
 return '<div class="pn ikp">'+ikHead()+'<div class="ik3"><div><svg viewBox="0 0 '+w+' '+h+'" style="width:100%;max-width:620px">'+g+'</svg><div class="mute" style="font-size:12px"><span style="color:#b5391f">━</span> 育成番付の順位　<span style="color:#c9a24a">■</span> その年の育成点</div></div>'+
 '<div><p style="margin:0 0 6px">通算 <b>118 点</b>・今年 <b>28 点</b>(6 位)</p><div class="ikc">'+IKB.map(x=>'<span>'+x[0]+' <b>'+x[1]+'</b></span>').join('')+'</div><h4>点の多い力士</h4>'+IKTOP.map((x,i)=>'<div>'+(i+1)+'. <b>'+x[0]+'</b> '+x[2]+' 点 <span class="mute">('+x[1]+')</span></div>').join('')+'</div></div></div>';}
''','''.ik3{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}@media(max-width:700px){.ik3{grid-template-columns:1fr}}'''),
}
CSS='''.ikp h4{margin:10px 0 4px}.ikg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:6px 0 10px}@media(max-width:600px){.ikg{grid-template-columns:1fr 1fr}}
.ikb{border:1px solid var(--line);border-radius:10px;padding:8px 12px}.ikb small{display:block;font-size:12px;opacity:.8}.ikb b{font-size:28px}.ikb span{font-size:12px;margin-left:4px}.ikb.hl{border:2px solid var(--ai)}
.ikc{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}.ikc span{border:1px solid var(--line);border-radius:14px;padding:2px 10px;font-size:13px}
.ik1l{font-size:15px}'''
for k,(note,js,css) in V.items():
    inj='<script>'+COMMON+js+'''
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;go('kiroku');const pn=document.querySelector('#app .pn');pn.insertAdjacentHTML('beforebegin',ikHTML());}catch(e){console.error(e)}},500);});
</script><style>'''+CSS+css+'''</style><div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 '''+k+''':'''+note+'''(数字は見本用)</div>'''
    s=base.replace('</body>\n</html>',inj+'</body>\n</html>',1).replace('<title>Grand Sumo Manager v122</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
