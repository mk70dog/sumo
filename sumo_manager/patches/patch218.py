# v214 -> v215:実在の力士の物語を 4 人足す(宇良・朝乃山・尊富士・安青錦。data/story2026.txt)、復活の文を力士ごとに、
#   引退のまどのボタンを「OK」に(v86 の決まり)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=214;\nconst SAVE='sumoManager214',SAVE213", "const APPV=215;\nconst SAVE='sumoManager215',SAVE214='sumoManager214',SAVE213")
rep('[SAVE213,SAVE212', '[SAVE214,SAVE213,SAVE212')
rep('<title>Grand Sumo Manager v214', '<title>Grand Sumo Manager v215')
D = {}
for l in open(os.path.join(here, '..', 'data', 'story2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.rstrip('\n').split('|'); n = a[0]
    d = D.setdefault(n, {'sum': '', 'kind': {}, 'ev': []})
    if a[1] == 'まとめ': d['sum'] = a[2]
    elif a[1] == '型': d['kind'][a[2]] = [int(x) if x.isdigit() else x for x in a[3:]] or [1]
    else: d['ev'].append([a[1], a[2], a[3] if len(a) > 3 else ''])
i = s.index('<script>window.STORYD='); j = s.index(';\n', i)
s = s[:i] + '<script>window.STORYD=' + json.dumps(D, ensure_ascii=False) + s[j:]
rep("const STORYP={\"炎鵬\":16,\"王鵬\":6,\"高安\":3};", "const STORYP={\"炎鵬\":16,\"王鵬\":6,\"高安\":3,\"尊富士\":6};")
rep("if(r.real&&!r.stP){r.stP=1;if(STORYP[r.n])r.pop=cl((r.pop||20)+STORYP[r.n],0,100);}", "if(r.real&&!r.stP){r.stP=1;r.stP2=1;if(STORYP[r.n])r.pop=cl((r.pop||20)+STORYP[r.n],0,100);}else if(r.real&&!r.stP2){r.stP2=1;if(r.n==='尊富士')r.pop=cl((r.pop||20)+6,0,100);}")
rep("function realTraits(r,t,i){r.real=1;r.stP=1;", "function realTraits(r,t,i){r.real=1;r.stP=1;r.stP2=1;")
# 復活の文を力士ごとに
rep("if(K.fukkatsu&&r.d===0&&o[0]>0&&r.real&&SD[r.n]){pp(r,5);sx(r,'再入幕。序ノ口からはい上がり、ふたたび幕内へ');addNews(r.n+'が再入幕。脊髄の大けがで序ノ口まで落ちた男が、幕内に帰ってきました。');}",
    "if(K.fukkatsu&&r.d===0&&o[0]>0&&r.real&&SD[r.n]){const fw=typeof K.fukkatsu[0]==='string'?K.fukkatsu[0]:'どん底まで落ちた';pp(r,5);sx(r,'再入幕。'+fw+'ところからはい上がり、ふたたび幕内へ');addNews(r.n+'が再入幕。'+fw+'男が、幕内に帰ってきました。');}")
rep("addNews(r.n+'が十両優勝。序ノ口からはい上がった男に、大きな拍手が送られました。');", "addNews(r.n+'が十両優勝。'+(typeof K.fukkatsu[0]==='string'?K.fukkatsu[0]:'どん底まで落ちた')+'男に、大きな拍手が送られました。');")
rep('<button class="btn main" onclick="closeM()">お疲れさまでした</button>', '<button class="btn main" onclick="closeM()">OK</button>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '物語', len(D), '人')
