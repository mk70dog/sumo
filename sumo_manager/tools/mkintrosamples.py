# 見本 int1〜2:取組の動画の初めに出す画像(ダルマさんの例:中継の題字「幕内 千秋楽」と、両力士の名前を大きく出す画面)
# 中継の画面そのもの(局の名前・枠の飾り)はまねず、ゲームの錦絵と色で作る。v76 に見本用の表示だけを足す。
base=open('sumo_manager_v76.html',encoding='utf-8').read()
CSS='''<style>
.ito{container-type:inline-size;position:absolute;inset:0;z-index:20;overflow:hidden;border-radius:6px;background:#120d08 center/cover;display:flex;align-items:center;justify-content:center;transition:opacity .4s;cursor:pointer}
.ito:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,.25),rgba(0,0,0,.72))}
.ito>*{position:relative;z-index:1}
.ifr{position:absolute;inset:8px;border:3px solid #c9a24a;outline:1px solid #c9a24a;outline-offset:4px;border-radius:4px;z-index:2;pointer-events:none}
.itt{text-align:center;color:#fff;font-family:'SMin',serif;font-weight:900;text-shadow:0 0 6px #000,0 3px 0 #000,3px 0 0 #000,-3px 0 0 #000,0 -3px 0 #000}
.itt .s{font-size:6cqw;letter-spacing:.5em;margin-bottom:4px}
.itt .b{font-size:28cqw;line-height:1;letter-spacing:.05em}
.itt .d{display:inline-block;margin-top:10px;font-size:9cqw;letter-spacing:.35em;border:3px solid #fff;border-radius:14px;padding:2px 10px 2px 22px;box-shadow:0 0 0 2px #000}
.itm{position:absolute;inset:0;display:grid;grid-template-columns:auto 1fr auto auto 1fr auto;align-items:center;padding:7% 6%;gap:1%;font-family:'SMin',serif;font-weight:900;color:#fff;text-shadow:0 0 6px #000,2px 2px 0 #000,-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000}
.itm .rk{writing-mode:vertical-rl;color:#f3c64a;font-size:5.2cqw;letter-spacing:.1em}
.itm .rk small{display:block;color:#fff;font-size:.65em;margin-top:.6em;letter-spacing:0}
.itm .nm{writing-mode:vertical-rl;font-size:14cqw;line-height:1;justify-self:center}
.itm .rc{writing-mode:vertical-rl;color:#f3c64a;font-size:5.6cqw;display:flex;gap:.3em}
.itm .rc span{display:block}
.it2{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;font-family:'SMin',serif;font-weight:900;color:#fff}
.it2>div{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-shadow:0 0 6px #000,2px 2px 0 #000}
.it2 .e{background:linear-gradient(90deg,rgba(28,48,92,.85),rgba(28,48,92,.35))}.it2 .w{background:linear-gradient(270deg,rgba(150,36,30,.85),rgba(150,36,30,.35))}
.it2 .side{font-size:4.4cqw;letter-spacing:.4em;color:#f3c64a}.it2 .nm{font-size:10cqw;line-height:1.05}.it2 .rk{font-size:4.4cqw}.it2 .rc{font-size:5.5cqw;color:#f3c64a}
.it2 .vs{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:7cqw;color:#fff;background:#000a;border:2px solid #c9a24a;border-radius:50%;width:1.8em;height:1.8em;display:flex;align-items:center;justify-content:center}
.it2 .ttl{position:absolute;left:0;right:0;top:4%;text-align:center;font-size:4.4cqw;letter-spacing:.3em}
.skip{position:absolute;right:12px;bottom:10px;z-index:3;font:12px sans-serif;color:#fffc}
</style>'''
JS=r'''
<script>
(function(){
const V='__V__';const KN='〇一二三四五六七八九十';
const kj=n=>n<=10?KN[n]:n<20?'十'+KN[n-10]:KN[Math.floor(n/10)]+'十'+(n%10?KN[n%10]:'');
function bg(){const t=document.createElement('div');t.className='st-bg1';document.body.appendChild(t);const u=getComputedStyle(t).backgroundImage;t.remove();return u;}
function dayName(d){return d>=15?'千秋楽':d===1?'初日':d===8?'中日':kj(d)+'日目';}
function rec(r,b){const c=G.B.rec[r.id];let w=c.w,l=c.l+c.ab;if(b.w===r.id)w--;else l--;return [w,l];}
function recTxt(x){return x[1]===0?['<span>'+kj(x[0])+'勝</span>']:['<span>'+kj(x[0])+'勝</span>','<span>'+kj(x[1])+'敗</span>'];}
function rk(r){return (r.rk||'').replace(/^[東西]/,'').replace(/[0-9]+/,m=>kj(+m)+'枚目');}
function card1(o){o.innerHTML='<div class="ifr"></div><div class="itt"><div class="s">大相撲</div><div class="b">幕内</div><div class="d">'+dayName(G.B.day)+'</div></div><div class="skip">押すと飛ばせます</div>';}
function card2(o,b){const p=dhPick(b);const E=p.E,W=p.Wt;const re=rec(E,b),rw=rec(W,b);
 if(V==='int1')o.innerHTML='<div class="ifr"></div><div class="itm"><div class="rk">'+esc(rk(E))+'<small>'+esc(E.home)+'・'+esc(G.heya[E.h].n)+'</small></div><div class="nm">'+esc(E.n)+'</div><div class="rc">'+recTxt(re).join('')+'</div><div class="rc">'+recTxt(rw).join('')+'</div><div class="nm">'+esc(W.n)+'</div><div class="rk">'+esc(rk(W))+'<small>'+esc(W.home)+'・'+esc(G.heya[W.h].n)+'</small></div></div><div class="skip">押すと飛ばせます</div>';
 else o.innerHTML='<div class="it2"><div class="e"><div class="side">東</div><div class="nm">'+esc(E.n)+'</div><div class="rk">'+esc(rk(E))+'・'+esc(G.heya[E.h].n)+'</div><div class="rc">'+re[0]+'勝'+re[1]+'敗</div></div><div class="w"><div class="side">西</div><div class="nm">'+esc(W.n)+'</div><div class="rk">'+esc(rk(W))+'・'+esc(G.heya[W.h].n)+'</div><div class="rc">'+rw[0]+'勝'+rw[1]+'敗</div></div><div class="vs">対</div><div class="ttl">大相撲 幕内 '+dayName(G.B.day)+'</div></div><div class="skip">押すと飛ばせます</div>';
}
const orig=window.dhRun;window.__stage=0;
window.dhRun=function(id,b){const wr=document.getElementById(id+'w');if(!wr||!b){orig(id,b);return;}
 const o=document.createElement('div');o.className='ito';o.style.backgroundImage=bg();wr.appendChild(o);let done=0;
 const go=()=>{if(done)return;done=1;o.style.opacity=0;setTimeout(()=>o.remove(),400);orig(id,b);};o.onclick=go;
 if(V==='int1'){card1(o);window.__stage=1;setTimeout(()=>{if(!done){card2(o,b);window.__stage=2;}},1500);setTimeout(go,4200);}
 else{card2(o,b);window.__stage=2;setTimeout(go,3000);}};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;while(G.phase==='train')doWeek();for(let d=0;d<13;d++)advanceDay();go('basho');stepDay();setTimeout(()=>{dhOpen('t',0);},300);}catch(e){console.error(e)}},400);});
})();
</script>
'''
NOTE={'int1':'int1:①題字「大相撲 幕内 千秋楽」→ ②両力士の名前を縦書きで大きく(番付・出身・部屋・成績)→ 取組','int2':'int2:東西に分けて名前と成績を並べる 1 枚だけ → 取組'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'</div></body>',1)
    s=s.replace('<title>Sumo Manager v76</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
