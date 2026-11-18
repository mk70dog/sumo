# 土俵の動きを取組の計算とつなぐ  v52 -> v53
# fight() で、見せる取組(nar がある取組)だけ出来事の記録 ev を残す(乱数は使わないので勝ち負けは前と同じ)。
# 動きは ev から作る:押し合いの値 p の動き=2 人の位置、組み手(突き押し/四つ・差し手・もろ差し)、引き・投げ・足技の失敗、土俵際の逆転、勇み足、長い相撲。
# 横に出る実況は「取組の様子」の文章そのもの(出来事の時に 1 行ずつ)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v52</title>', '<title>Sumo Manager v53</title>')
rep("const APPV=52;\nconst SAVE='sumoManager52',SAVE51", "const APPV=53;\nconst SAVE='sumoManager53',SAVE52='sumoManager52',SAVE51")
rep('[SAVE51,SAVE50', '[SAVE52,SAVE51,SAVE50')
rep(" if(g.v===51){g.v=52;}\n return g.v===52?g:null;}", " if(g.v===51){g.v=52;}\n if(g.v===52){g.v=53;}\n return g.v===53?g:null;}")
rep('G={v:52,', 'G={v:53,')
# --- fight: event log
rep(" const nar=ctx.nar?[]:null;const N=s=>{if(nar)nar.push(s);};",
    " const nar=ctx.nar?[]:null;const N=s=>{if(nar)nar.push(s);};const ev=nar?[]:null;const V=o=>{if(ev){o.n=nar.length;ev.push(o);}};")
rep("const fin=(wi,k,x)=>({w:S[wi],l:S[1-wi],wi:wi,k:k,nar:nar,hv:x==='hv',hard:x==='hard'});",
    "const fin=(wi,k,x)=>({w:S[wi],l:S[1-wi],wi:wi,k:k,nar:nar,ev:ev,hv:x==='hv',hard:x==='hard'});")
rep("N(Y.n+'は前のめりになり、そのまま'+k+'。あっけない一番。');return fin(x,k,'hv');}",
    "N(Y.n+'は前のめりになり、そのまま'+k+'。あっけない一番。');V({e:'henka',x,ok:1});return fin(x,k,'hv');}")
rep("N('立ち合い、'+X.n+'が変化。しかし'+Y.n+'は落ち着いて見ていた。');p+=(x===0?-1:1)*60;behind[y]=true;",
    "N('立ち合い、'+X.n+'が変化。しかし'+Y.n+'は落ち着いて見ていた。');p+=(x===0?-1:1)*60;behind[y]=true;V({e:'henka',x,ok:0,p});")
rep("if(Math.abs(p)<15)N('立ち合いは五分。');else{const x=p>0?0:1;N(S[x].n+(Math.abs(p)>35?'が鋭い踏み込みで一気に押し込む。':'が当たり勝った。'));}}",
    "if(Math.abs(p)<15)N('立ち合いは五分。');else{const x=p>0?0:1;N(S[x].n+(Math.abs(p)>35?'が鋭い踏み込みで一気に押し込む。':'が当たり勝った。'));}}\n V({e:'tachi',p});")
rep(" // 攻防\n let said=0;", " V({e:'form',f:form,g:q[0]>q[1]?0:q[1]>q[0]?1:-1,moro:q[0]>=1.5?0:q[1]>=1.5?1:-1});\n // 攻防\n let said=0;")
rep("N(Y.n+'が出てくるところ、'+X.n+'がタイミングよく体を開く。'+k+'!');return fin(j,k);}",
    "N(Y.n+'が出てくるところ、'+X.n+'がタイミングよく体を開く。'+k+'!');V({e:'hiki',x:j,ok:1});return fin(j,k);}")
rep("N(X.n+'が引いたが、'+Y.n+'はよく見てついていく。');p+=sg*45;","N(X.n+'が引いたが、'+Y.n+'はよく見てついていく。');p+=sg*45;V({e:'hiki',x:j,ok:0,p});")
rep("N(X.n+'が豪快な'+k+'! '+Y.n+'の体が土俵に転がった。');return fin(j,k,'hard');}",
    "N(X.n+'が豪快な'+k+'! '+Y.n+'の体が土俵に転がった。');V({e:'nage',x:j,ok:1});return fin(j,k,'hard');}")
rep("N(X.n+'の投げは'+Y.n+'に残された。');p+=sg*30;","N(X.n+'の投げは'+Y.n+'に残された。');p+=sg*30;V({e:'nage',x:j,ok:0,p});")
rep("N(X.n+'の足が飛んだ。'+k+'が決まった!');return fin(j,k,'hard');}","N(X.n+'の足が飛んだ。'+k+'が決まった!');V({e:'ashi',x:j,ok:1});return fin(j,k,'hard');}")
rep("N(X.n+'が足を飛ばすが、'+Y.n+'は崩れない。');p+=sg*25;","N(X.n+'が足を飛ばすが、'+Y.n+'は崩れない。');p+=sg*25;V({e:'ashi',x:j,ok:0,p});")
rep("if(ag>60&&Math.random()<.004){N(X.n+'は残そうとしたが、腰から崩れ落ちた。');return fin(1-j,'腰砕け');}","if(ag>60&&Math.random()<.004){N(X.n+'は残そうとしたが、腰から崩れ落ちた。');V({e:'koshi',x:j});return fin(1-j,'腰砕け');}")
rep("  p+=BE.k*d+randn()*BE.sd;\n", "  p+=BE.k*d+randn()*BE.sd;const vI=ev?ev.length:0;\n")
rep("   const x=p>0?0:1,y=1-x,X=S[x],Y=S[y];\n   if(Math.random()<.012){N(X.n+'が土俵際まで攻め込んだが、先に足が出てしまった。');return fin(y,'勇み足');}",
    "   const x=p>0?0:1,y=1-x,X=S[x],Y=S[y];if(ev)ev.splice(vI,0,{e:'r',p:Math.max(-100,Math.min(100,p)),n:nar.length});\n   if(Math.random()<.012){N(X.n+'が土俵際まで攻め込んだが、先に足が出てしまった。');V({e:'isami',x});return fin(y,'勇み足');}")
rep("N('土俵際、俵に足のかかった'+Y.n+'が逆転の'+k+'!');return fin(y,k,'hard');}","N('土俵際、俵に足のかかった'+Y.n+'が逆転の'+k+'!');V({e:'rev',x:y});return fin(y,k,'hard');}")
rep("   N(X.n+'が'+(form==='O'?'一気に押して':'寄り立てて')+'、'+k+'。');\n   return fin(x,k,/倒し/.test(k)?'hard':'');\n  }\n }",
    "   N(X.n+'が'+(form==='O'?'一気に押して':'寄り立てて')+'、'+k+'。');V({e:'out',x});\n   return fin(x,k,/倒し/.test(k)?'hard':'');\n  }\n  if(ev)ev.push({e:'r',p,n:nar.length});\n }")
rep(" const x=p>=0?0:1;N('長い相撲になった。最後は疲れの見えた'+S[1-x].n+'を、'+S[x].n+'が攻め切った。');",
    " const x=p>=0?0:1;N('長い相撲になった。最後は疲れの見えた'+S[1-x].n+'を、'+S[x].n+'が攻め切った。');V({e:'long',x});")
rep(" return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,big:ctx.big};", " return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,ev:f.ev,a:a,big:ctx.big};")
ui = open(os.path.join(here,'dohyo59_ui.js'),encoding='utf-8').read()
rep("function dhRun(id,b){const p=dhPick(b);const pl=dhPlan(b.k,p.winE,dhSeed(b),p.E.n,p.Wt.n);", ui+"\nfunction dhRun(id,b){const p=dhPick(b);const pl=(b.ev&&b.ev.length?dhPlanEv(b,p):null)||dhPlan(b.k,p.winE,dhSeed(b),p.E.n,p.Wt.n);")
# grip from plan
rep("const gW=.16+rnd()*.15,gL=rnd()<.5?.2+rnd()*.25:9;const gripE=pl.winE?gW:gL,gripW=pl.winE?gL:gW;",
    "const gW=.16+rnd()*.15,gL=rnd()<.5?.2+rnd()*.25:9;let gripE=pl.winE?gW:gL,gripW=pl.winE?gL:gW;if(pl.grip){gripE=pl.grip[0];gripW=pl.grip[1];}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
