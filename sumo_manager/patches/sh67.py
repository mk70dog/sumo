# 「勝負あり」の見せ方 5 案(nb66 v1 のあとに当てる)
def apply(s, v):
    def rep(old, new, n=1):
        nonlocal s
        c = s.count(old)
        if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
        s = s.replace(old, new)
    A = "gy.querySelector('.gyt').textContent='勝負あり!';gy.querySelector('.gyt').classList.add('fin');"
    WC = "(p.lose==='E'?'#2d4d7a':'#b5361f')"
    WN = "(p.lose==='E'?gw:ge).querySelector('.nm').textContent"
    css = ''
    if v == 1:
        # 行司の横に、縦書きの筆文字で大きく「勝負あり」
        rep(A, "gy.querySelector('.gyt').classList.add('fin');{const gx=gp[0]*S,gyy=gp[1]*S;const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('class','sh1');t.setAttribute('x',(gx+(gx>0?-34:34)).toFixed(0));t.setAttribute('y',(gyy-40).toFixed(0));t.textContent='勝負あり';sv.appendChild(t);setTimeout(()=>t.remove(),2600);}")
        css = ".dhw .sh1{writing-mode:vertical-rl;font:34px YSk,serif;fill:#1d1d1d;stroke:#fff8ea;stroke-width:5px;paint-order:stroke;animation:sh1 2.4s ease-out forwards}@keyframes sh1{0%{opacity:0;transform:translateY(-10px)}12%{opacity:1;transform:none}80%{opacity:1}100%{opacity:0}}"
    if v == 2:
        # 土俵の真ん中にドンと大きく(筆文字)、すぐ消えて決まり手の札へ
        rep(A, "gy.querySelector('.gyt').classList.add('fin');{const d=document.createElement('div');d.className='sh2';d.textContent='勝負あり';wr.appendChild(d);setTimeout(()=>d.remove(),1500);}")
        css = ".dhw .sh2{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);font:min(64px,13vw) YSk,serif;color:#1d1d1d;text-shadow:0 0 6px #fff8ea,0 0 12px #fff8ea;white-space:nowrap;pointer-events:none;z-index:3;animation:sh2 1.4s cubic-bezier(.2,1.5,.4,1) forwards}@keyframes sh2{0%{opacity:0;transform:translate(-50%,-50%) scale(2.2)}25%{opacity:1;transform:translate(-50%,-50%) scale(1)}75%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(.95)}}"
    if v == 3:
        # 勝った側の色の光が土俵を走り、軍配の上に「東/西 ○○」の小さな札
        rep(A, "gy.querySelector('.gyt').classList.add('fin');{const c="+WC+";wr.style.setProperty('--wc',c);wr.classList.remove('sh3');void wr.offsetWidth;wr.classList.add('sh3');setTimeout(()=>wr.classList.remove('sh3'),1600);const t=document.createElementNS('http://www.w3.org/2000/svg','g');t.setAttribute('class','sh3t');const nm="+WN+";const w=[...nm].length*13+46;t.setAttribute('transform','translate('+(gp[0]*S).toFixed(0)+','+(gp[1]*S+(gp[1]<0?44:-40)).toFixed(0)+')');t.innerHTML='<rect x=\"'+(-w/2)+'\" y=\"-13\" width=\"'+w+'\" height=\"24\" rx=\"5\" fill=\"'+c+'\" stroke=\"#e8c870\" stroke-width=\"2\"/><text y=\"5\" text-anchor=\"middle\" font-size=\"14\" font-weight=\"bold\" fill=\"#fff\">'+(p.lose==='E'?'西 ':'東 ')+nm+'</text>';sv.appendChild(t);setTimeout(()=>t.remove(),2600);}")
        css = ".dhw.sh3::after{content:"";position:absolute;inset:0;border-radius:6px;box-shadow:inset 0 0 0 6px var(--wc),inset 0 0 40px var(--wc);pointer-events:none;animation:sh3 1.5s ease-out forwards}@keyframes sh3{0%{opacity:0}15%{opacity:.95}100%{opacity:0}}.dhw .sh3t{animation:sh1b 2.5s ease-out forwards}@keyframes sh1b{0%{opacity:0}10%{opacity:1}85%{opacity:1}100%{opacity:0}}"
    if v == 4:
        # 土俵の上(客席の上)の帯に「勝負あり ― ○○の勝ち」
        rep(A, "gy.querySelector('.gyt').classList.add('fin');{let d=wr.querySelector('.sh4');if(!d){d=document.createElement('div');d.className='sh4';wr.appendChild(d);}d.innerHTML='勝負あり <span style=\"color:'+"+WC+"+'\">'+"+WN+"+'</span> の勝ち';d.classList.remove('on');void d.offsetWidth;d.classList.add('on');}")
        rep("wr.classList.remove('cheer','roar');", "wr.classList.remove('cheer','roar');{const d=wr.querySelector('.sh4');if(d)d.classList.remove('on');}")
        css = ".dhw .sh4{position:absolute;left:50%;top:2.5%;transform:translateX(-50%);background:#fff8ea;color:#1d1d1d;font:bold 16px sans-serif;padding:4px 16px;border-radius:14px;border:2px solid #5a3a1a;white-space:nowrap;opacity:0;pointer-events:none;z-index:2}.dhw .sh4 span{background:none}.dhw .sh4.on{animation:sh4 .4s ease-out forwards}@keyframes sh4{0%{opacity:0;transform:translate(-50%,-8px)}100%{opacity:1;transform:translate(-50%,0)}}"
    if v == 5:
        # 行司の声の吹き出し(しっぽが行司を指す)
        rep(A, "gy.querySelector('.gyt').classList.add('fin');{const gx=gp[0]*S,gyy=gp[1]*S;const up=gyy>-60;const bx=Math.max(-150,Math.min(150,gx)),by=up?gyy-62:gyy+62;const g=document.createElementNS('http://www.w3.org/2000/svg','g');g.setAttribute('class','sh5');g.innerHTML='<path d=\"M'+(bx-70)+','+(by-18)+' h140 a8,8 0 0 1 8,8 v20 a8,8 0 0 1 -8,8 h-'+(up?55:85)+' L'+gx+','+(up?gyy-16:gyy+16)+' L'+(bx+(up?5:-25))+','+(by+18)+' h-'+(up?75:45)+' a8,8 0 0 1 -8,-8 v-20 a8,8 0 0 1 8,-8z\" fill=\"#fff\" stroke=\"#6b3b8a\" stroke-width=\"2.5\"/><text x=\"'+bx+'\" y=\"'+(by+8)+'\" text-anchor=\"middle\" font-size=\"21\" font-weight=\"bold\" fill=\"#6b3b8a\">勝負あり!</text>';sv.appendChild(g);setTimeout(()=>g.remove(),2600);}")
        css = ".dhw .sh5{animation:sh5 2.5s ease-out forwards;transform-origin:center}@keyframes sh5{0%{opacity:0}8%{opacity:1}85%{opacity:1}100%{opacity:0}}"
    rep(".dhw .gyt.fin{display:block}", ".dhw .gyt.fin{display:none}" + css)
    return s
