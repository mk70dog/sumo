# 部屋の建物・夏合宿の見本 bd1〜bd3(ダルマさん「実施」:お金持ちの部屋のお金の使いみち)
# usage: python3 tools/mkbdsamples.py 本体.html 出力フォルダ
from playwright.sync_api import sync_playwright
import sys, os
f = os.path.abspath(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else 'samples'
os.makedirs(out, exist_ok=True)
CSS = """
.bdt{width:100%;border-collapse:collapse;font-size:14px}.bdt td,.bdt th{padding:6px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}
.bdt th{font-size:12px;color:var(--mute);font-weight:normal}.bdt .nm{font-weight:bold;color:var(--sumi)}.bdt .ef{font-size:12px;color:var(--mute)}
.bdg{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px;margin:8px 0}
.bdc{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--paper)}
.bdc h4{margin:0 0 4px;font-size:15px;color:var(--sumi)}.bdc .pr{font-size:18px;font-weight:bold;color:#a8823c}.bdc ul{margin:6px 0;padding-left:18px;font-size:13px}.bdc .ng{opacity:.55}
.bdnow{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;font-size:14px;margin:4px 0 8px}.bdnow b{font-size:16px}
.bdbar{height:12px;border-radius:6px;background:rgba(128,128,128,.25);overflow:hidden;margin:6px 0}.bdbar>i{display:block;height:100%;background:#a8823c}
.bdrow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:6px 0;font-size:14px}.bdrow select{font-size:14px;padding:4px 6px}
.bdcmp{font-size:13px;margin:6px 0;padding:8px 10px;border-left:3px solid #a8823c;background:rgba(168,130,60,.08)}
"""
OPT = [('古い部屋を買って改築', '4 億円', '半年', '家賃がなくなる(修繕・税金だけ)・広さは今と同じ', 40000),
       ('新築・都外', '5 億円', '2 年', '弟子 +6 人・稽古場 +1・家賃なし', 50000),
       ('新築・都内', '10 億円', '2 年', '弟子 +9 人・稽古場 +1・評判 +5・後援会 +', 100000),
       ('新築・両国の近く', '20 億円', '2 年', '弟子 +12 人・稽古場 +2・評判 +10・後援会 ++・勧誘しやすい', 200000)]
CAMP = [('静岡県', '後援会あり・つながり 42', 420), ('青森県', '出身の弟子 3 人', 380), ('千葉県', '近い・安い', 300)]
JS = r"""([v,OPT,CAMP])=>{
 const cb=document.getElementById('cvbub');if(cb)cb.remove();
 const fac=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith('部屋の施設')).parentElement;
 const anchor=fac.closest('.kacc')||fac;
 const money=Math.round(G.money);const man=x=>x>=10000?(x/10000).toFixed(x%10000?1:0)+' 億円':x.toLocaleString()+' 万円';
 const now='<div class="bdnow"><b>今:賃貸</b><span>家賃 155 万円/場所</span><span class="mute">資金 '+man(money)+'</span></div>';
 let h='';
 if(v===1){
  h+='<div class="pn"><h2>部屋の建物</h2>'+now+'<table class="bdt"><tr><th>えらぶ</th><th>費用</th><th>期間</th><th></th></tr>'+OPT.map(o=>'<tr><td><div class="nm">'+o[0]+'</div><div class="ef">'+o[3]+'</div></td><td>'+o[1]+'</td><td>'+o[2]+'</td><td><button class="btn sm"'+(money<o[4]/2?' disabled':'')+'>'+(money<o[4]/2?'資金不足':'これにする')+'</button></td></tr>').join('')+'</table><p class="kaku mute" style="font-size:13px">新築は着工で半分、完成で半分を払います。自前の建物は年がたつと修繕費が増え、40 年ほどで建て替えか大きな修繕が要ります。</p></div>';
  h+='<div class="pn"><h2>夏合宿<span class="sub">名古屋場所のあと・年 1 回</span></h2><table class="bdt">'+CAMP.map(c=>'<tr><td><div class="nm">'+c[0]+'</div><div class="ef">'+c[1]+'</div></td><td>'+c[2]+' 万円</td><td><button class="btn sm">ここで開く</button></td></tr>').join('')+'<tr><td><div class="nm">今年は開かない</div><div class="ef">お金を残す</div></td><td>0</td><td><button class="btn sm">開かない</button></td></tr></table><p class="kaku mute" style="font-size:13px">合宿で次の場所までの稽古の伸びが少し上がり、その土地とのつながりと後援会が増えます。</p></div>';
 } else if(v===2){
  h+='<details class="kacc" open><summary><b>部屋の建物</b><small>賃貸・家賃 155 万円/場所</small></summary><div class="pn">'+now+'<div class="bdg">'+OPT.map(o=>{const ng=money<o[4]/2;return '<div class="bdc'+(ng?' ng':'')+'"><h4>'+o[0]+'</h4><div class="pr">'+o[1]+'</div><div class="mute" style="font-size:12px">できるまで '+o[2]+'</div><ul>'+o[3].split('・').map(x=>'<li>'+x+'</li>').join('')+'</ul><button class="btn sm"'+(ng?' disabled':'')+'>'+(ng?'資金不足':'これにする')+'</button></div>';}).join('')+'</div><p class="kaku mute" style="font-size:13px">新築は着工で半分、完成で半分。自前の建物は古くなると修繕費が増えます。</p></div></details>';
  h+='<details class="kacc"><summary><b>夏合宿</b><small>今年:未定・名古屋場所のあと</small></summary><div class="pn"><div class="bdg">'+CAMP.map(c=>'<div class="bdc"><h4>'+c[0]+'</h4><div class="pr">'+c[2]+' 万円</div><div class="mute" style="font-size:12px">'+c[1]+'</div><button class="btn sm">ここで開く</button></div>').join('')+'</div></div></details>';
 } else {
  h+='<div class="pn"><h2>部屋の建物</h2><div class="bdnow"><b>工事中:新築・両国の近く</b><span>完成まで あと 7 場所</span></div><div class="bdbar"><i style="width:42%"></i></div><div class="mute" style="font-size:13px">残りの支払い 10 億円(完成のとき)・それまでは今の部屋の家賃</div>'
   +'<div class="bdrow" style="margin-top:10px"><span>ほかの案:</span><select>'+OPT.map(o=>'<option>'+o[0]+'('+o[1]+')</option>').join('')+'</select><button class="btn sm">くらべる</button></div>'
   +'<div class="bdcmp">新築・都内(10 億円・2 年):弟子 +9 人・稽古場 +1・評判 +5・後援会 +</div></div>';
  h+='<div class="pn"><h2>夏合宿<span class="sub">名古屋場所のあと</span></h2><div class="bdrow"><select>'+CAMP.map(c=>'<option>'+c[0]+' '+c[2]+' 万円('+c[1]+')</option>').join('')+'<option>今年は開かない</option></select><button class="btn sm">決める</button></div><div class="mute" style="font-size:13px">去年:静岡県で開いた(つながり +8・後援会 +24 人)</div></div>';
 }
 anchor.insertAdjacentHTML('afterend',h);
 return anchor.getBoundingClientRect().bottom+scrollY;
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for v in (1, 2, 3):
        for nm, (W, H) in {'': (1180, 820), '_phone': (390, 844)}.items():
            pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
            pg.goto('file://' + f); pg.evaluate("localStorage.clear();localStorage.setItem('sumoSkin','urushik')"); pg.reload()
            pg.evaluate("()=>{newGameReal('伊勢ヶ濱');UI.title=false;UI.start=null;while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();while(G.ev.length)resolveEv(G.ev[0].id,0);const c=cvScene();if(c)G.cvS=c.key;G.cvW=cvKey();G.money=120000;UI.view='keiei';applySkin('urushik');render();}")
            pg.wait_for_timeout(400)
            pg.add_style_tag(content=CSS); y = pg.evaluate(JS, [v, OPT, CAMP])
            pg.evaluate("y=>scrollTo(0,y-20)", y); pg.wait_for_timeout(150)
            name = 'bd%d%s' % (v, nm)
            pg.screenshot(path=os.path.join(out, name + '.png'))
            print(name, '横あふれ', pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
    b.close()
