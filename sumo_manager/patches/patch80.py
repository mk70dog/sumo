# v76 -> v77:字 Dela Gothic One(取組の前の画像・番付表・四股名)+取組の前の画像(見本 int1・dfc、ダルマさん「これで OK」)
# 字:本物の相撲字は無料のフォントがないため、OFL の Dela Gothic One(Copyright 2020 The Dela Gothic Project Authors)を、ゲームで使う字だけに減らして埋め込む(fonts/Dela-sub.woff2、0.2MB)。
# 取組の前の画像:中継の題字と両力士の名前の画面を参考に、局の名前・枠の飾りはまねずに錦絵の背景と金の枠で作る。①題字「大相撲 幕内 ○日目」②両力士(番付・出身・部屋・その取組の前の成績)→ 取組。押すと飛ばせる。同じ取組の「もう一度見る」では出さない。
import sys, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v76</title>', '<title>Sumo Manager v77</title>')
rep("const APPV=76;\nconst SAVE='sumoManager76',SAVE75", "const APPV=77;\nconst SAVE='sumoManager77',SAVE76='sumoManager76',SAVE75")
rep('[SAVE75,SAVE74', '[SAVE76,SAVE75,SAVE74')
rep(" return g.v===76?g:null;}", " if(g.v===76){g.v=77;}\n return g.v===77?g:null;}")
rep('G={v:76,', 'G={v:77,')
F = base64.b64encode(open('fonts/Dela-sub.woff2','rb').read()).decode()
CSS = ('<!-- Dela Gothic One: Copyright 2020 The Dela Gothic Project Authors (https://github.com/syakuzen/DelaGothic). SIL Open Font License 1.1. ゲームで使う字だけに減らして埋め込み -->\n'
 '<style id="fontDela">@font-face{font-family:Dela;src:url(data:font/woff2;base64,' + F + ') format("woff2")}'
 '.itt,.itm,.it2,.itt *,.itm *,.it2 *,.bz,.bz *,.fuda,.nm{font-family:Dela,sans-serif!important;font-weight:400!important}svg .nm,svg .nm *,svg text{font-family:inherit!important;font-weight:inherit!important}'
 '.ito{container-type:inline-size;position:absolute;inset:0;z-index:20;overflow:hidden;border-radius:6px;background:#120d08 center/cover;display:flex;align-items:center;justify-content:center;transition:opacity .4s;cursor:pointer}'
 '.ito:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,.25),rgba(0,0,0,.72))}.ito>*{position:relative;z-index:1}'
 '.ifr{position:absolute;inset:8px;border:3px solid #c9a24a;outline:1px solid #c9a24a;outline-offset:4px;border-radius:4px;z-index:2;pointer-events:none}'
 '.itt{text-align:center;color:#fff;text-shadow:0 0 6px #000,0 3px 0 #000,3px 0 0 #000,-3px 0 0 #000,0 -3px 0 #000}.itt .s{font-size:6cqw;letter-spacing:.5em;margin-bottom:4px}.itt .b{font-size:28cqw;line-height:1;letter-spacing:.05em}'
 '.itt .d{display:inline-block;margin-top:10px;font-size:9cqw;letter-spacing:.35em;border:3px solid #fff;border-radius:14px;padding:2px 10px 2px 22px;box-shadow:0 0 0 2px #000}'
 '.itm{position:absolute;inset:0;display:grid;grid-template-columns:auto 1fr auto auto 1fr auto;align-items:center;padding:7% 6%;gap:1%;color:#fff;text-shadow:0 0 6px #000,2px 2px 0 #000,-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000}'
 '.itm .rk{writing-mode:vertical-rl;color:#f3c64a;font-size:5.2cqw;letter-spacing:.1em}.itm .rk small{display:block;color:#fff;font-size:.65em;margin-top:.6em;letter-spacing:0}'
 '.itm .nm{writing-mode:vertical-rl;font-size:14cqw;line-height:1;justify-self:center}.itm .rc{writing-mode:vertical-rl;color:#f3c64a;font-size:5.6cqw;display:flex;gap:.3em}.itm .rc span{display:block}'
 '.ito .skip{position:absolute;right:12px;bottom:10px;z-index:3;font:12px sans-serif;color:#fffc}</style>\n')
JS = r'''<script>
/* v77:取組の前の画像(題字 → 両力士 → 取組) */
(function(){const KN='〇一二三四五六七八九十';
 const kj=n=>n<=10?KN[n]:n<20?'十'+KN[n-10]:KN[Math.floor(n/10)]+'十'+(n%10?KN[n%10]:'');
 const DV=['幕内','十両','幕下','三段目','序二段','序ノ口'];let BG=null;
 function bg(){if(BG!=null)return BG;const t=document.createElement('div');t.className='st-bg1';t.style.display='none';document.body.appendChild(t);BG=getComputedStyle(t).backgroundImage||'none';t.remove();return BG;}
 const dayName=d=>d>=15?'千秋楽':d===1?'初日':d===8?'中日':kj(d)+'日目';
 function rec(r,b){const c=G.B&&G.B.rec&&G.B.rec[r.id];if(!c)return null;let w=c.w,l=c.l+(c.ab||0);if(b.w===r.id)w--;else l--;return [Math.max(0,w),Math.max(0,l)];}
 const recH=x=>!x?'':(x[1]===0?'<span>'+kj(x[0])+'勝</span>':'<span>'+kj(x[0])+'勝</span><span>'+kj(x[1])+'敗</span>');
 const rk=r=>(r.rk||'').replace(/^[東西]/,'').replace(/[0-9]+/,m=>kj(+m)+'枚目');
 const side=r=>'<div class="rk">'+esc(rk(r))+'<small>'+esc(r.home||'')+'・'+esc(G.heya[r.h].n)+'</small></div>';
 const seen=new Set();const orig=dhRun;
 dhRun=function(id,b){const wr=document.getElementById(id+'w');const day=G.B?G.B.day:0;const key=b?b.w+'-'+b.l+'-'+G.bnum+'-'+day:'';
  if(!wr||!b||!G.B||seen.has(key)){orig(id,b);return;}seen.add(key);
  const p=dhPick(b),E=p.E,W=p.Wt;const o=document.createElement('div');o.className='ito';o.style.backgroundImage=bg();wr.appendChild(o);let done=0;
  const fin=()=>{if(done)return;done=1;o.style.opacity=0;setTimeout(()=>o.remove(),400);orig(id,b);};o.onclick=fin;
  o.innerHTML='<div class="ifr"></div><div class="itt"><div class="s">大相撲</div><div class="b">'+DV[Math.min(E.d,W.d)]+'</div><div class="d">'+dayName(day)+'</div></div><div class="skip">押すと飛ばせます</div>';
  setTimeout(()=>{if(done)return;o.innerHTML='<div class="ifr"></div><div class="itm">'+side(E)+'<div class="nm">'+esc(E.n)+'</div><div class="rc">'+recH(rec(E,b))+'</div><div class="rc">'+recH(rec(W,b))+'</div><div class="nm">'+esc(W.n)+'</div>'+side(W)+'</div><div class="skip">押すと飛ばせます</div>';},1500);
  setTimeout(fin,4200);};})();
</script>
'''
i = s.rfind('</body>')
s = s[:i] + CSS + JS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
