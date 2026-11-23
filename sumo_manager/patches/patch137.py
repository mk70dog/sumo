# v133 -> v134:v127〜v133 で増えた信頼の上ぶれを直す(総点検)。目標の達成で信頼 +4 → +2、届かず −1 → −2、世話人の信頼 +0.2 → +0.1/場所/人。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=133;\nconst SAVE='sumoManager133',SAVE132", "const APPV=134;\nconst SAVE='sumoManager134',SAVE133='sumoManager133',SAVE132")
rep('[SAVE132,SAVE131', '[SAVE133,SAVE132,SAVE131')
rep('<title>Grand Sumo Manager v133', '<title>Grand Sumo Manager v134')
rep("if(res>0){r.mor=cl(r.mor+10,0,100);r.tr=cl((r.tr==null?50:r.tr)+4,0,100);", "if(res>0){r.mor=cl(r.mor+10,0,100);r.tr=cl((r.tr==null?50:r.tr)+2,0,100);")
rep("else{r.mor=cl(r.mor-4,0,100);r.tr=cl((r.tr==null?50:r.tr)-1,0,100);", "else{r.mor=cl(r.mor-4,0,100);r.tr=cl((r.tr==null?50:r.tr)-2,0,100);")
rep("届けば 気力 +10・信頼 +4、届かなければ 気力 −4・信頼 −1(推定)", "届けば 気力 +10・信頼 +2、届かなければ 気力 −4・信頼 −2(推定)")
rep("r.tr=cl((r.tr==null?50:r.tr)+.2*G.sewa.length,0,100);", "r.tr=cl((r.tr==null?50:r.tr)+.1*G.sewa.length,0,100);")
rep("幕下以下の気力・信頼が少しずつ上がる。推定", "幕下以下の気力・信頼が少しずつ上がる(信頼 +0.1/場所)。推定")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
