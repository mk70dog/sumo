# 見本 dp1〜dp5:独立の段取りの場面(桐山親方が伊勢ヶ濱部屋から独立する例)。親方のコメントには絵を入れる。
# 使い方:cd sumo_manager; python3 tools/mkdpsamples.py
base=open('sumo_manager_v141.html',encoding='utf-8').read()
CSS='''<style>
#dpx{position:fixed;inset:0;z-index:999;background:rgba(20,16,12,.72);display:flex;align-items:flex-end;justify-content:center;padding:0 10px calc(10px + env(safe-area-inset-bottom))}
#dpx .in{width:100%;max-width:760px;background:#fffaf0;color:#1d1a16;border:2px solid #c9a24a;border-radius:10px 10px 6px 6px;box-shadow:0 -6px 24px rgba(0,0,0,.5);padding:14px 16px;max-height:86vh;overflow:auto;font-family:var(--kaku)}
#dpx h2{margin:0 0 4px;font-size:19px;display:flex;align-items:center;gap:8px}#dpx h2 .st{font-size:12px;font-weight:400;color:#7d7365;margin-left:auto}
.dpstep{display:flex;gap:4px;margin:0 0 10px}.dpstep i{flex:1;height:5px;border-radius:3px;background:#e4d8bf}.dpstep i.on{background:#b3261e}
.dpsay{display:flex;gap:10px;align-items:flex-start;margin:8px 0}.dpsay img,.dpsay .ff{width:84px;flex:none;border-radius:6px;border:3px solid #c9a24a}
.dpsay .ff{writing-mode:vertical-rl;background:linear-gradient(90deg,#d9c39a,#e9d8b4 40%,#d4bd92);font-weight:800;font-size:20px;text-align:center;padding:8px 0;min-height:110px;width:44px;border-width:1px;border-color:#8e7347}
.dpsay .bb{position:relative;flex:1;background:#fff;border:1px solid #c9b48a;border-radius:8px;padding:8px 11px;font-size:15px;line-height:1.6}
.dpsay .bb:before{content:'';position:absolute;left:-8px;top:18px;border:8px solid transparent;border-left:0;border-right-color:#c9b48a}
.dpsay .bb b.who{display:block;font-size:12px;color:#7d7365;font-weight:400}
.dpsay.r{flex-direction:row-reverse}.dpsay.r .bb:before{left:auto;right:-8px;border-right:0;border-left:8px solid #c9b48a}
.dpnote{font-size:13px;color:#5a5044;background:#f3ead6;border-radius:6px;padding:6px 10px;margin:6px 0}
.dpbtn{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.dpbtn button{flex:1;min-width:150px;padding:9px 8px;font:15px var(--kaku);border:1px solid #8e7347;background:#f3ead6;border-radius:6px}.dpbtn button.ai{background:#b3261e;color:#fff;border-color:#b3261e}
.dpbtn button small{display:block;font-size:11px;opacity:.8}
.dptg{display:inline-block;font-size:11px;background:#c9a24a33;border:1px solid #c9a24a88;border-radius:9px;padding:0 6px;margin:2px 3px 0 0}
.dprow{display:flex;gap:8px;align-items:center;border-bottom:1px dashed #d8c9a8;padding:6px 0}.dprow img,.dprow .ff{width:46px;border-radius:4px;border:2px solid #c9a24a;flex:none}
.dprow .ff{writing-mode:vertical-rl;background:#e2cfa6;font-weight:800;text-align:center;font-size:13px;padding:4px 0;width:26px;border-width:1px}
.dprow .nm{font:800 15px var(--kaku);min-width:5em}.dprow .ans{flex:1;font-size:14px}.ans .ok{color:#1d6b3a;font-weight:800}.ans .ng{color:#b3261e;font-weight:800}.ans .mg{color:#a06a00;font-weight:800}
.dpbig{display:flex;gap:14px;align-items:flex-start}.dpbig img{width:150px;border-radius:8px;border:3px solid #c9a24a}
.dpkan{border:3px double #b3261e;color:#b3261e;border-radius:6px;padding:10px;text-align:center;font-size:17px;font-weight:800;margin:6px 0;background:#fff}
.dpkan small{display:block;font-size:12px;font-weight:400;color:#5a5044}
</style>'''
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{
const I=n=>PIMG[n]||PIMGO[n]||null;
const face=(n,lab)=>{const s=I(n);return s?'<img src="'+s+'">':'<div class="ff">'+lab+'</div>';};
const say=(n,who,t,r)=>'<div class="dpsay'+(r?' r':'')+'">'+face(n,who)+'<div class="bb"><b class="who">'+who+'</b>'+t+'</div></div>';
const step=k=>'<div class="dpstep">'+[1,2,3,4].map(i=>'<i class="'+(i<=k?'on':'')+'"></i>').join('')+'</div>';
const H=n=>'<h2>桐山部屋を興す<span class="st">'+['','① 師匠に打ち明ける','② 弟子に声をかける','③ 理事会','④ 門出'][n]+'</span></h2>'+step(n);
const S=location.hash.slice(1)||'1';let h='';
if(S==='1')h=H(1)+say('照ノ富士','師匠 伊勢ヶ濱親方','そうか、部屋を持つか。……お前が育てた弟子だ。連れて行きたい者がいるなら、本人とよく話せ。うちとしても、送り出すからには立派な部屋にしてもらわんとな。')+
 say('宝富士','あなた(桐山親方)','ありがとうございます。近大の後輩たちを中心に、声をかけさせてください。',1)+
 '<div class="dpnote">師匠は<b>快く送り出してくれました</b>。連れて行ける人数はそのまま。元の部屋との関係も良いままです。</div><div class="dpbtn"><button class="ai">弟子に声をかけに行く</button></div>';
if(S==='2')h=H(2)+'<div style="font-size:13px;color:#7d7365">声をかけるのは 3 人。1 人目</div>'+
 '<div class="dpbig">'+face('錦富士','錦富士').replace('<img','<img style="width:150px;border-radius:8px;border:3px solid #c9a24a"')+'<div style="flex:1"><div style="font-size:20px;font-weight:800">錦富士 <span style="font-size:13px;font-weight:400">前頭・29歳</span></div><span class="dptg">同じ近畿大</span><span class="dptg">同郷・青森県</span>'+
 say('','錦富士','親方についていきたい気持ちはあります。ただ、今は番付が上がってきたところで……稽古相手がいなくなるのが少し怖いんです。').replace('<div class="ff">錦富士</div>','').replace('class="dpsay"','class="dpsay" style="margin-top:6px"')+'</div></div>'+
 '<div class="dpnote"><span class="mg">迷っています</span>。どう話しますか。</div>'+
 '<div class="dpbtn"><button class="ai">稽古の方針を語る<small>同じ大学の後輩に効きやすい</small></button><button>親御さんに会いに行く<small>同郷・同じ高校に効きやすい</small></button><button>答えを待つ<small>次の場所の後に返事</small></button></div>';
if(S==='3')h=H(2)+say('宝富士','あなた(桐山親方)','声をかけた 3 人の返事がそろった。',0)+
 [['錦富士','前頭','<span class="ok">ついて来る</span> 「親方の話を聞いて決めました」'],['翠富士','前頭','<span class="ok">ついて来る</span> 「すぐ行きます」'],['尊富士','前頭','<span class="ng">残ります</span> 「兄弟子たちと稽古を続けたいです」']].map(x=>'<div class="dprow">'+face(x[0],x[0])+'<span class="nm">'+x[0]+'<br><small style="font-weight:400">'+x[1]+'</small></span><span class="ans">'+x[2]+'</span></div>').join('')+
 '<div class="dpnote">残ると言った尊富士に、もう一度説得することもできます(見込み:やや低め。断られると元の部屋との関係が少し冷えます)。</div><div class="dpbtn"><button>もう一度説得する</button><button class="ai">本人の気持ちを尊重して次へ</button></div>';
if(S==='4')h=H(3)+'<div class="dpkan">日本相撲協会 理事会<br>桐山部屋の新設を承認<small>伊勢ヶ濱部屋から独立。力士 2 人とともに出発</small></div>'+
 say('照ノ富士','師匠 伊勢ヶ濱親方','承認が下りたな。これからは師匠同士だ。土俵では手加減せんぞ。')+'<div class="dpbtn"><button class="ai">門出へ</button></div>';
if(S==='5')h=H(4)+say('宝富士','新しい師匠 桐山親方','今日から桐山部屋だ。人数は少ないが、そのぶん一人ひとりをしっかり見る。まずは全員で関取を目指そう。')+
 '<div style="display:flex;gap:10px;justify-content:center;margin:8px 0">'+['錦富士','翠富士'].map(n=>'<div style="text-align:center">'+face(n,n).replace('<img','<img style="width:90px;border-radius:6px;border:3px solid #c9a24a"')+'<div style="font-weight:800">'+n+'</div></div>').join('')+'</div>'+
 '<div class="dpnote">元の部屋に残った力士:尊富士(のちに気持ちが変わることもあります)</div><div class="dpbtn"><button class="ai">新しい部屋を始める</button></div>';
document.body.insertAdjacentHTML('beforeend','<div id="dpx"><div class="in">'+h+'</div></div>');window.__ok=1;}catch(e){console.error(e)}},400);});
</script>'''
N={1:'① 師匠に打ち明ける',2:'② 一人ずつ声をかける(迷う力士)',3:'② のまとめ(返事の一覧)',4:'③ 理事会の承認',5:'④ 門出'}
for k,n in N.items():
    s=base.replace('</body>\n</html>',CSS+JS.replace("location.hash.slice(1)||'1'","'%d'"%k)+'<div style="position:fixed;left:6px;top:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 dp%d:%s</div></body>\n</html>'%(k,n),1)
    open('samples/dp%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
