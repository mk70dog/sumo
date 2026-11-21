# 二人相撲の勝負の形(v102)。親が形を選んで始め、子が参加→数場所進める→帯・記録の欄・決着を確かめる(#mpmock)。
# usage: python3 sb102.py 本体.html 形(1〜4) [期間y] [目標g] [場所数] [写真の前置き]
from playwright.sync_api import sync_playwright
import sys,json,os
f=sys.argv[1];K=int(sys.argv[2]);Y=int(sys.argv[3]) if len(sys.argv)>3 else 10;GL=sys.argv[4] if len(sys.argv)>4 else 'yok';NB=int(sys.argv[5]) if len(sys.argv)>5 else 8;pre=sys.argv[6] if len(sys.argv)>6 else '/tmp/sb102_'
ADV="""(n)=>{for(let b=0;b<n;b++){let g=0;while(G.phase==='train'&&g++<80)doWeek();g=0;while(G.phase==='basho'&&g++<40)advanceDay();
  forP(()=>{let k=0;while(G.ev.length&&k++<60){try{resolveEv(G.ev[0].id,0);}catch(e){G.ev.shift();}}});if(!nextCycle()){forP(()=>{G.ev.length=0;});nextCycle();}}}"""
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={'width':int(os.environ.get('SBW','1180')),'height':int(os.environ.get('SBH','820'))});errs=[]
  host=ctx.new_page();host.on('pageerror',lambda e:errs.append('H:'+str(e)))
  host.goto('file://'+f+'#mpmock');host.evaluate("localStorage.clear()");host.reload();host.wait_for_timeout(400)
  host.click('.st-two');host.evaluate("([k,y,g])=>{UI.mpSb={k:k,y:y,g:g};render();}",[K,Y,GL]);host.wait_for_selector('.sbpick');host.screenshot(path=pre+'pick.png')
  host.click('.st-go2 .st-real >> nth=0');host.click('.hcard >> nth=0');host.wait_for_timeout(350);host.click('#hsheet .btn.main')
  host.wait_for_function("()=>G&&G.mp&&G.mp.id");code=host.evaluate("G.mp.id");sbH=host.evaluate("G.mp.sb")
  guest=ctx.new_page();guest.on('pageerror',lambda e:errs.append('G:'+str(e)))
  guest.goto('file://'+f+'#mpmock');guest.wait_for_timeout(400);guest.click('.st-two');guest.click('.st-go2 .st-dok');guest.fill('#mp_code',code);guest.click("button[onclick='mpJoin()']")
  guest.wait_for_selector('.mpsel .btn');joinTxt=guest.evaluate("document.querySelector('#app').textContent.includes('勝負の形')");guest.screenshot(path=pre+'join.png')
  guest.click('.mpsel .btn >> nth=0')
  host.wait_for_function("()=>G.mp.gh>0&&G.P&&G.P.length===2",timeout=20000);host.wait_for_timeout(800)
  sbi=host.evaluate("[G.mp.sb.b0,G.mp.sb.n]")
  host.evaluate(ADV,NB)
  host.evaluate("async()=>{G.mp.n++;await mpWriteWorld();}")
  guest.wait_for_function("()=>MPG.n>=1&&mpIsP()",timeout=20000);guest.wait_for_timeout(600)
  hs=host.evaluate("(()=>{const s=G.mp.sb;return {n:s.n,ta:s.ta,tg:s.tg,yu:s.yu,nj:s.nj,r1:s.r1,done:s.done,last:s.log[s.log.length-1],ia:s.ia}})()")
  host.evaluate("go('kiroku')");host.wait_for_timeout(300);host.screenshot(path=pre+'h_kiroku.png',full_page=False)
  bandH=host.evaluate("(document.querySelector('.sbb')||{}).textContent||''");cardH=host.evaluate("(document.querySelector('.sbc h3')||{}).textContent||''")
  guest.evaluate("go('kiroku')");guest.wait_for_timeout(300);guest.screenshot(path=pre+'g_kiroku.png')
  bandG=guest.evaluate("(document.querySelector('.sbb')||{}).textContent||''");cardG=guest.evaluate("(document.querySelector('.sbc h3')||{}).textContent||''")
  bad=host.evaluate("/NaN|undefined|\\[object|Infinity/.test(document.querySelector('#app').textContent)");badg=guest.evaluate("/NaN|undefined|\\[object|Infinity/.test(document.querySelector('#app').textContent)")
  sw=[pg.evaluate("[document.documentElement.scrollWidth,innerWidth]") for pg in (host,guest)]
  print(json.dumps(dict(k=K,sb=sbH,joinBanner=joinTxt,start=sbi,host=hs,bandH=bandH,cardH=cardH,bandG=bandG,cardG=cardG,badH=bad,badG=badg,scroll=sw,errs=errs[:6]),ensure_ascii=False))
  b.close()
