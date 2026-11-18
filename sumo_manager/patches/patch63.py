# 部屋を支える人(見本 sup2):後援会長・タニマチ・かかりつけ医・師匠の家族  v59 -> v60
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v59</title>', '<title>Sumo Manager v60</title>')
rep("const APPV=59;\nconst SAVE='sumoManager59',SAVE58", "const APPV=60;\nconst SAVE='sumoManager60',SAVE59='sumoManager59',SAVE58")
rep('[SAVE58,SAVE57', '[SAVE59,SAVE58,SAVE57')
rep(" if(g.v===58){g.v=59;}\n return g.v===59?g:null;}", " if(g.v===58){g.v=59;}\n if(g.v===59){g.v=60;}\n return g.v===60?g:null;}")
rep('G={v:59,', 'G={v:60,')
core = open('patches/sup63_core.js', encoding='utf-8').read()
rep("function v14Basho(sum){\n", core + "function v14Basho(sum){spBasho(sum);\n")
# タニマチの紹介
rep(" if(Math.random()<.012+net*.5)add(mkProspect(6),'海外の相撲関係者の紹介');", " if(Math.random()<.012+net*.5)add(mkProspect(6),'海外の相撲関係者の紹介');\n tmInfo(add,spring);")
# 化粧廻し:後援会の力が足りなくても、親しいタニマチがいれば贈ってもらえる
rep("if(i===0){if(G.sup>=150){G.rep=cl(G.rep+1,0,100);G.sup+=5;r.pop=cl((r.pop||20)+3,0,100);return r.home+'の後援者から、'+r.n+'に化粧廻しが贈られました。';}",
    "if(i===0){const tm=tmBest(50);if(tm){tm.cl=cl(tm.cl+4,0,100);r.pop=cl((r.pop||20)+3,0,100);G.rep=cl(G.rep+1,0,100);return 'タニマチの'+tm.n+'さん('+tm.job+')から、'+r.n+'に化粧廻しが贈られました。';}if(G.sup>=150){G.rep=cl(G.rep+1,0,100);G.sup+=5;r.pop=cl((r.pop||20)+3,0,100);return r.home+'の後援者から、'+r.n+'に化粧廻しが贈られました。';}")
# 祝賀会:タニマチのご祝儀
rep("const cost=40+own().length*2,inc=Math.round(G.sup*.04+(G.supC||0)*1.5+sk*15);", "const cost=40+own().length*2,inc=Math.round(G.sup*.04+(G.supC||0)*1.5+sk*15+tmShugi());")
# かかりつけ医(外部との契約に足す。月 7.5 万円=場所 15 万円、推定)
rep("const CONN={gym:'トレーニングジム',clinic:'治療院(整体・鍼灸)',diet:'管理栄養士'};", "const CONN={gym:'トレーニングジム',clinic:'治療院(整体・鍼灸)',diet:'管理栄養士',doc:'かかりつけ医(整形外科)'};")
rep("['gym','clinic','diet'].map(k=>'<button", "['gym','clinic','diet','doc'].map(k=>'<button")
rep("const k=(c.gym?20+n:0)+(c.clinic?30:0)+(c.diet?15:0);if(k)F.out.push(['外部との契約('+['gym','clinic','diet'].filter",
    "const k=(c.gym?20+n:0)+(c.clinic?30:0)+(c.diet?15:0)+(c.doc?15:0);if(k)F.out.push(['外部との契約('+['gym','clinic','diet','doc'].filter")
# 効き目:重いけがの 2 割が中くらいで済む(早く見つける)、隠したけがに気づきやすい、治りが少し早い
rep(" const p=wpick(wts);const x=Math.random();const s=x<.55?1:x<.88?2:3;", " const p=wpick(wts);const x=Math.random();let s=x<.55?1:x<.88?2:3;if(s===3&&r.h===0&&G.con&&G.con.doc&&Math.random()<.2)s=2;")
rep("&&(r.tr==null?50:r.tr)<35&&G.phase!=='basho'&&Math.random()<(35-r.tr)/35*.6){r.inj.hid=1;", "&&(r.tr==null?50:r.tr)<35&&G.phase!=='basho'&&Math.random()<(35-r.tr)/35*.6*(G.con&&G.con.doc?.5:1)){r.inj.hid=1;")
rep("(isOwn&&r.pm==='治'?(G.con&&G.con.clinic?.35:.12):0);", "(isOwn&&r.pm==='治'?(G.con&&G.con.clinic?.35:.12):0)+(isOwn&&G.con&&G.con.doc?.05:0);")
# 出来事:宴席の誘い・後援会長の交代・師匠の息子の入門
EVT = r""" ,enkai:{t:'タニマチの宴席',init:enkaiInit,d:e=>{const r=G.R[e.rid];return 'タニマチの'+e.tn+'さんから、'+(r?r.n:'関取')+'を夜の宴席に招きたいと誘いがありました。断ると関係が冷えるかもしれません。深夜まで続く席では、酒の上での問題も起きがちです。';},
  c:['親方も同席して早めに切り上げる','関取だけ行かせる','丁寧に断る'],
  ap:(e,i)=>{const t=(G.sp&&G.sp.tm||[]).find(x=>x.n===e.tn);const r=G.R[e.rid];if(!t||!r)return '';
   if(i===0){t.cl=cl(t.cl+4,0,100);r.mor=cl(r.mor+2,0,100);if(Math.random()<.03){G.ev.push({k:'scand',rid:r.id,tp:'ken',hid:0,id:Math.random().toString(36).slice(2,8)});return '席で客と言い争いになってしまいました。';}return '親方が同席し、宴席は和やかに終わりました。'+t.n+'さんは上機嫌です。';}
   if(i===1){t.cl=cl(t.cl+7,0,100);r.fat=cl(r.fat+6,0,100);if(Math.random()<.12){G.ev.push({k:'scand',rid:r.id,tp:Math.random()<.5?'yoa':'ken',hid:1,id:Math.random().toString(36).slice(2,8)});return r.n+'は深夜まで飲み、問題を起こしてしまいました。';}return r.n+'は朝方まで付き合いました。'+t.n+'さんは大喜びですが、稽古には疲れが残っています。';}
   t.cl=cl(t.cl-8,0,100);return '丁寧にお断りしました。'+t.n+'さんは少し残念そうでした。';}}
 ,kaicho:{t:'後援会長の交代',init:e=>{const L=[mkKai(),mkKai(),mkKai()];L[0].face=RI(13,18);L[0].cl=RI(40,60);L[1].face=RI(7,11);L[1].cl=RI(75,90);L[2].face=RI(9,14);L[2].cl=RI(55,70);L[2].age=RI(45,55);e.c=L;},
  d:e=>'後援会長の'+e.old+'さんが、高齢などを理由に退任を申し出ました。次の会長を選びます。',
  c:e=>(e.c||[]).map((k,i)=>['顔の広い','長く支えてきた','若手経営者の'][i]+k.n+'さん('+k.job+'・'+k.age+'歳・顔の広さ '+k.face+')'),
  ap:(e,i)=>{if(!e.c)EVT.kaicho.init(e);const k=e.c[i];G.sp.kai=k;return k.n+'さんが新しい後援会長に就きました。';}}
 ,shison:{t:'師匠の息子の入門',d:e=>'師匠の'+e.rel+'が中学を卒業し、父の部屋に入門したいと言っています。',
  c:()=>['受け入れる','ほかの部屋に預ける'],
  ap:(e,i)=>{const k=e.kid;if(i===0&&ownAll().length<cap()){const r=mkNisei(k,0);r.n=shikona(me().pre);r.join=G.bnum;r.kn=40;r.menu='基';r.it=1;G.R[r.id]=r;G.pend.push(r.id);achieve('nisei','二世力士の入門');return '師匠の'+e.rel+'が入門しました。四股名は「'+r.n+'」。前相撲から始めます。';}
   const r=mkNisei(k,pick(openAI()));r.n=shikona();G.R[r.id]=r;G.aiPend.push(r.id);return '師匠の'+e.rel+'は、ほかの部屋に入門しました(親子で同じ部屋だと甘えが出るため、預ける例もあります)。';}}
};
function genEvents(){"""
rep("};\nfunction genEvents(){", EVT)
rep(" if(Math.random()<.18){const e={k:'kika'};", " if(Math.random()<.15){const e={k:'enkai'};if(EVT.enkai.init(e)!==false&&!G.ev.some(x=>x.k==='enkai'))G.ev.push(e);}\n if(Math.random()<.18){const e={k:'kika'};")
# kaicho は init を ap 前に必要とするので、作るときに init する
rep("if(!G.ev.some(e=>e.k==='kaicho'))G.ev.push({k:'kaicho',old:K.n});", "if(!G.ev.some(e=>e.k==='kaicho')){const e={k:'kaicho',old:K.n,id:Math.random().toString(36).slice(2,8)};EVT.kaicho.init(e);G.ev.push(e);}")
rep("G.ev.push({k:'shison',kid:", "G.ev.push({id:Math.random().toString(36).slice(2,8),k:'shison',kid:")
# 画面:部屋の人の図の左右(見本 sup2)
UI = r'''function spCard(t,w,n,e,tag,warn){return '<div class="spc"><div class="t">'+t+(tag?'<span class="lb'+(warn?' w':'')+'">'+tag+'</span>':'')+'</div><div class="w">'+w+'</div>'+(n==null?'':'<div class="w">親しさ<span class="bar"><i style="width:'+Math.round(n)+'%"></i></span>'+Math.round(n)+'</div>')+'<div class="e">'+e+'</div></div>';}
function spSides(){const P=spInit();const K=P.kai;const L=[],Rr=[];
 if(K)L.push(spCard('後援会長',esc(K.n)+'('+esc(K.job)+'・'+Math.floor(K.age)+'歳)',K.cl,'顔の広さ '+K.face+'。後援会員の増え方、法人の後援に効く',K.age>=72?'高齢':''));
 P.tm.forEach(t=>L.push(spCard('タニマチ',esc(t.n)+'('+esc(t.job)+')',t.cl,['ちゃんこの差し入れ・関取の食事','化粧廻し・祝賀会のご祝儀','化粧廻し・祝賀会のご祝儀が大きい'][t.fut-1]+(t.cl>=50?'。新弟子の紹介も':''),t.enk?'宴席に誘いがち':'',t.enk)));
 if(!P.tm.length)L.push('<p class="mute kaku">タニマチはいません。</p>');
 const D=G.con&&G.con.doc;Rr.push(spCard('かかりつけ医',D?esc(P.docN)+'(場所 15 万円)':'契約していません',null,(D?'けが・病気を早く見つける。重いけがになりにくく、隠したけがにも気づく。':'稽古の画面の「外部との契約」で契約できます。')+'協会の相撲診療所(国技館の中・内科と整形外科)はいつでも使えます'));
 const ks=P.fam.kids;Rr.push(spCard('師匠の家族',ks.length?ks.map(k=>k.rel+' '+Math.floor(k.age)+'歳'+(k.sumo?(k.age<15?'(相撲をしている)':''):'')).join('・'):'子どもはいません',null,ks.some(k=>k.sumo&&k.age<15)?'息子は入門を考えている(二世力士の候補)':ks.some(k=>k.help)?'部屋の仕事を手伝っている':'家族は架空'));
 return [L.join(''),Rr.join('')];}
'''
rep("function orgHTML(){", UI + "function orgHTML(){")
rep("return '<div class=\"pn\"><h2>部屋の人の図<span class=\"sub\">枠が赤=部屋が雇う人</span></h2><div class=\"org\">",
    "const SS=spSides();return '<div class=\"pn\"><h2>部屋の人の図<span class=\"sub\">枠が赤=部屋が雇う人・左右=部屋を支える人</span></h2><div class=\"sw3\"><div class=\"side\"><div class=\"kaku\" style=\"font-weight:700;margin-bottom:4px\">後援する人</div>'+SS[0]+'</div><div class=\"mid\"><div class=\"org\">")
rep("関取 '+o.filter(r=>r.d<=1).length+'・若い衆 '+young+'</div></div>'+", "関取 '+o.filter(r=>r.d<=1).length+'・若い衆 '+young+'</div></div></div><div class=\"side\"><div class=\"kaku\" style=\"font-weight:700;margin-bottom:4px\">医師・家族</div>'+SS[1]+'</div></div>'+")
rep("<li><b>マネージャー</b>:部屋が自分で契約する人(協会員ではない)。給料は部屋。</li></ul>'",
    "<li><b>マネージャー</b>:部屋が自分で契約する人(協会員ではない)。給料は部屋。</li><li><b>後援会長</b>:地元の名士が務める後援会の顔役。</li><li><b>タニマチ</b>:大口の後援者。化粧廻しやご祝儀、新弟子の紹介。宴席の誘いには注意。</li><li><b>かかりつけ医</b>:部屋が契約する医師。協会の相撲診療所とは別。</li></ul>'")
rep("若者頭は公開の一覧が見つからず、架空の人です。効き目の数字は推定。</p></div>';}", "若者頭は公開の一覧が見つからず、架空の人です。後援会長・タニマチ・かかりつけ医・師匠の家族もすべて架空。効き目の数字は推定。</p></div>';}")
CSS = '''.spc{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:var(--paper);margin-bottom:8px}
.spc .t{font-weight:700;font-size:16px}.spc .w{font-size:13px;margin:2px 0}.spc .e{font-size:12px;color:var(--mute)}
.bar{display:inline-block;width:70px;height:7px;border-radius:4px;background:rgba(0,0,0,.1);vertical-align:1px;margin:0 4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--shu)}
.lb{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--ai);color:var(--ai);margin-left:4px}.lb.w{border-color:#b8860b;color:#b8860b}
.sw3{display:grid;grid-template-columns:1fr 2.2fr 1fr;gap:10px;align-items:start}@media(max-width:760px){.sw3{grid-template-columns:1fr}}
</style>'''
k = s.index('</style>'); s = s[:k] + CSS + s[k+len('</style>'):]
# 師匠が代わったら家族も新しく(新しい師匠の家族)
rep(" achieve('gen'+h.gen,h.gen+'代目の親方に継承');", " achieve('gen'+h.gen,h.gen+'代目の親方に継承');if(G.sp)G.sp.fam=mkFam();")
# 不具合直し:名跡の返還で、顧問料を見ないまま決まると資金が NaN になっていた
rep("ap:(e,i)=>{const m=(G.myoL||[]).find(x=>x.n===e.n);if(!m)return '';if(i===0){if(G.money<e.pr)", "ap:(e,i)=>{const m=(G.myoL||[]).find(x=>x.n===e.n);if(!m)return '';if(!e.pr)e.pr=myoPrice();if(i===0){if(G.money<e.pr)")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
