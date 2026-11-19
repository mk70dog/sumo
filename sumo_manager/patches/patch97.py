# v93 -> v94:独立する親方の一覧に、連れて行ける内弟子がいない親方が出ていて選べなかった(ダルマさんの写真:大山親方〈2025-05 引退〉は候補 0 人)
# 内弟子の候補を数える部品 dokWs(x) に分け、候補が 1 人もいない親方は一覧に出さない。カードに「内弟子の候補 ○ 人」。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v93</title>', '<title>Grand Sumo Manager v94</title>')
rep("const APPV=93;\nconst SAVE='sumoManager93',SAVE92", "const APPV=94;\nconst SAVE='sumoManager94',SAVE93='sumoManager93',SAVE92")
rep('[SAVE92,SAVE91', '[SAVE93,SAVE92,SAVE91')
rep(" if(g.v===92){g.v=93;}\n return g.v===93?g:null;}", " if(g.v===92){g.v=93;}\n if(g.v===93){g.v=94;}\n return g.v===94?g:null;}")
rep('G={v:93,', 'G={v:94,')
rep("function dokSheet(n){const x=dokList().find(y=>y.n===n);if(!x)return;const ws=[];REALB.forEach((l,i)=>{const f=l.split('|');const ry=x.ret?(+x.ret.slice(0,4)+(+x.ret.slice(5,7)-1)/12):2020;const ag=realAge(f[4]);const k=KEI[f[1]];const ea=k?(k[3]?22:k[4]?22:k[2]?18:15):18;const dy=2026.87-ag+ea;if(f[3]===x.par&&!/^[YO]$/.test(f[0])&&dy>=ry)ws.push({n:f[1],rk:(f[0]?{S:'関脇',K:'小結'}[f[0]]:dokRk(i)),age:Math.floor(ag)});});",
    "function dokWs(x){if(x._ws)return x._ws;const ws=[];REALB.forEach((l,i)=>{const f=l.split('|');const ry=x.ret?(+x.ret.slice(0,4)+(+x.ret.slice(5,7)-1)/12):2020;const ag=realAge(f[4]);const k=KEI[f[1]];const ea=k?(k[3]?22:k[4]?22:k[2]?18:15):18;const dy=2026.87-ag+ea;if(f[3]===x.par&&!/^[YO]$/.test(f[0])&&dy>=ry)ws.push({n:f[1],rk:(f[0]?{S:'関脇',K:'小結'}[f[0]]:dokRk(i)),age:Math.floor(ag)});});x._ws=ws;return ws;}\nfunction dokOK(){return dokList().filter(x=>dokWs(x).length>0);}\nfunction dokSheet(n){const x=dokList().find(y=>y.n===n);if(!x)return;const ws=dokWs(x);")
rep("function dokHTML(){if(!UI.dk)UI.dk={fi:-1};const fi=UI.dk.fi;const L=dokList().filter(x=>fi<0||x.ic===fi);",
    "function dokHTML(){if(!UI.dk)UI.dk={fi:-1};const fi=UI.dk.fi;const L=dokOK().filter(x=>fi<0||x.ic===fi);")
rep("定年前の親方('+dokList().length+' 人)から選びます", "定年前の親方のうち、連れて行ける内弟子の候補がいる '+dokOK().length+' 人から選びます")
rep("<div class=\"s\">いま '+esc(x.par)+'部屋の部屋付き親方</div></button>", "<div class=\"s\">いま '+esc(x.par)+'部屋の部屋付き親方・内弟子の候補 '+dokWs(x).length+' 人</div></button>")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
