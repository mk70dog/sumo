# v71 -> v72:設計 20「見立て・研究と助言・相性」(見本 hyo1+ken3、ダルマさん「お任せで実施」)
# 能力の数字は裏に残し(計算はそのまま)、画面は「人の見立て」にする。研究・助言・苦手意識・体重差は取組に少し効く。
# 出典:Number 2025/3/1(二所ノ関親方〈元稀勢の里〉は苦手の栃東に仕切り位置を変えるなど対策)、Number 2022/4/22(二所ノ関部屋の映像研究と稽古)。
# ひとこと(ダビスタ風):ダルマさんの追加の要望(2026-11-19)。素質の見立て+8 週の伸び+年齢から決まった言い回し。
# 数値はすべて推定(評価の癖・誤差、研究 最大 +0.3〈映像の方針で +0.1〉、助言 +0.15、苦手意識 −0.4、体重差 40kg 以上で ±0.3)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

rep('<title>Sumo Manager v71</title>', '<title>Sumo Manager v72</title>')
rep("const APPV=71;\nconst SAVE='sumoManager71',SAVE70", "const APPV=72;\nconst SAVE='sumoManager72',SAVE71='sumoManager71',SAVE70")
rep('[SAVE70,SAVE69', '[SAVE71,SAVE70,SAVE69')
rep(" if(g.v===70){mig71(g);g.v=71;}\n return g.v===71?g:null;}", " if(g.v===70){mig71(g);g.v=71;}\n if(g.v===71){g.kpol=g.kpol||'nin';g.v=72;}\n return g.v===72?g:null;}")
rep('G={v:71,', 'G={v:72,')

CORE = r'''
/* v72:見立て(人の評価)。裏の数字は今のまま。誤差と癖は推定 */
function aVal(r,k){return k==='kos'||k==='mae'?atTot(r,k):r.a[k];}
let _hyA={};function hyAvg(d){const key=d+'_'+G.bnum+'_'+(G.wn||0)+'_'+(G.B&&G.B.day||0);if(_hyA.key!==key)_hyA={key:key};if(_hyA[d])return _hyA[d];
 const L=Object.values(G.R).filter(x=>x&&!x.ret&&x.a&&x.d===d);const A={};AK.forEach(k=>{A[k]=L.length?L.reduce((a,x)=>a+aVal(x,k),0)/L.length:12;});A._o=L.length?L.reduce((a,x)=>a+ovr(x),0)/L.length:10;return _hyA[d]=A;}
const HYW=[['すばらしい','s'],['良い','g'],['ふつう','n'],['物足りない','m'],['課題','k']];
function hyWi(d){return d>=2.5?0:d>=1?1:d>=-1?2:d>=-2.5?3:4;}
function hyH(d){const w=HYW[hyWi(d)];return '<span class="w5 '+w[1]+'">'+w[0]+'</span>';}
function hyN(r,s,i){return (hhR(r.id,s*37+i+5)-.5)*2;}
function hyErr(r,meki){return (1.1-Math.min(100,kn(r))/100*.7)*cl(1.6-(meki||10)*.05,.5,1.6);}
function hySeeO(r){if(r.h===0)return ovr(r)+.8+hyN(r,9,0)*hyErr(r,(me().oy||{}).meki);const e=Math.max(.6,2.4-(G.staff.filter(s=>s.role==='sc').length*.4));return ovr(r)+hyN(r,8,0)*e*.6;}
function hyOW(r){return hyH(hySeeO(r)-hyAvg(r.d)._o);}
function coSp(s){return s.sk.osh>=s.sk.yot+2?'osh':s.sk.waz>=Math.max(s.sk.osh,s.sk.yot)+2?'waz':'yot';}
function evals(r){const L=[];const oy=me().oy||{};
 L.push({k:'oy',n:'師匠',d:oyN()+'。全部見るが、自分の弟子は甘めに見がち',f:(k,i)=>aVal(r,k)+.8+hyN(r,1,i)*hyErr(r,oy.meki)*1.3});
 G.staff.filter(s=>s.role==='co').slice(0,3).forEach((s,j)=>{const sp=coSp(s);const nm={osh:'押し',yot:'四つ',waz:'技'}[sp];
  L.push({k:'co'+s.sid,n:s.n,d:'部屋付き親方。'+nm+'の目は確か、ほかは見立てが粗い',f:(k,i)=>aVal(r,k)+hyN(r,2+j,i)*hyErr(r,s.sk.meki)*(CAT[k]===sp?.35:1.8)});});
 L.push({k:'tr',n:'トレーナー',d:G.con&&G.con.gym?'トレーニングジム(外部契約)。体の項目を測定して数字で出す':'トレーニングジムと契約すると、体の項目を測ってもらえます(「スタッフ」の外部契約)',num:1,f:(k)=>G.con&&G.con.gym&&['str','exp','end','flx','rec'].includes(k)?Math.round(r.a[k]):null});
 if(me().ic>=0){const n=r.dekN||0;L.push({k:'ic',n:'一門の親方',d:n?IC[me().ic]+'一門の親方。出稽古で '+n+' 週肌を合わせた(回数が多いほど確か)':'出稽古をすると、一門の親方の見立てが聞けます',f:(k,i)=>n&&['tac','tsk','mae','mig','hid','yor','kos','tos','gam'].includes(k)?aVal(r,k)+hyN(r,6,i)*cl(2.2-n*.15,.4,2.2):null});}
 L.push({k:'ki',n:'記者',d:'相撲担当の記者。最近の成績と人気に引っぱられる',f:()=>null,ki:1});return L;}
function kiCom(r){const lh=r.hist[r.hist.length-1];if(r.d>2||!lh)return '<div class="cm">記者はまだ取材に来ていません(幕下より上になると記事が出ます)。</div>';
 const A=hyAvg(r.d);const ks=['tac','tsk','mig','hid','yor','nag','hik','tgw'];const sc=ks.map(k=>[k,aVal(r,k)-A[k]+hyN(r,7,AK.indexOf(k))*1.6]).sort((a,b)=>b[1]-a[1]);
 const nm=k=>(AT.find(x=>x[0]===k)||[0,k])[1];const w=lh.w,l=lh.l+(lh.ab||0);
 const f=w>=11?'好調。上位でも十分に通用する':w>=8?'勝ち越しは安定してきた':w>=6?'もうひと息で勝ち越し':'精彩を欠いた';
 return '<div class="cm"><div class="wh">記者の記事(前の場所 '+w+'勝'+l+'敗)</div>「'+f+'。持ち味は'+nm(sc[0][0])+'。'+(sc[sc.length-1][1]<-1?'ただ'+nm(sc[sc.length-1][0])+'に課題が残る':'大きな穴は見当たらない')+'」</div>';}
const HYG=[['体',['str','exp','end','flx','rec','kos']],['押し',['tac','tsk','mae','hik']],['四つ',['mig','hid','yor']],['技',['nag','ash','tgw']],['心',['tos','rei','sho','gam']]];
function hyBody(r){const E=evals(r);const e=E.find(x=>x.k===UI.hyo)||E[0];const A=hyAvg(r.d);const nm=k=>(AT.find(x=>x[0]===k)||[0,k])[1];
 let h='<div class="evb">'+E.map(x=>'<button class="'+(x.k===e.k?'on':'')+'" onclick="hySel('+r.id+',\''+x.k+'\')">'+esc(x.n)+'</button>').join('')+'</div><div class="who">'+esc(e.d)+'</div>';
 if(e.ki)return h+kiCom(r);
 return h+'<div class="hy">'+HYG.map(([g,ks])=>'<div class="bx"><h4>'+g+'</h4>'+ks.map(k=>{const x=e.f(k,AK.indexOf(k));const pen=injPen(r,k);
  return '<div class="hr"><span>'+nm(k)+(pen>=.5?'<i class="shu" style="font-style:normal;font-size:11px" title="けがの影響"> けが</i>':'')+'</span>'+(x==null?'<span class="q">―</span>':e.num?'<b>'+x+'</b>':hyH(x-A[k]))+'</div>';}).join('')+'</div>').join('')+'</div>';}
function hySel(id,k){UI.hyo=k;const r=G.R[id];const o=document.getElementById('hyo');if(o&&r)o.innerHTML=hyBody(r);}
function hyPot(r){const [a,b]=potRange(r);const g=v=>gradeOf(v);return g(a)===g(b)?g(a):g(a)+'〜'+g(b);}
function hyoPanel(r){const co=G.staff.find(s=>s.role==='co');const oyM=(me().oy||{}).meki;
 const pc=co?gradeOf(potOf(r)+hyN(r,3,99)*hyErr(r,co.sk.meki)):null;const bf=r.bf!=null?Math.round(r.bf*100):null;
 return '<h3>能力の見立て<span class="mute kaku" style="font-size:13px;margin-left:8px">数字は測れるものだけ。ほかは人の評価(同じ地位の力士とくらべて)です</span></h3>'+
 (r.h===0?'<div class="ms">'+esc(oyN())+'のひとこと:'+keyH(r)+'</div>':'')+'<div class="ms">総合の見立て:師匠 '+hyOW(r)+(r.d<=2&&r.hist.length?'・記者 '+hyH(ovr(r)-A0(r)+(r.hist[r.hist.length-1].w-7.5)*.25+hyN(r,8,1)):'')+'</div>'+
 '<div class="ms">素質の見立て:師匠 <b>'+hyPot(r)+'</b>'+(pc?'・'+esc(co.n)+' <b>'+pc+'</b>':'')+(r.daiki?' <span class="tag shu">大器晩成</span>':'')+'<span class="mute" style="font-size:12px">(本当の素質はだれにも分かりません)</span></div>'+
 '<div class="ms">数字で分かること:'+Math.round(r.ht)+'cm・'+Math.round(r.w)+'kg'+(bf!=null?'・体脂肪 '+bf+'%':'')+(G.con&&G.con.gym?'・背筋力 '+Math.round(150+r.a.str*7)+'kg・握力 '+Math.round(40+r.a.str*2)+'kg(トレーナーの測定)':'')+'</div>'+
 '<div id="hyo">'+hyBody(r)+'</div>';}
function A0(r){return hyAvg(r.d)._o;}
/* v72:ひとこと(ダビスタ風のキーになる言い回し)。師匠の見立て(素質)と、この 8 週の伸びから */
function keyCom(r){if(r.h!==0||!r.cap)return [];const L=[];const k=kn(r);const sp=potOf(r)+hyN(r,4,0)*hyErr(r,(me().oy||{}).meki)*1.5;const g=GT[r.gt]||GT[1];
 if(k<15)L.push(['見極めはこれからです','n']);
 else if(r.age>26){const rel=hySeeO(r)-hyAvg(r.d)._o;L.push(rel>=2.5?['番付以上の力があります','s']:rel>=-1?['番付相応の力です','n']:['番付を守るのが精いっぱいです','m']);}
 else if(sp>=17)L.push(['かなりの逸材です','s']);else if(sp>=15)L.push(['大物になる器です','s']);else if(sp>=13)L.push(['関取は十分に狙えます','g']);else if(sp>=10.5)L.push(['地道にやれば番付は上がります','n']);else L.push(['正直、上は厳しいかもしれません','m']);
 const wl=r.wlog||[];const d=wl.length>=9?wl[wl.length-1].o-wl[wl.length-9].o:null;
 if(r.daiki&&G.bnum-r.daiki<=6)L.push(['急に化けてきました。遅咲きの大器かもしれません','s']);
 else if(d!=null&&d>=.5)L.push(['最近メキメキ力をつけています','s']);else if(d!=null&&d>=.2)L.push(['順調に伸びています','g']);
 else if(r.age>=g.d)L.push(['そろそろ衰えが見えてきました','m']);else if(d!=null&&d<=-.3)L.push(['力が落ちてきました','m']);
 else if(d!=null&&potOf(r)-ovr(r)<.6&&r.age<28)L.push(['伸び悩んでいます','m']);else if(r.age<=g.e-2&&potOf(r)-ovr(r)>=2)L.push(['まだまだ伸びます','g']);
 return L;}
function keyH(r,n){return keyCom(r).slice(0,n||2).map(x=>'<span class="kcm '+x[1]+'">「'+x[0]+'」</span>').join('');}

/* v72:研究と助言・苦手意識・体重差(取組の直前に効く。推定) */
const KPOL={nin:'本人に任せる',eizo:'映像でいっしょに研究する',kei:'研究より稽古で覚えさせる'};
function kenPol(r){return r.h===0?(G.kpol||'nin'):'nin';}
function kenB(r){const p=kenPol(r);if(p==='kei')return 0;return cl((r.a.ken-8)*.03,0,.3)*(p==='eizo'?1:.7)+(p==='eizo'?.1:0);}
function advMate(r,o){if(!o.h2h)return null;for(const k in o.h2h){const x=o.h2h[k];const m=G.R[k];if(m&&+k!==r.id&&m.h===r.h&&!m.ret&&x[1]>=2&&x[1]>x[0])return m;}return null;}
function h2rOf(r,o){return (r.h2r&&r.h2r[o.id])||'';}
function nigate(r,o){const t=h2rOf(r,o);return t.length>=4&&t.split('x').length-1>=4;}
function kenPrep(r,o){r._pr+=kenB(r)+(advMate(r,o)?.15:0)-(nigate(r,o)?.4:0);r._dw=(r.w||150)-(o.w||150);}
function kenH(a,o){const L=[];const st=styleName(o);const kb=kenB(a);
 if(kenPol(a)==='kei')L.push('<div class="cm"><div class="wh">親方の方針</div>研究はしない(稽古で覚えた相撲を取る)</div>');
 else if(kb>=.12)L.push('<div class="cm"><div class="wh">本人('+esc(a.n)+')・研究熱心'+(kenPol(a)==='eizo'?'・親方と映像で研究':'')+'</div>「'+(/押/.test(st)?'相手は押してくる。下からあてがって、まわしを取りに行きます':/四つ/.test(st)?'相手は四つが得意。差されないよう、先に前みつを狙います':'動きの速い相手。足を止めず、低く当たります')+'」<br><span class="mute" style="font-size:12px">→ 相手への備え(少し有利)</span></div>');
 const m=advMate(a,o);if(m)L.push('<div class="cm"><div class="wh">兄弟子・'+esc(m.n)+'('+esc(o.n)+'に勝ち越している)</div>「'+(o.a.tgw>=13?'土俵際の逆転があるから、最後まで足を止めるな':o.a.hik>=13?'引きがうまい。前に出すぎて落ちないように':'先に当たって、相手の得意の形にさせるな')+'」<br><span class="mute" style="font-size:12px">→ 少し有利</span></div>');
 const t=h2rOf(a,o);if(nigate(a,o))L.push('<div class="shu kaku" style="font-size:13px">苦手意識:この相手に直近 5 回で 4 敗以上。この相手にだけ力が少し落ちます(勝てば消えます)。</div>');
 else if(t.split('x').length-1>=3)L.push('<div class="mute kaku" style="font-size:12px">この相手には直近 '+t.length+' 回で '+(t.split('x').length-1)+' 敗。もう 1 敗すると苦手意識がつきます。</div>');
 const dw=Math.round((a.w||150)-(o.w||150));if(Math.abs(dw)>=40)L.push('<div class="mute kaku" style="font-size:12px">体重差 '+Math.abs(dw)+'kg:'+(dw<0?'軽い側なので、引き・足技・土俵際が少し効きます':'重い側なので、寄り・押しが少し効きます')+'</div>');
 return L.join('');}
function kpolH(){return '<div class="btns" style="margin:4px 0"><span class="kaku" style="font-size:13px">対戦相手の研究(親方の方針):</span>'+selH(Object.keys(KPOL).map(k=>[k,KPOL[k]]),G.kpol||'nin','setKpol(this.value)')+'</div>';}
function setKpol(v){G.kpol=v;save();render();}
'''
rep("function inb(r,k){return k==='kos'?kbOf(r)+taiOf(r)", CORE + "function inb(r,k){return k==='kos'?kbOf(r)+taiOf(r)")
# 体重差 40kg 以上:軽い側は引き・足技・土俵際、重い側は寄り・突き押し・立ち合いが少し効く(推定 +0.3)
rep("+(k==='hik'||k==='ash'||k==='tgw'?(minoOf(r)-10)*.05:0))*r._f+r._pr);}",
    "+(k==='hik'||k==='ash'||k==='tgw'?(minoOf(r)-10)*.05:0)+(r._dw!=null&&Math.abs(r._dw)>=40?(r._dw<0?(k==='hik'||k==='ash'||k==='tgw'?.3:0):(k==='yor'||k==='tsk'||k==='tac'?.3:0)):0))*r._f+r._pr);}")
rep("prepF(A,ctx.big);prepF(B,ctx.big);", "prepF(A,ctx.big);prepF(B,ctx.big);kenPrep(A,B);kenPrep(B,A);")
# 直近 5 番の記録(苦手意識。勝てば消える)
rep("r.h2h=r.h2h||{};const x=r.h2h[o.id]||[0,0];x[r===W?0:1]++;r.h2h[o.id]=x;",
    "r.h2h=r.h2h||{};const x=r.h2h[o.id]||[0,0];x[r===W?0:1]++;r.h2h[o.id]=x;r.h2r=r.h2r||{};const ng=nigate(r,o);let t=(h2rOf(r,o)+(r===W?'o':'x')).slice(-5);if(r===W&&ng)t='';r.h2r[o.id]=t;")
# 方針の稽古への影響(映像研究は稽古の伸び 0.98 倍、稽古で覚えさせるは 1.02 倍。推定)/出稽古の週を数える
rep("if(r.osp&&G.bnum-(r.join||0)<9)gm*=.85;", "if(r.osp&&G.bnum-(r.join||0)<9)gm*=.85;if(isOwn&&G.kpol==='eizo')gm*=.98;if(isOwn&&G.kpol==='kei')gm*=1.02;")
rep("r.lw=mk;", "r.lw=mk;if(isOwn&&mk==='出')r.dekN=(r.dekN||0)+1;")

# ---- 画面 ----
rep("'+styleName(r)+injTag(r)+(r.kad?'<span class=\"tag shu\">角番</span>':'')+'</div>'+\n '<div class=\"sts\"", "'+styleName(r)+injTag(r)+(r.kad?'<span class=\"tag shu\">角番</span>':'')+'</div>'+(r.h===0?'<div style=\"font-size:12px\">'+keyH(r,1)+'</div>':'')+\n '<div class=\"sts\"")
i = s.index("  h+='<h3>能力<span"); j = s.index('\n', i)
assert s.count("  h+='<h3>能力<span") == 1 and s[i:j].endswith("</div>';")
s = s[:i] + "  h+=hyoPanel(r);" + s[j:]
rep("width:'+ovr(r)*5+'%", "width:'+hySeeO(r)*5+'%")
rep("f1(ovr(r))", "hyOW(r)", 4)
rep("<th>総合</th>", "<th>見立て</th>", 2)
rep("総合の見立て:<b>'+f1(ovr(r)-e*.5+randSeed(r.id)*e)+'</b> 前後", "総合の見立て(記者・同じ地位の力士とくらべて):'+hyOW(r)+'")
rep("日目の取組<span class=\"sub\">部屋の力士・作戦を決められます</span></h2>';", "日目の取組<span class=\"sub\">部屋の力士・作戦を決められます</span></h2>'+kpolH();")
rep("'<div class=\"kaku\" style=\"font-size:13px\">相手:'+styleName(o)+'・立ち合い '+lvWord(o.a.tac)+'・引き技 '+lvWord(o.a.hik)+'・対戦 '+hh[0]+'勝'+hh[1]+'敗</div>'",
    "'<div class=\"kaku\" style=\"font-size:13px\">相手:'+styleName(o)+'・立ち合い '+lvWord(o.a.tac)+'・引き技 '+lvWord(o.a.hik)+'・対戦 '+hh[0]+'勝'+hh[1]+'敗</div>'+kenH(a,o)")
rep("'<p class=\"kaku\" style=\"margin:6px 0\">「稽古」で弟子ごとの稽古と強さを決めて", "kpolH()+'<p class=\"kaku\" style=\"margin:6px 0\">「稽古」で弟子ごとの稽古と強さを決めて")
CSS = ".hy{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px}.hy .bx{border:1px solid var(--line);border-radius:6px;padding:6px 8px}.hy .bx h4{margin:0 0 4px;font-size:14px;color:var(--ai)}" \
      ".hr{display:flex;justify-content:space-between;font-size:13px;padding:1px 0}.w5{font-weight:bold}.w5.s{color:var(--shu)}.w5.g{color:#b5651d}.w5.m{color:#2c6a8c}.w5.k{color:#667}.q{color:#bbb}" \
      ".evb{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}.evb button{border:1px solid var(--line);background:transparent;color:inherit;border-radius:14px;padding:3px 10px;font-size:13px;cursor:pointer}.evb button.on{background:var(--ai);color:#fff}" \
      ".who{font-size:12px;color:var(--mute);margin:2px 0 6px}.ms{font-size:13px;margin:4px 0}.ms b{font-size:15px;color:var(--ai)}.cm{background:rgba(160,130,80,.15);border-radius:8px;padding:6px 10px;margin:4px 0;font-size:13px}.cm .wh{font-size:11px;color:var(--mute)}.kcm{font-weight:bold;margin-right:6px;display:inline-block}.kcm.s{color:var(--shu)}.kcm.g{color:#b5651d}.kcm.m{color:#2c6a8c}.w5{white-space:nowrap}.sts .w5{font-size:11px;letter-spacing:-.5px}"
rep(".spt{display:inline-block;", CSS + ".spt{display:inline-block;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
