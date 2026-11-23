# ホーム画面の会話ポップアップの見本 cv1〜cv3(ダルマさん「ホームの画面に親方をはじめ色々な方面から会話形式のコメントをポップアップで表示。独立モード時のはじめのやり取りのような会話形式」)
# 本体を開いて伊勢ヶ濱部屋で始め、部屋の画面に見本の会話を重ねて写真を撮る。会話の中身は見本用(実装では「部屋の声」koePeople の数値から作る)。
# usage: python3 tools/mkconvsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.cvov{position:fixed;inset:0;background:rgba(10,8,6,.55);z-index:900;display:flex;align-items:center;justify-content:center;padding:14px}
.cvbox{background:#fbf6ea;color:#1d1a16;border:3px double #8e7347;border-radius:10px;max-width:720px;width:100%;max-height:88vh;overflow:auto;padding:14px 16px;box-shadow:0 10px 40px rgba(0,0,0,.5)}
.cvbox h2{margin:0 0 4px;font:800 20px var(--kaku,serif);display:flex;justify-content:space-between;align-items:baseline}
.cvbox h2 small{font-size:13px;color:#7d7365;font-weight:400}
.cvbox .dpsay .bb{background:#fff;border:1px solid #d8c9a8;border-radius:10px;padding:8px 10px;font-size:15px;line-height:1.6}
.cvbox .dpsay.r{flex-direction:row-reverse}.cvbox .dpsay.r .bb{background:#f1e6cc}
.cvbox .dpsay img{width:64px;height:84px;object-fit:cover;border-radius:4px;border:1px solid #8e7347;flex:none}
.cvbox .who{display:block;font-size:12px;color:#7d7365}
.cvbtn{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
.cvbtn button{font:700 15px var(--kaku,serif);padding:8px 16px;border-radius:6px;border:1px solid #8e7347;background:#fff}
.cvbtn button.ai{background:#1d1a16;color:#e9d39a;border-color:#c9a24a}
.cvdots{display:flex;gap:4px;margin:2px 0 8px}.cvdots i{width:18px;height:4px;background:#d8c9a8;border-radius:2px}.cvdots i.on{background:#b5361f}
.cvsheet{position:fixed;left:0;right:0;bottom:0;z-index:900;background:#fbf6ea;color:#1d1a16;border-top:3px double #8e7347;box-shadow:0 -8px 30px rgba(0,0,0,.45);padding:12px 16px 16px;border-radius:14px 14px 0 0}
.cvsheet .row{display:flex;gap:14px;align-items:flex-start;max-width:900px;margin:0 auto}
.cvsheet img{width:84px;height:110px;object-fit:cover;border-radius:5px;border:1px solid #8e7347;flex:none}
.cvsheet .dpff{min-height:110px}
.cvsheet .nm{font:800 17px var(--kaku,serif)}.cvsheet .nm small{font-weight:400;color:#7d7365;font-size:12px;margin-left:6px}
.cvsheet .tx{font-size:17px;line-height:1.7;margin-top:4px}
.cvsheet .ft{display:flex;justify-content:space-between;align-items:center;max-width:900px;margin:10px auto 0;font-size:13px;color:#7d7365}
.cvsheet .ft button{font:700 15px var(--kaku,serif);padding:8px 18px;border-radius:6px;border:1px solid #c9a24a;background:#1d1a16;color:#e9d39a}
.cvfl{position:absolute;z-index:50;display:flex;gap:8px;align-items:flex-start;max-width:46%}
.cvfl img{width:54px;height:70px;object-fit:cover;border-radius:4px;border:2px solid #e9d39a;flex:none;box-shadow:0 2px 8px rgba(0,0,0,.4)}
.cvfl .dpff{min-height:70px;width:30px;font-size:13px}
.cvfl .bb{background:rgba(251,246,234,.96);color:#1d1a16;border:1px solid #8e7347;border-radius:12px;padding:7px 10px;font-size:14px;line-height:1.55;box-shadow:0 3px 10px rgba(0,0,0,.35)}
.cvfl .bb b{display:block;font-size:11px;color:#7d7365}
.cvfl.dim{opacity:.55}
.cvfl.now .bb{border:2px solid #b5361f}
.cvctl{position:absolute;right:12px;bottom:12px;z-index:60;display:flex;gap:6px}
.cvctl button{font:700 14px var(--kaku,serif);padding:6px 14px;border-radius:6px;border:1px solid #c9a24a;background:#1d1a16;color:#e9d39a}
"""
JS = r"""(v)=>{
 const me0=me();const top=heyaTop();const o=own();const inj=o.filter(r=>r.inj&&r.inj.s>=2);const ij=inj[0]||o[o.length-1];
 const okn=G.okami?G.okami.n:'おかみさん';const oy=me0.o2;const oyN=me0.n+'親方';
 const L=[
  {k:[oy],lb:oyN,who:oyN+'(師匠)',t:'けが人が '+inj.length+' 人か。今週は無理はさせられんな。'},
  {k:[],lb:okn,who:okn+'(おかみさん)',t:ij.n+'は'+(ij.inj?ij.inj.p:'体')+'を痛めてから元気がありません。ちゃんこは食べやすいものにしておきますね。',r:1},
  {k:[ij.n],lb:ij.n,who:ij.n+'('+ij.rkS+')',t:'早く土俵に戻りたいです。治療院には毎日通っています。'},
  {k:[oy],lb:oyN,who:oyN,t:'焦るな。治してからが勝負だ。'},
  {k:[top.n],lb:top.n,who:top.n+'('+top.rkS+'・部屋頭)',t:'親方、今週は出稽古に行かせてください。上を目指したいんです。',r:1}];
 const say=(x,i,cls)=>dpSay(x.k,x.lb,x.who,x.t,x.r);
 const app=document.body;let h='';
 if(v===1){h='<div class="cvov"><div class="cvbox"><h2>朝の稽古場<small>稽古 第1週 ・ 部屋の会話 3/5</small></h2><div class="cvdots">'+L.map((x,i)=>'<i class="'+(i<3?'on':'')+'"></i>').join('')+'</div>'+L.slice(0,3).map(say).join('')+'<div class="cvbtn"><button>あとで読む</button><button class="ai">次へ</button></div></div></div>';}
 if(v===2){const x=L[2];h='<div class="cvsheet"><div class="row">'+dpFace(x.k,x.lb)+'<div style="flex:1;min-width:0"><div class="nm">'+esc(x.who)+'<small>朝の稽古場 ・ 稽古 第1週</small></div><div class="tx">'+esc(x.t)+'</div></div></div><div class="ft"><span>会話 3/5 ・ 押すと次へ</span><span><button style="background:#fff;color:#1d1a16;border-color:#8e7347;margin-right:6px">閉じる</button><button>次へ ▶</button></span></div></div>';}
 if(v===3){const pic=document.querySelector('.hpic, .hmimg, #home .pic')||[...document.querySelectorAll('#app div')].find(e=>{const b=e.getBoundingClientRect();return b.width>innerWidth*.7&&b.height>innerHeight*.45&&getComputedStyle(e).backgroundImage!=='none';})||document.querySelector('#app');
  pic.style.position='relative';const pos=[[16,4],[50,14],[24,40],[8,58],[52,64]];
  pic.insertAdjacentHTML('beforeend',L.map((x,i)=>'<div class="cvfl'+(i<4?'':' now')+(i<3?' dim':'')+'" style="left:'+pos[i][1]+'%;top:'+pos[i][0]+'%">'+dpFace(x.k,x.lb)+'<div class="bb"><b>'+esc(x.who)+'</b>'+esc(x.t)+'</div></div>').join('')+'<div class="cvctl"><button>▶ 次へ</button><button>閉じる</button></div>');return;}
 app.insertAdjacentHTML('beforeend',h);}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
        for v in (1, 2, 3):
            pg = b.new_page(viewport={'width': W, 'height': H})
            pg.goto('file://' + f); pg.evaluate("localStorage.clear()")
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;UI.view='home';render();}")
            pg.add_style_tag(content=CSS); pg.wait_for_timeout(300)
            pg.evaluate(JS, v); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, 'cv%d%s.png' % (v, nm)))
            pg.close()
    b.close()
print('ok')
