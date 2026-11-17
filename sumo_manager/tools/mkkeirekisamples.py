# 力士・親方の詳しい画面に「経歴」を出す見本 4 つ → samples/kei1〜4.html
# 色や部品はゲーム本体(v25)の CSS をそのまま使う。データは data/keireki*.txt から読む。
import re, json, html
D = '/home/claude/sumo/sumo_manager/'
OUT = D + 'samples/'
src = open(D + 'sumo_manager_v25.html', encoding='utf-8').read()
CSS = re.findall(r'<style>(.*?)</style>', src, re.S)[0]
CSS = re.sub(r'url\(data:[^)]*\)', 'none', CSS)

def rows(fn, n):
    R = {}
    for l in open(D + 'data/' + fn, encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        p = l.rstrip('\n').split('|')
        R[p[0]] = p
    return R
K = rows('keireki2026.txt', 9); L = rows('keireki_low2026.txt', 9); T = rows('keireki_toshi2026.txt', 10)

def kei(p):  # 9 項目の形にそろえる
    return dict(home=p[1], chu=p[2], ko=p[3], dai=p[4], sha=p[5], ama=[x for x in p[6].split(';') if x], fam=[x for x in p[7].split(';') if x], src=p[8])
def keiT(p):
    return dict(home=p[2], chu=p[3], ko=p[4], dai=p[5], sha=p[6], ama=[x for x in p[7].split(';') if x], fam=[x for x in p[8].split(';') if x], src=p[9])

PEOPLE = [
  dict(id='r1', kind='力士', name='大の里', rank='横綱', heya='二所ノ関', debut='2023 年 5 月', age=26, body='192cm・191kg', style='突き押し・右四つ', best='横綱', kei=kei(K['大の里'])),
  dict(id='r2', kind='力士', name='朝玉勢', rank='東幕下52枚目', heya='高砂', debut='2016 年 1 月', age=33, body='181cm・138kg', style='押し・叩き', best='十両12枚目', kei=kei(L['朝玉勢'])),
  dict(id='t1', kind='親方', name='甲山', moto='大碇', rank='年寄・委員', heya='伊勢ノ海', role='部屋付き', age=54, best='前頭11枚目', since='2004 年 11 月', kei=keiT(T['甲山'])),
]
PJ = json.dumps(PEOPLE, ensure_ascii=False)

COMMON_JS = r"""
const P=""" + PJ + r""";let cur=P[0].id;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function toast(t){const e=document.getElementById('toast');e.textContent=t;e.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(()=>e.classList.remove('on'),1500);}
function famLink(f){const m=f.match(/^([^:]+):(.+)$/);if(!m)return esc(f);const who=m[2];const nm=who.replace(/[(（].*$/,'');
 if(nm==='元力士')return esc(m[1])+':元力士';
 return esc(m[1])+':<a href="#" onclick="toast(\'('+'見本)'+esc(nm)+'の画面へ移ります\');return false" style="color:var(--ai);text-decoration:underline">'+esc(nm)+'</a>'+esc(who.slice(nm.length));}
function medal(a){if(/優勝|横綱/.test(a))return '<span class="md g">優勝</span>';if(/準優勝|2位/.test(a))return '<span class="md s">2位</span>';if(/3位|ベスト4|4強/.test(a))return '<span class="md b">4強</span>';if(/ベスト8|8強/.test(a))return '<span class="md n">8強</span>';return '<span class="md n">・</span>';}
function sch(k){const a=[];if(k.chu)a.push(['中学',k.chu]);if(k.ko)a.push(['高校',k.ko]);if(k.dai)a.push(['大学',k.dai]);if(k.sha)a.push(['社会人',k.sha]);return a;}
function head(p){
 if(p.kind==='力士')return '<div style="display:flex;gap:16px;align-items:flex-start"><div class="fuda" style="font-size:30px;min-height:170px">'+esc(p.name)+'</div><div style="flex:1;min-width:0"><div class="rk big" style="font-size:22px;color:var(--ai);width:auto;text-align:left;background:none">'+esc(p.rank)+'</div><dl class="kv" style="margin-top:6px"><dt>部屋</dt><dd>'+esc(p.heya)+'部屋</dd><dt>初土俵</dt><dd>'+esc(p.debut)+'</dd><dt>年齢</dt><dd>'+p.age+'歳</dd><dt>体格</dt><dd>'+esc(p.body)+'</dd><dt>取り口</dt><dd>'+esc(p.style)+'</dd><dt>最高位</dt><dd>'+esc(p.best)+'</dd></dl></div></div>';
 return '<div style="display:flex;gap:16px;align-items:flex-start"><div class="fuda sk" style="font-size:30px;min-height:150px">'+esc(p.name)+'</div><div style="flex:1;min-width:0"><div style="font-size:22px;color:var(--ai);font-weight:700">'+esc(p.name)+'親方 <span class="mute kaku" style="font-size:14px">元'+esc(p.best.replace(/\d.*$/,''))+'・'+esc(p.moto)+'</span></div><dl class="kv" style="margin-top:6px"><dt>所属</dt><dd>'+esc(p.heya)+'部屋('+esc(p.role)+')</dd><dt>役職</dt><dd>'+esc(p.rank)+'</dd><dt>年齢</dt><dd>'+p.age+'歳(定年まで '+(65-p.age)+' 年)</dd><dt>最高位</dt><dd>'+esc(p.best)+'</dd><dt>襲名</dt><dd>'+esc(p.since)+'</dd></dl></div></div>';}
function rest(p){return p.kind==='力士'?'<h3>能力・状態</h3><div class="ph"></div><div class="ph" style="width:70%"></div><div class="ph" style="width:85%"></div><p class="mute kaku" style="font-size:12px">(ここから下は今の画面と同じ:能力・状態・信頼・けが など)</p>':'<h3>弟子・部屋での役目</h3><div class="ph"></div><div class="ph" style="width:60%"></div><p class="mute kaku" style="font-size:12px">(ここから下は今の画面と同じ)</p>';}
function srcLine(k){return '<p class="mute kaku" style="font-size:11px;margin-top:6px">出典:'+esc(k.src)+'。空欄は分からなかったところ。</p>';}
function sel(id){cur=id;draw();}
function pickers(){return '<div class="pk">'+P.map(p=>'<button class="'+(p.id===cur?'on':'')+'" onclick="sel(\''+p.id+'\')">'+esc(p.kind)+':'+esc(p.name)+'</button>').join('')+'</div>';}
function draw(){const p=P.find(x=>x.id===cur);document.getElementById('mbox').innerHTML='<button class="btn sm x">閉じる</button>'+body(p);document.getElementById('pkw').innerHTML=pickers();}
window.onload=draw;
"""

EXTRA_CSS = r"""
#mdl{display:flex}
.tagS{position:fixed;left:8px;bottom:6px;font:12px sans-serif;background:rgba(0,0,0,.65);color:#fff;padding:3px 8px;border-radius:3px;z-index:80}
#pkw{position:fixed;top:6px;right:6px;z-index:80}.pk{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.pk button{font:12px sans-serif;background:rgba(0,0,0,.6);color:#fff;border:1px solid #e9c46a;border-radius:999px;padding:4px 10px}.pk button.on{background:#b5361f}
#toast{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);background:rgba(20,15,10,.9);color:#fff;padding:10px 20px;border-radius:999px;font:15px sans-serif;z-index:90;opacity:0;transition:opacity .2s;pointer-events:none}#toast.on{opacity:1}
.ph{height:12px;background:#e8dfcc;border-radius:3px;margin:6px 0}
.md{display:inline-block;min-width:34px;text-align:center;font:bold 11px/18px sans-serif;border-radius:9px;margin-right:6px;color:#fff;vertical-align:1px}
.md.g{background:#b8901f}.md.s{background:#8c8f96}.md.b{background:#9a5b2c}.md.n{background:#c9bda4;color:#4a4134}
.bgfake{position:fixed;inset:0;background:#e9e0cc}
"""

def page(no, title, css, js):
    return ('<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>経歴の見本 %d</title><style>%s%s%s</style></head><body><div class="bgfake"></div>'
            '<div class="tagS">見本 kei%d:%s</div><div id="pkw"></div><div id="mdl" class="on"><div class="box" id="mbox"></div></div><div id="toast"></div>'
            '<script>%s%s</script></body></html>') % (no, CSS, EXTRA_CSS, css, no, title, COMMON_JS, js)

# 1 今の画面に「経歴」の欄を足す
j1 = r"""function body(p){const k=p.kei;let h=head(p);
 h+='<h3>経歴</h3><dl class="kv"><dt>出身地</dt><dd>'+esc(k.home||'—')+'</dd>'+sch(k).map(s=>'<dt>'+s[0]+'</dt><dd>'+esc(s[1])+'</dd>').join('')+
 (k.ama.length?'<dt>アマ時代</dt><dd>'+k.ama.map(esc).join('<br>')+'</dd>':'')+(k.fam.length?'<dt>相撲界の家族</dt><dd>'+k.fam.map(famLink).join('<br>')+'</dd>':'')+'</dl>'+srcLine(k);
 return h+rest(p);}"""

# 2 年表で見せる
c2 = r""".tl{position:relative;margin:6px 0 0 8px;padding-left:22px;border-left:3px solid var(--line);font-family:var(--kaku);font-size:14px}
.tl li{list-style:none;position:relative;margin:0 0 12px}.tl li:before{content:"";position:absolute;left:-30px;top:3px;width:13px;height:13px;border-radius:50%;background:var(--paper,#fff);border:3px solid var(--ai)}
.tl li.pro:before{background:var(--shu);border-color:var(--shu)}.tl .w{font-size:12px;color:var(--mute)}.tl b{font-size:15px}.tl .a{margin-top:3px;font-size:13px}"""
j2 = r"""function place(a,k){if(/中学/.test(a))return '中学';if(/高校|インターハイ|少年|選抜/.test(a))return '高校';if(k.dai&&!/大学院/.test(k.dai))return '大学';return k.ko?'高校':'中学';}
function body(p){const k=p.kei;let h=head(p);const S=sch(k);const by={};k.ama.forEach(a=>{const w=place(a,k);(by[w]=by[w]||[]).push(a);});
 h+='<h3>歩み</h3><ul class="tl"><li><span class="w">生まれ</span><br><b>'+esc(k.home||'—')+'</b></li>'+S.map(s=>'<li><span class="w">'+s[0]+'</span><br><b>'+esc(s[1])+'</b>'+((by[s[0]]||[]).map(a=>'<div class="a">'+medal(a)+esc(a)+'</div>').join(''))+'</li>').join('');
 if(p.kind==='力士')h+='<li class="pro"><span class="w">'+esc(p.debut)+'</span><br><b>'+esc(p.heya)+'部屋に入門・初土俵</b></li><li class="pro"><span class="w">いま</span><br><b>'+esc(p.rank)+'</b>(最高位 '+esc(p.best)+')</li>';
 else h+='<li class="pro"><span class="w">現役</span><br><b>'+esc(p.moto)+'・最高位 '+esc(p.best)+'</b></li><li class="pro"><span class="w">'+esc(p.since)+'</span><br><b>年寄「'+esc(p.name)+'」を襲名</b></li>';
 h+='</ul>'+(k.fam.length?'<h3>相撲界の家族</h3><p class="kaku" style="font-size:14px">'+k.fam.map(famLink).join('・')+'</p>':'')+srcLine(k);return h+rest(p);}"""

# 3 タブで分ける
c3 = r""".tabs{display:flex;gap:0;margin:12px 0 0;border-bottom:2px solid var(--ai)}.tabs button{flex:1;font:15px var(--kaku);padding:9px 4px;background:#efe5cf;border:1px solid var(--line);border-bottom:none;border-radius:6px 6px 0 0;color:var(--sumi2)}
.tabs button.on{background:var(--ai);color:#fff;border-color:var(--ai)}.tbx{border:1px solid var(--line);border-top:none;padding:10px 12px;background:rgba(255,255,255,.5)}
.blk{margin-bottom:10px}.blk .t{font:12px var(--kaku);color:var(--mute);margin-bottom:2px}.blk .v{font:15px var(--kaku)}"""
j3 = r"""let tab=1;function st(n){tab=n;draw();}
function body(p){const k=p.kei;let h=head(p);const T=p.kind==='力士'?['能力・状態','経歴','記録']:['部屋での役目','経歴','記録'];
 h+='<div class="tabs">'+T.map((t,i)=>'<button class="'+(i===tab?'on':'')+'" onclick="st('+i+')">'+t+'</button>').join('')+'</div><div class="tbx">';
 if(tab===1){h+='<div class="blk"><div class="t">出身地</div><div class="v">'+esc(k.home||'—')+'</div></div><div class="blk"><div class="t">学校・社会人</div><div class="v">'+(sch(k).map(s=>s[0]+':'+esc(s[1])).join('<br>')||'—')+'</div></div>'+
  (k.ama.length?'<div class="blk"><div class="t">アマ時代の主な成績</div><div class="v">'+k.ama.map(a=>medal(a)+esc(a)).join('<br>')+'</div></div>':'')+
  (k.fam.length?'<div class="blk"><div class="t">相撲界の家族</div><div class="v">'+k.fam.map(famLink).join('<br>')+'</div></div>':'')+srcLine(k);}
 else h+='<div class="ph"></div><div class="ph" style="width:70%"></div><div class="ph" style="width:85%"></div><p class="mute kaku" style="font-size:12px">(今の画面の中身がここに入ります)</p>';
 return h+'</div>';}"""

# 4 経歴カード(学校の札・成績の印・家族の図)
c4 = r""".kc{border:1px solid var(--line);border-radius:6px;background:linear-gradient(#fffdf7,#f6efdf);padding:10px 12px;margin-top:10px;font-family:var(--kaku)}
.kc .home{font-size:15px}.kc .home:before{content:"◆ ";color:var(--shu)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.chip{border:1.5px solid var(--ai);border-radius:999px;padding:3px 10px;font-size:13px;background:#fff}.chip i{font-style:normal;font-size:11px;color:#fff;background:var(--ai);border-radius:999px;padding:0 6px;margin-right:5px}
.amal{font-size:13px;line-height:1.9}.tree{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px}.tree .me{border:2px solid var(--shu);background:#fff;padding:4px 10px;border-radius:4px;font-weight:700}
.tree .fm{border:1px solid var(--line);background:#fff;padding:3px 8px;border-radius:4px;font-size:13px}.tree .fm small{display:block;font-size:10px;color:var(--mute)}"""
j4 = r"""function body(p){const k=p.kei;let h=head(p);
 h+='<div class="kc"><div class="home">'+esc(k.home||'—')+' 出身</div><div class="chips">'+(sch(k).map(s=>'<span class="chip"><i>'+s[0]+'</i>'+esc(s[1])+'</span>').join('')||'<span class="mute" style="font-size:13px">学校は分かっていません</span>')+'</div>'+
 (k.ama.length?'<div class="amal">'+k.ama.map(a=>medal(a)+esc(a)).join('<br>')+'</div>':'')+
 (k.fam.length?'<div class="tree"><span class="me">'+esc(p.name)+'</span>'+k.fam.map(f=>{const m=f.split(':');return '<span class="fm"><small>'+esc(m[0])+'</small>'+famLink(f).replace(/^[^:]+:/,'')+'</span>';}).join('')+'</div>':'')+srcLine(k)+'</div>';
 return h+rest(p);}"""

S = [(1, '今の画面に「経歴」の欄を足す', '', j1), (2, '年表(歩み)で見せる', c2, j2), (3, 'タブで「経歴」を分ける', c3, j3), (4, '経歴カード(学校の札・成績の印・家族の図)', c4, j4)]
for no, t, c, j in S:
    open(OUT + 'kei%d.html' % no, 'w', encoding='utf-8').write(page(no, t, c, j))
print('ok')

# 5 タブ(kei3)の「経歴」の中身を経歴カード(kei4)にする
j5 = r"""let tab=1;function st(n){tab=n;draw();}
function card(p,k){return '<div class="kc" style="margin-top:0"><div class="home">'+esc(k.home||'—')+' 出身</div><div class="chips">'+(sch(k).map(s=>'<span class="chip"><i>'+s[0]+'</i>'+esc(s[1])+'</span>').join('')||'<span class="mute" style="font-size:13px">学校は分かっていません</span>')+'</div>'+
 (k.ama.length?'<div class="amal">'+k.ama.map(a=>medal(a)+esc(a)).join('<br>')+'</div>':'')+
 (k.fam.length?'<div class="tree"><span class="me">'+esc(p.name)+'</span>'+k.fam.map(f=>{const m=f.split(':');return '<span class="fm"><small>'+esc(m[0])+'</small>'+famLink(f).replace(/^[^:]+:/,'')+'</span>';}).join('')+'</div>':'')+srcLine(k)+'</div>';}
function card2(p,k){return '<div class="kc" style="margin-top:0">'+(k.ama.length?'<div class="amal">'+k.ama.map(a=>medal(a)+esc(a)).join('<br>')+'</div>':'<p class="mute" style="font-size:13px">アマ時代の成績は分かっていません</p>')+(k.fam.length?'<div class="tree"><span class="me">'+esc(p.name)+'</span>'+k.fam.map(f=>{const m=f.split(':');return '<span class="fm"><small>'+esc(m[0])+'</small>'+famLink(f).replace(/^[^:]+:/,'')+'</span>';}).join('')+'</div>':'')+srcLine(k)+'</div>';}
function body(p){const k=p.kei;let h=head(p);const T=p.kind==='力士'?['能力・状態','経歴','記録']:['部屋での役目','経歴','記録'];
 h+='<div class="tabs">'+T.map((t,i)=>'<button class="'+(i===tab?'on':'')+'" onclick="st('+i+')">'+t+'</button>').join('')+'</div><div class="tbx">';
 if(tab===1)h+=card(p,k);else h+='<div class="ph"></div><div class="ph" style="width:70%"></div><div class="ph" style="width:85%"></div><p class="mute kaku" style="font-size:12px">(今の画面の中身がここに入ります)</p>';
 return h+'</div>';}"""
# 6 名前の下に学校の札だけをいつも出し、くわしい経歴はタブの中のカードで
j6 = j5.replace("""let h=head(p);const T""","""let h=head(p);h+='<div class="chips" style="margin:10px 0 0"><span class="chip" style="border-color:var(--shu)"><i style="background:var(--shu)">出身</i>'+esc(k.home||'—')+'</span>'+sch(k).map(s=>'<span class="chip"><i>'+s[0]+'</i>'+esc(s[1])+'</span>').join('')+'</div>';const T""")
j6 = j6.replace("if(tab===1)h+=card(p,k);","if(tab===1)h+=card2(p,k);")
S += [(5, 'タブ+経歴カード(kei3+kei4)', c3+c4, j5), (6, '学校の札はいつも見せる+タブの中に経歴カード', c3+c4, j6)]
for no, t, c, j in S[4:]:
    open(OUT + 'kei%d.html' % no, 'w', encoding='utf-8').write(page(no, t, c, j))
print('ok')
