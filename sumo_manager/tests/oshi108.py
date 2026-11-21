# v108:注目選手 3 人(選ぶ・タブ・本場所の並び・力士のまど・前の版の数字 1 つ)
import asyncio,sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'sumo_manager_v108.html'
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1180,'height':820})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/sumo/sumo_manager/'+F);await pg.wait_for_timeout(800)
    r=await pg.evaluate("""()=>{localStorage.clear();newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;go('home');const o=own().slice().sort((a,b)=>a.pos-b.pos);const out={};
     G.oshi=o[2].id;out.old=oshiIds().length===1&&oshiR().id===o[2].id;G.oshi=null;out.auto=oshiL().length===1&&oshiL()[0].id===heyaTop().id;
     oshiPick();osTog(o[5].id);osTog(o[1].id);osTog(o[7].id);osTog(o[9].id);out.three=JSON.stringify(G.oshi)===JSON.stringify([o[5].id,o[1].id,o[7].id]);closeM();
     render();out.tabs=document.querySelectorAll('.ostab button').length;UI.osTab=2;render();out.tab2=document.querySelector('.hbo h3 a').textContent===o[7].n;
     showR(o[1].id);out.rmv=document.body.innerHTML.includes('注目選手から外す');closeM();
     let n=0;while(G.phase==='train'&&n++<40)doWeek();stepDay();stepDay();stepDay();closeM();go('basho');
     const tr=[...document.querySelectorAll('tr.os')].length;out.hoshi=tr;out.nx=[...document.querySelectorAll('.nx.os')].length;out.r1=[...document.querySelectorAll('.r1.os')].length;
     const first=[...document.querySelectorAll('.r1')].slice(0,out.r1).every(e=>e.classList.contains('os'));out.r1top=first;
     osTog(o[5].id,1);closeM();out.after=oshiIds().length;return out;}""")
    print(r,errs)
    await pg.screenshot(path='/tmp/o108.png')
    await b.close()
asyncio.run(main())
