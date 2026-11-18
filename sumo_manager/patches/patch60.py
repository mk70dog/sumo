# 番付の力(誇り・自信・重圧):番付が上がると本来の力より少し強く  v56 -> v57
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v56</title>', '<title>Sumo Manager v57</title>')
rep("const APPV=56;\nconst SAVE='sumoManager56',SAVE55", "const APPV=57;\nconst SAVE='sumoManager57',SAVE56='sumoManager56',SAVE55")
rep('[SAVE55,SAVE54', '[SAVE56,SAVE55,SAVE54')
rep(" if(g.v===55){g.v=56;}\n return g.v===56?g:null;}", " if(g.v===55){g.v=56;}\n if(g.v===56){g.v=57;}\n return g.v===57?g:null;}")
rep('G={v:56,', 'G={v:57,')

CORE = r'''
/* 番付の力:誇り・自信・まわりの支えで、本来の力より強くなる(重圧で弱くなる力士もいる)。数字は推定 */
const BZ={Y:.01,O:.003,S:.006,K:.004};
function bzGrp(t){return t==='Y'?'Y':t==='O'?'O':(t==='S'||t==='K')?'SK':'';}
function bzCalc(r){const base=r.d===0&&r.t?(BZ[r.t]||0):0;if(!base)return {v:0,base:0};
 const g=bzGrp(r.t);let ten=0;const h=r.hist||[];for(let i=h.length-1;i>=0&&bzGrp(h[i].t)===g&&h[i].d===0;i--)ten++;
 const per=r.per||'';let m=ten===0?.5:ten===1?.8:1;const L=[];
 if(per==='豪快'||per==='野心家'||per==='負けず嫌い'){m*=1.3;L.push(per+'で自信になりやすい');}
 else if(per==='繊細'){m=ten===0?-.5:ten===1?.3:.8;L.push(ten===0?'繊細で、上がったばかりの重圧':'繊細で、重圧を感じやすい');}
 else if(per==='気分屋'){m*=R(0,1.6);L.push('気分屋で場所ごとにぶれる');}
 m+=(r.a.sho-10)*.03+(r.a.pro-10)*.02;
 if(r.h===0){let d=0;oshiItems(r).forEach(x=>{if(x.k==='doki'||x.k==='tsu')return;if(x.c==='p')d++;else if(x.c==='n')d--;});const sp=cl(d*.08,-.25,.25);if(sp)L.push(sp>0?'まわりの支えが厚い':'まわりの支えが薄い');m+=sp;}
 if(ten===0)L.unshift('新'+(g==='Y'?'横綱':g==='O'?'大関':'三役')+'の場所');
 return {v:base*cl(m,-.6,1.8),base,ten,note:L.join('・')};}
'''
rep("function prepF(r,big){", CORE.lstrip('\n') + "function prepF(r,big){")
rep("f*=1+(r.bfm||0);r._f=f;", "f*=1+(r.bfm||0)+(r.bzf||0);r._f=f;")
rep("r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);}",
    "r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);}\n  {const z=bzCalc(r);r.bzf=z.v;r.bzn=z.note||'';}")
# 画面:状態に「番付の力」
rep("'</dd><dt>人気</dt><dd>'+gg(r.", "'</dd>'+(r.bzf?'<dt>番付の力</dt><dd>'+(r.bzf>0?'<b class=\"shu\">自信 +':'<b class=\"ai\">重圧 ')+(r.bzf*100).toFixed(1)+'%</b>'+(r.bzn?'<br><span class=\"mute\" style=\"font-size:12px\">'+esc(r.bzn)+'</span>':'')+'</dd>':'')+'<dt>人気</dt><dd>'+gg(r.")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
