# 二人相撲 第 3 段階(v122):通信が切れたときの扱い(#mpmock)。
# 切れる → 帯の札と間隔ののび → 戻る/鍵の誤り/親の待つ時間と待たずに進める/子が切れている間に変えた稽古をもう一度当てる/相手の iPad が開いていない
# usage: python3 cn122.py 本体.html [幅x高さ] [写真の前置き]
from playwright.sync_api import sync_playwright
import sys,json
f=sys.argv[1];W,H=(int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '1180x820').split('x'));pre=sys.argv[3] if len(sys.argv)>3 else '/tmp/cn122_'
R={}
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':W,'height':H});errs=[]
  host=ctx.new_page();host.on('pageerror',lambda e:errs.append('H:'+str(e)))
  host.goto('file://'+f+'#mpmock');host.evaluate("localStorage.clear()");host.reload();host.wait_for_timeout(400)
  host.click('.st-two');host.click('.st-go2 .st-real >> nth=0');host.click('.hcard >> nth=0');host.wait_for_timeout(350);host.click('#hsheet .btn.main')
  host.wait_for_function("()=>G&&G.mp&&G.mp.id");code=host.evaluate("G.mp.id")
  guest=ctx.new_page();guest.on('pageerror',lambda e:errs.append('G:'+str(e)))
  guest.goto('file://'+f+'#mpmock');guest.wait_for_timeout(400);guest.click('.st-two');guest.click('.st-go2 .st-dok');guest.fill('#mp_code',code);guest.click("button[onclick='mpJoin()']")
  guest.wait_for_selector('.mpsel .btn');guest.click('.mpsel .btn >> nth=0')
  host.wait_for_function("()=>G.mp.gh>0&&G.P&&G.P.length===2",timeout=20000);guest.wait_for_function("()=>mpIsP()",timeout=20000);guest.wait_for_timeout(1500)
  band=lambda pg:pg.evaluate("((document.querySelector('.cnst')||{}).textContent||'')+' | '+((document.querySelector('.cnx')||{}).textContent||'')")
  R['ok']=[band(host),band(guest)]
  # 子が切れる
  guest.evaluate("window.__r=MPT.read;MPT.read=async()=>{throw new TypeError('Failed to fetch')};MPT.__w=MPT.write;MPT.write=async()=>{throw new TypeError('Failed to fetch')};0")
  guest.wait_for_function("()=>MP.fail>=3",timeout=30000);guest.evaluate("render()")
  R['off']=[band(guest),guest.evaluate("[MP.fail,mpIvNow()]")];guest.screenshot(path=pre+'off.png')
  # 切れている間に子が稽古を変える(+お金を使う変更として設備の契約もさわる)
  rid=guest.evaluate("(()=>{const r=own().find(x=>!x.inj&&x.menu!=='三');setR(r.id,'menu','三');setR(r.id,'it',3);G.money-=50;return r.id})()")
  # 親は準備して待たずに進める
  host.evaluate("mpSetWait(5)");host.evaluate("doWeekUI()");host.wait_for_timeout(300)
  R['hostCard']=host.evaluate("(document.querySelector('.cnrow')||{}).textContent||''");host.screenshot(path=pre+'host_wait.png')
  n0=host.evaluate("G.mp.n");host.evaluate("mpGoNow()");host.wait_for_function("n=>G.mp.n>n&&!G.mp.hReady",arg=n0,timeout=20000);n1=host.evaluate("G.mp.n")
  R['hostNews']=host.evaluate("(G.log||G.news||[]).slice(0,40).map(x=>typeof x==='string'?x:(x.t||'')).filter(x=>/待たずに/.test(x)).slice(0,1)")
  hostMenu=host.evaluate("id=>[G.R[id].menu,G.R[id].it]",rid)
  # 子が戻る
  guest.evaluate("MPT.read=window.__r;MPT.write=MPT.__w;window.dispatchEvent(new Event('online'));0")
  guest.wait_for_function("n=>MPG.n>=n&&MP.fail===0",arg=n1,timeout=20000);guest.wait_for_timeout(800)
  R['back']=band(guest);R['lost']=guest.evaluate("MPX.lost");R['alert']=guest.evaluate("(document.querySelector('#mdl')||{}).textContent||''")[:160]
  R['guestMenuAfter']=guest.evaluate("id=>[G.R[id].menu,G.R[id].it]",rid);R['hostMenuAtAdvance']=hostMenu
  guest.screenshot(path=pre+'back.png')
  # 子から送り直された差分に稽古が入っているか
  guest.evaluate("closeM&&closeM()");guest.wait_for_timeout(1500)
  R['resent']=host.evaluate("(async()=>{const f=await MPT.read(G.mp.id);const g=mpJ(f['guest.json']);if(!g.d)return 'なし';const o=mpJ(await mpDec(g.d));return JSON.stringify(o.o).includes('\"menu\"')})()")
  # 鍵の誤り
  guest.evaluate("MPT.read=async()=>{throw new Error('読めませんでした(401)')};0");guest.wait_for_function("()=>MP.fail>=1&&MP.ek==='key'",timeout=20000);guest.evaluate("render()")
  R['key']=band(guest);guest.evaluate("MPT.read=window.__r;mpRetry()");guest.wait_for_function("()=>MP.fail===0",timeout=20000)
  # 親の iPad が開いていない(親を止めて、いる印を古くする)
  host.evaluate("mpStop()");guest.evaluate("localStorage.setItem('mpmock_'+MPG.id+'_hb_h.json',JSON.stringify({ts:Date.now()-7*60*1000}))")
  guest.wait_for_function("()=>mpConn().k==='away'",timeout=20000);guest.evaluate("render()");R['away']=band(guest);guest.screenshot(path=pre+'away.png')
  R['scroll']=[pg.evaluate("[document.documentElement.scrollWidth,innerWidth]") for pg in (host,guest)]
  R['bad']=[pg.evaluate("/NaN|undefined|\\[object|Infinity/.test(document.querySelector('#app').textContent)") for pg in (host,guest)]
  R['errs']=errs[:6]
  print(json.dumps(R,ensure_ascii=False,indent=1))
  b.close()
