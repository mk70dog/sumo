# 受け持つ部屋の選び方を見本 1「カードで並べる」に  v22 -> v23
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

# --- 版 ---
rep('<title>Sumo Manager v22</title>', '<title>Sumo Manager v23</title>')
rep("const APPV=22;\nconst SAVE='sumoManager22',SAVE21", "const APPV=23;\nconst SAVE='sumoManager23',SAVE22='sumoManager22',SAVE21")
rep('[SAVE21,SAVE20,SAVE19', '[SAVE22,SAVE21,SAVE20,SAVE19')
rep(" if(g.v===21){g.v=22;}\n return g.v===22?g:null;}", " if(g.v===21){g.v=22;}\n if(g.v===22){g.v=23;}\n return g.v===23?g:null;}")
rep('G={v:22,', 'G={v:23,')

# --- 見た目(見本 1 と同じ) ---
CSS = r"""
/* v23 受け持つ部屋のカード */
.st-wrap.wide{max-width:1100px}
.hlead{color:#f2e8d0;text-align:center;font:14px/1.6 var(--kaku);margin:10px 0}
.hbar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 8px}
.hbar>b{color:#f2e8d0;font:13px var(--kaku);margin-right:2px}
.hchip{background:rgba(10,8,6,.55);border:1.5px solid #c9a24a;color:#f2e8d0;border-radius:999px;padding:5px 12px;font:14px var(--kaku);cursor:pointer}
.hchip.on{background:#c9a24a;color:#1d1a16;font-weight:bold}
.hgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.hcard{background:rgba(253,249,238,.97);border:1.5px solid #c9a24a;border-radius:6px;padding:10px 12px;text-align:left;box-shadow:0 4px 12px rgba(0,0,0,.4);color:#1d1a16;font-family:var(--min);cursor:pointer}
.hcard:active{transform:translateY(1px)}
.hcard .t{display:flex;align-items:center;gap:6px}.hcard .t b{font-size:22px;letter-spacing:.08em}.hcard .t .hfr{margin-left:auto}
.hcard .s{font:13px/1.6 var(--kaku);color:#4a443b;margin-top:4px}
.hcard .n{display:flex;gap:12px;align-items:center;font:13px var(--kaku);margin-top:6px}.hcard .n em{font-style:normal;font-size:20px;font-weight:bold;color:#b5361f;margin-right:2px}
.hic{display:inline-block;color:#fff;border-radius:3px;padding:0 6px;font:12px/1.7 var(--kaku);white-space:nowrap}
.hic.i0{background:#2c3e5c}.hic.i1{background:#3f6b4a}.hic.i2{background:#8a5a1a}.hic.i3{background:#6b2e6b}.hic.i4{background:#b5361f}
.hfr{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;font:bold 14px var(--kaku);color:#fff;flex:none}
.hfr.S{background:#b8892c}.hfr.A{background:#b5361f}.hfr.B{background:#2c3e5c}.hfr.C{background:#5a6b5a}.hfr.D{background:#7d7365}
.hlv{font:12px var(--kaku);padding:1px 8px;border-radius:999px;white-space:nowrap;margin-left:auto}
.hlv.e{background:#fbe0c8;color:#8a3a10}.hlv.n{background:#e3e8f0;color:#2c3e5c}.hlv.h{background:#e8e2d6;color:#5a4a33}
#hcover{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:35;display:none}#hcover.on{display:block}
#hsheet{position:fixed;left:0;right:0;bottom:0;z-index:40;transform:translateY(105%);transition:transform .25s;padding:0 10px calc(10px + env(safe-area-inset-bottom))}
#hsheet.on{transform:none}
#hsheet .in{max-width:760px;margin:0 auto;background:#fffaf0;color:#1d1a16;border:2px solid #c9a24a;border-radius:10px 10px 6px 6px;box-shadow:0 -6px 24px rgba(0,0,0,.5);padding:14px 16px;max-height:78vh;overflow:auto}
#hsheet h2{font-size:24px;letter-spacing:.1em;display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0;border:0;padding:0}
#hsheet .x{margin-left:auto;background:none;border:1px solid #b9a988;border-radius:4px;padding:2px 10px;font:14px var(--kaku);color:#1d1a16}
#hsheet dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:10px 0;font:14px/1.6 var(--kaku)}
#hsheet dt{color:#7d7365;white-space:nowrap}#hsheet dd{margin:0}
#hsheet label{display:block;font:13px var(--kaku);color:#4a443b;margin:4px 0}
#hsheet select{width:100%;background:#fffdf7;color:#1d1a16;border-color:#b9a988}
#hsheet .btn.main{display:block;width:100%;margin-top:10px;font-size:20px}
#hsheet h2 .hlv{margin-left:0}
body.hs-open .st-credit{display:none}
"""
rep('</style>', CSS + '</style>', 1)

# --- 画面 ---
rep("function nightHTML(body){return '<div class=\"st-bg4\"></div><div class=\"st-wrap\">",
    "function nightHTML(body){return '<div class=\"st-bg4\"></div><div class=\"st-wrap'+(UI.start==='real'?' wide':'')+'\">")

_i = s.index("function realStartHTML(){"); _e = s.index("この部屋で始める</button></div>';}\n", _i) + len("この部屋で始める</button></div>';}\n")
old_start = s[_i:_e]
assert old_start.count("function ") == 1, old_start[:200]
NEW = r"""function realStartHTML(){if(!UI.hs)UI.hs={so:'sk',fi:-1};const L=heyaList(),so=UI.hs.so,fi=UI.hs.fi;
 const SO=[['sk','関取の多い順'],['c','力士の多い順'],['est','歴史の古い順'],['money','お金の多い順']];
 const V=L.filter(x=>fi<0||x.ic===fi).sort((a,b)=>so==='est'?(a.est||9999)-(b.est||9999):(b[so]-a[so])||(b.c-a.c));
 return '<p class="hlead">2026 年九州場所の番付(全 592 人・45 部屋)から始めます。部屋を押すと詳しい説明が出ます。<br>能力は番付と年齢からの推定です。これから起きる勝敗・けが・不祥事などは、すべてゲーム内の架空の出来事です。</p>'+
 '<div class="hbar"><b>並べ方</b>'+SO.map(x=>'<button class="hchip'+(so===x[0]?' on':'')+'" onclick="hsSet(\'so\',\''+x[0]+'\')">'+x[1]+'</button>').join('')+'</div>'+
 '<div class="hbar"><b>一門</b><button class="hchip'+(fi<0?' on':'')+'" onclick="hsSet(\'fi\',-1)">すべて</button>'+ICR.map((n,i)=>'<button class="hchip'+(fi===i?' on':'')+'" onclick="hsSet(\'fi\','+i+')">'+n+'</button>').join('')+'</div>'+
 '<div class="hgrid">'+V.map(x=>'<button class="hcard" onclick="heyaSheet(\''+x.n+'\')"><div class="t"><b>'+esc(x.n)+'</b>'+hIc(x)+hFr(x)+'</div>'+
  '<div class="s">師匠 '+esc(x.m)+'(元'+esc(x.mb)+')</div><div class="n"><span><em>'+x.c+'</em>人</span><span>関取<em>'+x.sk+'</em>人</span>'+hLv(x)+'</div>'+
  '<div class="s">部屋頭 '+(x.top?esc(x.top)+'('+x.topr+')':'—')+'</div></button>').join('')+'</div>'+
 '<div id="hcover" onclick="heyaClose()"></div><div id="hsheet"><div class="in"></div></div>';}
/* 部屋ごとのあらまし(実名モードの開始時。資金力と始めのお金は本体の計算と同じ推定) */
function heyaList(){if(heyaList._c)return heyaList._c;const RK={Y:'横綱',O:'大関',S:'関脇',K:'小結'};
 heyaList._c=REALH.map(x=>{const n=x[0],ws=[];REALB.forEach((l,i)=>{const f=l.split('|');if(f[3]===n)ws.push([i,f[0],f[1]]);});
  const sk=ws.filter(w=>w[0]<70).length,tp=ws[0];const topr=tp?(RK[tp[1]]||(tp[0]<42?'前頭':tp[0]<70?'十両':tp[0]<190?'幕下':tp[0]<350?'三段目':'序二段以下')):'';
  const t=TOSHI.find(r=>r[2]===n&&r[3]===1);const mb=t?t[5]:(RK[x[4]]||'力士');const mbs=/横綱/.test(mb)?5:/大関/.test(mb)?3:/関脇/.test(mb)?1:0;
  const d=HEYAD[n]||['',0,''];const hf=HFIN[n];const sc=sk*3+ws.length*.3+mbs+(d[1]&&d[1]<1950?3:d[1]&&d[1]<1990?1:0)+(hf&&hf[3]?1:0);
  const oya=TOSHI.filter(r=>r[2]===n&&r[3]!==1).length;const post=t&&/理事|監事|役員待遇/.test(t[1])?t[1]:'';
  return {n:n,ic:x[1],m:x[2],age:x[3],mb:mb,post:post,c:ws.length,sk:sk,top:tp?tp[2]:'',topr:topr,loc:d[0],est:d[1],hist:d[2],fr:finRank(sc),money:Math.round(800+sc*110),oya:oya};});
 return heyaList._c;}
const hIc=x=>'<span class="hic i'+x.ic+'">'+ICR[x.ic]+'一門</span>';
const hFr=x=>'<span class="hfr '+x.fr+'" title="資金力">'+x.fr+'</span>';
const hLv=x=>{const l=x.fr==='S'||x.fr==='A'?['e','やさしい']:x.fr==='B'?['n','ふつう']:['h','むずかしい'];return '<span class="hlv '+l[0]+'">'+l[1]+'</span>';};
function hsSet(k,v){UI.hs[k]=v;const y=window.scrollY;render();window.scrollTo(0,y);}
function heyaSheet(n){const x=heyaList().find(h=>h.n===n);if(!x)return;
 $('#hsheet .in').innerHTML='<h2>'+esc(x.n)+'部屋 '+hIc(x)+hLv(x).replace('margin-left:auto','')+'<button class="x" onclick="heyaClose()">閉じる</button></h2>'+
 '<dl><dt>師匠</dt><dd>'+esc(x.m)+'(元'+esc(x.mb)+')・'+x.age+' 歳'+(x.post?'・協会の'+x.post:'')+'</dd>'+
 '<dt>力士</dt><dd>'+x.c+' 人(うち関取 '+x.sk+' 人)・部屋付き親方 '+x.oya+' 人</dd>'+
 '<dt>部屋頭</dt><dd>'+(x.top?esc(x.top)+'('+x.topr+')':'—')+'</dd>'+
 '<dt>資金力</dt><dd>'+hFr(x)+' 始めのお金 '+man(x.money)+'(推定)</dd>'+
 (x.loc?'<dt>場所</dt><dd>'+esc(x.loc)+'</dd>':'')+(x.est?'<dt>創設</dt><dd>'+x.est+' 年</dd>':'')+(x.hist?'<dt>歩み</dt><dd>'+esc(x.hist)+'</dd>':'')+'</dl>'+
 '<input type="hidden" id="r_h" value="'+esc(x.n)+'"><label>師匠の取り口(指導の得意分野)</label><select id="r_t"><option value="">現役時代に合わせる</option><option value="押">押し相撲</option><option value="四">四つ相撲</option><option value="技">技能派</option></select>'+
 '<button class="btn main" onclick="doStartReal()">'+esc(x.n)+'部屋で始める</button>';
 $('#hsheet').classList.add('on');$('#hcover').classList.add('on');document.body.classList.add('hs-open');}
function heyaClose(){const a=$('#hsheet'),b=$('#hcover');if(a)a.classList.remove('on');if(b)b.classList.remove('on');document.body.classList.remove('hs-open');}
"""
s = s.replace(old_start, NEW, 1)

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
