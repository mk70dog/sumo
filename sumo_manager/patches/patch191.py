# v187 -> v188:部屋の声に弟子・スタッフ・まわりの人(記者・後援会・床山・呼出・近所・学校・一門)。新弟子の候補に話の中身。メディアの言い回しを増やす
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=187;\nconst SAVE='sumoManager187',SAVE186", "const APPV=188;\nconst SAVE='sumoManager188',SAVE187='sumoManager187',SAVE186")
rep('[SAVE186,SAVE185', '[SAVE187,SAVE186,SAVE185')
rep('<title>Grand Sumo Manager v187', '<title>Grand Sumo Manager v188')
# メディアの言い回し(v188)
rep("mAdd(S,r.n+'('+mHN(r)+'・'+r.rkS+')、'+(r.inj?r.inj.p:pick(['右ひざ','左足首','腰','右肩','左ひじ']))+'のけがで次の場所は休場の見込み。',",
 "{const N=r.n+'('+mHN(r)+'・'+r.rkS+')',Pp=(r.inj?r.inj.p:pick(['右ひざ','左足首','腰','右肩','左ひじ']));mAdd(S,pick([N+'、'+Pp+'のけがで次の場所は休場の見込み。',N+'が'+Pp+'を痛め、稽古を休んでいる。出場は微妙か。',N+'、'+Pp+'に不安。関係者は「次の場所は厳しい」。',N+'が'+Pp+'の治療に専念。部屋は出場について明言を避けた。']),")
rep("{k:'kyu',id:r.id,b:G.bnum});}","{k:'kyu',id:r.id,b:G.bnum});}}")
rep("mAdd(S,r.n+'('+mHN(r)+'・'+Math.floor(r.age)+' 歳)、近く引退か。周囲に「体が限界」ともらす。',",
 "mAdd(S,pick([r.n+'('+mHN(r)+'・'+Math.floor(r.age)+' 歳)、近く引退か。周囲に「体が限界」ともらす。',r.n+'('+mHN(r)+'・'+Math.floor(r.age)+' 歳)に引退の気配。年寄名跡の準備を進めているとの話も。',r.n+'('+Math.floor(r.age)+' 歳)、「次の場所が最後かも」と親しい人に話したという。']),")
rep("mAdd(S,mHN(r)+'の'+r.n+'('+Math.floor(r.age)+' 歳・'+r.rkS+')、稽古場で兄弟子を圧倒。将来の関取候補との声。',",
 "mAdd(S,pick([mHN(r)+'の'+r.n+'('+Math.floor(r.age)+' 歳・'+r.rkS+')、稽古場で兄弟子を圧倒。将来の関取候補との声。',mHN(r)+'の若手 '+r.n+'('+Math.floor(r.age)+' 歳)、出稽古先の関取とも互角に取ったという。',r.n+'('+mHN(r)+'・'+Math.floor(r.age)+' 歳)、師匠が「この子は伸びる」と期待を口にした。']),")
rep("mAdd(S,schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)、卒業後は'+(c?'大相撲入りへ。':(a.kind==='高'?'大学に進んで相撲を続ける見込み。':'角界には進まない見込み。')),",
 "mAdd(S,schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)'+(c?pick(['、卒業後は大相撲入りへ。','、複数の部屋が勧誘。本人は角界入りに前向き。','が卒業後のプロ入りを決意したもよう。']):pick([a.kind==='高'?'、卒業後は大学に進んで相撲を続ける見込み。':'、卒業後は角界には進まない見込み。',a.kind==='高'?'、大学の推薦の話が進んでいるという。':'、一般企業への就職が決まったもよう。'])),")
rep("mAdd(S,(S==='loc'?'近所の':'')+schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)は伸びる。全国大会でも上位に入る力がある。',",
 "mAdd(S,(S==='loc'?'近所の':'')+schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)'+pick(['は伸びる。全国大会でも上位に入る力がある。','、この一年で見違えるほど強くなったという。','、監督が「全国で上位を狙える」と話している。']),")
rep(open(os.path.join(here, 'koe187.js'), encoding='utf-8').read(), open(os.path.join(here, 'koe188.js'), encoding='utf-8').read())
ui = ''
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
