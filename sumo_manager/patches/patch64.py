# 決まり手 82 手+非技 5・裏の得意技、決まり手の札の文字あふれ・判子の四角の不具合  v60 -> v61
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v60</title>', '<title>Sumo Manager v61</title>')
rep("const APPV=60;\nconst SAVE='sumoManager60',SAVE59", "const APPV=61;\nconst SAVE='sumoManager61',SAVE60='sumoManager60',SAVE59")
rep('[SAVE59,SAVE58', '[SAVE60,SAVE59,SAVE58')
rep(" if(g.v===59){g.v=60;}\n return g.v===60?g:null;}", " if(g.v===59){g.v=60;}\n if(g.v===60){g.v=61;}\n return g.v===61?g:null;}")
rep('G={v:60,', 'G={v:61,')
core = open('patches/km64_core.js', encoding='utf-8').read()
rep("function fight(A,B,ctx){", core + "function fight(A,B,ctx){")
# 決まったあと、まれに同じ系統の珍しい技へ(実況の最後の行の技の名前も合わせる)
rep("const fin=(wi,k,x)=>({w:S[wi],l:S[1-wi],wi:wi,k:k,nar:nar,ev:ev,hv:x==='hv',hard:x==='hard'});",
    "const fin=(wi,k,x)=>{const k2=kmRare(S[wi],k);if(k2!==k&&nar&&nar.length){nar[nar.length-1]=nar[nar.length-1].split(k).join(k2);if(nar[nar.length-1].indexOf(k2)<0)nar.push('決まり手は「'+k2+'」と場内に告げられた。');}return {w:S[wi],l:S[1-wi],wi:wi,k:k2,nar:nar,ev:ev,hv:x==='hv',hard:x==='hard'||(k2!==k&&!HIGI.includes(k2))};};")
# 珍しい技:力士に記録・ニュース
rep("return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,ev:f.ev,a:a,big:ctx.big};",
    "if(kmIsRare(f.k)&&!HIGI.includes(f.k)){W.rare=W.rare||{};W.rare[f.k]=(W.rare[f.k]||0)+1;if(W.h===0||(W.d===0&&L.d===0))addNews((W.h===0?'':'幕内で')+W.n+'が珍しい決まり手「'+f.k+'」で'+L.n+'を破りました。館内が大きくどよめきました。');}\n return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,ev:f.ev,a:a,big:ctx.big,rare:kmIsRare(f.k)&&!HIGI.includes(f.k)};")
# 土俵の動き:新しい決まり手の型
rep("function dhType(k){k=k||'';if(/うっちゃり|打っ棄り/.test(k))return 'uchari';",
    "function dhType(k){k=k||'';if(/うっちゃり|打っ棄り|反り|もたれ/.test(k))return 'uchari';if(/無双|呼び戻し|徳利|二丁/.test(k))return 'nage';if(/股|払い|褄取り|裾取り|三所|二枚蹴り|ちょん掛け/.test(k))return 'taoshi';if(/割り出し|吊り|極め|鯖折り|踏み出し/.test(k))return /送り/.test(k)?'okuri':'yori';if(/素首|巻き落とし|つき手|つきひざ/.test(k))return 'hiki';")
# 不具合:判子(中身が空の四角)が決着のゆれで 0.5 秒だけ出ていた
rep(".dhw.boom .stamp{animation:dhb .5s}", ".dhw .stamp{display:none}")
# 不具合:決まり手の札の文字が札からあふれて 2 列になる → 折り返さず、入りきらなければ字を小さく
rep(".dhw .kmo b{font:min(34px,6.5vw) YSk,serif;color:#141210;letter-spacing:3px}.dhw .kmo span{font:min(17px,3.6vw) YSk,serif;color:#b5361f;letter-spacing:2px}",
    ".dhw .kmo b{font:min(34px,6.5vw) YSk,serif;color:#141210;letter-spacing:3px;white-space:nowrap}.dhw .kmo span{font:min(17px,3.6vw) YSk,serif;color:#b5361f;letter-spacing:2px;white-space:nowrap}.dhw .kmo{overflow:hidden}")
rep("wr.insertAdjacentHTML('beforeend','<div class=\"kmo'+(lo[0]>0?' l':'')+'\"><b>'+esc(pl.k)+'</b><span>'+esc(pl.WN)+'</span></div>');}",
    "wr.insertAdjacentHTML('beforeend','<div class=\"kmo'+(lo[0]>0?' l':'')+'\"><b>'+esc(pl.k)+'</b><span>'+esc(pl.WN)+'</span></div>');const ko=wr.querySelector('.kmo'),kb=ko.querySelector('b'),ks=ko.querySelector('span');const H=ko.clientHeight-20;const n1=[...pl.k].length,n2=[...String(pl.WN)].length;let fs=Math.min(34,Math.floor(H/(n1*1.12+.4*n2*1.12+.6)));fs=Math.max(11,fs);kb.style.fontSize=fs+'px';kb.style.letterSpacing=(fs>20?3:1)+'px';ks.style.fontSize=Math.max(10,Math.round(fs*.5))+'px';}")
# 力士の画面:得意の決まり手の下に「珍しい技」
rep("if(r.km){const km=Object.entries(r.km).sort((a,b)=>b[1]-a[1]).slice(0,6);h+='<h3>得意の決まり手</h3><div class=\"kaku\">'+km.map(([k,v])=>esc(k)+' '+v).join('・')+'</div>';}",
    "if(r.km){const km=Object.entries(r.km).sort((a,b)=>b[1]-a[1]).slice(0,6);h+='<h3>得意の決まり手</h3><div class=\"kaku\">'+km.map(([k,v])=>esc(k)+' '+v).join('・')+'</div>';}\n  if(r.rare&&Object.keys(r.rare).length){h+='<h3>決めた珍しい技</h3><div class=\"kaku\">'+Object.entries(r.rare).sort((a,b)=>b[1]-a[1]).map(([k,v])=>'<span class=\"tag shu\">'+esc(k)+(v>1?' '+v+'回':'')+'</span>').join(' ')+'</div>';}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
