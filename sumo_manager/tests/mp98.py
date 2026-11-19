# 二人相撲:子が「部屋付き親方として独立」して参加する(#mpmock)。親は実在の部屋で始める。
# usage: python3 mp98.py 本体.html [幅x高さ] [写真の前置き]
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1];W,H=(int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '1180x820').split('x'));pre=sys.argv[3] if len(sys.argv)>3 else '/tmp/mp98_'
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':W,'height':H});errs=[]
  host=ctx.new_page();host.on('pageerror',lambda e:errs.append('H:'+str(e)))
  host.goto('file://'+f+'#mpmock');host.evaluate("localStorage.clear()");host.reload();host.wait_for_timeout(400)
  host.click('.st-two');host.click('.st-go2 .st-real >> nth=0');host.click('.hcard >> nth=0');host.wait_for_timeout(350);host.click('#hsheet .btn.main')
  host.wait_for_function("()=>G&&G.mp&&G.mp.id");code=host.evaluate("G.mp.id");hn=host.evaluate("G.heya[0].n")
  guest=ctx.new_page();guest.on('pageerror',lambda e:errs.append('G:'+str(e)))
  guest.goto('file://'+f+'#mpmock');guest.wait_for_timeout(400);guest.click('.st-two');guest.click('.st-go2 .st-dok');guest.fill('#mp_code',code);guest.click('.mpkey .btn.main')
  guest.wait_for_selector('.mpsel .btn');guest.screenshot(path=pre+'g_select.png')
  guest.click('text=独立して新しい部屋を興す');guest.wait_for_selector('.hcard');guest.wait_for_timeout(300)
  cards=guest.evaluate("document.querySelectorAll('.hcard').length");par=guest.evaluate("dokList().map(x=>x.par)")
  guest.screenshot(path=pre+'g_dok.png')
  n=guest.evaluate("dokOK()[0].n");guest.evaluate("n=>dokSheet(n)",n);guest.wait_for_timeout(300)
  guest.check('.dkw input >> nth=0');guest.wait_for_timeout(200);guest.screenshot(path=pre+'g_sheet.png');guest.click('#dkgo')
  guest.wait_for_timeout(300);waiting=guest.evaluate("document.querySelector('#app').textContent.includes('独立の申し込み中')")
  host.wait_for_function("()=>G.mp.gh>0&&G.P&&G.P.length===2",timeout=20000)
  hv=host.evaluate("(()=>{const k=G.mp.gh;const h=G.heya[k];return [h.n,h.hist,G.order.filter(i=>G.R[i].h===k&&!G.R[i].ret).length,G.toshi.find(t=>t.n===h.n).heya,G.toshi.find(t=>t.n===h.n).shi,Math.round(G.P[pI(k)].money)];})()")
  guest.wait_for_function("()=>mpIsP()",timeout=20000);guest.wait_for_timeout(300)
  gv=guest.evaluate("[MPG.gh,MPG.dk,document.querySelector('#hdr .title').textContent,own().length,G.money,G.fac.shuku,G.bld.k]")
  guest.screenshot(path=pre+'g_home.png')
  # 1 週進める
  guest.evaluate("doWeekUI()");host.evaluate("doWeekUI()");host.wait_for_function("()=>G.mp.n===2",timeout=20000);guest.wait_for_function("()=>MPG.n===2&&mpIsP()",timeout=20000)
  # 子:終了して続きから
  guest.evaluate("quitTop()");guest.click('.st-two');guest.click("text=続きから(子)");guest.wait_for_function("()=>MPG.n===2&&mpIsP()",timeout=20000)
  sw=[pg.evaluate("[document.documentElement.scrollWidth,innerWidth]") for pg in (host,guest)]
  print(json.dumps(dict(host=hn,cards=cards,parents=sorted(set(par)),hostInDok=hn in par,dok=n,waiting=waiting,hostAfter=hv,guestAfter=gv,scroll=sw,errs=errs[:6]),ensure_ascii=False))
  b.close()
