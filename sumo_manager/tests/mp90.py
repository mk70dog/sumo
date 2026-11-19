# 二人相撲 第 2 段階の通しテスト(2 ページ、#mpmock で Gist の代わりに localStorage)
# 子が一人用と同じ画面で 稽古・施設・外部契約・勧誘・作戦 を決め、親の iPad で進めたあと、親の世界に子の決めたことが入っているか。
# usage: python3 mp90.py 本体.html [幅x高さ] [写真の前置き]
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1];W,H=(int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '1180x820').split('x'));pre=sys.argv[3] if len(sys.argv)>3 else '/tmp/mp90_'
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':W,'height':H});errs=[]
  host=ctx.new_page();host.on('pageerror',lambda e:errs.append('H:'+str(e)))
  host.goto('file://'+f+'#mpmock');host.evaluate("localStorage.clear()");host.reload();host.wait_for_timeout(400)
  host.click('.st-two');host.click('.st-go2 .st-real >> nth=0');host.click('.hcard >> nth=0');host.wait_for_timeout(350);host.click('#hsheet .btn.main')
  host.wait_for_function("()=>G&&G.mp&&G.mp.id");code=host.evaluate("G.mp.id")
  guest=ctx.new_page();guest.on('pageerror',lambda e:errs.append('G:'+str(e)))
  guest.goto('file://'+f+'#mpmock');guest.wait_for_timeout(400);guest.click('.st-two');guest.click('.st-go2 .st-dok');guest.fill('#mp_code',code);guest.click('.mpkey .btn.main')
  guest.wait_for_selector('.mpsel .btn');gname=guest.evaluate("document.querySelector('.mpsel .btn').textContent");guest.click('.mpsel .btn >> nth=0')
  host.wait_for_function("()=>G.mp.gh>0&&G.P&&G.P.length===2",timeout=15000);gh=host.evaluate("G.mp.gh")
  guest.wait_for_function("()=>mpIsP()",timeout=20000);guest.wait_for_timeout(300)
  title=guest.evaluate("document.querySelector('#hdr .title').textContent")
  guest.screenshot(path=pre+'guest_home.png')
  # 子が決める:稽古・施設・外部契約・勧誘
  rid=guest.evaluate("own().sort((a,b)=>a.pos-b.pos)[0].id")
  guest.evaluate("setR(%d,'menu','筋');setR(%d,'it',2)"%(rid,rid))
  m0=guest.evaluate("G.money");guest.evaluate("setCon('gym');upFac('iryo')")
  off=guest.evaluate("(()=>{const p=G.pros[0];if(!p)return null;const m=offerPros(p.cid,1);return [p.cid,String(m).slice(0,40),G.pend.length];})()")
  gstate=guest.evaluate("[G.money,G.con.gym,G.fac.iryo,G.pend.length,G.R[%d].menu]"%rid)
  guest.evaluate("go('keiko')");guest.wait_for_timeout(200);guest.screenshot(path=pre+'guest_keiko.png')
  guest.evaluate("doWeekUI()");guest.wait_for_timeout(300);rd=guest.evaluate("[MPG.ready,MPG.act]")
  guest.evaluate("go('keiko')");guest.wait_for_timeout(200);guest.screenshot(path=pre+'guest_keiko_ready.png')
  guest.evaluate("go('home')");guest.wait_for_timeout(200);guest.screenshot(path=pre+'guest_ready.png')
  host.evaluate("go('home')");host.wait_for_timeout(200);host.screenshot(path=pre+'host_home.png')
  host.evaluate("doWeekUI()");host.wait_for_timeout(200);host.screenshot(path=pre+'host_ready.png')
  host.wait_for_function("()=>G.mp.n===2",timeout=20000)
  hv=host.evaluate("(()=>{const i=pI(G.mp.gh);const P=G.P[i];return [G.wk,P.con.gym,P.fac.iryo,P.pend.length,G.R[%d].menu,G.R[%d].lw,Math.round(P.money),Math.round(G.money)];})()"%(rid,rid))
  guest.wait_for_function("()=>MPG.n===2&&mpIsP()",timeout=20000);gw=guest.evaluate("[G.wk,MPG.ready,G.con.gym,G.fac.iryo,G.pend.length,Math.round(G.money)]")
  # 初日まで → 子が作戦 → 1 日目
  guest.evaluate("doToBasho()");host.evaluate("doToBasho()");host.wait_for_function("()=>G.mp.n===3&&G.phase==='basho'",timeout=20000)
  guest.wait_for_function("()=>MPG.n===3",timeout=20000);guest.evaluate("go('basho')");guest.wait_for_timeout(300);guest.screenshot(path=pre+'guest_basho.png')
  guest.evaluate("const r=G.R[%d];if(!r.tac)r.tac={ta:'任',kumi:'任'};setTac(%d,'ta','張')"%(rid,rid))
  guest.evaluate("stepDay()");host.evaluate("stepDay()");host.wait_for_function("()=>G.mp.n===4&&G.B.day===1",timeout=20000)
  tac=host.evaluate("G.R[%d].tac"%rid)
  # 千秋楽まで → 場所後の出来事に答える → 次の場所
  guest.wait_for_function("()=>MPG.n===4",timeout=20000);guest.evaluate("stepAll()");host.evaluate("stepAll()");host.wait_for_function("()=>G.mp.n===5&&G.phase==='post'",timeout=20000)
  guest.wait_for_function("()=>MPG.n===5",timeout=20000);gev=guest.evaluate("G.ev.length")
  guest.evaluate("closeM&&closeM();while(G.ev.length)resolveEv(G.ev[0].id,0);render()");guest.evaluate("doNext()")
  host.evaluate("closeM&&closeM();while(G.ev.length)resolveEv(G.ev[0].id,0);render()");host.evaluate("doNext()")
  host.wait_for_function("()=>G.mp.n===6&&G.phase==='train'",timeout=20000);bn=host.evaluate("[G.bnum,G.phase,G.P.map((p,i)=>i===G.PA?G.ev.length:p.ev.length)]")
  guest.wait_for_function("()=>MPG.n===6",timeout=20000);guest.wait_for_timeout(300)
  # 子:終了して続きから
  guest.evaluate("quitTop()");guest.click('.st-two');guest.click("text=続きから(子)");guest.wait_for_function("()=>MPG.n===6&&mpIsP()",timeout=20000)
  sw=[pg.evaluate("[document.documentElement.scrollWidth,innerWidth]") for pg in (host,guest)]
  print(json.dumps(dict(code=code,gname=gname,gh=gh,title=title,offer=off,guestLocal=gstate,ready=rd,hostAfter=hv,guestAfter=gw,tac=tac,guestEv=gev,next=bn,scroll=sw,errs=errs[:6]),ensure_ascii=False))
  b.close()
