# 設計 17:部屋のお金と後援会  v13 -> v14
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:80]))
    s = s.replace(old, new)

# --- 版と保存キー ---
rep('<title>Sumo Manager v13</title>', '<title>Sumo Manager v14</title>')
rep("const SAVE='sumoManager13',SAVE12", "const SAVE='sumoManager14',SAVE13='sumoManager13',SAVE12")
rep('[SAVE12,SAVE11', '[SAVE13,SAVE12,SAVE11')
rep("if(g.v===12){mig13(g);g.v=13;}\n return g.v===13?g:null;}",
    "if(g.v===12){mig13(g);g.v=13;}\n if(g.v===13){mig14(g);g.v=14;}\n return g.v===14?g:null;}")
rep('G={v:13,', "G={v:14,supC:3,chi:{1:25,3:25,5:25},bld:{k:'rent'},yfin:[],yacc:{i:0,o:0},")
rep("G.sup=100+o.length*12+sek*60;",
    "G.sup=100+o.length*12+sek*60;G.supC=Math.round(2+o.length/3+sek*4);G.chi={1:30,3:30,5:30};G.bld={k:(me().age||40)>=50?'own':'rent'};")

# --- スマホの横あふれ(グリッドの中身が縮めるように) ---
rep(".grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}",
    ".grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.grid2>*,.grid3>*{min-width:0}.tb td.num{white-space:nowrap}")

# --- 仕組み本体 ---
CORE = r"""/* v14: 部屋のお金と後援会(設計 17) */
const KYO={Y:46,O:36,S:26,K:26};
const CHI={1:{n:'大阪',r:3},3:{n:'名古屋',r:2},5:{n:'九州',r:5}};
function regOf(r){const p=String(r.home||'').replace(/[都府県]$/,'');return REG.findIndex(x=>x.p.includes(p));}
function mig14(g){if(g.supC==null)g.supC=Math.max(2,Math.round((g.sup||100)/25));g.chi=g.chi||{1:30,3:30,5:30};g.bld=g.bld||{k:'own'};g.yfin=g.yfin||[];g.yacc=g.yacc||{i:0,o:0};}
function bldCost(){const b=G.bld||{k:'own'};return b.k==='rent'?60+G.fac.shuku*15:20+G.fac.shuku*6;}
function supCEq(){const o=own();const sek=o.filter(r=>r.d<=1).length;const top=o.some(r=>r.t==='Y')?10:o.some(r=>r.t==='O')?6:0;const sc=(G.scl||[]).filter(x=>G.bnum-x.b<6).length;
 return Math.max(1,3+G.rep*.25+sek*4+top+((G.jin==null?50:G.jin)-50)*.1-sc*3);}
function v14Basho(sum){
 const S=G.supC==null?5:G.supC;G.supC=Math.max(0,Math.round(S+(supCEq()-S)*.12+randn()*.6));
 G.chi=G.chi||{1:30,3:30,5:30};const o=own();
 for(const k in CHI){const reg=CHI[k].r;const loc=o.filter(r=>r.d<=1&&regOf(r)===reg).length;const lo=o.filter(r=>regOf(r)===reg).length;
  const eq=18+loc*12+lo*1.5+G.rep*.2;G.chi[k]=cl(G.chi[k]+(eq-G.chi[k])*.08,0,100);}
 if(G.bnum%6===0)addNews('後援会の年会費が更新されました。個人会員 '+G.sup+' 人・法人会員 '+G.supC+' 社です。');
}
function yfinPanel(){const L=(G.yfin||[]).slice(-6).reverse();if(!L.length)return '';
 return '<h3>年ごとの収支</h3><div style="overflow-x:auto"><table class="tb"><tr><th>年</th><th class="num">収入</th><th class="num">支出</th><th class="num">差し引き</th><th class="num hide-s">年末の資金</th></tr>'+L.map(x=>'<tr><td>'+x.y+'</td><td class="num">'+man(x.i)+'</td><td class="num">'+man(x.o)+'</td><td class="num"><b class="'+(x.i-x.o<0?'shu':'mid')+'">'+man(x.i-x.o)+'</b></td><td class="num hide-s">'+man(x.m)+'</td></tr>').join('')+'</table></div>';}
"""
rep('function B_rec(r)', CORE + 'function B_rec(r)')
rep(" v12Basho(sum);\n v13Basho(sum);", " v12Basho(sum);\n v13Basho(sum);\n v14Basho(sum);")

# --- 収支(実際の給付額に合わせる) ---
rep("F.in.push(['稽古場経費・部屋維持費('+n+' 人)',n*18]);",
    "F.in.push(['相撲部屋維持費・稽古場維持費('+n+' 人)',n*16]);")
rep("syo+={Y:80,O:60,S:40,K:40}[r.t]||(r.d===0?28:r.d===1?16:0);",
    "syo+=KYO[r.t]||(r.d===0?21:r.d===1?19:0);")
rep("F.in.push(['後援会の会費('+G.sup+' 人)',Math.round(G.sup*.6)]);",
    "F.in.push(['後援会の年会費・個人('+G.sup+' 人)',Math.round(G.sup*.35)]);if(G.supC)F.in.push(['後援会の年会費・法人('+G.supC+' 社)',Math.round(G.supC*20/6)]);")
rep("F.out.push(['ちゃんこ・生活費('+mealName()+')',Math.round((n+G.pend.length)*15*mealCost())]);",
    "const bi=(G.bnum-1)%6;const chiB=CHI[bi];const cv=chiB?((G.chi||{})[bi]||0):0;const nn=n+G.pend.length;\n"
    " F.out.push(['ちゃんこの食費('+mealName()+')'+(chiB&&cv>=30?'・地方の差し入れあり':''),Math.round(nn*22*mealCost()*(chiB?(cv>=30?.75:.9):1))]);\n"
    " F.out.push(['水道光熱費',15+nn*4]);\n"
    " F.out.push([(G.bld&&G.bld.k==='rent')?'部屋の家賃':'建物の修繕・税金',bldCost()]);")
rep("const bi=(G.bnum-1)%6;if(bi===1||bi===3||bi===5)F.out.push([CITY[bi]+'場所の宿舎・移動',120+6*n]);",
    "if(chiB){F.out.push([chiB.n+'場所の移動・荷物',10+2*nn]);if(cv<30)F.out.push([chiB.n+'場所の宿舎・稽古場(自前で手配)',60+2*nn]);const gi=Math.round(cv*.8+o.filter(r=>r.d<=1).length*8);if(gi)F.in.push([chiB.n+'の激励会・千秋楽のご祝儀',gi]);}")
rep(" G.acc={dek:0,med:0,sc:0,tourIn:0,tourOut:0};\n const tin",
    " if(G.money<0)F.out.push(['借入金の利息',Math.max(1,Math.round(-G.money*.004))]);\n G.acc={dek:0,med:0,sc:0,tourIn:0,tourOut:0};\n const tin")
rep("F.net=tin-tout;F.tin=tin;F.tout=tout;F.b=G.bnum;",
    "F.net=tin-tout;F.tin=tin;F.tout=tout;F.b=G.bnum;\n G.yacc=G.yacc||{i:0,o:0};G.yacc.i+=tin;G.yacc.o+=tout;"
    "if(G.bnum%6===0){G.yfin=G.yfin||[];G.yfin.push({y:G.y0?(G.y0+Math.floor((G.bnum-1)/6))+'年':(Math.floor((G.bnum-1)/6)+1)+'年目',i:Math.round(G.yacc.i),o:Math.round(G.yacc.o),m:Math.round(G.money+F.net)});if(G.yfin.length>40)G.yfin.shift();G.yacc={i:0,o:0};}")

# --- 祝賀会 ---
rep(""" party:{t:'後援会の祝賀会',d:()=>'後援会が場所後の祝賀会を開いてくれます。親方として出席しますか?',c:['出席する(費用 50 万円)','欠席する'],
  ap:(e,i)=>{if(i===0){G.money-=50;const n=Math.round(G.sup*.06)+6;G.sup+=n;return'祝賀会は盛況でした。後援会員が '+n+' 人増えました。';}G.sup=Math.max(30,G.sup-3);return'欠席しました。少し不満の声が出ています。';}},""",
""" party:{t:'千秋楽の祝賀会',d:()=>'千秋楽の夜、後援会が祝賀会を開きます。会場の費用は部屋が持ち、会員の参加費とご祝儀が入ります(個人 '+G.sup+' 人・法人 '+(G.supC||0)+' 社)。',c:['親方と弟子みんなで出る','親方だけ顔を出す','欠席する'],
  ap:(e,i)=>{const sk=own().filter(r=>r.d<=1).length;
   if(i===0){const cost=40+own().length*2,inc=Math.round(G.sup*.04+(G.supC||0)*1.5+sk*15);G.money+=inc-cost;const n=Math.round(G.sup*.05)+5;G.sup+=n;if(Math.random()<.5)G.supC=(G.supC||0)+1;own().forEach(r=>{r.tr=cl((r.tr==null?50:r.tr)+.5,0,100);r.mor=cl(r.mor+2,0,100);});
    return '祝賀会は盛況でした。費用 '+man(cost)+'、参加費とご祝儀 '+man(inc)+'。後援会員が '+n+' 人増えました。';}
   if(i===1){const cost=10,inc=Math.round(G.sup*.02+(G.supC||0)*.8);G.money+=inc-cost;const n=Math.round(G.sup*.02);G.sup+=n;return '親方があいさつに回りました。ご祝儀 '+man(inc)+'。';}
   G.sup=Math.max(30,G.sup-3);if(Math.random()<.3)G.supC=Math.max(0,(G.supC||0)-1);return'欠席しました。少し不満の声が出ています。';}},""")

# --- 地方場所の準備 ---
rep(" ,yokoshin:{t:'横綱審議委員会'",
""" ,chiho:{t:'地方場所の準備',d:e=>{const c=CHI[e.bi];const v=Math.round((G.chi||{})[e.bi]||0);return '次は'+c.n+'場所です。'+c.n+'の後援会(つながり '+v+')が宿舎と稽古場を用意してくれるかどうかで、費用が大きく変わります。'+(v<30?'今のままだと、宿舎は自前で借りることになりそうです(つながり 30 以上で用意してもらえます)。':'今回も宿舎と稽古場を用意してもらえそうです。');},
  c:()=>['親方があいさつに回る(20 万円)','後援会に任せる'],
  ap:(e,i)=>{if(i===0){G.money-=20;G.chi[e.bi]=cl((G.chi[e.bi]||0)+10,0,100);return CHI[e.bi].n+'の後援会を回り、つながりを深めました。';}return '後援会に任せました。';}}
 ,yokoshin:{t:'横綱審議委員会'""")
rep("if(Math.random()<.18){const e={k:'kika'};",
    "{const nb=G.bnum%6;if(CHI[nb]&&Math.random()<.6&&!G.ev.some(e=>e.k==='chiho'))G.ev.push({k:'chiho',bi:nb});}\n if(Math.random()<.18){const e={k:'kika'};")

# --- 経営画面 ---
rep("""<dt>後援会</dt><dd>'+G.sup+' 人(1 人 6000 円/場所)</dd></dl><p class="kaku mute" style="font-size:13px">関取が多いほど、優勝・三賞を取るほど評判が上がり、後援会員が増えます。評判は勧誘のしやすさにも効きます。関取が変化で勝つと、評判が少し下がります。</p>""",
"""<dt>後援会(個人)</dt><dd>'+G.sup+' 人(年会費 平均 2 万円ほど)</dd><dt>後援会(法人)</dt><dd>'+(G.supC||0)+' 社(年会費 一口 20 万円)</dd><dt>地方の後援会</dt><dd>'+Object.keys(CHI).map(k=>CHI[k].n+' '+Math.round((G.chi||{})[k]||0)).join('・')+'</dd><dt>部屋の建物</dt><dd>'+((G.bld&&G.bld.k==='rent')?'賃貸(家賃 ':'自前(修繕・税金 ')+man(bldCost())+'/場所)</dd></dl><p class="kaku mute" style="font-size:13px">関取が多いほど、優勝・三賞を取るほど評判が上がり、後援会員が増えます。評判は勧誘のしやすさにも効きます。関取が変化で勝つと、評判が少し下がります。法人会員は関取の数・横綱や大関の有無・評判で増え、不祥事のあとは離れていきます。地方場所(大阪・名古屋・九州)は、地方の後援会とのつながりが 30 以上なら宿舎と稽古場を用意してもらえ、差し入れで食費も減ります。その地方出身の弟子や関取がいると、つながりが強まります。</p>""")
rep("""'<div class="grid2"><div class="pn"><h2>前の場所の収支</h2>'+finHTML(G.fin)+'</div>""",
"""'<div class="grid2"><div class="pn"><h2>前の場所の収支</h2>'+finHTML(G.fin)+yfinPanel()+'<p class="kaku mute" style="font-size:13px">協会からは、幕下以下の弟子 1 人に月 7 万円の力士養成費、全員 1 人に場所ごと 11.5 万円の相撲部屋維持費と 4.5 万円の稽古場維持費が出ます。関取になると、養成費の代わりに養成奨励金(年額 十両 114 万円・平幕 126 万円・三役 156 万円・大関 216 万円・横綱 276 万円)が出ます。いちばん大きな支出は食費です。借金には利息がかかります。</p></div>""")

# --- 収支の表:項目名を折り返す ---
rep("F.in.map(x=>'<tr><td>'+x[0]+'</td><td class=\"num\">'", "F.in.map(x=>'<tr><td style=\"white-space:normal\">'+x[0]+'</td><td class=\"num\" style=\"white-space:nowrap\">'")
rep("F.out.map(x=>'<tr><td>'+x[0]+'</td><td class=\"num\">'", "F.out.map(x=>'<tr><td style=\"white-space:normal\">'+x[0]+'</td><td class=\"num\" style=\"white-space:nowrap\">'")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
