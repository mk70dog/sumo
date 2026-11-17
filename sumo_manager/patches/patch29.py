# 設計 19:力士・親方の経歴を詳しい画面に出す(見本 kei5:タブ+経歴カード)  v25 -> v26
# データは data/keireki2026.txt(関取)・keireki_low2026.txt(幕下以下)・keireki_toshi2026.txt(親方)から埋め込む。
import os, sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
DD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data') + os.sep

def load(fn, nf):
    out = []
    for l in open(DD + fn, encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        p = l.rstrip('\n').split('|')
        if len(p) != nf: raise SystemExit('項目数が違う: %s %r' % (fn, l[:40]))
        out.append(p)
    return out
KEI = {}
for p in load('keireki2026.txt', 9) + load('keireki_low2026.txt', 9):
    KEI[p[0]] = p[1:]          # 出身地,中学,高校,大学,社会人,アマ,家族,出典
KEIT = {}
for p in load('keireki_toshi2026.txt', 10):
    KEIT[p[1]] = p[2:]         # 元の四股名 → 同じ 8 項目
DATA = 'const KEI=' + json.dumps(KEI, ensure_ascii=False, separators=(',', ':')) + ';\nconst KEIT=' + json.dumps(KEIT, ensure_ascii=False, separators=(',', ':')) + ';\n'

# 版
rep('<title>Sumo Manager v25</title>', '<title>Sumo Manager v26</title>')
rep("const APPV=25;\nconst SAVE='sumoManager25',SAVE24", "const APPV=26;\nconst SAVE='sumoManager26',SAVE25='sumoManager25',SAVE24")
rep('[SAVE24,SAVE23', '[SAVE25,SAVE24,SAVE23')
rep(" if(g.v===24){g.v=25;}\n return g.v===25?g:null;}",
    " if(g.v===24){g.v=25;}\n if(g.v===25){for(const id in g.R){const r=g.R[id];if(r&&r.debut&&!r.kk)r.kk=r.n;}g.v=26;}\n return g.v===26?g:null;}")
rep('G={v:25,', 'G={v:26,')

# 実名スタート:経歴を引くための元の四股名(改名しても引けるように)
rep('for(const id in X.R){const r=X.R[id];const d=DEBUT[r.n];', 'for(const id in X.R){const r=X.R[id];r.kk=r.n;const d=DEBUT[r.n];')

CSS = r"""
/* v26 経歴(タブ+経歴カード) */
.rtabs{display:flex;margin:14px 0 0;border-bottom:2px solid var(--ai)}
.rtabs button{flex:1;font:15px var(--kaku);padding:9px 4px;background:transparent;border:1px solid var(--line);border-bottom:none;border-radius:6px 6px 0 0;color:var(--mute);min-height:42px}
.rtabs button.on{background:var(--ai);color:#fff;border-color:var(--ai)}
.rtbx{border:1px solid var(--line);border-top:none;padding:10px 12px 12px}
.rtbx>h3:first-child{margin-top:4px}
.kc{border:1px solid var(--line);border-radius:6px;background:var(--paper);padding:10px 12px;font-family:var(--kaku)}
.kc .home{font-size:15px}.kc .home:before{content:"◆ ";color:var(--shu)}
.kc .chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.kc .chip{border:1.5px solid var(--ai);border-radius:999px;padding:3px 10px;font-size:13px}
.kc .chip i{font-style:normal;font-size:11px;color:#fff;background:var(--ai);border-radius:999px;padding:0 6px;margin-right:5px}
.kc .amal{font-size:13px;line-height:1.9}
.kc .md{display:inline-block;min-width:34px;text-align:center;font:bold 11px/18px var(--kaku);border-radius:9px;margin-right:6px;color:#fff;vertical-align:1px}
.kc .md.g{background:#b8901f}.kc .md.s{background:#8c8f96}.kc .md.b{background:#9a5b2c}.kc .md.n{background:#a99c82}
.kc .tree{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.kc .tree .me{border:2px solid var(--shu);padding:4px 10px;border-radius:4px;font-weight:700}
.kc .tree .fm{border:1px solid var(--line);padding:3px 8px;border-radius:4px;font-size:13px}.kc .tree .fm small{display:block;font-size:10px;color:var(--mute)}
.kc a.lk{color:var(--ai);text-decoration:underline}
.kc .src{font-size:11px;color:var(--mute);margin-top:8px}
a.tlk{color:var(--ai);text-decoration:underline}
"""
rep('</style>', CSS + '</style>', 1)

JS = DATA + r"""
/* v26 経歴 */
function keiOf(r){if(!r)return null;const k=KEI[r.kk||r.n]||(r.kk?null:null);return k||null;}
function keiTOf(t){return t?(KEIT[t.mo]||KEI[t.mo]||null):null;}
function keiMedal(a){if(/準優勝|2位/.test(a))return '<span class="md s">2位</span>';if(/優勝|横綱/.test(a))return '<span class="md g">優勝</span>';if(/3位|ベスト4|4強/.test(a))return '<span class="md b">4強</span>';if(/ベスト8|8強/.test(a))return '<span class="md n">8強</span>';return '<span class="md n">・</span>';}
function keiFind(nm){
 for(const id of G.order){const r=G.R[id];if(r&&!r.ret&&(r.n===nm||r.kk===nm))return 'showR('+id+')';}
 if(G.toshi){const k=G.toshi.findIndex(t=>!t.left&&(t.mo===nm||t.n===nm));if(k>=0)return 'showT('+k+')';}
 return '';}
function keiFam(f){const m=f.match(/^([^:]+):(.+)$/);if(!m)return {rel:'',h:esc(f)};const who=m[2];const nm=who.replace(/[(（].*$/,'');
 if(nm==='元力士')return {rel:m[1],h:'元力士'};const go=keiFind(nm);
 return {rel:m[1],h:(go?'<a href="#" class="lk" onclick="'+go+';return false">'+esc(nm)+'</a>':esc(nm))+esc(who.slice(nm.length))};}
/* k: [出身地,中学,高校,大学,社会人,アマ,家族,出典] */
function keiCard(name,k){
 const sc=[];if(k[1])sc.push(['中学',k[1]]);if(k[2])sc.push(['高校',k[2]]);if(k[3])sc.push(['大学',k[3]]);if(k[4])sc.push(['社会人',k[4]]);
 const ama=(k[5]||'').split(';').filter(x=>x),fam=(k[6]||'').split(';').filter(x=>x);
 return '<div class="kc"><div class="home">'+esc(k[0]||'—')+' 出身</div><div class="chips">'+(sc.map(x=>'<span class="chip"><i>'+x[0]+'</i>'+esc(x[1])+'</span>').join('')||'<span class="mute" style="font-size:13px">学校は分かっていません</span>')+'</div>'+
 (ama.length?'<div class="amal">'+ama.map(a=>keiMedal(a)+esc(a)).join('<br>')+'</div>':'')+
 (fam.length?'<div class="tree"><span class="me">'+esc(name)+'</span>'+fam.map(f=>{const x=keiFam(f);return '<span class="fm"><small>'+esc(x.rel)+'</small>'+x.h+'</span>';}).join('')+'</div>':'')+
 '<div class="src">'+(k[7]?'出典:'+esc(k[7])+'。':'')+'空欄は分からなかったところです。本名は載せていません。</div></div>';}
function keiR(r){const k=keiOf(r);if(k)return keiCard(r.n,k);
 return keiCard(r.n,[r.home||'','',r.hs?r.hs+'高校':'',r.uni||'','','',r.nisei?'父:'+r.nisei.f+'('+r.nisei.br+')':'',''])
  .replace('<div class="src">','<div class="src">'+(r.debut?'この力士のくわしい経歴は調べても見つかりませんでした(番付の出身だけ)。':'ゲームの中で入門した力士です。'));}
function rTab(n,id){UI.rtab=n;showR(id);}
function rTabs(id,L){const t=UI.rtab||0;return '<div class="rtabs">'+L.map((x,i)=>'<button class="'+(i===t?'on':'')+'" onclick="rTab('+i+','+id+')">'+x+'</button>').join('')+'</div>';}
function tTab(n,k){UI.ttab=n;showT(k);}
function showT(k){const t=G.toshi&&G.toshi[k];if(!t)return;const a=ageOf(t.b);const hi=tHeya(t.heya);const tb=UI.ttab||0;
 let h='<button class="btn sm x" onclick="closeM()">閉じる</button><div style="display:flex;gap:16px;align-items:flex-start"><div class="fuda sk" style="font-size:30px;min-height:150px">'+esc(t.n)+'</div><div style="flex:1;min-width:0">'+
 '<div style="font-size:22px;color:var(--ai);font-weight:700">'+esc(t.n)+'親方 <span class="mute kaku" style="font-size:14px">元'+esc(String(t.best||'').replace(/\d.*$/,''))+'・'+esc(t.mo||'')+'</span></div>'+
 '<dl class="kv" style="margin-top:6px"><dt>所属</dt><dd>'+(hi>=0?'<a href="#" class="tlk" onclick="showHeya('+hi+');return false">'+esc(t.heya)+'部屋</a>':esc(t.heya)+'部屋')+'('+(t.shi?'師匠':'部屋付き')+')</dd><dt>役職</dt><dd>'+esc(t.post||'年寄')+'</dd><dt>年齢</dt><dd>'+a+'歳'+(a<65?'(定年まで '+(65-a)+' 年)':'')+'</dd><dt>最高位</dt><dd>'+esc(t.best||'—')+'</dd>'+(t.since?'<dt>襲名</dt><dd>'+esc(String(t.since).replace('-',' 年 '))+' 月</dd>':'')+'</dl></div></div>';
 h+='<div class="rtabs">'+['部屋での役目','経歴','記録'].map((x,i)=>'<button class="'+(i===tb?'on':'')+'" onclick="tTab('+i+','+k+')">'+x+'</button>').join('')+'</div><div class="rtbx">';
 if(tb===1){const kk=keiTOf(t);h+=kk?keiCard(t.n,kk):keiCard(t.n,[t.from||'','','','','','','','']).replace('<div class="src">','<div class="src">この親方の経歴は調べても分かりませんでした。');}
 else if(tb===2){h+='<dl class="kv"><dt>現役の四股名</dt><dd>'+esc(t.mo||'—')+'</dd><dt>最高位</dt><dd>'+esc(t.best||'—')+'</dd><dt>年寄名跡</dt><dd>'+esc(t.n)+(t.since?'('+esc(String(t.since).replace('-',' 年 '))+' 月から)':'')+'</dd><dt>出身</dt><dd>'+esc(t.from||'—')+'</dd></dl>';}
 else{const n=hi>=0?G.order.filter(id=>{const r=G.R[id];return r.h===hi&&!r.ret;}).length:0;
  h+='<dl class="kv"><dt>役目</dt><dd>'+(t.shi?'部屋の師匠として弟子を育て、部屋を切り盛りしています。':'部屋付きの親方として、師匠を助けて弟子に稽古をつけています。')+'</dd>'+(hi>=0?'<dt>部屋の力士</dt><dd>'+n+' 人</dd>':'')+'<dt>協会</dt><dd>'+esc(t.post&&t.post!=='年寄'?t.post:'年寄(平年寄)')+'</dd></dl>';}
 h+='</div>';openM(h);}
"""
rep("function showR(id){", JS + "function showR(id){")

# 力士の画面:見出しの下を「能力・状態/経歴/記録」のタブに分ける
rep("+'</dl></div></div>';\n if(isOwn){\n", "+'</dl></div></div>';\n const H0=h;h='';\n if(isOwn){\n")
rep(" if(r.h2h){const hh=", " const P0=h;h='';\n if(r.h2h){const hh=")
rep(" openM(h);\n}", " const P2=h;const tb=UI.rtab||0;\n h=H0+rTabs(id,['能力・状態','経歴','記録'])+'<div class=\"rtbx\">'+(tb===1?keiR(r):tb===2?(P2||'<p class=\"mute kaku\">まだ記録がありません。</p>'):P0)+'</div>';\n openM(h);\n}")

# 部屋の詳しい画面:親方の名前を押すと親方の画面へ
rep("TS.map(t=>(t.shi?'<b>師匠</b> ':'')+esc(t.n)+'(元・'",
    "TS.map(t=>(t.shi?'<b>師匠</b> ':'')+'<a href=\"#\" class=\"tlk\" onclick=\"showT('+G.toshi.indexOf(t)+');return false\">'+esc(t.n)+'</a>(元・'")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
