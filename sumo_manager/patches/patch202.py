# v198 -> v199:親方の返事を相手の立場と話で変える
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=198;\nconst SAVE='sumoManager198',SAVE197", "const APPV=199;\nconst SAVE='sumoManager199',SAVE198='sumoManager198',SAVE197")
rep('[SAVE197,SAVE196', '[SAVE198,SAVE197,SAVE196')
rep('<title>Grand Sumo Manager v198', '<title>Grand Sumo Manager v199')

# v199:親方の返事を相手で変える
rep("const rep=/痛|けが/.test(ln)?'焦るな。治してからが勝負だ。':/新弟子/.test(ln)?'いい子がいたら、まず会ってみよう。':/疲れ/.test(ln)?'少し軽めにするか。体が資本だからな。':/雰囲気|元気/.test(ln)?'稽古場の空気は、上の者が作るものだ。':/調子|好調|動け/.test(ln)?'その調子だ。気を抜くなよ。':'わかった。頼むぞ。';","const rep=cvReply(a,ln,sd);")
rep("function cvPick(a,s){",open(os.path.join(here,'cvr199.js'),encoding='utf-8').read()+"function cvPick(a,s){")
rep("function weekDots(){return '<div class=\"daybar\">'+Array.from({length:WEEKS},(_,i)=>'<i class=\"'+(i<G.wk-1?'d':'')+'\"></i>').join('')+'</div>';}","function weekDots(){return '<div class=\"daybar\" title=\"場所までの稽古の '+WEEKS+' 週。済んだ週が赤、今の週が金の枠\">'+Array.from({length:WEEKS},(_,i)=>'<i class=\"'+(i<G.wk-1?'d':i===G.wk-1?'now':'')+'\"></i>').join('')+'</div>';}")
rep("if((r.hist||[]).length<=2)add(3,","if((r.hist||[]).length<=2&&r.d>=3&&r.age<23)add(3,")
ui = '<style>/* v199:場所までの週の帯(漆黒の画面で済んだ週の色が出ていなかった) */body .daybar i.d{background:var(--shu,#b5361f)!important}body .daybar i.now{box-shadow:inset 0 0 0 2px var(--kin,#c9a24a)}</style>\n'

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
