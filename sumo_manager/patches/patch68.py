# v64 -> v65:注目選手の「同期」が実在の力士で全員「同期なし」になっていた不具合を直す
# 実在の力士は初土俵(rikishi_debut.csv)から r.join を入れているが、ゲーム開始より前なので 1 以下になり、同期の判定から外れていた
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v64</title>', '<title>Sumo Manager v65</title>')
rep("const APPV=64;\nconst SAVE='sumoManager64',SAVE63", "const APPV=65;\nconst SAVE='sumoManager65',SAVE64='sumoManager64',SAVE63")
rep('[SAVE63,SAVE62', '[SAVE64,SAVE63,SAVE62')
rep(" if(g.v===63){g.v=64;}\n return g.v===64?g:null;}", " if(g.v===63){g.v=64;}\n if(g.v===64){g.v=65;}\n return g.v===65?g:null;}")
rep('G={v:64,', 'G={v:65,')
rep("x.join===r.join&&(r.join||1)>1)", "x.join===r.join&&((r.join||1)>1||(r.joinReal&&x.joinReal)))")
rep("s:'同じ場所に入門した力士がいない(記録の前に入門)'", "s:r.joinReal?'同じ場所に初土俵を踏んだ現役の力士がいない':'同じ場所に入門した力士がいない'")
# 同じ段なら競い合う(追い風)、ひとつ上の段ならふつう、段が 2 つ以上離れた(関取どうしは 12 枚以上)ときだけ焦り。
# 比べる相手は「同期のいちばん上」ではなく「すぐ上にいる同期」(ライバル)。同期が多いと、ほとんどが焦りになっていたため
rep("else{const b=dk[0];const df=r.pos-b.pos;const v=df>24?-30:df>0?20:30;",
    "else{const up=dk.filter(x=>x.pos<r.pos);const b=up.length?up[up.length-1]:dk[0];const df=r.pos-b.pos;const far=df>0&&(r.d-b.d>=2||(r.d===b.d&&df>24&&r.d<=1));const mid=df>0&&!far&&r.d!==b.d;const v=far?-30:mid?0:df>0?20:30;")
rep("t:df>40?'差をつけられ焦り':df>0?'競い合う':'同期の出世頭',s:df>24?", "t:far?'差をつけられ焦り':mid?'同期が先を行く':df>0?'競い合う':'同期の出世頭',s:mid?'同期の '+b.n+'('+G.heya[b.h].n+'・'+b.rkS+')がひとつ上の段にいる':far?")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
