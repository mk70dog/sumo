# v72 -> v73:候補 ①推移グラフの総合を師匠の見立てに ②記者の記事を場所ごとのニュースに ③ひとことの言い回しを増やす(ダルマさん「候補を実施」)
# 数値・言い回しの条件はすべて推定。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v72</title>', '<title>Sumo Manager v73</title>')
rep("const APPV=72;\nconst SAVE='sumoManager72',SAVE71", "const APPV=73;\nconst SAVE='sumoManager73',SAVE72='sumoManager72',SAVE71")
rep('[SAVE71,SAVE70', '[SAVE72,SAVE71,SAVE70')
rep(" if(g.v===71){g.kpol=g.kpol||'nin';g.v=72;}\n return g.v===72?g:null;}", " if(g.v===71){g.kpol=g.kpol||'nin';g.v=72;}\n if(g.v===72){g.v=73;}\n return g.v===73?g:null;}")
rep('G={v:72,', 'G={v:73,')

# ① 週の記録に週番号(見立ての揺れに使う)
rep("o:Math.round(ovr(r)*10)/10,m:Math.round(r.mor)});", "o:Math.round(ovr(r)*10)/10,m:Math.round(r.mor),n:G.wn});")
rep("<div>総合 '+spark(wl.map(x=>x.o),", "<div>総合(師匠の見立て) '+spark(wl.map((x,i)=>hyTrend(r,x,i)),")

# ② 記者の記事:文章だけの版を作り、画面とニュースで使う
rep("function kiCom(r){const lh=r.hist[r.hist.length-1];if(r.d>2||!lh)return '<div class=\"cm\">記者はまだ取材に来ていません(幕下より上になると記事が出ます)。</div>';",
    """function hyTrend(r,x,i){const e=hyErr(r,(me().oy||{}).meki);return x.o+.8+hyN(r,9,0)*e+(hhR(r.id,400+(x.n!=null?x.n:i))-.5)*.25*e;}
function kiTxt(r){const lh=r.hist[r.hist.length-1];if(r.d>2||!lh)return '';const A=hyAvg(r.d);const ks=['tac','tsk','mig','hid','yor','nag','hik','tgw'];const sc=ks.map(k=>[k,aVal(r,k)-A[k]+hyN(r,7,AK.indexOf(k))*1.6]).sort((a,b)=>b[1]-a[1]);
 const nm=k=>(AT.find(x=>x[0]===k)||[0,k])[1];const w=lh.w,l=lh.l+(lh.ab||0);
 const f=lh.yu?'見事な優勝。文句なしの内容':(lh.ab>0&&lh.ab>=lh.w+lh.l)?'休場が響いた。まずは体を治したい':w>=11?'好調。上位でも十分に通用する':w>=8?'勝ち越しは安定してきた':w>=6?'もうひと息で勝ち越し':'精彩を欠いた';
 return f+'。持ち味は'+nm(sc[0][0])+'。'+(sc[sc.length-1][1]<-1?'ただ'+nm(sc[sc.length-1][0])+'に課題が残る':'大きな穴は見当たらない');}
function kiNews(){const L=own().filter(r=>r.d<=2&&r.hist.length&&r.hist[r.hist.length-1].b===G.bnum).map(r=>{const lh=r.hist[r.hist.length-1];return [r,(r.d<=1?3:0)+Math.abs(lh.w-7.5)+(lh.yu?5:0)];}).sort((a,b)=>b[1]-a[1]).slice(0,2);
 L.forEach(([r])=>{const lh=r.hist[r.hist.length-1];addNews('〔記者の記事〕'+r.n+'('+lh.rk+'・'+lh.w+'勝'+(lh.l+(lh.ab||0))+'敗):「'+kiTxt(r)+'」');});}
function kiCom(r){const lh=r.hist[r.hist.length-1];if(r.d>2||!lh)return '<div class="cm">記者はまだ取材に来ていません(幕下より上になると記事が出ます)。</div>';""")
rep("function v12Basho(sum){", "function v12Basho(sum){kiNews();")

# ③ ひとことを増やす(出来事が先。カードには 1 つめが出る)
rep("function keyCom(r){if(r.h!==0||!r.cap)return [];const L=[];",
    """function keyEv(r){const lh=r.hist[r.hist.length-1],h2=r.hist[r.hist.length-2];
 if(r.inj)return r.inj.s>=2?['今はけがを治すのが先です','m']:['けがを抱えながらよくやっています','n'];
 if(G.bnum-(r.join||0)<=3&&r.d>=3)return ['部屋の暮らしにも慣れてきました','n'];
 if(lh&&G.phase!=='basho'&&lh.b===G.bnum){if(r.d<=1&&lh.d>=2)return ['関取になって顔つきが変わりました','s'];if(r.d===0&&lh.d===1)return ['幕内でも十分にやれます','s'];if(r.d>=2&&lh.d<=1)return ['悔しさを糧に、すぐ戻ってほしい','m'];}
 if(lh&&lh.yu)return ['優勝して自信をつけました','s'];
 if(r.hist.length>=3&&r.hist.slice(-3).every(x=>x.w>(x.l+(x.ab||0))))return ['安定して勝ち越せるようになりました','g'];
 if(lh&&lh.w>=11)return ['先場所の勢いが続いています','s'];
 if(lh&&h2&&lh.w<(lh.l+(lh.ab||0))&&h2.w<(h2.l+(h2.ab||0)))return ['負けが込んで、少し自信をなくしています','m'];
 if(r.mor<30)return ['少し元気がありません','m'];if(r.cond>=85)return ['今が絶好調です','s'];
 return null;}
function keyCom(r){if(r.h!==0||!r.cap)return [];const L=[];const ev=keyEv(r);if(ev)L.push(ev);""")
rep("function keyH(r,n){return keyCom(r).slice(0,n||2)", "function keyH(r,n){return keyCom(r).slice(0,n||3)")
rep('.sts .w5{font-size:11px;letter-spacing:-.5px}', '.sts .w5{font-size:10px;letter-spacing:-1px}')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
