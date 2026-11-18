# 行司の軍配と終盤の観客(見本 gun1〜3 と patch65 で共通に使う)。v=1,2,3
def apply(s, v):
    def rep(old, new, n=1):
        nonlocal s
        c = s.count(old)
        if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
        s = s.replace(old, new)
    # 行司を少し大きく。軍配に光る輪、勝った力士への線
    rep('function dhGyoji(){return \'<g class="gyo"><g class="grot">', 'function dhGyoji(){return \'<g class="gyo"><g class="gsc" transform="scale(1.3)"><line class="gpt" x1="20" y1="0" x2="20" y2="0" stroke="#e8c870" stroke-width="3" stroke-dasharray="5 4" opacity="0"/><g class="grot">')
    rep('<ellipse rx="9" ry="7" fill="#1d1d1d" stroke="#c9a24a" stroke-width="2.5"/></g></g><text class="gyt"', '<ellipse rx="9" ry="7" fill="#1d1d1d" stroke="#c9a24a" stroke-width="2.5"/><circle class="gfl" r="11" fill="none" stroke="#ffe27a" stroke-width="3" opacity="0"/></g></g></g><text class="gyt"')
    # 決着:軍配をぐっと上げて勝った側へ差し出す(0.5 秒で大きく)、名前を大きく
    fin = ("{const g0=[16,-14],g1=[30,-2];const t0=performance.now();const ease=t=>{const c=1.7;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2);};"
           "const an=now=>{const t=Math.min(1,(now-t0)/480),e=ease(t);gb.setAttribute('transform','translate('+(g0[0]+(g1[0]-g0[0])*e).toFixed(1)+','+(g0[1]+(g1[1]-g0[1])*e).toFixed(1)+') scale('+(1+.9*e).toFixed(2)+')');if(t<1)requestAnimationFrame(an);};requestAnimationFrame(an);"
           "const fl=gy.querySelector('.gfl');fl.style.animation='none';void fl.getBBox();fl.style.animation='gfl .9s ease-out 3';"
           "const dist=Math.hypot(wv[0]-gp[0],wv[1]-gp[1])*S/1.3;const ln=gy.querySelector('.gpt');ln.setAttribute('x2',Math.max(24,dist-30).toFixed(0));ln.setAttribute('transform','rotate('+ga.toFixed(1)+')');ln.setAttribute('opacity',.9);"
           "const gt=gy.querySelector('.gyt');gt.textContent=pl.WN+'!';gt.setAttribute('font-size',17);gt.setAttribute('opacity',1);gt.setAttribute('fill',pl.winE?'#b5361f':'#2d4d7a');gt.setAttribute('y',gp[1]<0?-34:40);}")
    rep("gb.setAttribute('transform','translate(26,0)');gy.querySelector('.gyt').textContent='勝負あり!';", fin)
    # はじめに戻す
    rep("wr.classList.remove('cheer','roar');", "wr.classList.remove('cheer','roar','late','wave','stand');{const ln=sv.querySelector('.gpt');if(ln)ln.setAttribute('opacity',0);const gb0=sv.querySelector('.gb');if(gb0)gb0.setAttribute('transform','translate(16,-14)');sv.querySelectorAll('.bub,.zab').forEach(e=>e.remove());}")
    # 終盤(後半・土俵際)は観客がだんだんざわつく
    rep("wr.classList.toggle('cheer',!!hot);", "wr.classList.toggle('cheer',!!hot);wr.classList.toggle('late',pt>.55&&pt<pl.fin);")
    css = ".dhw.late .crowd .fan>g{animation:fan .45s ease-in-out infinite alternate}@keyframes gfl{0%{opacity:1;r:9}100%{opacity:0;r:26}}"
    if v == 1:
        # 大歓声:観客の波(全体が順に揺れる)
        rep("wr.classList.remove('cheer');wr.classList.add('roar');setTimeout(()=>wr.classList.remove('roar'),2500);",
            "wr.classList.remove('cheer','late');wr.classList.add('roar','wave');setTimeout(()=>wr.classList.remove('roar','wave'),3200);")
        css += ".dhw.wave .crowd .fan>g{animation:fan .2s ease-in-out infinite alternate}.dhw.wave .crowd .fan:nth-child(4n)>g{animation-delay:.1s}.dhw.wave .crowd .fan:nth-child(4n+1)>g{animation-delay:.05s}.dhw.wave .crowd{animation:cflash .5s 3}@keyframes cflash{50%{filter:brightness(1.35)}}"
    if v == 2:
        # 歓声の吹き出し:終盤と決着で客席から声が上がる
        rep("wr.classList.remove('cheer');wr.classList.add('roar');setTimeout(()=>wr.classList.remove('roar'),2500);",
            "wr.classList.remove('cheer','late');wr.classList.add('roar');setTimeout(()=>wr.classList.remove('roar'),3000);dhBub(sv,8,['おおーっ!','よしっ!','わぁー!','すごい!','うまい!',pl.WN+'!']);")
        rep("wr.classList.toggle('late',pt>.55&&pt<pl.fin);", "wr.classList.toggle('late',pt>.55&&pt<pl.fin);if(hot&&rmax>.78&&!sv._bub){sv._bub=1;dhBub(sv,3,['残れー!','いけー!','粘れ!']);setTimeout(()=>sv._bub=0,900);}")
        rep("function dhGyoji(){", "function dhBub(sv,n,L){const g=sv.querySelector('.crowd');if(!g)return;for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,R=188+Math.random()*16;const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('class','bub');t.setAttribute('x',(Math.cos(a)*R).toFixed(0));t.setAttribute('y',(Math.sin(a)*R).toFixed(0));t.setAttribute('text-anchor','middle');t.textContent=L[i%L.length];t.style.animationDelay=(i*.12).toFixed(2)+'s';sv.appendChild(t);setTimeout(()=>t.remove(),2600);}}\nfunction dhGyoji(){")
        css += ".dhw .bub{font:bold 13px sans-serif;fill:#fff;stroke:#b5361f;stroke-width:3px;paint-order:stroke;opacity:0;animation:bub 1.6s ease-out forwards}@keyframes bub{0%{opacity:0;transform:translateY(6px)}20%{opacity:1}100%{opacity:0;transform:translateY(-18px)}}"
    if v == 3:
        # 総立ち:観客が立ち上がる(大きく明るく)。横綱が負けたら座布団が舞う
        rep("wr.classList.remove('cheer');wr.classList.add('roar');setTimeout(()=>wr.classList.remove('roar'),2500);",
            "wr.classList.remove('cheer','late');wr.classList.add('roar','stand');setTimeout(()=>wr.classList.remove('roar','stand'),3200);if(pl.zab)dhZab(sv);")
        rep("function dhGyoji(){", "function dhZab(sv){const C=['#7a2a2a','#2a4a7a','#6a5a2a','#3a6a4a','#5a3a6a'];for(let i=0;i<26;i++){const a=Math.random()*Math.PI*2,R=185+Math.random()*20;const x=Math.cos(a)*R,y=Math.sin(a)*R;const r=document.createElementNS('http://www.w3.org/2000/svg','rect');r.setAttribute('class','zab');r.setAttribute('width',11);r.setAttribute('height',11);r.setAttribute('x',-5.5);r.setAttribute('y',-5.5);r.setAttribute('fill',C[i%C.length]);r.setAttribute('stroke','#e8d8a8');r.style.setProperty('--x0',x.toFixed(0)+'px');r.style.setProperty('--y0',y.toFixed(0)+'px');r.style.setProperty('--x1',(x*.45+(Math.random()-.5)*60).toFixed(0)+'px');r.style.setProperty('--y1',(y*.45+(Math.random()-.5)*60).toFixed(0)+'px');r.style.animationDelay=(Math.random()*.6).toFixed(2)+'s';sv.appendChild(r);setTimeout(()=>r.remove(),3200);}}\nfunction dhGyoji(){")
        rep("const pl=(b.ev&&b.ev.length?dhPlanEv(b,p):null)||dhPlan(b.k,p.winE,dhSeed(b),p.E.n,p.Wt.n);", "const pl=(b.ev&&b.ev.length?dhPlanEv(b,p):null)||dhPlan(b.k,p.winE,dhSeed(b),p.E.n,p.Wt.n);{const W=G.R[b.w],L=G.R[b.l];pl.zab=!!(W&&L&&L.t==='Y'&&!W.t&&W.d===0);}")
        css += ".dhw.stand .crowd .fan>g{animation:stand .25s ease-in-out infinite alternate}@keyframes stand{0%{transform:scale(1.15)}100%{transform:translateY(-4px) scale(1.35);filter:brightness(1.3)}}.dhw .zab{animation:zab 1.8s cubic-bezier(.3,.6,.5,1) forwards;transform:translate(var(--x0),var(--y0))}@keyframes zab{0%{transform:translate(var(--x0),var(--y0)) rotate(0)}60%{transform:translate(var(--x1),var(--y1)) rotate(400deg)}100%{transform:translate(var(--x1),var(--y1)) rotate(520deg);opacity:.9}}"
    rep("@keyframes dhb{0%{opacity:0}40%{opacity:1}100%{opacity:1}}", "@keyframes dhb{0%{opacity:0}40%{opacity:1}100%{opacity:1}}" + css)
    return s
