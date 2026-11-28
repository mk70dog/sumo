# v213 -> v214:土俵の物語 ②(ゲームの中で生まれる物語)・③(引退のときの名場面 3 つ、殿堂の札)。部品 patches/sto217_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=213;\nconst SAVE='sumoManager213',SAVE212", "const APPV=214;\nconst SAVE='sumoManager214',SAVE213='sumoManager213',SAVE212")
rep('[SAVE212,SAVE211', '[SAVE213,SAVE212,SAVE211')
rep('<title>Grand Sumo Manager v213', '<title>Grand Sumo Manager v214')
# v213 の物語の部品:ゲームの中で物語の型が付いた力士(あと一歩の男・復活)も同じように扱う、名場面の重み
rep("function kinds(r){const D=SD[r.n];return (D&&r.real)?D.kind:{};}", "function kinds(r){const D=SD[r.n];return Object.assign({},(D&&r.real)?D.kind:{},r.stK||{});}")
rep("function sx(r,t){r.stoX=r.stoX||[];r.stoX.push({b:G.bnum,t:t});", "function sx(r,t,s){r.stoX=r.stoX||[];r.stoX.push({b:G.bnum,t:t,s:s||(/悲願/.test(t)?120:/優勝/.test(t)?100:/大関/.test(t)?90:/再入幕|復帰/.test(t)?70:/金星/.test(t)?60:/決定戦/.test(t)?55:40)});")
rep("Object.values(G.R).forEach(r=>{if(!r||r.ret||!r.real||!SD[r.n])return;const rc=B.rec[r.id];if(!rc)return;const K=kinds(r);",
    "Object.values(G.R).forEach(r=>{if(!r||r.ret||!((r.real&&SD[r.n])||r.stK))return;const rc=B.rec[r.id];if(!rc)return;const K=kinds(r);")
rep("const nc0=nextCycle;nextCycle=function(){const old={};try{Object.values(G.R).forEach(r=>{if(r&&r.real&&SD[r.n])old[r.id]=[r.d,r.t];});}catch(e){}",
    "const nc0=nextCycle;nextCycle=function(){const old={};try{Object.values(G.R).forEach(r=>{if(r&&((r.real&&SD[r.n])||r.stK))old[r.id]=[r.d,r.t];});}catch(e){}")
rep("if(K.fukkatsu&&r.d===0&&o[0]>0){pp(r,5);sx(r,'再入幕。序ノ口からはい上がり、ふたたび幕内へ');addNews(r.n+'が再入幕。脊髄の大けがで序ノ口まで落ちた男が、幕内に帰ってきました。');}",
    "if(K.fukkatsu&&r.d===0&&o[0]>0&&r.real&&SD[r.n]){pp(r,5);sx(r,'再入幕。序ノ口からはい上がり、ふたたび幕内へ');addNews(r.n+'が再入幕。脊髄の大けがで序ノ口まで落ちた男が、幕内に帰ってきました。');}\n  else if(K.fukkatsu&&r.d===0&&o[0]>0&&!r.fkM){r.fkM=1;pp(r,3);sx(r,'どん底から、ついに幕内へ');}")
rep("sx(r,'悲願の幕内初優勝。優勝次点 '+H.j+' 回、決定戦 '+H.k+' 度の涙を越えて');", "sx(r,'悲願の幕内初優勝。優勝次点 '+H.j+' 回'+(H.k?'、決定戦 '+H.k+' 度の涙':'')+'を越えて');")
# 殿堂の札に名場面
rep("sek:x.sek||null,st:x.st||[]}));", "sek:x.sek||null,st:x.st||[],mem:x.mem||null}));")
rep("st:hyNote(r),now:r.rk,id:r.id}));", "st:hyNote(r),now:r.rk,id:r.id,mem:(typeof memOf==='function'?memOf(r):null)}));")
rep("(p.act?'・現役':'・'+hyYr(p.b)+'引退')+'</div></div>';}", "(p.act?'・現役':'・'+hyYr(p.b)+'引退')+'</div>'+(p.mem&&p.mem.length?'<ol class=\"hym\">'+p.mem.map(m=>'<li>'+esc(m.t)+'</li>').join('')+'</ol>':'')+'</div>';}")
ui = open(os.path.join(here, 'sto217_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
