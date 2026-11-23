# 新弟子の画面「学校とのつきあい」の見本 sk1〜sk3(ダルマさん「見やすくわかりやすく サンプル」、漆黒・金の画面の写真)
# 本体を開いて伊勢ヶ濱部屋で始め、schoolPanel を見本の形に差し替えて写真を撮る。数値は本体の値(G.rel など)をそのまま使う。
# usage: python3 tools/mksksamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.skx{font-family:var(--kaku,sans-serif)}
.skx .nmx{font-weight:700;font-size:16px;color:var(--sumi);letter-spacing:.02em}
.skx .subx{font-size:12px;color:var(--mute);margin-top:2px}
.skx .ob{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--kin);color:var(--kin);margin-left:4px}
.skx .lead{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}
.skx .lead span{font-size:13px;padding:4px 10px;border-radius:14px;background:var(--washi2);border:1px solid var(--line);color:var(--sumi2)}
.skx .lead b{color:var(--kin)}
.skx .bar{display:block!important;overflow:visible!important;margin:0!important;width:100%!important;max-width:none!important;position:relative;height:10px;border-radius:5px;background:var(--washi2);border:1px solid var(--line);overflow:visible;min-width:120px}
.skx .bar i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:linear-gradient(90deg,#7a6326,var(--kin))}
.skx .bar i.lo{background:#555}
.skx .bar u{position:absolute;left:20%;top:-4px;bottom:-4px;width:2px;background:var(--ai)}
.skx .st{display:inline-block;font-size:12px;font-weight:700;padding:1px 8px;border-radius:10px;white-space:nowrap}
.skx .st.ok{background:rgba(212,175,74,.18);color:var(--kin);border:1px solid var(--kin)}
.skx .st.near{background:rgba(143,176,224,.15);color:var(--ai);border:1px solid var(--ai)}
.skx .st.far{color:var(--mute);border:1px solid var(--line)}
.skx .act{display:flex;gap:6px;flex-wrap:wrap}
.skx .act button{font:600 13px var(--kaku,sans-serif);padding:6px 10px;border-radius:6px;border:1px solid #3a3a3a;background:linear-gradient(#1e1e1e,#111);color:var(--sumi);line-height:1.25;text-align:left}
.skx .act button small{display:block;font-size:11px;color:var(--mute);font-weight:400}
/* sk1 表 */
.skx table{width:100%;border-collapse:collapse}
.skx th{font-size:12px;color:var(--mute);text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);font-weight:400}
.skx td{padding:9px 8px;border-bottom:1px solid var(--line);vertical-align:middle}
.skx td.rl{width:34%}
.skx .rlrow{display:flex;align-items:center;gap:8px}.skx .rlrow .bar{flex:1}
.skx .num{font-size:15px;font-weight:700;min-width:26px;text-align:right;color:var(--sumi)}
/* sk2 カード */
.skx .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.skx .cd{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 12px;display:flex;flex-direction:column;gap:7px}
.skx .cd.ok{border-color:var(--kin)}
.skx .cd .hd{display:flex;justify-content:space-between;align-items:flex-start;gap:6px}
.skx .cd .act button{flex:1}
.skx .cd .rlrow>div{flex:1 1 auto}
/* sk3 段 */
.skx .sum{display:flex;gap:10px;margin:4px 0 10px;flex-wrap:wrap}
.skx .sum div{flex:1;min-width:120px;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 10px;text-align:center}
.skx .sum b{display:block;font-size:24px;color:var(--kin)}.skx .sum div:nth-child(2) b{color:var(--ai)}.skx .sum div:nth-child(3) b{color:var(--mute)}
.skx .sum small{font-size:12px;color:var(--mute)}
.skx h4{font-size:14px;margin:12px 0 4px;color:var(--sumi2);border-left:3px solid var(--kin);padding-left:8px}
.skx h4.n{border-color:var(--ai)}.skx h4.f{border-color:#555}
.skx .ln{display:flex;align-items:center;gap:10px;padding:7px 4px;border-bottom:1px solid var(--line)}
.skx .ln .a{flex:1;min-width:0}
.skx .ln .b{width:160px}
.skx .ln .act button{padding:5px 9px}
@media (max-width:700px){.skx td.rl{width:auto}.skx table,.skx tbody,.skx tr,.skx td{display:block;width:100%}.skx tr{border-bottom:1px solid var(--line);padding:6px 0}.skx td{border:none;padding:3px 4px}.skx th{display:none}
 .skx .ln{flex-wrap:wrap}.skx .ln .b{width:100%;order:3}.skx .ln .act{order:2}}
"""
JS = r"""(v)=>{
 const L=SCH.map(x=>x[0]).sort((a,b)=>(G.rel[b]||0)-(G.rel[a]||0)).slice(0,10);
 const rv=n=>Math.round(G.rel[n]||0);
 const st=n=>{const x=rv(n);return x>=20?'<span class="st ok">紹介してくれる</span>':x>=10?'<span class="st near">あと '+(20-x)+'</span>':'<span class="st far">まだ遠い</span>';};
 const bar=n=>{const x=rv(n);return '<div class="bar"><i class="'+(x<20?'lo':'')+'" style="width:'+Math.min(100,x)+'%"></i><u></u></div>';};
 const sub=n=>{const s=schOf(n);return '<div class="subx">'+s[2]+(s[1]==='高'?'・高校':s[1]==='大'?'・大学':'')+(alumni(0,n)?'<span class="ob">部屋の OB '+alumni(0,n)+' 人</span>':'')+'</div>';};
 const act=(n,short)=>'<div class="act"><button>親方が挨拶'+(short?'':'<small>関係 +5・5 万円</small>')+'</button><button>出稽古に招く'+(short?'':'<small>関係 +7・10 万円</small>')+'</button></div>';
 const lead='<div class="lead"><span>関係 <b>20 以上</b> で卒業前の選手を紹介してくれる</span><span>1 場所ごとに <b>少しずつ下がる</b></span><span>挨拶 <b>+5</b>・出稽古 <b>+7</b></span></div>';
 let h='<h3>学校とのつきあい</h3>';
 if(v===1){h+=lead+'<table><tr><th>学校</th><th>関係(青い線=20)</th><th></th></tr>'+L.map(n=>'<tr><td><div class="nmx">'+esc(schLabel(n))+'</div>'+sub(n)+'</td><td class="rl"><div class="rlrow"><span class="num">'+rv(n)+'</span>'+bar(n)+'</div><div style="margin-top:4px">'+st(n)+'</div></td><td>'+act(n)+'</td></tr>').join('')+'</table>';}
 if(v===2){h+=lead+'<div class="grid">'+L.map(n=>'<div class="cd '+(rv(n)>=20?'ok':'')+'"><div class="hd"><div><div class="nmx">'+esc(schLabel(n))+'</div>'+sub(n)+'</div>'+st(n)+'</div><div class="rlrow" style="display:flex;gap:8px;align-items:center;width:100%"><span class="num">'+rv(n)+'</span><div style="flex:1 1 auto;width:100%">'+bar(n)+'</div></div>'+act(n)+'</div>').join('')+'</div>';}
 if(v===3){const A=L.filter(n=>rv(n)>=20),B=L.filter(n=>rv(n)>=10&&rv(n)<20),C=L.filter(n=>rv(n)<10);
  const row=n=>'<div class="ln"><div class="a"><div class="nmx">'+esc(schLabel(n))+' <span class="num" style="font-size:13px;color:var(--mute)">'+rv(n)+'</span></div>'+sub(n)+'</div><div class="b">'+bar(n)+'</div>'+act(n,1)+'</div>';
  h+='<div class="sum"><div><b>'+A.length+'</b><small>紹介してくれる学校</small></div><div><b>'+B.length+'</b><small>あと少し(10〜19)</small></div><div><b>'+C.length+'</b><small>まだ遠い</small></div></div>'+
   '<div class="lead"><span>関係 <b>20 以上</b> で紹介</span><span>挨拶 <b>+5</b>(5 万円)</span><span>出稽古 <b>+7</b>(10 万円)</span><span>1 場所ごとに少しずつ下がる</span></div>'+
   (A.length?'<h4>紹介してくれる学校</h4>'+A.map(row).join(''):'')+(B.length?'<h4 class="n">あと少しの学校</h4>'+B.map(row).join(''):'')+(C.length?'<h4 class="f">まだ遠い学校</h4>'+C.map(row).join(''):'');}
 window.schoolPanel=function(){return '<div class="skx">'+h+'</div>'+amaPanel();};
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2 if nm == '' else 2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')")
            pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);if(!G.ama)amaInit();const ks=Object.keys(G.rel);if(ks.length>2){G.rel[ks[2]]=14;}if(ks.length>3)G.rel[ks[3]]=17;applySkin('urushik');}")
            pg.add_style_tag(content=CSS)
            pg.evaluate(JS, v)
            pg.evaluate("()=>{UI.view='scout';render();}")
            pg.wait_for_timeout(400)
            el = pg.query_selector('.skx')
            pg.evaluate("()=>{const e=document.querySelector('.skx');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-110);}")
            pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(out, 'sk%d%s.png' % (v, nm)))
            print('sk%d%s' % (v, nm), pg.evaluate("[document.documentElement.scrollWidth,innerWidth]"))
    b.close()
