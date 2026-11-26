# v189 -> v190:新弟子の「年の波」(実際の 2018〜2025 年の数から毎年くじ)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=189;\nconst SAVE='sumoManager189',SAVE188", "const APPV=190;\nconst SAVE='sumoManager190',SAVE189='sumoManager189',SAVE188")
rep('[SAVE188,SAVE187', '[SAVE189,SAVE188,SAVE187')
rep('<title>Grand Sumo Manager v189', '<title>Grand Sumo Manager v190')
# v190:新弟子の「年の波」。毎年、実際の 2018〜2025 年の入門者数から 1 年をくじで選び、その割合で補充の目標を上下させる(1 年目が 2026 年なら 2026 年の実際)
rep(" const need=Math.max(0,TOTAL-25-G.order.length,Math.round((TOTAL-G.order.length)*([.12,1,.9,.2,.2,.1][(G.bnum-1)%6])));",
 " nyrF();const TG=TOTAL+Math.round(G.nyr.off||0);const need=Math.max(0,TG-25-G.order.length,Math.round((TG-G.order.length)*([.12,1,.9,.2,.2,.1][(G.bnum-1)%6])));")
rep("const DAIKI_P=.014;","""/* v190:新弟子の年の波。実際の新しく登録した力士の数(協会の事業報告書):2018 74・2019 70・2020 71・2021 59・2022 78・2023 45・2024 60・2025 65。2026 年は 9 月場所まで 48 人 → 年 55 人ほど(九州場所は推定) */
const NYR={2018:74,2019:70,2020:71,2021:59,2022:78,2023:45,2024:60,2025:65};
function nyrF(){const y=curYear();if(!G.nyr||G.nyr.y!==y){let f,src;if(y===2026){f=55/65;src=2026;}else{const ks=Object.keys(NYR).map(Number).filter(k=>!G.nyr||k!==G.nyr.src);src=pick(ks);f=NYR[src]/65;}
  G.nyr={y:y,f:f,src:src,off:.5*((G.nyr&&G.nyr.off)||0)+(f-1)*65};if(G.phase)addNews(f<.85?'今年は新弟子が少ない年になりそうだと、協会の関係者は話しています。':f>1.1?'今年は入門の希望者が多く、新弟子の多い年になりそうです。':'今年の新弟子の数は、例年並みになりそうです。');}
 return G.nyr.f;}
const DAIKI_P=.014;""")
rep("if((G.bnum-1)%6===1)add(2,['春場所の前は、新弟子の話が一番多い時期です。',","if(G.nyr&&G.nyr.f<.85)add(3,['今年は新弟子が少ない年です。どこの部屋も、いい子の取り合いです。','入門の希望者が少なくて、どの部屋も苦労しているようです。']);if(G.nyr&&G.nyr.f>1.1)add(3,['今年は入門の希望者が多いと聞きます。いい子を見逃さないようにします。']);\n if((G.bnum-1)%6===1)add(2,['春場所の前は、新弟子の話が一番多い時期です。',")
rep("a.push(['協会は、今度の場所も満員御礼が続きそうだと見ています。',","if(G.nyr&&G.nyr.f<.85)a.push(['今年は新弟子が少ないですね。角界の将来を心配する声も出ています。']);if(G.nyr&&G.nyr.f>1.1)a.push(['今年は新弟子が多いそうですね。いい話題です。']);\n  a.push(['協会は、今度の場所も満員御礼が続きそうだと見ています。',")
ui = ''
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
