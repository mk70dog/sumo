# v169 -> v170:お金持ちの部屋のお金の使いみち(ダルマさん「実施」→ 見本 bd1〜bd3 →「お任せ」→ bd1+工事の進み具合の棒)。数値は推定(伊勢ヶ濱の新部屋 総工費 25 億円・2028 年完成予定の報道だけ実際)。
#   部屋の建物:賃貸なら「古い部屋を買って改築(4 億円・半年)」、新築 都外 5 億・都内 10 億・両国の近く 20 億(2 年)。着工で半分、完成で半分。
#     新築で弟子の上限・稽古場の段階・評判・後援会が上がる。完成で部屋開きのご祝儀。自前の建物は築 15 年をこえると修繕費が年ごとに増え、築 40 年をこえると稽古の伸びが少し下がる。大きな修繕(1.5 億円・半年)で築 10 年相当に戻る。
#   夏合宿:名古屋場所のあと、弟子の出身の多い地方か関東で開く。費用 (120+7×人数) 万円(関東は ×0.75)。次の場所までの稽古の伸び +4%、後援会と(大阪・名古屋・九州なら)地方のつながりが増える。
#   出典:東スポ 177121(都内で新築は少なくとも数億円、改築は安いが制約)、週刊女性PRIME 41534(伊勢ヶ濱 総工費 25 億円・2028 年完成予定)、文藝春秋 h12679(夏合宿は各部屋の恒例、高砂部屋の平塚合宿)、秋田魁 20260611(押尾川部屋の大潟村合宿)。
import sys
LOGIC = r'''/* 部屋の建物の案(費用は万円・推定) */
const BDOPT={
 kai:{n:'古い部屋を買って改築',c:40000,d:3,cap:0,kei:0,rep:0,sup:0,supC:0,ef:'家賃がなくなる(修繕・税金だけ)・広さは今と同じ',rent:1},
 shu:{n:'大きな修繕',c:15000,d:3,cap:0,kei:0,rep:0,sup:0,supC:0,ef:'築 10 年ほどに戻る(修繕費が下がる)',own:1},
 ng:{n:'新築・都外',c:50000,d:12,cap:6,kei:1,rep:0,sup:0,supC:0,loc:'千葉県',ef:'弟子 +6 人・稽古場 +1・家賃なし(都外は費用安め)'},
 nt:{n:'新築・都内',c:100000,d:12,cap:9,kei:1,rep:5,sup:60,supC:2,loc:'東京都',ef:'弟子 +9 人・稽古場 +1・評判 +5・後援会 +60 人'},
 nr:{n:'新築・両国の近く',c:200000,d:12,cap:12,kei:2,rep:10,sup:150,supC:5,loc:'東京都墨田区両国',ef:'弟子 +12 人・稽古場 +2・評判 +10(勧誘しやすい)・後援会 +150 人'}
};
function bdUp(){if(typeof closeM==='function')closeM();if(typeof save==='function')save();if(typeof render==='function')render();}
function bdB(){G.bld=G.bld||{k:'own'};return G.bld;}
function bdList(){const b=bdB();if(b.pj)return [];return Object.keys(BDOPT).filter(k=>{const o=BDOPT[k];if(o.rent)return b.k==='rent';if(o.own)return b.k==='own'&&bdAge()>=20;return true;});}
function bdBuy(k,ok){const b=bdB();const o=BDOPT[k];if(!o||b.pj||!bdList().includes(k))return;const h=Math.round(o.c/2);
 if(G.money<o.c){alertM('資金が足りません','始めるには全額の '+man(o.c)+' の資金が必要です(払うのは いま半分・完成のときに半分)。');return;}
 if(!ok){openM('<h2>'+esc(o.n)+'</h2><p class="kaku">費用 '+man(o.c)+'(いま '+man(h)+'、'+(o.d>=6?'2 年後':'半年後')+'の完成のときに '+man(o.c-h)+')。<br>'+esc(o.ef)+'。</p><p class="kaku mute" style="font-size:13px">完成までに資金を使いすぎると、完成のときの支払いで借金になることがあります。工事は途中でやめられません。</p><button class="btn main" onclick="bdBuy(\''+k+'\',1)">これで始める</button> <button class="btn" onclick="closeM()">やめる</button>');return;}
 G.money-=h;G.yacc=G.yacc||{i:0,o:0};G.yacc.o+=h;b.pj={k:k,s:G.bnum,e:G.bnum+o.d,rest:o.c-h};addNews((o.d>=6?'新しい部屋の工事を始めました':o.n+'を始めました')+'('+o.n+'・'+man(o.c)+')。');bdUp();}
function campOpts(){const o=own();const nn=o.length;const cnt={};o.forEach(r=>{const g=regOf(r);if(g>=0)cnt[g]=(cnt[g]||0)+1;});
 const L=Object.keys(cnt).map(Number).filter(g=>g!==1).sort((a,b)=>cnt[b]-cnt[a]).slice(0,2);L.push(1);
 return L.map(g=>{const ck=Object.keys(CHI).find(k=>CHI[k].r===g);return {g:g,n:REG[g].n,cnt:cnt[g]||0,ck:ck,c:Math.round((120+nn*7)*(g===1?.75:1))};});}
function campSet(g){const b=bdB();b.camp=g;bdUp();}
function bdFin(F,o){const b=bdB();
 if(b.pj&&G.bnum>=b.pj.e){const k=b.pj.k,O=BDOPT[k];F.out.push([O.n+'(完成のときの支払い)',b.pj.rest]);
  if(k==='shu'){b.bb=G.bnum-60;addNews('部屋の大きな修繕が終わりました。');}
  else{const old=b.cx||{cap:0};G.capB=Math.max(0,(G.capB||0)-old.cap+O.cap);G.fac.keiko=Math.min(5,G.fac.keiko+O.kei);G.rep=Math.min(100,G.rep+O.rep);G.sup+=O.sup;G.supC=(G.supC||0)+O.supC;
   b.k='own';b.bb=G.bnum;b.cx={cap:O.cap,k:k};if(O.loc){const H=G.heya[ME()];if(H)H.loc=O.loc;}
   if(k!=='kai'){const g=Math.round(G.sup*.25+(G.supC||0)*5);F.in.push(['部屋開きのご祝儀',g]);addNews('新しい部屋が完成し、部屋開きをしました('+O.n+')。');}else addNews('買った部屋の改築が終わり、引っ越しました。');}
  b.pj=null;}
 if((G.bnum-1)%6===3&&b.camp!=null){const c=campOpts().find(x=>x.g===b.camp)||campOpts()[0];F.out.push(['夏合宿('+c.n+')',c.c]);
  const su=10+2*c.cnt;G.sup+=su;let ch=0;if(c.ck){G.chi=G.chi||{};G.chi[c.ck]=(G.chi[c.ck]||0)+8;ch=8;}
  b.campB=G.bnum+1;b.campL={y:String(bname(G.bnum)).split(' ')[0],n:c.n,su:su,ch:ch};b.camp=null;addNews('夏合宿を'+c.n+'で開きました(後援会 +'+su+' 人'+(ch?'・地方のつながり +'+ch:'')+')。');}
}
'''
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=169;\nconst SAVE='sumoManager169',SAVE168", "const APPV=170;\nconst SAVE='sumoManager170',SAVE169='sumoManager169',SAVE168")
rep('[SAVE168,SAVE167', '[SAVE169,SAVE168,SAVE167')
rep('<title>Grand Sumo Manager v169', '<title>Grand Sumo Manager v170')
# 優勝の副賞の印は二人相撲でも人ごとに(G.bld の中へ)
rep('if(my)G.riceB=G.bnum+1;', 'if(my){G.bld=G.bld||{k:"own"};G.bld.riceB=G.bnum+1;}')
rep('const rice=G.riceB===G.bnum', 'const rice=(G.bld||{}).riceB===G.bnum')
# 修繕費は古くなると増える
rep("function bldCost(){const b=G.bld||{k:'own'};return Math.round((b.k==='rent'?60+G.fac.shuku*15:20+G.fac.shuku*6)*locF(G.heya[ME()]));}",
    "function bdAge(){const b=G.bld||{k:'own'};if(b.k!=='own')return 0;if(b.bb==null)b.bb=G.bnum-RI(60,240);return Math.max(0,Math.floor((G.bnum-b.bb)/6));}\n"
    "function bldCost(){const b=G.bld||{k:'own'};const af=b.k==='own'?1+Math.max(0,bdAge()-15)*.06:1;return Math.round((b.k==='rent'?60+G.fac.shuku*15:20+G.fac.shuku*6)*locF(G.heya[ME()])*af);}\n"+LOGIC)
rep("F.out.push([(G.bld&&G.bld.k==='rent')?'部屋の家賃':'建物の修繕・税金',bldCost()]);",
    "F.out.push([(G.bld&&G.bld.k==='rent')?'部屋の家賃':'建物の修繕・税金(築 '+bdAge()+' 年)',bldCost()]);")
# 稽古:合宿の次の場所は +4%、築 40 年をこえると −3%
rep('kf:.9+.05*G.fac.keiko,', "kf:.9+.05*G.fac.keiko+((G.bld||{}).campB===G.bnum?.04:0)-(bdAge()>=40?.03:0),")
# 場所ごとの収支:工事の進み・合宿
rep(" if(G.acc.dek)F.out.push(['出稽古の費用',G.acc.dek]);",
    " bdFin(F,o);\n if(G.acc.dek)F.out.push(['出稽古の費用',G.acc.dek]);")
BLOCK = r"""<style>
/* v170 部屋の建物・夏合宿(見本 bd1) */
.bdt{width:100%;border-collapse:collapse;font-size:14px}.bdt td,.bdt th{padding:6px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}
.bdt th{font-size:12px;color:var(--mute);font-weight:normal}.bdt .nm{font-weight:bold;color:var(--sumi)}.bdt .ef{font-size:12px;color:var(--mute)}
.bdt td:nth-child(2),.bdt td:nth-child(3),.bdt .btn{white-space:nowrap}@media(max-width:520px){.bdt td,.bdt th{padding:6px 3px}.bdt .btn{padding:5px 8px;font-size:13px}}
.bdnow{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;font-size:14px;margin:4px 0 8px}.bdnow b{font-size:16px}
.bdbar{height:12px;border-radius:6px;background:rgba(128,128,128,.25);overflow:hidden;margin:6px 0}.bdbar>i{display:block;height:100%;background:#a8823c}
</style>
<script>
function bdPanel(){const b=bdB();const age=bdAge();let h='<div class="pn" id="bdpn"><h2>部屋の建物</h2>';
 h+='<div class="bdnow"><b>今:'+(b.k==='rent'?'賃貸':'自前・築 '+age+' 年')+'</b><span>'+(b.k==='rent'?'家賃 ':'修繕・税金 ')+man(bldCost())+'/場所</span><span class="mute">資金 '+man(G.money)+'</span></div>';
 if(b.pj){const O=BDOPT[b.pj.k];const all=b.pj.e-b.pj.s,done=Math.min(all,G.bnum-b.pj.s);h+='<div class="bdnow"><b>工事中:'+esc(O.n)+'</b><span>完成まで あと '+Math.max(1,b.pj.e-G.bnum+1)+' 場所</span></div><div class="bdbar"><i style="width:'+Math.round(done/all*100)+'%"></i></div><div class="mute" style="font-size:13px">残りの支払い '+man(b.pj.rest)+'(完成のとき)・それまでは今の部屋のまま</div>';}
 else{const L=bdList();h+='<table class="bdt"><tr><th>えらぶ</th><th>費用</th><th>期間</th><th></th></tr>'+L.map(k=>{const o=BDOPT[k];const ng=G.money<o.c;return '<tr><td><div class="nm">'+o.n+'</div><div class="ef">'+o.ef+'</div></td><td>'+man(o.c)+'</td><td>'+(o.d>=6?'2 年':'半年')+'</td><td><button class="btn sm"'+(ng?' disabled':'')+' onclick="bdBuy(\''+k+'\')">'+(ng?'資金不足':'これにする')+'</button></td></tr>';}).join('')+'</table>';}
 h+='<p class="kaku mute" style="font-size:13px">始めるには全額の資金が要ります(払うのは着工で半分、完成で半分)。自前の建物は築 15 年をこえると修繕費が増え、築 40 年をこえると稽古の伸びが少し下がります(大きな修繕か建て替えで戻ります)。費用は推定です。</p></div>';
 const C=campOpts();h+='<div class="pn" id="cmpn"><h2>夏合宿<span class="sub">名古屋場所のあと・年 1 回</span></h2><table class="bdt">'+C.map(c=>'<tr><td><div class="nm">'+c.n+(b.camp===c.g?' ✓':'')+'</div><div class="ef">'+(c.cnt?'出身の弟子 '+c.cnt+' 人':'近い・安い')+(c.ck?'・'+CHI[c.ck].n+'とのつながり '+Math.round((G.chi||{})[c.ck]||0):'')+'</div></td><td>'+man(c.c)+'</td><td><button class="btn sm'+(b.camp===c.g?' on':'')+'" onclick="campSet('+c.g+')">'+(b.camp===c.g?'✓ ここに決定':'ここで開く')+'</button></td></tr>').join('')
  +'<tr><td><div class="nm">今年は開かない'+(b.camp==null?' ✓':'')+'</div><div class="ef">お金を残す</div></td><td>0</td><td><button class="btn sm" onclick="campSet(null)">開かない</button></td></tr></table>'
  +(b.campL?'<div class="mute" style="font-size:13px">前の合宿:'+esc(b.campL.y)+' '+esc(b.campL.n)+'(後援会 +'+b.campL.su+' 人'+(b.campL.ch?'・つながり +'+b.campL.ch:'')+')</div>':'')
  +'<p class="kaku mute" style="font-size:13px">合宿で次の場所までの稽古の伸びが少し上がり(+4%)、後援会とその地方とのつながりが増えます。費用は推定です。</p></div>';
 return h;}
(function(){const R0=render;render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='keiei'&&G&&!document.getElementById('bdpn')){const fh=[...document.querySelectorAll('.pn>h2')].find(e=>e.textContent.startsWith('部屋の施設'));if(fh){const fac=fh.parentElement;const a=fac.closest('.kacc')||fac;a.insertAdjacentHTML('afterend',bdPanel());}}}catch(e){console.error(e);}return x;};})();
</script>
"""
i = s.rindex('</body>')
s = s[:i] + BLOCK + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
