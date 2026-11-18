function mStars(n){return '<span class="mst">'+'★'.repeat(n)+'<i>'+'★'.repeat(5-n)+'</i></span>';}
function mWhen(it){const d=G.bnum-it.b;return d<=0?(it.wk?'稽古 第'+it.wk+'週':'今場所'):d===1?'前の場所':d+' 場所前';}
function mediaHTML(){const M=G.media;if(!M||!M.L.length)return '<div class="pn"><h2>メディア</h2><p class="kaku mute">まだ情報がありません。稽古の週が進むと、新聞・記者・事情通などから情報が届きます。</p></div>';
 const nw=M.L.filter(x=>x.id>(M.seen||0)).length;const L=M.L.slice(0,UI.mAll?80:12);
 const st=Object.keys(MSRC).filter(k=>k!=='kyo').map(k=>{const o=M.st[k]||[0,0];return '<tr><td>'+mStars(MSRC[k][1])+'</td><td class="nm">'+MSRC[k][0]+'</td><td class="num">'+o[0]+' / '+o[1]+'</td><td class="num"><b>'+(o[1]?Math.round(100*o[0]/o[1])+'%':'—')+'</b></td></tr>';}).join('');
 const h='<div class="pn"><h2>メディア<span class="sub">'+(nw?'新しい情報 '+nw+' 件':'新しい情報はありません')+'</span></h2><p class="kaku mute" style="font-size:13px;margin:0 0 6px">出どころによって確かさが違います。★が多いほど確か。うわさは結果が出ると「当たった」「外れた」が付きます。</p>'+
 '<div class="mgrid">'+L.map(x=>{const s=MSRC[x.s];return '<div class="mit'+(x.id>(M.seen||0)?' nw':'')+'"><div class="mh"><span class="msrc" style="background:'+s[2]+'">'+s[0]+'</span>'+mStars(s[1])+'<span class="mwk">'+mWhen(x)+'</span></div><div class="mt">'+esc(x.t)+'</div>'+(x.sub&&!x.res?'<div class="msub">'+esc(x.sub)+'</div>':'')+
  '<div class="mres '+(x.res==='hit'||x.res==='fix'?'ok':x.res==='miss'?'ng':'')+'">'+(x.res==='fix'?'確定':x.res==='hit'?'当たった':x.res==='miss'?'外れた':'まだ')+(x.rd?':'+esc(x.rd):'')+'</div></div>';}).join('')+'</div>'+
 (M.L.length>12?'<p style="text-align:center;margin:8px 0 0"><button class="btn sm" onclick="UI.mAll=!UI.mAll;render()">'+(UI.mAll?'新しい 12 件だけ':'ぜんぶ見る('+M.L.length+' 件)')+'</button></p>':'')+
 '<h3>出どころごとの当たった割合</h3><table class="tb"><tr><th>確かさ</th><th>出どころ</th><th>当たった数</th><th>割合</th></tr>'+st+'</table></div>';
 M.seen=M.L.length?M.L[0].id:0;return h;}
