# 「受け持つ部屋の選び方」の見本 5 つを作る → sumo_manager/samples/heya1〜5.html
import json, os
D = json.load(open('/tmp/heya.json', encoding='utf-8'))
OUT = '/home/claude/sumo/sumo_manager/samples/'
DATA = json.dumps(D, ensure_ascii=False)

BASE_CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif;color:#1d1a16;background:#111;min-height:100vh}
.k{font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif}
button{font-family:inherit;cursor:pointer;-webkit-tap-highlight-color:transparent}
.bg{position:fixed;inset:-20px;background:url(../img/start_torikumi_blur.jpg) center/cover;filter:brightness(.42);z-index:0}
.wrap{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:0 12px 120px}
.roof{width:min(620px,86vw);margin:0 auto}.roof .r{height:22px;background:linear-gradient(#3a2a12,#1c140a);clip-path:polygon(6% 0,94% 0,100% 100%,0 100%)}
.roof .m{height:18px;background:#4b2a6b;border-bottom:3px solid #c9a24a}.roof .f{display:flex;justify-content:space-between;padding:0 6%}
.roof .f i{display:block;width:14px;height:18px;border-radius:0 0 7px 7px}.roof .f i:nth-child(1){background:#2a7a4a}.roof .f i:nth-child(2){background:#b3261e}.roof .f i:nth-child(3){background:#f4f1e8}.roof .f i:nth-child(4){background:#1c1c1c}
h1{text-align:center;color:#e9c46a;font-size:clamp(24px,4vw,36px);letter-spacing:.1em;text-shadow:0 2px 6px #000;margin:6px 0 2px}
.lead{text-align:center;color:#f2e8d0;font-size:14px;margin-bottom:12px}
.tag{position:fixed;left:8px;top:8px;font:12px sans-serif;color:#fff;background:rgba(0,0,0,.6);padding:3px 8px;border-radius:3px;z-index:30}
.paper{background:rgba(253,249,238,.97);border:2px solid #c9a24a;border-radius:6px;box-shadow:0 8px 24px rgba(0,0,0,.5);padding:12px}
.ic{display:inline-block;color:#fff;border-radius:3px;padding:0 6px;font:12px/1.7 "Hiragino Sans","Noto Sans JP",sans-serif;white-space:nowrap}
.ic.出羽海{background:#2c3e5c}.ic.二所ノ関{background:#3f6b4a}.ic.時津風{background:#8a5a1a}.ic.高砂{background:#6b2e6b}.ic.伊勢ヶ濱{background:#b5361f}
.fr{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;font:bold 14px sans-serif;color:#fff;flex:none}
.fr.S{background:#b8892c}.fr.A{background:#b5361f}.fr.B{background:#2c3e5c}.fr.C{background:#5a6b5a}.fr.D{background:#7d7365}
.lv{font:12px "Hiragino Sans","Noto Sans JP",sans-serif;padding:1px 8px;border-radius:999px;white-space:nowrap}
.lv.e{background:#fbe0c8;color:#8a3a10}.lv.n{background:#e3e8f0;color:#2c3e5c}.lv.h{background:#e8e2d6;color:#5a4a33}
/* 詳しい説明(下から出る) */
#sheet{position:fixed;left:0;right:0;bottom:0;z-index:40;transform:translateY(105%);transition:transform .25s;padding:0 10px 10px}
#sheet.on{transform:none}
#sheet .in{max-width:760px;margin:0 auto;background:#fffaf0;border:2px solid #c9a24a;border-radius:10px 10px 6px 6px;box-shadow:0 -6px 24px rgba(0,0,0,.5);padding:14px 16px;max-height:70vh;overflow:auto}
#sheet h2{font-size:24px;letter-spacing:.1em;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
#sheet .x{margin-left:auto;background:none;border:1px solid #b9a988;border-radius:4px;padding:2px 10px;font-size:14px}
#sheet dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:10px 0;font:14px/1.6 "Hiragino Sans","Noto Sans JP",sans-serif}
#sheet dt{color:#7d7365;white-space:nowrap}#sheet dd{margin:0}
#sheet .go{display:block;width:100%;margin-top:8px;background:linear-gradient(#c8432a,#9e2d18);color:#fff;border:1px solid #7b2010;border-bottom-width:3px;border-radius:5px;font-size:20px;letter-spacing:.14em;padding:12px}
#cover{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:35;display:none}#cover.on{display:block}
"""

BASE_JS = r"""
const H=""" + DATA + r""";
const LV=x=>x.fr==='S'||x.fr==='A'?['e','やさしい']:x.fr==='B'?['n','ふつう']:['h','むずかしい'];
const lvTag=x=>{const l=LV(x);return '<span class="lv '+l[0]+'">'+l[1]+'</span>';};
const icTag=x=>'<span class="ic '+x.ic+'">'+x.ic+'一門</span>';
const frTag=x=>'<span class="fr '+x.fr+'" title="資金力">'+x.fr+'</span>';
const man=v=>v>=10000?(v/10000).toFixed(2).replace(/\.?0+$/,'')+' 億円':v.toLocaleString()+' 万円';
function sheet(n){const x=H.find(h=>h.n===n);
 document.querySelector('#sheet .in').innerHTML='<h2>'+x.n+'部屋 '+icTag(x)+lvTag(x)+'<button class="x" onclick="closeS()">閉じる</button></h2>'+
 '<dl><dt>師匠</dt><dd>'+x.m+'(元'+x.mb+')・'+x.age+' 歳'+(x.post?'・協会の'+x.post:'')+'</dd>'+
 '<dt>力士</dt><dd>'+x.c+' 人(うち関取 '+x.sk+' 人)・部屋付き親方 '+x.oyaN+' 人</dd>'+
 '<dt>部屋頭</dt><dd>'+(x.top?x.top+'(' +x.topr+')':'—')+'</dd>'+
 '<dt>資金力</dt><dd>'+frTag(x)+' 始めのお金 '+man(x.money)+'</dd>'+
 '<dt>場所</dt><dd>'+x.loc+'</dd><dt>創設</dt><dd>'+x.est+' 年</dd><dt>歩み</dt><dd>'+x.hist+'</dd></dl>'+
 '<button class="go" onclick="alert(\'見本です。ここで '+x.n+'部屋 で始まります\')">'+x.n+'部屋で始める</button>';
 document.getElementById('sheet').classList.add('on');document.getElementById('cover').classList.add('on');}
function closeS(){document.getElementById('sheet').classList.remove('on');document.getElementById('cover').classList.remove('on');}
"""

def page(no, title, css, body, js):
    return ('<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>部屋の選び方 見本 %d</title><style>%s%s</style></head><body><div class="tag">見本 %d:%s</div><div class="bg"></div>'
            '<div class="wrap"><div class="roof"><div class="r"></div><div class="m"></div><div class="f"><i></i><i></i><i></i><i></i></div></div>'
            '<h1>受け持つ部屋を選ぶ</h1>%s</div><div id="cover" onclick="closeS()"></div><div id="sheet"><div class="in"></div></div>'
            '<script>%s%s</script></body></html>') % (no, BASE_CSS, css, no, title, body, BASE_JS, js)

# ---------- 1 カードで並べる(並べ替え・一門で絞る) ----------
p1css = r"""
.bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
.bar b{color:#f2e8d0;font:13px sans-serif;margin-right:2px}
.chip{background:rgba(10,8,6,.55);border:1.5px solid #c9a24a;color:#f2e8d0;border-radius:999px;padding:5px 12px;font:14px "Hiragino Sans",sans-serif}
.chip.on{background:#c9a24a;color:#1d1a16;font-weight:bold}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.card{background:rgba(253,249,238,.97);border:1.5px solid #c9a24a;border-radius:6px;padding:10px 12px;text-align:left;box-shadow:0 4px 12px rgba(0,0,0,.4)}
.card:active{transform:translateY(1px)}
.card .t{display:flex;align-items:center;gap:6px}.card .t b{font-size:22px;letter-spacing:.08em}.card .t .fr{margin-left:auto}
.card .s{font:13px/1.6 "Hiragino Sans",sans-serif;color:#4a443b;margin-top:4px}
.card .n{display:flex;gap:12px;font:13px "Hiragino Sans",sans-serif;margin-top:6px}.card .n em{font-style:normal;font-size:20px;font-weight:bold;color:#b5361f;margin-right:2px}
"""
p1body = '<p class="lead">部屋をカードで並べます。押すと詳しい説明が下から出ます。</p><div class="bar"><b>並べ方</b><span id="so"></span></div><div class="bar"><b>一門</b><span id="fi"></span></div><div class="grid" id="g"></div>'
p1js = r"""
let so='sk',fi='';const SO=[['sk','関取の多い順'],['c','力士の多い順'],['est','歴史の古い順'],['money','お金の多い順']];
function draw(){document.getElementById('so').innerHTML=SO.map(x=>'<button class="chip '+(so===x[0]?'on':'')+'" onclick="so=\''+x[0]+'\';draw()">'+x[1]+'</button>').join(' ');
 document.getElementById('fi').innerHTML=['','出羽海','二所ノ関','時津風','高砂','伊勢ヶ濱'].map(x=>'<button class="chip '+(fi===x?'on':'')+'" onclick="fi=\''+x+'\';draw()">'+(x||'すべて')+'</button>').join(' ');
 const L=H.filter(x=>!fi||x.ic===fi).sort((a,b)=>so==='est'?a.est-b.est:(b[so]-a[so])||(b.c-a.c));
 document.getElementById('g').innerHTML=L.map(x=>'<button class="card" onclick="sheet(\''+x.n+'\')"><div class="t"><b>'+x.n+'</b>'+icTag(x)+frTag(x)+'</div>'+
  '<div class="s">師匠 '+x.m+'(元'+x.mb+')'+'</div><div class="n"><span><em>'+x.c+'</em>人</span><span>関取<em>'+x.sk+'</em>人</span><span style="margin-left:auto">'+lvTag(x)+'</span></div>'+
  '<div class="s">部屋頭 '+(x.top||'—')+'('+x.topr+')</div></button>').join('');}
draw();
"""
open(OUT + 'heya1.html', 'w', encoding='utf-8').write(page(1, 'カードで並べる', p1css, p1body, p1js))

# ---------- 2 むずかしさで分ける ----------
p2css = r"""
.sec{margin-bottom:14px}.sec h2{color:#fff;font-size:20px;letter-spacing:.1em;padding:6px 12px;border-radius:5px 5px 0 0;display:flex;align-items:baseline;gap:10px}
.sec h2 small{font:13px "Hiragino Sans",sans-serif;opacity:.9}
.sec.e h2{background:#b8892c}.sec.n h2{background:#2c3e5c}.sec.h h2{background:#5a4a33}
.row{display:flex;gap:8px;overflow-x:auto;padding:10px;background:rgba(253,249,238,.95);border-radius:0 0 6px 6px;scroll-snap-type:x mandatory}
.pl{flex:none;width:150px;scroll-snap-align:start;background:#fff;border:1.5px solid #d8c9a6;border-radius:6px;padding:8px;text-align:center}
.pl b{display:block;font-size:20px;letter-spacing:.06em}.pl .s{font:12px/1.6 "Hiragino Sans",sans-serif;color:#4a443b}
.pl .n{font:13px sans-serif;margin-top:4px}.pl .n em{font-style:normal;font-weight:bold;font-size:18px;color:#b5361f}
"""
p2body = '<p class="lead">ゲームのむずかしさで 3 つに分けます。横にすべらせて選びます。</p><div id="g"></div>'
p2js = r"""
const G3=[['e','やさしい','関取が多く、お金もある部屋。すぐに優勝争いができます',x=>x.fr==='S'||x.fr==='A'],
 ['n','ふつう','関取が少しいる部屋。育てながら上を目指します',x=>x.fr==='B'],
 ['h','むずかしい','関取がいない小さな部屋。一から育てます',x=>x.fr==='C'||x.fr==='D']];
document.getElementById('g').innerHTML=G3.map(g=>{const L=H.filter(g[3]).sort((a,b)=>b.sk-a.sk||b.c-a.c);
 return '<div class="sec '+g[0]+'"><h2>'+g[1]+'<small>'+g[2]+'(' +L.length+' 部屋)</small></h2><div class="row">'+
 L.map(x=>'<button class="pl" onclick="sheet(\''+x.n+'\')"><b>'+x.n+'</b>'+icTag(x)+'<div class="s">元'+x.mb+'・'+x.m+'</div><div class="n"><em>'+x.c+'</em>人・関取<em>'+x.sk+'</em></div></button>').join('')+'</div></div>';}).join('');
"""
open(OUT + 'heya2.html', 'w', encoding='utf-8').write(page(2, 'むずかしさで分ける', p2css, p2body, p2js))

# ---------- 3 一門ごとに木札で並べる ----------
p3css = r"""
.tabs{display:flex;gap:4px;overflow-x:auto}.tabs button{flex:1;min-width:110px;border:0;border-radius:6px 6px 0 0;padding:10px 6px;font-size:17px;color:#fff;opacity:.6;letter-spacing:.08em}
.tabs button.on{opacity:1;font-weight:bold}
.board{background:linear-gradient(#5a3d1e,#3e2a14);border-radius:0 0 6px 6px;padding:16px 10px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center;min-height:300px}
.fuda{writing-mode:vertical-rl;background:linear-gradient(90deg,#d9c39a,#f0e2c0 40%,#d4bd92);border:1px solid #8e7347;border-radius:2px;color:#1d1a16;padding:10px 6px;font-weight:800;letter-spacing:.14em;box-shadow:0 3px 6px rgba(0,0,0,.5);display:flex;align-items:center;gap:6px}
.fuda small{font:11px "Hiragino Sans",sans-serif;font-weight:400;letter-spacing:0;color:#4a443b}
.fuda.big{font-size:26px;min-height:200px}.fuda.mid{font-size:22px;min-height:170px}.fuda.sml{font-size:19px;min-height:150px}
.fuda .fr{writing-mode:horizontal-tb}
.note{color:#f2e8d0;font:13px sans-serif;text-align:center;margin-top:8px}
"""
p3body = '<p class="lead">一門(部屋のグループ)ごとに、部屋の名前を木札で並べます。札が大きいほど力士が多い部屋です。</p><div class="tabs" id="t"></div><div class="board" id="b"></div><p class="note">札の上の丸は資金力(S がいちばん上)。札を押すと詳しい説明が出ます。</p>'
p3js = r"""
const IC=['出羽海','二所ノ関','時津風','高砂','伊勢ヶ濱'],ICC={'出羽海':'#2c3e5c','二所ノ関':'#3f6b4a','時津風':'#8a5a1a','高砂':'#6b2e6b','伊勢ヶ濱':'#b5361f'};let cur='出羽海';
function draw(){document.getElementById('t').innerHTML=IC.map(i=>'<button class="'+(i===cur?'on':'')+'" style="background:'+ICC[i]+'" onclick="cur=\''+i+'\';draw()">'+i+'<br><span style="font-size:12px">'+H.filter(x=>x.ic===i).length+' 部屋</span></button>').join('');
 document.getElementById('b').style.borderTop='4px solid '+ICC[cur];
 document.getElementById('b').innerHTML=H.filter(x=>x.ic===cur).sort((a,b)=>b.c-a.c).map(x=>'<button class="fuda '+(x.c>=25?'big':x.c>=15?'mid':'sml')+'" onclick="sheet(\''+x.n+'\')">'+frTag(x)+x.n+'<small>'+x.c+'人・関取'+x.sk+'</small></button>').join('');}
draw();
"""
open(OUT + 'heya3.html', 'w', encoding='utf-8').write(page(3, '一門ごとに木札で並べる', p3css, p3body, p3js))

# ---------- 4 表で比べる ----------
p4css = r"""
.tw{background:rgba(253,249,238,.97);border:2px solid #c9a24a;border-radius:6px;overflow:auto;max-height:calc(100vh - 170px)}
table{border-collapse:collapse;width:100%;font:14px "Hiragino Sans","Noto Sans JP",sans-serif}
th{position:sticky;top:0;background:#3e2a14;color:#f2e8d0;padding:8px 6px;white-space:nowrap;cursor:pointer;text-align:left;font-weight:600}
th.on{background:#b5361f}th .a{font-size:11px;margin-left:2px}
td{padding:7px 6px;border-bottom:1px solid #e3d9c4;white-space:nowrap}td.n{text-align:right;font-variant-numeric:tabular-nums}
td.nm{font-family:"Hiragino Mincho ProN","Noto Serif JP",serif;font-weight:700;font-size:17px}
tr{cursor:pointer}tr:hover td{background:#f4ecda}
@media(max-width:700px){.hide{display:none}}
"""
p4body = '<p class="lead">表で比べます。上の見出しを押すと、その順に並べかえます。行を押すと詳しい説明が出ます。</p><div class="tw"><table id="t"></table></div>'
p4js = r"""
const C=[['n','部屋',0],['ic','一門',0,1],['m','師匠',0,1],['c','力士',1],['sk','関取',1],['top','部屋頭',0,1],['fr','資金力',0],['money','始めのお金',1,1],['est','創設',1,1]];let sk='sk',dir=-1;
function draw(){const L=H.slice().sort((a,b)=>{const x=a[sk],y=b[sk];return (typeof x==='number'?(x-y):String(x).localeCompare(String(y),'ja'))*dir||b.c-a.c;});
 document.getElementById('t').innerHTML='<tr>'+C.map(c=>'<th class="'+(sk===c[0]?'on ':'')+(c[3]?'hide':'')+'" onclick="if(sk===\''+c[0]+'\')dir=-dir;else{sk=\''+c[0]+'\';dir='+(c[2]?-1:1)+'};draw()">'+c[1]+(sk===c[0]?'<span class="a">'+(dir<0?'▼':'▲')+'</span>':'')+'</th>').join('')+'<th>むずかしさ</th></tr>'+
 L.map(x=>'<tr onclick="sheet(\''+x.n+'\')"><td class="nm">'+x.n+'</td><td class="hide">'+icTag(x)+'</td><td class="hide">'+x.m+'<span style="color:#7d7365;font-size:12px">(元'+x.mb+')</span></td><td class="n">'+x.c+'</td><td class="n">'+x.sk+'</td><td class="hide">'+(x.top||'—')+'</td><td>'+frTag(x)+'</td><td class="n hide">'+man(x.money)+'</td><td class="n hide">'+x.est+'</td><td>'+lvTag(x)+'</td></tr>').join('');}
draw();
"""
open(OUT + 'heya4.html', 'w', encoding='utf-8').write(page(4, '表で比べる', p4css, p4body, p4js))

# ---------- 5 質問に答えて選ぶ ----------
p5css = r"""
.q{max-width:760px;margin:0 auto 10px}.q h2{font-size:18px;letter-spacing:.06em;margin-bottom:8px}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.opts button{background:#fff;border:2px solid #d8c9a6;border-radius:8px;padding:10px;text-align:left;font-size:16px}
.opts button small{display:block;font:12px/1.5 "Hiragino Sans",sans-serif;color:#7d7365;margin-top:2px}
.opts button.on{border-color:#b5361f;background:#fbe9e2;box-shadow:0 0 0 2px #b5361f inset}
.res{max-width:760px;margin:12px auto 0}.res h2{color:#e9c46a;font-size:20px;text-align:center;letter-spacing:.1em;margin-bottom:8px;text-shadow:0 2px 4px #000}
.pick{display:flex;align-items:center;gap:12px;width:100%;background:rgba(253,249,238,.97);border:2px solid #c9a24a;border-radius:8px;padding:10px 12px;margin-bottom:8px;text-align:left}
.pick .no{font:bold 26px sans-serif;color:#b5361f;width:30px;text-align:center}.pick b{font-size:22px;letter-spacing:.08em}
.pick .s{font:13px/1.6 "Hiragino Sans",sans-serif;color:#4a443b}.pick .fr{margin-left:auto}
.all{display:block;margin:6px auto 0;background:none;border:0;color:#f2e8d0;text-decoration:underline;font:14px sans-serif}
"""
p5body = ('<p class="lead">3 つの質問に答えると、合う部屋を 3 つすすめます。</p>'
          '<div class="paper q"><h2>1. どんな部屋から始めたい?</h2><div class="opts" id="q1"></div></div>'
          '<div class="paper q"><h2>2. 一門(部屋のグループ)は?</h2><div class="opts" id="q2"></div></div>'
          '<div class="paper q"><h2>3. 師匠はどんな人がいい?</h2><div class="opts" id="q3"></div></div>'
          '<div class="res" id="r"></div>')
p5js = r"""
const A={q1:'n',q2:'',q3:''};
const Q={q1:[['e','強い部屋','関取が多い。すぐ優勝争い'],['n','ほどほど','関取が少し。育てながら'],['h','小さな部屋','関取なし。一から育てる']],
 q2:[['','こだわらない',''],['出羽海','出羽海',''],['二所ノ関','二所ノ関',''],['時津風','時津風',''],['高砂','高砂',''],['伊勢ヶ濱','伊勢ヶ濱','']],
 q3:[['','こだわらない',''],['top','横綱・大関だった人','現役で大活躍した師匠'],['young','若い師匠','40 歳代まで'],['vet','ベテランの師匠','55 歳以上']]};
function score(x){let s=0;const l=LV(x)[0];s+=l===A.q1?10:0;if(A.q2&&x.ic===A.q2)s+=6;else if(A.q2)s-=20;
 if(A.q3==='top'&&/横綱|大関/.test(x.mb))s+=5;if(A.q3==='young'&&x.age<50)s+=5;if(A.q3==='vet'&&x.age>=55)s+=5;return s+x.c/100;}
function draw(){for(const k in Q)document.getElementById(k).innerHTML=Q[k].map(o=>'<button class="'+(A[k]===o[0]?'on':'')+'" onclick="A.'+k+'=\''+o[0]+'\';draw()">'+o[1]+(o[2]?'<small>'+o[2]+'</small>':'')+'</button>').join('');
 const L=H.slice().sort((a,b)=>score(b)-score(a)).slice(0,3);
 document.getElementById('r').innerHTML='<h2>あなたに合う部屋</h2>'+L.map((x,i)=>'<button class="pick" onclick="sheet(\''+x.n+'\')"><span class="no">'+(i+1)+'</span><span><b>'+x.n+'</b> '+icTag(x)+' '+lvTag(x)+'<div class="s">師匠 '+x.m+'(元'+x.mb+'・'+x.age+'歳)・力士 '+x.c+' 人・関取 '+x.sk+' 人</div></span>'+frTag(x)+'</button>').join('')+'<button class="all" onclick="alert(\'見本です。ここから全部屋の一覧へ進みます\')">すべての部屋から選ぶ</button>';}
draw();
"""
open(OUT + 'heya5.html', 'w', encoding='utf-8').write(page(5, '質問に答えて選ぶ', p5css, p5body, p5js))
print('ok')
