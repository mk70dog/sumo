# v94 -> v95:独立で連れて行く内弟子の決め方を直す(ダルマさん「内弟子の設定が曖昧?」→ 案 C:調べて分かった内弟子+つながりでの推定)
# 実際:中村親方(元嘉風、2019 年 9 月引退)の内弟子・友風は 2017 年 5 月初土俵(Number 2025/10/21、文藝春秋)=現役中に誘った弟子も内弟子。
#       中村親方の内弟子だった白熊・麒麟龍は元の部屋に残った(マネーポスト)=内弟子でも全員がついて来るとは限らない。
#       大森は北陣親方(元遠藤)の内弟子として追手風部屋に入門(sumo-guide.com 幕下力士一覧 2026 年 11 月)。
# 決め方:①記事で分かった内弟子(DOKUCH)②同じ大学 ③同じ高校 ④同郷(都道府県)⑤親方の引退後に入門(初土俵の年月があればそれを使う)。点数の合計で候補にし、理由を札で出す。
#        独立のとき、選んだ力士がついて来るかは点数で決まる(推定:3 点以上 90%・2 点 80%・それ未満 65%)。だれもついて来なければいちばん点の高い 1 人は来る。残った力士はお知らせに出す。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v94</title>', '<title>Grand Sumo Manager v95</title>')
rep("const APPV=94;\nconst SAVE='sumoManager94',SAVE93", "const APPV=95;\nconst SAVE='sumoManager95',SAVE94='sumoManager94',SAVE93")
rep('[SAVE93,SAVE92', '[SAVE94,SAVE93,SAVE92')
rep(" if(g.v===93){g.v=94;}\n return g.v===94?g:null;}", " if(g.v===93){g.v=94;}\n if(g.v===94){g.v=95;}\n return g.v===95?g:null;}")
rep('G={v:94,', 'G={v:95,')
old_ws = "function dokWs(x){if(x._ws)return x._ws;const ws=[];REALB.forEach((l,i)=>{const f=l.split('|');const ry=x.ret?(+x.ret.slice(0,4)+(+x.ret.slice(5,7)-1)/12):2020;const ag=realAge(f[4]);const k=KEI[f[1]];const ea=k?(k[3]?22:k[4]?22:k[2]?18:15):18;const dy=2026.87-ag+ea;if(f[3]===x.par&&!/^[YO]$/.test(f[0])&&dy>=ry)ws.push({n:f[1],rk:(f[0]?{S:'関脇',K:'小結'}[f[0]]:dokRk(i)),age:Math.floor(ag)});});x._ws=ws;return ws;}"
new_ws = r"""/* 記事で分かった内弟子(親方の名跡 → 四股名)。出典は引き継ぎ資料 */
const DOKUCH={'北陣':['大森']};
function dokWs(x){if(x._ws)return x._ws;const ws=[];const T=(typeof KEIT!=='undefined'&&KEIT[x.sh])||[];const cut=t=>(t||'').replace(/[(（].*$/,'').trim();
 const tu=cut(T[3]),th=cut(T[2]);const ry=x.ret?(+x.ret.slice(0,4)+(+x.ret.slice(5,7)-1)/12):2020;const U=DOKUCH[x.n]||[];
 REALB.forEach((l,i)=>{const f=l.split('|');if(f[3]!==x.par||/^[YO]$/.test(f[0]))return;const ag=realAge(f[4]);const k=KEI[f[1]];const db=DEBUT[f[1]];
  let dy;if(db&&db[0]){const p=String(db[0]).split('-');dy=+p[0]+((+p[1]||1)-1)/12;}else{const ea=k?(k[3]?22:k[4]?22:k[2]?18:15):18;dy=2026.87-ag+ea;}
  let sc=0;const tg=[];
  if(U.includes(f[1])){sc+=3;tg.push('内弟子(記事あり)');}
  if(tu&&k&&cut(k[3])&&cut(k[3])===tu){sc+=3;tg.push('同じ'+tu.replace(/大学$/,'大'));}
  if(th&&k&&cut(k[2])&&cut(k[2])===th){sc+=2;tg.push('同じ高校');}
  if(x.home&&f[2]===x.home){sc+=1;tg.push('同郷・'+x.home);}
  if(dy>=ry){sc+=1;tg.push('引退後に入門');}
  if(sc>=1)ws.push({n:f[1],rk:(f[0]?{S:'関脇',K:'小結'}[f[0]]:dokRk(i)),age:Math.floor(ag),sc:sc,tg:tg});});
 ws.sort((a,b)=>b.sc-a.sc);x._ws=ws;return ws;}
function dokGo(x,names){const L=dokWs(x).filter(w=>names.includes(w.n));const go=[],stay=[];
 L.forEach(w=>{(Math.random()<(w.sc>=3?.9:w.sc>=2?.8:.65)?go:stay).push(w.n);});
 if(!go.length&&L.length){go.push(L[0].n);stay.splice(stay.indexOf(L[0].n),1);}return {go,stay};}"""
rep(old_ws, new_ws)
rep("連れて行けるのは自分の内弟子が原則。'+esc(x.n)+'親方が引退した '+esc(x.ret||'')+' より後に入門したと考えられる力士だけを出しています(生年と学歴からの推定。学歴がわからない力士は高校卒業で入門とみなす)。</p>",
    "連れて行けるのは自分の内弟子が原則。誰が内弟子かはほとんど公表されていないので、記事で分かった内弟子と、つながり(同じ大学・同じ高校・同郷・'+esc(x.n)+'親方の引退〈'+esc(x.ret||'')+'〉の後に入門)から推定した候補を出しています。札の多い力士ほど、ついて来てくれる見込みが高くなります(内弟子でも元の部屋に残る例があります)。</p>")
rep("ws.map((w,i)=>'<label class=\"dkc\"><input type=\"checkbox\" value=\"'+esc(w.n)+'\" onchange=\"dokChk(this)\"> <b>'+esc(w.n)+'</b> <span>'+w.rk+'・'+w.age+' 歳</span></label>')",
    "ws.map((w,i)=>'<label class=\"dkc\"><input type=\"checkbox\" value=\"'+esc(w.n)+'\" onchange=\"dokChk(this)\"> <b>'+esc(w.n)+'</b> <span>'+w.rk+'・'+w.age+' 歳</span>'+w.tg.map(t=>'<em class=\"dktg\">'+esc(t)+'</em>').join('')+'</label>')")
rep("function doStartDok(n){const ws=[...document.querySelectorAll('.dkw input:checked')].map(e=>e.value);if(!ws.length)return;UI.start=null;UI.title=false;newGameDok(n,ws,$('#r_t').value);save();UI.view='home';render();}",
    "function doStartDok(n){const ws=[...document.querySelectorAll('.dkw input:checked')].map(e=>e.value);if(!ws.length)return;const x=dokList().find(y=>y.n===n);const R=x?dokGo(x,ws):{go:ws,stay:[]};UI.start=null;UI.title=false;newGameDok(n,R.go,$('#r_t').value);\n if(R.stay.length)addNews(R.stay.join('・')+'は、話し合いの末、元の'+(x?x.par:'')+'部屋に残ることになりました(内弟子でも元の部屋に残る例があります)。');save();UI.view='home';render();}")
rep('</head>', '<style>.dkw{grid-template-columns:1fr!important}.dkc{display:flex!important;align-items:center;flex-wrap:wrap;gap:2px 6px}.dkc .dktg{font-style:normal;font-size:11px;background:#c9a24a33;border:1px solid #c9a24a88;border-radius:9px;padding:0 6px;margin-left:4px;white-space:nowrap}</style></head>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
