# v96 -> v97:素質のひとこと(力士の札)の言い方を、今の番付と年齢に合わせる(ダルマさん「大物になる器/正直上は厳しい が多すぎ」)
# v96 までは素質の見立て sp だけで 5 段階(17 逸材・15 大物・13 関取は十分・10.5 地道に・それ未満「正直、上は厳しい」)。
# 実在スタート 8 部屋 177 人で「正直、上は厳しい」49 人(序二段だけで 27 人)、「大物になる器」8 人(全員幕下)。
# 直し:段(関取/幕下/三段目以下)ごとに目標を変え、言い方を 2 つずつ用意(力士ごとに決まる)。「上は厳しい」は 22 歳以上で見立てが低いときだけ。数字は推定。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v96</title>', '<title>Grand Sumo Manager v97</title>')
rep("const APPV=96;\nconst SAVE='sumoManager96',SAVE95", "const APPV=97;\nconst SAVE='sumoManager97',SAVE96='sumoManager96',SAVE95")
rep('[SAVE95,SAVE94', '[SAVE96,SAVE95,SAVE94')
rep(" if(g.v===95){g.v=96;}\n return g.v===96?g:null;}", " if(g.v===95){g.v=96;}\n if(g.v===96){g.v=97;}\n return g.v===97?g:null;}")
rep('G={v:96,', 'G={v:97,')
rep(" else if(sp>=17)L.push(['かなりの逸材です','s']);else if(sp>=15)L.push(['大物になる器です','s']);else if(sp>=13)L.push(['関取は十分に狙えます','g']);else if(sp>=10.5)L.push(['地道にやれば番付は上がります','n']);else L.push(['正直、上は厳しいかもしれません','m']);",
    " else L.push(potWord(r,sp));")
rep("function keyCom(r){", """/* v97:素質のひとこと。今の段と年齢で目標を変え、言い方は 2 つずつ(力士ごとに決まる)。しきい値は推定 */
function potWord(r,sp){const v=x=>x[hhR(r.id,7)<.5?0:1];const d=r.d;
 if(d<=1){if(sp>=17.5)return [v(['横綱・大関も夢ではありません','まだまだ上を狙える器です']),'s'];if(sp>=16)return [v(['三役を狙える力があります','上位でも十分に戦えます']),'s'];if(sp>=14.5)return [v(['幕内に定着できる力です','関取として伸びる余地があります']),'g'];return [v(['関取の座を守るのが目標です','今の地位で踏ん張りどころです']),'n'];}
 if(d===2){if(sp>=17)return [v(['かなりの逸材です','幕内上位まで行ける器です']),'s'];if(sp>=15.5)return [v(['大物になる器です','十両はすぐそこです']),'s'];if(sp>=13.5)return [v(['関取は十分に狙えます','関取が見えてきました']),'g'];if(sp>=11.5)return [v(['関取まであと一歩、伸び方しだいです','幕下上位を目指せます']),'n'];return [v(['幕下で力をつけるのが先です','幕下に定着するのが目標です']),'n'];}
 if(sp>=16)return [v(['かなりの逸材です','将来が楽しみな器です']),'s'];if(sp>=14)return [v(['将来の関取候補です','いずれ関取を狙えそうです']),'g'];if(sp>=12)return [v(['幕下までは行けそうです','稽古しだいで幕下が見えます']),'g'];
 if(sp>=10||r.age<22)return [v(['地道にやれば番付は上がります',r.age<22?'まだ体ができていません。気長に見ます':'こつこつ番付を上げていきましょう']),'n'];
 return [v(['正直、上は厳しいかもしれません','今の段で踏ん張るのが目標です']),'m'];}
function keyCom(r){""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
