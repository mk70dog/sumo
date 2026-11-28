# v204 -> v205:実在の力士の「新入幕・新十両・新三役」の誤り(ゲーム前の最高位を見ていなかった)を直す。戻ったときは「再入幕」など
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=204;\nconst SAVE='sumoManager204',SAVE203", "const APPV=205;\nconst SAVE='sumoManager205',SAVE204='sumoManager204',SAVE203")
rep('[SAVE203,SAVE202', '[SAVE204,SAVE203,SAVE202')
rep('<title>Grand Sumo Manager v204', '<title>Grand Sumo Manager v205')
# 実際の最高位(r.bestS)の段階と、ゲームの中も含めて前にその段階にいたか
rep("function stMk15(r){",
 "/* v205 実際の最高位(ゲームを始める前の記録)の段階。横綱 6・大関 5・三役 4・幕内 3・十両 2 */\n"
 "function bsLv(r){const x=r&&r.bestS;if(!x)return 0;return /横綱/.test(x)?6:/大関/.test(x)?5:/関脇|小結/.test(x)?4:/前頭|幕内/.test(x)?3:/十両/.test(x)?2:1;}\n"
 "function wasLv(r,lv){return bsLv(r)>=lv||(r.hist||[]).some(h=>rankLv({t:h.t,d:h.d})>=lv);}\n"
 "const STLVR={2:'再十両',3:'再入幕',4:'三役に返り咲き',5:'大関に返り咲き'};\n"
 "function stFixReal(r){const b=bsLv(r);if(b<2||r.stFx)return;r.stFx=1;(r.sto||[]).forEach(e=>{if(e.k!=='up')return;for(let lv=2;lv<=Math.min(b,5);lv++)if(e.t.indexOf(STLV[lv]+'(')===0){e.t=STLVR[lv]+e.t.slice(STLV[lv].length);break;}});r.stB=Math.max(r.stB||1,b);r.stD=Math.min(r.stD==null?9:r.stD,b>=3?0:1);}\n"
 "function stMk15(r){")
rep("let bd=9,bl=1;H.forEach", "let bd=bsLv(r)>=3?0:bsLv(r)>=2?1:9,bl=Math.max(1,bsLv(r));H.forEach")
rep("r.stB=bl;r.stD=Math.min(bd,r.d);", "r.stB=Math.max(bl,bsLv(r));r.stD=Math.min(bd,r.d,bsLv(r)>=3?0:bsLv(r)>=2?1:9);")
rep("if(lvN>(r.stB||1)&&lvN>=2){stPush(r,'up',STLV[lvN]+'('+r.rk+')');",
 "stFixReal(r);if(lvN>lvO&&lvN>=2&&lvN<=(r.stB||1)&&STLVR[lvN]&&!(r.fall&&lvN>=r.fall.lv))stPush(r,'up',STLVR[lvN]+'('+r.rk+')');\n  if(lvN>(r.stB||1)&&lvN>=2){stPush(r,'up',STLV[lvN]+'('+r.rk+')');")
# 番付発表の知らせ
rep("msgs.push('🎌 '+r.n+'が大関に昇進!');", "msgs.push('🎌 '+r.n+(wasLv(r,5)?'が大関に復帰!':'が大関に昇進!'));")
rep("msgs.push(r.n+'が新三役('+TITLE[r.t]+')に!');", "msgs.push(r.n+(wasLv(r,4)?'が三役に返り咲き('+TITLE[r.t]+')!':'が新三役('+TITLE[r.t]+')に!'));")
rep("else if(r.d===0&&o.d>0){msgs.push(r.n+'が新入幕!');", "else if(r.d===0&&o.d>0){msgs.push(r.n+(wasLv(r,3)?'が再入幕!':'が新入幕!'));")
rep("else if(r.d===1&&o.d>1){msgs.push(r.n+'が新十両! 関取の仲間入りです。", "else if(r.d===1&&o.d>1){msgs.push(r.n+(wasLv(r,2)?'が再十両! 関取に戻りました。':'が新十両! 関取の仲間入りです。')+'")
# 読み込んだ保存データも直す
rep("G=load();\nif(G&&!G.order)G=null;", "G=load();\nif(G&&!G.order)G=null; if(G&&G.R){try{for(const id in G.R){const r=G.R[id];if(r&&r.sto)stFixReal(r);}}catch(e){}}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
