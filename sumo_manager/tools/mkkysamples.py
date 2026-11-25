# 協会の役員(理事長・理事)の見本 ky1〜ky2(ダルマさん「実施」:理事長の交代・部屋の閉鎖と新設)
# usage: python3 tools/mkkysamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """.kyc{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:4px 0 8px}.kyc b{font-size:18px;color:var(--sumi)}
.kyr{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.kyr span{border:1px solid var(--line);border-radius:12px;padding:2px 9px;font-size:13px}.kyr span.me{border-color:#a8823c;color:#a8823c;font-weight:bold}
.kyt{width:100%;border-collapse:collapse;font-size:13px}.kyt td{padding:4px 6px;border-bottom:1px solid var(--line)}"""
R = ['八角', '浅香山', '藤島', '尾上', '片男波', '追手風', '出羽海', '高田川', '佐渡ヶ嶽', '伊勢ノ海']
H = [('2015〜2034', '八角(元・北勝海)', '八角部屋'), ('2034〜2040', '藤島(元・武双山)', '藤島部屋'), ('2040〜', '佐渡ヶ嶽(元・琴櫻)', '佐渡ヶ嶽部屋')]
JS = r"""([v,R,H])=>{const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const pn=[...document.querySelectorAll('.pn')][0];
 const chips='<div class="kyr">'+R.map((n,i)=>'<span'+(i===7?' class="me"':'')+'>'+n+'</span>').join('')+'</div>';
 const hist='<table class="kyt">'+H.map(x=>'<tr><td>'+x[0]+'</td><td>'+x[1]+'</td><td class="mute">'+x[2]+'</td></tr>').join('')+'</table>';
 let h='';
 if(v===1){h='<details class="kacc" open><summary><b>協会の役員</b><small>理事長 八角(元・北勝海)・2015 年〜</small></summary><div class="pn"><div class="mute" style="font-size:13px">理事 10 人(2026 年の選挙・任期 2 年。次は 2028 年 初場所のあと)</div>'+chips+'<h3 style="font-size:14px;margin:10px 0 4px">歴代の理事長(このゲームで)</h3>'+hist+'</div></details>';}
 else {h='<div class="pn"><h2>協会の役員<span class="sub">次の選挙 2028 年</span></h2><div class="kyc"><span class="mute">理事長</span><b>八角(元・北勝海)</b><span class="mute">八角部屋・2015 年〜</span></div>'+chips+'<details style="margin-top:6px"><summary class="mute" style="font-size:13px">歴代の理事長を見る(3 人)</summary>'+hist+'</details></div>';}
 pn.insertAdjacentHTML('beforebegin',h);return pn.previousElementSibling.getBoundingClientRect().top+scrollY;}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (1, 2):
        for nm, (W, Hh) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': Hh}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear()"); pg.reload()
            pg.evaluate("()=>{newGameReal('高田川');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();UI.view='kiroku';applySkin('urushik');render();}")
            pg.wait_for_timeout(400); pg.add_style_tag(content=CSS)
            y = pg.evaluate(JS, [v, R, H]); pg.evaluate("y=>scrollTo(0,y-(innerWidth<760?370:150))", y); pg.wait_for_timeout(150)
            name = 'ky%d%s' % (v, nm); pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
