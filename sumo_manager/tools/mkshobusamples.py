# 見本 sb0〜sb3:二人相撲の「勝負の形」(v101 の次の版の見本。通信はしない・数字はすべて見本用の作り物)
# sb0=始めるときに形を選ぶ画面(親)と、子の参加画面
# sb1=点数勝負、sb2=先に目標に届いたほうの勝ち、sb3=部屋番付(④記録だけは帯も欄も出さない)
# 使い方:cd sumo_manager; python3 tools/mkshobusamples.py
base=open('sumo_manager_v101.html',encoding='utf-8').read()
CSS='''<style>
.mpb{position:relative;z-index:60;display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:#1d2a3a;color:#fff;padding:6px 12px;font:13px sans-serif}
.mpb .pl{display:flex;align-items:center;gap:6px;background:#ffffff1a;border-radius:14px;padding:2px 10px}
.mpb .dot{width:10px;height:10px;border-radius:50%;background:#888}.mpb .dot.ok{background:#5c5}.mpb .dot.wait{background:#fc4}
.mpb .mpt{margin-left:auto;opacity:.8}
.sbb{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:#2b3d52;color:#fff;padding:5px 12px;font:13px sans-serif;border-top:1px solid #ffffff22}
.sbb .tag{background:#c9a44c;color:#222;border-radius:10px;padding:1px 9px;font-weight:bold}
.sbb .sc{display:flex;align-items:center;gap:6px;background:#ffffff1a;border-radius:14px;padding:2px 10px}.sbb .sc b{font-size:15px}
.sbb .lead{color:#ffd76a;font-weight:bold}
.sbb .bar{display:inline-block;width:90px;height:8px;background:#ffffff33;border-radius:4px;overflow:hidden;vertical-align:middle}.sbb .bar i{display:block;height:100%;background:#c9a44c}
.sbc{border:2px solid var(--ai);border-radius:10px;padding:12px;margin:10px 0;background:#fffc;font-family:sans-serif}
.sbc h3{margin:0 0 8px}.sbc .mute{color:#777;font-size:12px}
.sbg{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:600px){.sbg{grid-template-columns:1fr}}
.sbp{border:1px solid var(--line);border-radius:8px;padding:8px}
.opt{display:block;border:2px solid var(--line);border-radius:10px;padding:10px 12px;margin:8px 0;background:#fff}
.opt.on{border-color:var(--ai);background:#fff7e0}.opt b{font-size:16px}.opt .ds{font-size:13px;color:#555;margin-top:3px}
.opt .ch{display:flex;gap:6px;margin-top:6px;flex-wrap:wrap}.opt .ch span{border:1px solid var(--line);border-radius:14px;padding:2px 12px;font-size:13px;background:#fff}.opt .ch span.on{background:var(--ai);color:#fff;border-color:var(--ai)}
table.sbt{border-collapse:collapse;width:100%;font-size:13px}table.sbt th,table.sbt td{border-bottom:1px solid var(--line);padding:3px 6px;text-align:right}table.sbt th:first-child,table.sbt td:first-child{text-align:left}
table.sbt tr.me td{background:#fff3cf}
.trk{position:relative;height:34px;margin:6px 0 22px}.trk .ln{position:absolute;left:0;right:0;top:15px;height:4px;background:#ddd;border-radius:2px}
.trk .pg{position:absolute;left:0;top:15px;height:4px;border-radius:2px}
.trk .st{position:absolute;top:8px;width:18px;height:18px;border-radius:50%;background:#fff;border:2px solid #bbb;margin-left:-9px}.trk .st.d{background:var(--ai);border-color:var(--ai)}
.trk .st em{position:absolute;top:22px;left:50%;transform:translateX(-50%);font:11px sans-serif;font-style:normal;white-space:nowrap;color:#555}
.trk .who{position:absolute;top:-6px;font:bold 11px sans-serif;margin-left:-14px;padding:1px 5px;border-radius:8px;color:#fff;white-space:nowrap}
.sw{position:fixed;right:6px;bottom:6px;z-index:9999;display:flex;gap:4px}.sw button{font:13px sans-serif;padding:6px 10px;border-radius:8px;border:1px solid #888;background:#fff}.sw button.on{background:#1d2a3a;color:#fff}
</style>'''
JS=r'''
<script>
(function(){
const V='__V__';
const MP='<div class="mpb"><b>二人相撲</b><span class="pl"><span class="dot ok"></span>木瀬部屋(親)準備できた</span><span class="pl"><span class="dot wait"></span>伊勢ノ海部屋(子)稽古を決めています…</span><span class="mpt">受け取り 14:52:10</span></div>';
// 見本用の点数(場所ごと)。木瀬=A、伊勢ノ海=B
const A=[3,3,4,5,4,6,5,7,6,8,9,7,8,10,9,11,10,9,12,11,13,12,14,13];
const B=[2,3,3,4,5,5,6,6,7,7,8,9,9,8,10,10,11,12,11,12,12,13,12,14];
const BN=['2026年1月','3月','5月','7月','9月','11月'];
function bname(i){const y=2026+Math.floor((i)/6),m=['1','3','5','7','9','11'][i%6];return y+'年'+m+'月';}
const N=17; // 見本は 17 場所目(2028年11月)まで進んだ状態
const cumA=[],cumB=[];A.slice(0,N).reduce((s,x,i)=>cumA[i]=s+x,0);B.slice(0,N).reduce((s,x,i)=>cumB[i]=s+x,0);
const ta=cumA[N-1],tb=cumB[N-1];
function chart(){const w=560,h=170,px=34,py=12,n=N,mx=Math.max(ta,tb)*1.08;const X=i=>px+(w-px-10)*i/(n-1),Y=v=>h-18-(h-18-py)*v/mx;
 const pa=cumA.map((v,i)=>X(i)+','+Y(v)).join(' '),pb=cumB.map((v,i)=>X(i)+','+Y(v)).join(' ');
 let g='';for(let k=0;k<=4;k++){const v=Math.round(mx*k/4);g+='<line x1="'+px+'" x2="'+(w-10)+'" y1="'+Y(v)+'" y2="'+Y(v)+'" stroke="#e5dcc6"/><text x="'+(px-4)+'" y="'+(Y(v)+4)+'" font-size="10" text-anchor="end" fill="#888">'+v+'</text>';}
 [0,5,11,16].forEach(i=>g+='<text x="'+X(i)+'" y="'+(h-4)+'" font-size="10" text-anchor="middle" fill="#888">'+bname(i).replace('年','/').replace('月','')+'</text>');
 return '<svg viewBox="0 0 '+w+' '+h+'" style="width:100%;max-width:640px">'+g+'<polyline points="'+pb+'" fill="none" stroke="#3b7fc4" stroke-width="2.5"/><polyline points="'+pa+'" fill="none" stroke="#b5391f" stroke-width="2.5"/><circle cx="'+X(n-1)+'" cy="'+Y(ta)+'" r="4" fill="#b5391f"/><circle cx="'+X(n-1)+'" cy="'+Y(tb)+'" r="4" fill="#3b7fc4"/></svg><div class="mute"><span style="color:#b5391f">━</span> 木瀬部屋(親)　<span style="color:#3b7fc4">━</span> 伊勢ノ海部屋(子)</div>';}
// ---------- 帯 ----------
function bandSB(){
 if(V==='sb1')return '<div class="sbb"><span class="tag">点数勝負 10 年</span><span class="sc">木瀬 <b>'+ta+'</b>点</span><span class="sc">伊勢ノ海 <b>'+tb+'</b>点</span><span class="lead">木瀬が '+(ta-tb)+' 点リード</span><span style="margin-left:auto">残り 7 年 1 場所(43 場所)</span></div>';
 if(V==='sb2')return '<div class="sbb"><span class="tag">目標:横綱を出す</span><span class="sc">木瀬 大関まで <span class="bar"><i style="width:84%"></i></span></span><span class="sc">伊勢ノ海 関脇まで <span class="bar"><i style="width:68%"></i></span></span><span style="margin-left:auto" class="lead">木瀬がリード</span></div>';
 if(V==='sb3')return '<div class="sbb"><span class="tag">部屋番付</span><span class="sc">今場所 <b>木瀬 1位</b>・伊勢ノ海 2位</span><span class="sc">通算 1位 9回・2位 8回</span><span style="margin-left:auto">終わりなし</span></div>';
 return '';}
// ---------- 記録の「勝負」欄 ----------
function cardSB(){
 if(V==='sb1'){let rows='';for(let i=N-1;i>=N-6;i--)rows+='<tr><td>'+bname(i)+'</td><td>'+A[i]+'</td><td>'+B[i]+'</td><td>'+(cumA[i])+'</td><td>'+(cumB[i])+'</td></tr>';
  return '<div class="sbc"><h3>勝負(点数勝負 10 年)</h3><div class="sbg"><div class="sbp"><b style="color:#b5391f">木瀬部屋(親)</b><div style="font-size:26px;font-weight:bold">'+ta+'<small style="font-size:13px"> 点</small></div><div class="mute">1 位</div></div><div class="sbp"><b style="color:#3b7fc4">伊勢ノ海部屋(子)</b><div style="font-size:26px;font-weight:bold">'+tb+'<small style="font-size:13px"> 点</small></div><div class="mute">2 位・'+(ta-tb)+' 点差</div></div></div>'+
  '<h4 style="margin:10px 0 2px">点数の移り変わり</h4>'+chart()+
  '<h4 style="margin:10px 0 2px">場所ごとの点数</h4><table class="sbt"><tr><th>場所</th><th>木瀬</th><th>伊勢ノ海</th><th>木瀬 合計</th><th>伊勢ノ海 合計</th></tr>'+rows+'</table>'+
  '<h4 style="margin:10px 0 2px">先場所(2028年9月)の木瀬の点数のわけ</h4><div style="font-size:13px;line-height:1.7">関取 4 人 +4 ／ 三役 1 人 +2 ／ 大関 1 人 +3 ／ 十両優勝 +3 ／ 三賞 +2 ／ 新入幕 +3 ／ 不祥事 −5 ＝ <b>'+A[N-1]+' 点</b><br><span class="mute">点数のきまりは推定です(遊びながら直します)。期間が終わると、多いほうが勝ち。そのあとも続けられます。</span></div></div>';}
 if(V==='sb2'){const st=['幕下','十両','幕内','三役','大関','横綱'],pos=[8,24,42,62,80,100];
  const trk=(who,col,p)=>'<div class="trk"><div class="ln"></div><div class="pg" style="width:'+p+'%;background:'+col+'"></div>'+st.map((s,i)=>'<div class="st'+(pos[i]<=p?' d':'')+'" style="left:'+pos[i]+'%"><em>'+s+'</em></div>').join('')+'<div class="who" style="left:'+p+'%;background:'+col+'">'+who+'</div></div>';
  return '<div class="sbc"><h3>勝負(先に目標に届いたほうの勝ち)</h3><p style="margin:0 0 4px"><b>目標:自分の部屋から横綱を出す</b></p>'+
  '<div class="sbp"><b style="color:#b5391f">木瀬部屋(親)</b>:いちばん高い力士 大関'+trk('いまここ','#b5391f',80)+'</div><div style="height:6px"></div>'+
  '<div class="sbp"><b style="color:#3b7fc4">伊勢ノ海部屋(子)</b>:いちばん高い力士 関脇'+trk('いまここ','#3b7fc4',68)+'</div>'+
  '<p class="mute" style="margin:8px 0 0">ほかの目標:「幕内優勝を先に 3 回」「関取を先に 5 人」から、始めるときに選べます。届いた時点でお知らせ(そのあとも続けられます)。</p></div>';}
 if(V==='sb3'){let rows='';const rk=[[1,2],[1,2],[2,1],[1,2],[1,2],[2,1],[1,2],[1,2],[2,1],[1,2],[1,2],[2,1],[1,2],[1,2],[2,1],[1,2],[1,2]];
  for(let i=N-1;i>=N-8;i--){const r=rk[i];rows+='<tr class="'+(r[0]===1?'me':'')+'"><td>'+bname(i)+'</td><td>'+r[0]+' 位</td><td>'+r[1]+' 位</td><td>'+(A[i]+3)+'</td><td>'+(B[i]+2)+'</td></tr>';}
  return '<div class="sbc"><h3>勝負(部屋番付・終わりなし)</h3><p style="margin:0 0 6px">部屋の格は、場所ごとに「関取の数・最高位・優勝・三賞」から決めます(点数の目安はわかりやすく画面に出します)。</p>'+
  '<div class="sbg"><div class="sbp"><b style="color:#b5391f">木瀬部屋(親)</b><br>今場所 <b style="font-size:22px">1 位</b><br><span class="mute">通算 1 位 9 回・2 位 8 回</span></div><div class="sbp"><b style="color:#3b7fc4">伊勢ノ海部屋(子)</b><br>今場所 <b style="font-size:22px">2 位</b><br><span class="mute">通算 1 位 8 回・2 位 9 回</span></div></div>'+
  '<h4 style="margin:10px 0 2px">場所ごとの順位</h4><table class="sbt"><tr><th>場所</th><th>木瀬</th><th>伊勢ノ海</th><th>木瀬の格点</th><th>伊勢ノ海の格点</th></tr>'+rows+'</table></div>';}
 return '';}
// ---------- 始めるときの選択画面(sb0) ----------
function pickHTML(sel){
 const o=(k,t,d,ch)=>'<div class="opt'+(sel===k?' on':'')+'"><b>'+(sel===k?'◉ ':'○ ')+t+'</b><div class="ds">'+d+'</div>'+(ch?'<div class="ch">'+ch+'</div>':'')+'</div>';
 const chp=(a,s)=>a.map((x,i)=>'<span class="'+(i===s?'on':'')+'">'+x+'</span>').join('');
 return '<div class="pn sbc"><h2>勝負の形を選ぶ<span class="sub">親(木瀬部屋)が決めます。子には参加の画面に出ます</span></h2>'+
 o(1,'① 点数勝負','場所ごとの点数を足して、期間が終わったときに多いほうが勝ち。','期間: '+chp(['5 年','10 年','20 年'],1))+
 o(2,'② 先に目標に届いたほうの勝ち','決まった目標に先に届いたほうが勝ち。','目標: '+chp(['横綱を出す','幕内優勝 3 回','関取 5 人'],0))+
 o(3,'③ 部屋番付','場所ごとにふたりの部屋の格を順位づけ。終わりなしで、通算の順位を競う。','')+
 o(4,'④ 記録だけ','勝ち負けはつけない。いまの二人相撲のまま、成績表を並べて見られる。','')+
 '<p class="mute">どの形でも、そのあとも遊びつづけられます。始めたあとは形を変えられません(ふたりが同意すればやり直し)。</p><div class="btns"><button class="btn main big">この形で合言葉を作る</button></div></div>';}
function joinHTML(){return '<div class="pn sbc"><h2>受け持つ部屋を選ぶ<span class="sub">木瀬部屋(親)の世界に参加します</span></h2>'+
 '<div class="sbp" style="background:#fff7e0;margin-bottom:10px"><b>勝負の形:点数勝負(10 年)</b><div class="ds" style="font-size:13px">2026年1月〜2035年11月の 60 場所で、点数の多いほうが勝ち。親が決めた形です。</div></div>'+
 '<div class="btns"><button class="btn">伊勢ノ海部屋<br><small>関取 1・弟子 12</small></button> <button class="btn">高田川部屋<br><small>関取 3・弟子 20</small></button></div></div>';}
function mount(view){
 document.querySelectorAll('.mpb,.sbb,.sbc').forEach(e=>e.remove());
 const app=document.querySelector('#app');
 if(view==='pick'){go('home');const pn=app.querySelector('.pn');pn.insertAdjacentHTML('beforebegin',pickHTML(+((V.match(/\d/)||[1])[0])||1));app.insertAdjacentHTML('afterbegin',MP);return;}
 if(view==='join'){go('home');const pn=app.querySelector('.pn');pn.insertAdjacentHTML('beforebegin',joinHTML());app.insertAdjacentHTML('afterbegin',MP);return;}
 go(view);app.insertAdjacentHTML('afterbegin',MP+bandSB());
 if(view==='kiroku'){const pn=app.querySelector('.pn');pn.insertAdjacentHTML('beforebegin',cardSB());}
}
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;for(let i=0;i<2;i++)doWeek();
 const views=V==='sb0'?[['pick','親:形を選ぶ'],['join','子:参加画面']]:[['home','ホーム(帯)'],['kiroku','記録(勝負欄)']];
 const sw=document.createElement('div');sw.className='sw';sw.innerHTML=views.map((v,i)=>'<button data-v="'+v[0]+'">'+v[1]+'</button>').join('');document.body.appendChild(sw);
 const pick=v=>{sw.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));mount(v);};
 sw.onclick=e=>{const b=e.target.closest('button');if(b)pick(b.dataset.v);};
 pick(window.__first||views[0][0]);
 window.__pick=pick;
}catch(e){console.error(e)}},400);});
})();
</script>
'''
NOTE={'sb0':'sb0:始めるとき(親)に形を選ぶ画面と、子の参加画面。①点数 ②目標 ③部屋番付 ④記録だけ',
 'sb1':'sb1:①点数勝負。上に点数の帯、記録に「勝負」欄(点数の移り変わり・場所ごとの内訳)',
 'sb2':'sb2:②先に目標に届いたほうの勝ち。帯に目標への進み具合、記録に番付の道のり',
 'sb3':'sb3:③部屋番付(終わりなし)。帯に今場所の順位、記録に場所ごとの順位表'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:55vw">見本 '+n+'(通信はしません・数字は見本用)</div></body>',1)
    s=s.replace('<title>Grand Sumo Manager v101</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
