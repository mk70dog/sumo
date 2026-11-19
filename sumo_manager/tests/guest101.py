# 二人相撲の子の画面を巡回(#mpmock)。親は実在の部屋、子は部屋を選んで参加。全画面とボタン、3 サイズ。
from playwright.sync_api import sync_playwright
import sys, json, re
f=sys.argv[1]
BAD=re.compile(r'NaN|undefined|\[object|Infinity|(?<![A-Za-z])null(?![A-Za-z])')
SKIP=re.compile(r'quitTop|location|doUpd|askUpd|checkUpd|reset|newGame|goStart|imp|load|file|topMode|clearLog|copyLog|download|confirm|setSkin|setFont|mpCancel|mpGuestReady|doWeekUI|doToBasho|stepDay|stepAll|doNext')
out={}
with sync_playwright() as p:
  b=p.chromium.launch()
  for nm,(W,H) in {'ipad_l':(1180,820),'ipad_p':(820,1180),'phone':(390,844)}.items():
    ctx=b.new_context(viewport={'width':W,'height':H});errs=[]
    h=ctx.new_page();h.on('pageerror',lambda e:errs.append('H:'+str(e)[:150]))
    h.goto('file://'+f+'#mpmock');h.evaluate("localStorage.clear()");h.reload();h.wait_for_timeout(300)
    h.click('.st-two');h.click('.st-go2 .st-real >> nth=0');h.click('.hcard >> nth=0');h.wait_for_timeout(300);h.click('#hsheet .btn.main')
    h.wait_for_function("()=>G&&G.mp&&G.mp.id");code=h.evaluate("G.mp.id")
    g=ctx.new_page();g.on('pageerror',lambda e:errs.append('G:'+str(e)[:150]))
    g.goto('file://'+f+'#mpmock');g.wait_for_timeout(300);g.evaluate("()=>{window.alert=()=>{};window.confirm=()=>false;}")
    g.click('.st-two');g.click('.st-go2 .st-dok');g.fill('#mp_code',code);g.click('.mpkey .btn.main')
    g.wait_for_selector('.mpsel .btn');g.click('.mpsel .btn >> nth=1')
    h.wait_for_function("()=>G.mp.gh>0",timeout=20000);g.wait_for_function("()=>mpIsP()",timeout=20000);g.wait_for_timeout(300)
    bad={};wide={}
    for v in ['home','rikishi','keiko','basho','banzuke','scout','staff','keiei','kiroku','sys']:
      g.evaluate("v=>{try{closeM()}catch(e){};go(v)}",v);g.wait_for_timeout(80)
      n=g.evaluate("()=>document.querySelectorAll('#app button[onclick]').length")
      for i in range(-1,min(n,50)):
        if i>=0:
          oc=g.evaluate("i=>{const e=document.querySelectorAll('#app button[onclick]')[i];return e?e.getAttribute('onclick'):null}",i)
          if oc is None or SKIP.search(oc) or "go('" in oc: continue
          try:g.evaluate("i=>document.querySelectorAll('#app button[onclick]')[i].click()",i)
          except Exception as ex: errs.append('click '+oc[:50])
          g.wait_for_timeout(15)
        t=g.evaluate("()=>[...document.querySelectorAll('#app, #mdl.on #mbox')].map(e=>e.innerText).join('\\n')")
        bl=[l[:100] for l in t.split('\n') if BAD.search(l)]
        if bl: bad.setdefault(v,bl[:3])
        sw=g.evaluate("()=>document.documentElement.scrollWidth")
        if sw>W+1: wide.setdefault(v,sw)
        if i>=0: g.evaluate("v=>{try{closeM()}catch(e){};if(UI.view!==v)UI.view=v;render()}",v)
    out[nm]={'bad':bad,'wide':wide,'errs':errs[:6]}
    ctx.close()
  b.close()
print(json.dumps(out,ensure_ascii=False,indent=1))
