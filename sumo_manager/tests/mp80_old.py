# 二人相撲の通しテスト(2 ページ、#mpmock で Gist の代わりに localStorage)
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1];W,H=(int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '1180x820').split('x'))
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':W,'height':H});errs=[]
  host=ctx.new_page();host.on('pageerror',lambda e:errs.append('H:'+str(e)))
  host.goto('file://'+f+'#mpmock');host.evaluate("localStorage.clear()");host.reload();host.wait_for_timeout(400)
  host.click('.st-two');host.click('.st-go2 .st-real');host.click('.hcard >> nth=0');host.wait_for_timeout(350);host.click('#hsheet .btn.main')
  host.wait_for_function("()=>G&&G.mp&&G.mp.id");code=host.evaluate("G.mp.id");host.screenshot(path='/tmp/mp_host_wait.png')
  guest=ctx.new_page();guest.on('pageerror',lambda e:errs.append('G:'+str(e)))
  guest.goto('file://'+f+'#mpmock');guest.wait_for_timeout(400);guest.click('.st-two');guest.click('.st-go2 .st-dok');guest.fill('#mp_code',code);guest.click('.mpkey .btn.main')
  guest.wait_for_selector('.mpsel .btn');gname=guest.evaluate("document.querySelector('.mpsel .btn').textContent");guest.click('.mpsel .btn >> nth=0')
  host.wait_for_function("()=>G.mp.gh>0",timeout=15000);gh=host.evaluate("G.mp.gh")
  # 子が稽古を決める(最初の力士を 筋・強め)、候補を 1 人勧誘
  guest.wait_for_selector('table.tb select');rid=guest.evaluate("G.order.map(id=>G.R[id]).filter(r=>r.h===MPG.gh&&!r.ret).sort((a,b)=>a.pos-b.pos)[0].id")
  guest.select_option('table.tb tr:nth-child(2) td:nth-child(4) select','筋');guest.select_option('table.tb tr:nth-child(2) td:nth-child(5) select','2')
  off=guest.evaluate("(G.pros||[]).length");
  if off: guest.check('.mpo2 input >> nth=0')
  guest.click('.mpready .btn.main');guest.screenshot(path='/tmp/mp_guest_ready.png')
  # 親が進める → ふたりとも準備で 1 週進む
  host.evaluate("go('home')");host.screenshot(path='/tmp/mp_host_home.png');host.evaluate("doWeekUI()")
  host.wait_for_function("()=>G.mp.n===1",timeout=20000);wk=host.evaluate("[G.wk,G.R[%d].gm,G.R[%d].gi,G.R[%d].lw]"%(rid,rid,rid))
  guest.wait_for_function("()=>MPG.n===1",timeout=20000);gw=guest.evaluate("[G.wk,MPG.ready]")
  news=host.evaluate("G.news.filter(x=>/二人相撲/.test(x)).slice(0,3)")
  # 初日まで:子がもう一度準備
  guest.click('.mpready .btn.main');host.evaluate("doToBasho()");host.wait_for_function("()=>G.mp.n===2&&G.phase==='basho'",timeout=20000)
  guest.wait_for_function("()=>MPG.n===2",timeout=20000);guest.wait_for_timeout(300);guest.screenshot(path='/tmp/mp_guest_basho.png')
  ta=guest.evaluate("!!document.querySelector('table.tb td:nth-child(5) select')")
  if ta: guest.select_option('table.tb tr:nth-child(2) td:nth-child(5) select >> nth=0','張')
  guest.click('.mpready .btn.main');host.evaluate("stepDay()");host.wait_for_function("()=>G.mp.n===3&&G.B.day===1",timeout=20000)
  tac=host.evaluate("G.R[%d].tac"%rid)
  # 子:終了してもう一度続きから
  guest.wait_for_function("()=>MPG.n===3",timeout=20000);guest.evaluate("quitTop()");guest.click('.st-two');guest.click("text=続きから(子)");guest.wait_for_function("()=>MPG.n===3&&UI.mpGuest",timeout=20000)
  # 親:一人相撲の記録とは別
  one=host.evaluate("[!!localStorage.getItem('gsmMP'),!!localStorage.getItem(SAVE)]")
  sw=[pg.evaluate("[document.documentElement.scrollWidth,innerWidth]") for pg in (host,guest)]
  print(json.dumps(dict(code=code,gname=gname,gh=gh,afterWeek=wk,guestWeek=gw,news=news,tacOK=ta,tac=tac,saves=one,scroll=sw,errs=errs[:4]),ensure_ascii=False))
  b.close()
