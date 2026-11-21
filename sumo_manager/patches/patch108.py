# v104 -> v105:若い実力者が番付より先に強くなる(ダルマさん「『若い実力者が番付より先に強くなる』案を実施」)
# 実際の三役の優勝は、のちの大関・横綱が関脇・小結のうちに勝つ形が多い(貴景勝・正代・照ノ富士・御嶽海・若隆景・霧馬山・豊昇龍・大の里・安青錦など)。
# ゲームは三役の優勝が少ない(15 年・8 シードで 11.9%、実際 22%)。
# 試してやめた案:三役・前頭 4 枚目以内の若い素質の高い力士の伸びを 1.5 倍 → すぐ大関・横綱に上がってしまい、横綱の優勝 50.5→55.4%、三役 11.9→11.5%。
# 入れた案:「大関取りの勢い」。三役で、若く(SKI.a 歳以下)、前の場所に幕内で SKI.w 勝以上した力士は、その場所だけ力が SKI.v 上がる(番付の力 bzf に足す)。
#   強さそのもの(伸びしろ)は変えないので、勝つのは三役のあいだ(大関に上がれば消える)。数字は推定(測定で合わせた)。
import sys
src, dst = sys.argv[1], sys.argv[2]
v, w, a = (sys.argv[3:6] if len(sys.argv) >= 6 else ['.035', '9', '28'])
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v104</title>', '<title>Grand Sumo Manager v105</title>')
rep("const APPV=104;\nconst SAVE='sumoManager104',SAVE103", "const APPV=105;\nconst SAVE='sumoManager105',SAVE104='sumoManager104',SAVE103")
rep('[SAVE103,SAVE102', '[SAVE104,SAVE103,SAVE102')
rep(" if(g.v===103){g.v=104;}\n return g.v===104?g:null;}", " if(g.v===103){g.v=104;}\n if(g.v===104){g.v=105;}\n return g.v===105?g:null;}")
rep('G={v:104,', 'G={v:105,')
rep("const BZ={Y:.004,O:.002,S:.008,K:.006};", "const BZ={Y:.004,O:.002,S:.008,K:.006};\n/* v105:大関取りの勢い(若い三役が前の場所に幕内で好成績なら、その場所だけ力が上がる。推定) */\nconst SKI={v:%s,w:%s,a:%s};" % (v, w, a))
rep(" if(ten===0)L.unshift('新'+(g==='Y'?'横綱':g==='O'?'大関':'三役')+'の場所');\n return {v:base*cl(m,-.6,1.8),base,ten,note:L.join('・')};}",
    " if(ten===0)L.unshift('新'+(g==='Y'?'横綱':g==='O'?'大関':'三役')+'の場所');\n let ik=0;{const lh=h[h.length-1];if(g==='SK'&&r.age<=SKI.a&&lh&&lh.d===0&&lh.w>=SKI.w){ik=SKI.v;L.push('大関取りの勢い');}}\n return {v:base*cl(m,-.6,1.8)+ik,base,ten,note:L.join('・')};}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, v, w, a)
