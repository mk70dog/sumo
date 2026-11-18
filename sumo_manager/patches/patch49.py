# 注目選手の続き:まわりの 6 項目を力士の画面に、星取表・次の取組に★  v45 -> v46
# 使い方: python3 patch49.py src dst [A|B|AB]  A=力士の画面に「まわり」タブ  B=能力・状態の上に札で並べる  AB=両方(既定。ダルマさんの選択)
import sys, os
src, dst = sys.argv[1], sys.argv[2]; V = sys.argv[3] if len(sys.argv) > 3 else 'AB'
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v45</title>', '<title>Sumo Manager v46</title>')
rep("const APPV=45;\nconst SAVE='sumoManager45',SAVE44", "const APPV=46;\nconst SAVE='sumoManager46',SAVE45='sumoManager45',SAVE44")
rep('[SAVE44,SAVE43', '[SAVE45,SAVE44,SAVE43')
rep(" if(g.v===44){g.v=45;g.oshi=null;}\n return g.v===45?g:null;}", " if(g.v===44){g.v=45;g.oshi=null;}\n if(g.v===45){g.v=46;}\n return g.v===46?g:null;}")
rep('G={v:45,', 'G={v:46,')
# 図と一覧を部品に分ける
rep("function oshiHTML(){const r=oshiR();if(!r)return '';const L=oshiItems(r);const n=L.length;",
"function oshiRing(r){const L=oshiItems(r);const n=L.length;const pos=L.map((x,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;return [50+40*Math.cos(a),50+40*Math.sin(a)];});const col=c=>c==='p'?'var(--shu)':c==='n'?'var(--ai)':'var(--line)';\n return '<div class=\"ow\"><div class=\"ring\"><svg>'+pos.map((p,i)=>'<line x1=\"50%\" y1=\"50%\" x2=\"'+p[0]+'%\" y2=\"'+p[1]+'%\" stroke=\"'+col(L[i].c)+'\" stroke-width=\"'+(L[i].c==='0'?1.5:3)+'\"/>').join('')+'</svg><div class=\"c\">'+esc(r.n)+'</div>'+L.map((x,i)=>'<div class=\"pb s'+x.c+'\" style=\"left:'+pos[i][0]+'%;top:'+pos[i][1]+'%\"><b>'+x.lb+'</b>'+esc(x.t)+'</div>').join('')+'</div>'+\n '<ul class=\"ol\">'+L.map(x=>'<li class=\"s'+x.c+'\"><b>'+x.lb+'</b>'+(x.c==='p'?' <span class=\"ob sp\">追い風</span>':x.c==='n'?' <span class=\"ob sn\">向かい風</span>':'')+'<br><span>'+esc(x.s)+'</span></li>').join('')+'</ul></div>';}\n"
"function oshiTags(r){return '<div class=\"otg\">'+oshiItems(r).map(x=>'<span class=\"otag s'+x.c+'\">'+x.lb+':'+esc(x.t)+'</span>').join('')+'</div>';}\n"
"function oshiHTML(){const r=oshiR();if(!r)return '';const L=oshiItems(r);const n=L.length;")
if 'A' in V:
    rep("h=H0+rTabs(id,['能力・状態','経歴','記録'])+'<div class=\"rtbx\">'+(tb===1?keiR(r):tb===2?(P2||'<p class=\"mute kaku\">まだ記録がありません。</p>'):P0)+'</div>';",
        "h=H0+rTabs(id,isOwn&&!pd?['能力・状態','経歴','記録','まわり']:['能力・状態','経歴','記録'])+'<div class=\"rtbx\">'+(tb===3&&isOwn&&!pd?'<p class=\"kaku mute\" style=\"margin:4px 0 8px\">まわりからの追い風・向かい風。追い風は気持ちを少し上げ、向かい風は少し下げます。</p>'+oshiRing(r)+(oshiR()&&oshiR().id===r.id?'<p class=\"kaku\"><span class=\"ost\">★</span> 注目選手</p>':'<p><button class=\"btn sm\" onclick=\"G.oshi='+r.id+';save();showR('+r.id+')\">★ 注目選手にする</button></p>'):tb===1?keiR(r):tb===2?(P2||'<p class=\"mute kaku\">まだ記録がありません。</p>'):P0)+'</div>';")
if 'B' in V:
    rep("  h+=trustBox(r);", "  h+=oshiTags(r);\n  h+=trustBox(r);")
# 星取表・次の取組に★
rep("'<tr><td>'+esc(r.rkS)+'</td><td class=\"nm clk2\" onclick=\"showR('+r.id+')\">'+esc(r.n)+injTag(r)",
    "'<tr'+(oshiR()&&oshiR().id===r.id?' class=\"os\"':'')+'><td>'+esc(r.rkS)+'</td><td class=\"nm clk2\" onclick=\"showR('+r.id+')\">'+(oshiR()&&oshiR().id===r.id?'<span class=\"ost\">★</span>':'')+esc(r.n)+injTag(r)")
rep("const nx=B.cur.filter(p=>G.R[p[0]].h===0||G.R[p[1]].h===0);", "const nx=B.cur.filter(p=>G.R[p[0]].h===0||G.R[p[1]].h===0);{const os=oshiR();if(os){const k=nx.findIndex(p=>p[0]===os.id||p[1]===os.id);if(k>0)nx.unshift(nx.splice(k,1)[0]);}}")
rep("return '<div class=\"nx\"><div class=\"nxm\"><div><span class=\"nm\">'+esc(a.n)+'</span>",
    "return '<div class=\"nx'+(oshiR()&&oshiR().id===a.id?' os':'')+'\"><div class=\"nxm\"><div>'+(oshiR()&&oshiR().id===a.id?'<span class=\"ost\">★</span>':'')+'<span class=\"nm\">'+esc(a.n)+'</span>")
rep(".r1.os{", "tr.os td{background:var(--washi2)}.nx.os{border-left-color:var(--shu)!important}.otg{margin:4px 0 8px}.otag{display:inline-block;font:12px/1.8 var(--kaku);border:1px solid var(--line);color:var(--sumi2);border-radius:12px;padding:0 9px;margin:2px 4px 0 0}.otag.sp{border-color:var(--shu);color:var(--shu)}.otag.sn{border-color:var(--ai);color:var(--ai)}\n.r1.os{")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', V)
