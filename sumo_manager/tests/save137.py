# v137 保存の直し:前の版の保存で保存の場所がいっぱいのときに、新しい版で遊んで保存し、読み直すと進みが残るか。
# usage: python3 save137.py 本体.html [前の版の保存キー]
import sys, json
from playwright.sync_api import sync_playwright
f=sys.argv[1]; oldk=sys.argv[2] if len(sys.argv)>2 else 'sumoManager136'
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context();pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+f);pg.wait_for_timeout(800)
    # 前の版の保存(本物)と、ほかの古い版のごみで保存の場所を埋める
    pg.evaluate("""(oldk)=>{localStorage.clear();newGameReal('伊勢ヶ濱');const s=saveStr();localStorage.setItem(oldk,s);
      let i=100;try{for(;i<136;i++){localStorage.setItem('sumoManager'+i,s);}}catch(e){}let j=0;const sm='x'.repeat(50000);try{for(;j<400;j++)localStorage.setItem('sumoManager'+(i+1)+'_'+j,sm);}catch(e){}try{localStorage.setItem('sumoManager'+(i+1),'x'.repeat(40000));}catch(e){}window.__fill=i+'/'+j;}""",oldk)
    fill=pg.evaluate("()=>window.__fill")
    pg.reload();pg.wait_for_timeout(1500)
    a=pg.evaluate("()=>({wk:G&&G.wk,b:G&&G.bnum})")
    pg.evaluate("()=>{doWeek();doWeek();save();}")
    s1=pg.evaluate(r"()=>{const v=localStorage.getItem(SAVE);return {has:!!v,lz:v?v.slice(0,4):'',len:v?v.length:0,keys:Object.keys(localStorage).filter(k=>/^sumoManager\d+$/.test(k)).length,err:G._svErr||0};}")
    pg.reload();pg.wait_for_timeout(1500)
    c=pg.evaluate("()=>({wk:G&&G.wk,b:G&&G.bnum})")
    print(json.dumps({'fill':fill,'before':a,'saved':s1,'after':c,'errs':errs},ensure_ascii=False))
