# 現実とのマッチング(3):決まり手の割合・部屋の入れ替わり  v29 -> v30
# 決まり手:実際は 2018 年に押し出しが全決まり手の 25.1% で、初めて寄り切りを上回った(Number)。突き落とし 年 120 件超・突き出し 79 件(2019 年、幕内の年間 約 1890 番)。
#   v29 は押し出し 22%・寄り切り 16%、蹴返し 2.8% と足技が多すぎた。足技の起こる確率を下げ、突き押しの決まり手の中で押し出し、四つの決まり手の中で寄り切りを増やした。
# 部屋:2022 年に武隈・押尾川・安治川が新設、尾車が閉鎖、2024 年に中村が新設(部屋数 44、マネーポスト)、いまは 45(文藝春秋)。年に 1 つ前後が入れ替わる。
#   v29 は新設・閉鎖とも年 0.35 ほど。独立を起こりやすくし(部屋が 46 以上なら抑える)、弟子 5 人以下の部屋の合併を少し増やした。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v29</title>', '<title>Sumo Manager v30</title>')
rep("const APPV=29;\nconst SAVE='sumoManager29',SAVE28", "const APPV=30;\nconst SAVE='sumoManager30',SAVE29='sumoManager29',SAVE28")
rep('[SAVE28,SAVE27', '[SAVE29,SAVE28,SAVE27')
rep(" if(g.v===28){g.v=29;}\n return g.v===29?g:null;}", " if(g.v===28){g.v=29;}\n if(g.v===29){g.v=30;}\n return g.v===30?g:null;}")
rep('G={v:29,', 'G={v:30,')
# 決まり手
rep("const fa=(ag>-20?1:.4)*.004+Math.max(0,E(X,'ash')-10)*.004;","const fa=(ag>-20?1:.4)*.0025+Math.max(0,E(X,'ash')-10)*.0025;")
rep("wpick([['蹴返し',2],['足取り',2],['渡し込み',1]].concat(i===1?[['蹴手繰り',1]]:[]))","wpick([['蹴返し',.4],['足取り',.6],['渡し込み',.6]].concat(i===1?[['蹴手繰り',1]]:[]))")
rep("['外掛け',3],['内掛け',3],['切り返し',2],['渡し込み',1],['河津掛け',.2],['蹴返し',1]]","['外掛け',3],['内掛け',3],['切り返し',2],['渡し込み',1],['河津掛け',.2],['蹴返し',.3]]")
rep("wpick([['押し出し',55],['突き出し',E(X,'tsk')>=13?16:5],['押し倒し',13],","wpick([['押し出し',63],['突き出し',E(X,'tsk')>=13?16:5],['押し倒し',10],")
rep("wpick([['寄り切り',62],['寄り倒し',14],","wpick([['寄り切り',80],['寄り倒し',11],")
# 部屋の入れ替わり
rep("op.forEach(i=>{const n=cnt[i]||0;const pr=(n>=16?.02:n>=12?.012:n>=9?.004:0)*(op.length<40?2:op.length<43?1:op.length<45?.4:.05);if(Math.random()<pr)spinOff(i);});",
    "op.forEach(i=>{const n=cnt[i]||0;const pr=(n>=16?.035:n>=12?.025:n>=9?.012:0)*(op.length<42?2:op.length<44?1.2:op.length<46?.5:.06);if(Math.random()<pr)spinOff(i);});")
rep("openAI().forEach(i=>{if((cnt[i]||0)<=3&&Math.random()<.04)closeHeya(i,'gappei');});","openAI().forEach(i=>{const n=cnt[i]||0;if(n<=5&&Math.random()<(n<=3?.05:.015))closeHeya(i,'gappei');});")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
