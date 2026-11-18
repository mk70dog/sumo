# 実在の部屋ごとに始めの施設を変える  v40 -> v41
# 資料で確かめた 7 部屋は実際に合わせ、ほかは関取の数・お金の多さ・弟子の数から推定(推定と明記)。
#  二所ノ関:土俵 2 面・敷地 1800 坪の自前の建物(Number 2021/11/13・2022/6/27) → 稽古場 3・宿舎 5・持ち家
#  伊勢ヶ濱:元倉庫を仮の稽古場(週刊女性PRIME 2026、新部屋は 2028 年完成予定) → 稽古場 1・借りもの
#  中村:旧陸奥部屋の建屋を借り受け、1 日 3 食・酸素カプセル(文藝春秋・Number 2025/7/10) → 食堂 3・医務室 2・借りもの
#  音羽山:区が売った会館を直した賃貸の部屋(墨田区 2024/2/8) → 借りもの
#  押尾川:上の階が賃貸マンションの建物の下層階(東洋経済) → 借りもの
#  秀ノ山:2024 年 11 月に東向島に部屋の建物が完成(東京スポーツ) → 持ち家
#  時津風:双葉山の道場がルーツ、両国(さんたつ) → 持ち家
# 推定:稽古場 1(+関取 3 人以上で 1・6 人以上でさらに 1)、医務室・食堂は資金力 S・A なら 2(ほか 1)、宿舎は弟子が入る段階(2〜5)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v40</title>', '<title>Sumo Manager v41</title>')
rep("const APPV=40;\nconst SAVE='sumoManager40',SAVE39", "const APPV=41;\nconst SAVE='sumoManager41',SAVE40='sumoManager40',SAVE39")
rep('[SAVE39,SAVE38', '[SAVE40,SAVE39,SAVE38')
rep(" if(g.v===39){g.v=40;}\n return g.v===40?g:null;}", " if(g.v===39){g.v=40;}\n if(g.v===40){g.v=41;}\n return g.v===41?g:null;}")
rep('G={v:40,', 'G={v:41,')
rep("function heyaSheet(n){",
    "const FACV={'二所ノ関':{keiko:3,shuku:5,bld:'own'},'伊勢ヶ濱':{keiko:1,bld:'rent'},'中村':{shoku:3,iryo:2,bld:'rent'},'音羽山':{bld:'rent'},'押尾川':{bld:'rent'},'秀ノ山':{bld:'own'},'時津風':{bld:'own'}};\n"
    "function realFac(n,sek,cnt,fr,age){const ri=fr==='S'||fr==='A';const f={keiko:Math.min(5,1+(sek>=3?1:0)+(sek>=6?1:0)),iryo:ri?2:1,shoku:ri?2:1,shuku:Math.min(5,Math.max(2,Math.ceil((cnt-4)/3)))};let b=(age||40)>=50?'own':'rent';const v=FACV[n];if(v){for(const k in v)if(k!=='bld')f[k]=v[k];if(v.bld)b=v.bld;}return {f:f,b:b,src:!!v};}\n"
    "function heyaSheet(n){")
rep("(x.loc?'<dt>場所</dt><dd>'+esc(x.loc)+'</dd>':'')",
    "(()=>{const q=realFac(x.n,x.sk,x.c,x.fr,x.age);return '<dt>施設</dt><dd>稽古場 '+q.f.keiko+'・医務室 '+q.f.iryo+'・食堂 '+q.f.shoku+'・宿舎 '+q.f.shuku+' / '+(q.b==='own'?'持ち家':'借りもの')+(q.src?'(資料あり)':'(推定)')+'</dd>';})()+(x.loc?'<dt>場所</dt><dd>'+esc(x.loc)+'</dd>':'')")
rep("G.fac.shuku=3;G.capB=Math.max(0,o.length+3-(4+3*G.fac.shuku));",
    "const hl0=heyaList().find(x=>x.n===hn)||{fr:'B'};const rf=realFac(hn,sek,o.length,hl0.fr,me().age);G.fac=Object.assign({},rf.f);G.capB=Math.max(0,o.length+3-(4+3*G.fac.shuku));")
rep("G.bld={k:(me().age||40)>=50?'own':'rent'};", "G.bld={k:rf.b};")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
