# v136 -> v137:保存の直し(ダルマさん「途中からが書きかわらない」)。前の版の保存がたまって iPad の保存の上限を超え、保存が黙って失敗していた。
# 保存を縮め(LZW、patches/lz137_core.js)、保存できたら前の版の保存を消す。失敗したら知らせる。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=136;\nconst SAVE='sumoManager136',SAVE135", "const APPV=137;\nconst SAVE='sumoManager137',SAVE136='sumoManager136',SAVE135")
rep('[SAVE135,SAVE134', '[SAVE136,SAVE135,SAVE134')
rep('<title>Grand Sumo Manager v136', '<title>Grand Sumo Manager v137')
core = open(os.path.join(here, 'lz137_core.js'), encoding='utf-8').read()
rep("function saveStr(){", core + "function saveStr(){")
rep("function save(){try{localStorage.setItem(SAVE,saveStr());}catch(e){}}", "function save(){try{lsPut(SAVE,saveStr());}catch(e){}}")
rep("let s=localStorage.getItem(SAVE);if(s)return JSON.parse(s);", "let s=lsGet(SAVE);if(s)return JSON.parse(s);")
rep("s=localStorage.getItem(k);if(s){const g=migrate", "s=lsGet(k);if(s){const g=migrate")
rep("try{localStorage.setItem('gsmMP',saveStr());}catch(e){}", "try{lsPut('gsmMP',saveStr());}catch(e){}")
rep("const s=localStorage.getItem('gsmMP');if(!s)return;const g=migrate", "const s=lsGet('gsmMP');if(!s)return;const g=migrate")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
