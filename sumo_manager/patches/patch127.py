# v123 -> v124:優勝の割合を実際に近づける(ダルマさん「続ける」→ 測定と設計案 →「続ける」)。
# 大関の番付の力 +0.2% → −0.6%(大関の地位の重圧)、大関取りの勢い +3.5% → +5.5%。どちらも推定。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=123;\nconst SAVE='sumoManager123',SAVE122", "const APPV=124;\nconst SAVE='sumoManager124',SAVE123='sumoManager123',SAVE122")
rep('[SAVE122,SAVE121', '[SAVE123,SAVE122,SAVE121')
rep('<title>Grand Sumo Manager v123', '<title>Grand Sumo Manager v124')
rep("const BZ={Y:.004,O:.002,S:.008,K:.006};", "const BZ={Y:.004,O:-.006,S:.008,K:.006};")
rep("const SKI={v:.035,w:9,a:28};", "const SKI={v:.055,w:9,a:28};")
# 大関の番付の力がマイナス(重圧)のとき、性格・場所数の効き方を逆向きにする(豪快など=重圧を感じにくい、繊細・新大関=重圧が大きい)
rep(" return {v:base*cl(m,-.6,1.8)+ik,base,ten,note:L.join('・')};}",
    " if(base<0){m=cl(2-m,.2,2.4);for(let i=0;i<L.length;i++)L[i]=L[i].replace('で自信になりやすい','で重圧を感じにくい');return {v:base*m+ik,base,ten,note:L.join('・')};}\n return {v:base*cl(m,-.6,1.8)+ik,base,ten,note:L.join('・')};}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
