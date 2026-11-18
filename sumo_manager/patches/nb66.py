# 土俵の中の文字を減らす・力士名をバッジに・行司が力士と重ならないように(見本 nb1〜3 と本番で共通)
import re
def apply(s, v):
    def rep(old, new, n=1):
        nonlocal s
        c = s.count(old)
        if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
        s = s.replace(old, new)
    OLD_NM = "'<text class=\"nm\" y=\"'+(-h-14)+'\" text-anchor=\"middle\" font-size=\"13\" font-weight=\"bold\" fill=\"'+col+'\" stroke=\"#fff8ea\" stroke-width=\"3\" paint-order=\"stroke\">'+esc(nm)+'</text>"
    if v in (1, 3):
        # 名前を色つきのバッジ(角の丸い札)に。東=赤、西=青
        rep(OLD_NM, "''+(()=>{const w=[...String(nm)].length*12.5+14;return '<g class=\"nm\" transform=\"translate(0,'+(-h-14)+')\"><rect x=\"'+(-w/2).toFixed(1)+'\" y=\"-11\" width=\"'+w.toFixed(1)+'\" height=\"18\" rx=\"9\" fill=\"'+col+'\" stroke=\"#fff8ea\" stroke-width=\"1.5\"/><text y=\"3\" text-anchor=\"middle\" font-size=\"12\" font-weight=\"bold\" fill=\"#fff\">'+esc(nm)+'</text></g>';})()+'")
    else:
        # 名前の頭の 1 字を丸いバッジに(フルネームは下の棒と横の実況に)
        rep(OLD_NM, "'<g class=\"nm\" transform=\"translate(0,'+(-h-10)+')\"><circle r=\"10\" fill=\"'+col+'\" stroke=\"#fff8ea\" stroke-width=\"2\"/><text y=\"4.5\" text-anchor=\"middle\" font-size=\"12\" font-weight=\"bold\" fill=\"#fff\">'+esc([...String(nm)][0]||'')+'</text></g>")
    # 名前の位置を動かすところ:バッジは transform で動かす(v2 は固定)
    a = s.find('function dhPlay('); b = s.find('const DH_CSS', a)
    f = s[a:b]
    f = re.sub(r"n([EW])\.setAttribute\('y',", (lambda m: "nyS(n%s," % m.group(1)) if v != 2 else (lambda m: "nyN(n%s," % m.group(1)), f)
    s = s[:a] + f + s[b:]
    rep("function dhGyoji(){", "function nyS(e,y){e.setAttribute('transform','translate(0,'+y+')');}function nyN(e,y){}\nfunction dhGyoji(){")
    # 土俵の中の文字を減らす:技の札(上手をつかんだ! など)・行司の声(のこった など)・「ここで落ちた」「残った!」は出さない(横の実況にはそのまま出る)
    rep("@keyframes dhb{0%{opacity:0}40%{opacity:1}100%{opacity:1}}", "@keyframes dhb{0%{opacity:0}40%{opacity:1}100%{opacity:1}}.dhw .tg,.dhw .mkt,.dhw .zan{display:none}.dhw .gyt{display:none}.dhw .gyt.fin{display:block}")
    rep("gy.querySelector('.gyt').textContent='勝負あり!';", "gy.querySelector('.gyt').textContent='勝負あり!';gy.querySelector('.gyt').classList.add('fin');")
    rep("wr.classList.remove('cheer','roar');", "wr.classList.remove('cheer','roar');{const g0=sv.querySelector('.gyt');if(g0)g0.classList.remove('fin');sv._gs=0;}")
    # 行司:2 人の横で、力士から離れた側に立つ(近いときは薄く)
    off = .62 if v != 2 else .78
    lim = .9 if v != 2 else .95
    rep("let tx=cx+nx*.5,ty=cy+ny*.5;const tr2=Math.hypot(tx,ty);if(tr2>.88){tx*=.88/tr2;ty*=.88/tr2;}",
        "const cand=sg=>{let x=cx+nx*%s*sg,y=cy+ny*%s*sg;const r2=Math.hypot(x,y);if(r2>%s){x*=%s/r2;y*=%s/r2;}const d=Math.min(Math.hypot(x-p.E[0],y-p.E[1]),Math.hypot(x-p.W[0],y-p.W[1]));return [x,y,d];};const c1=cand(1),c2=cand(-1);if(!sv._gs)sv._gs=c1[2]>=c2[2]?1:-1;else if((sv._gs===1?c2[2]-c1[2]:c1[2]-c2[2])>.18)sv._gs=-sv._gs;let [tx,ty]=sv._gs===1?c1:c2;" % (off, off, lim, lim, lim))
    rep("gy.querySelector('.grot').setAttribute('transform','rotate('+ga.toFixed(1)+')');\n", "gy.querySelector('.grot').setAttribute('transform','rotate('+ga.toFixed(1)+')');{const gd=Math.min(Math.hypot(gp[0]-p.E[0],gp[1]-p.E[1]),Math.hypot(gp[0]-p.W[0],gp[1]-p.W[1]));gy.setAttribute('opacity',gd<.3?.45:1);}\n")
    if v == 3:
        # 技や土俵際は、土俵の上の帯に 1 行だけ出す
        rep("zan.setAttribute('opacity',edge?(.6+.4*Math.sin(ts/90)):0);", "zan.setAttribute('opacity',edge?(.6+.4*Math.sin(ts/90)):0);{const bn=wr.querySelector('.dhban');if(bn){const nm=g=>g.querySelector('.nm').textContent;const t=fxE.tag?nm(ge)+' '+fxE.tag:fxW.tag?nm(gw)+' '+fxW.tag:edge?'土俵際!':'';if(bn.textContent!==t){bn.textContent=t;bn.style.opacity=t?1:0;}}}")
        rep("{const o=wr.querySelector('.kmo');if(o)o.remove();}", "{const o=wr.querySelector('.kmo');if(o)o.remove();}if(!wr.querySelector('.dhban'))wr.insertAdjacentHTML('beforeend','<div class=\"dhban\"></div>');")
        rep(".dhw .gyt.fin{display:block}", ".dhw .gyt.fin{display:block}.dhw .dhban{position:absolute;left:50%;top:3%;transform:translateX(-50%);background:rgba(20,16,12,.82);color:#ffe9a8;font:bold 14px sans-serif;padding:3px 12px;border-radius:12px;opacity:0;transition:opacity .2s;white-space:nowrap;pointer-events:none;z-index:1}")
    return s
