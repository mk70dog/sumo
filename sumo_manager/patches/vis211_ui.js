/* v208 新弟子候補に会いに行く:前回との違い・見立ての記録・見る人ごとのくせ・親方が行く効き目を本物らしく。数字はすべて推定 */
(function(){
/* 親方の現役時代の地位(実在の部屋の表 REALH)。名のある親方ほど口説く力が大きい(推定) */
function oyFame(){const h=me();const x=(typeof REALH!=='undefined')?REALH.find(a=>a[2]===h.o2):null;const t=x?x[4]:'';return t==='Y'?[1.5,'元横綱']:t==='O'?[1.3,'元大関']:[1,''];}
/* 目利きが低い人は甘めに見る(素質を高く見がち)。目利き 11 で ±0(推定) */
function vBias(mk){return Math.max(-.3,Math.min(.8,(11-(mk||8))*.12));}
const biasW=b=>b>=.35?'甘め':b<=-.15?'辛め':'ふつう';
/* 遠くの候補(北海道・沖縄・海外)は、親方が行くと 2 週空ける(推定) */
const isFar=p=>!!(p.r&&(p.r.fr||/北海道|沖縄/.test(p.r.home||'')));
const rng=p=>{const e=p.err==null?6:p.err;return {lo:Math.max(1,p.eo-e*.6),hi:p.eo+e*.6,plo:Math.max(1,p.ep-e),phi:Math.min(20,p.ep+e)};};
function snap(p,who,mk,b,first){const q=rng(p);return {wn:G.wn,bn:G.bnum,wk:G.phase==='train'?G.wk:0,who:who,mk:mk,b:b,first:first?1:0,
 lo:+q.lo.toFixed(1),hi:+q.hi.toFixed(1),plo:+q.plo.toFixed(1),phi:+q.phi.toFixed(1),g:gradeOf(p.ep),st:p.v>=2?styleName(p.r):null,per:p.v>=3?p.r.per:null,note:''};}
const GR='SABCDE';const gi=g=>{const i=GR.indexOf(String(g).charAt(0));return i<0?9:i;};
/* 見に行った人のひとこと(目についたところ) */
function vNote(p,up){const L=AT.filter(a=>a[2]!=='心'&&p.r.a[a[0]]!=null);const s=L.slice().sort((x,y)=>p.r.a[y[0]]-p.r.a[x[0]]);
 const best=pick(s.slice(0,3)),weak=pick(s.slice(-3));
 const A=['「'+best[1]+'がいい。思っていたより使える」','「'+best[1]+'が目についた。そこは本物だ」','「'+best[1]+'は、もう少し伸びそうだ」'];
 const B=['「'+weak[1]+'がまだ弱い。そこは稽古次第だ」','「前より'+weak[1]+'の甘さが見えた」','「'+weak[1]+'は鍛えないと上では苦しい」'];
 const C=['「体の芯がしっかりしてきた」','「前に見たときより顔つきが締まっていた」','「家族も相撲に理解があるようだ」','「稽古場の態度がまじめだった」'];
 return up>0?pick(A):up<0?pick(B):pick(C.concat(A.slice(0,1),B.slice(0,1)));}
/* 会いに行く */
const tp0=trackPros;
trackPros=function(cid,who){const p=G.pros.find(x=>x.cid===cid);if(!p)return tp0(cid,who);if(p.lastV===G.wn||G.money<3)return tp0(cid,who);
 const V=visitors().find(x=>String(x.k)===String(who==null?'oy':who))||visitors()[0];
 p.vlog=p.vlog||[];if(!p.vlog.length&&p.eo!=null)p.vlog.push(snap(p,p.src||'はじめの情報',p.mk,0,1));
 const prev=p.vlog[p.vlog.length-1];const int0=p.int,st0=p.v>=2,per0=p.v>=3;
 const m=tp0(cid,who);
 /* 見る人のくせ:甘めの人は素質を高めに見る(平均に混ぜる) */
 const b=+vBias(V.mk).toFixed(2);p.ep=Math.min(20,p.ep+b/p.v);
 /* 親方が行った:口説く力(回数で小さくなる)・ほかの部屋の関心が下がる・遠いと 2 週空ける */
 let oyTxt='';
 if(V.k==='oy'){const F=oyFame();p.visOyN=(p.visOyN||0)+1;p.int=Math.max(0,int0-Math.round(R(3,8)*F[0]));
  if(isFar(p)){G.awayN=(G.awayN||0)+1;oyTxt+='遠方なので、親方は来週も部屋を空けます。';}
  oyTxt+=(F[1]?F[1]+'の親方が来たことに、本人も家族も驚いていました。':'親方が直接来たことで、本人と家族の気持ちがこちらに向きました。')+'ほかの部屋の関心が少し下がりました。';}
 const cur=snap(p,V.k==='oy'?'親方':V.n,V.mk,b,0);
 const d=gi(prev.g)-gi(cur.g);cur.note=vNote(p,d>0?1:d<0?-1:(cur.phi-cur.plo)<(prev.phi-prev.plo)-.5?0:0);
 p.vlog.push(cur);if(p.vlog.length>12)p.vlog.splice(1,p.vlog.length-12);
 /* 前回との違いの知らせ */
 const L=[];
 L.push('素質:'+(prev.g===cur.g?cur.g+'(変わらず)':prev.g+' → '+cur.g+(d>0?' ↑':' ↓'))+'  幅 '+prev.plo+'〜'+prev.phi+' → '+cur.plo+'〜'+cur.phi);
 L.push('今の力:'+prev.lo+'〜'+prev.hi+' → '+cur.lo+'〜'+cur.hi);
 if(!st0&&cur.st)L.push('新しくわかった:取り口は「'+cur.st+'」');
 if(!per0&&cur.per)L.push('新しくわかった:性格は「'+cur.per+'」');
 L.push('ひとこと:'+cur.note);
 L.push('見た人:'+cur.who+'(目利き '+Math.round(V.mk)+'・見方は'+biasW(b)+')');
 if(oyTxt)L.push(oyTxt);
 if(V.k==='oy')L.push('今週は親方が部屋を空けるので、全員の稽古の伸びが少し下がり、自分で見る注目選手は 1 人になります。');
 p.vNew=G.wn;UI.vRes={n:p.n,L:L};
 return m;};
/* 親方が何度も行くほど決まりやすい(1 回目 +8%・2 回目 +4%・3 回目 +2%。名のある親方は大きめ。推定) */
const ob0=offerBonus;
offerBonus=function(p){let b=ob0(p);const n=p.visOyN||(p.visOy?1:0);if(n>0){const F=oyFame()[0];b+=-.08+Math.min(.14,[0,.08,.12,.14][Math.min(3,n)])*F;}return b;};
/* 遠方:来週も親方が空ける */
const dw0=doWeek;doWeek=function(){if(G&&G.awayN&&G.phase==='train'){G.tmp.away=(G.tmp.away||0)+1;G.awayN--;}return dw0.apply(this,arguments);};
/* 結果を見せる */
const dt0=doTrack;doTrack=function(cid){UI.vRes=null;dt0(cid);if(UI.vRes){const x=UI.vRes;UI.vRes=null;
 openM('<h2>'+esc(x.n)+'に会いに行きました</h2><div class="kaku vdf">'+x.L.map(t=>'<div>'+esc(t)+'</div>').join('')+'</div><div class="btns" style="margin-top:10px"><button class="btn main" onclick="closeM()">OK</button><button class="btn" onclick="closeM();vLog(\''+cid+'\')">見立ての記録</button></div>');}};
/* 見立ての記録 */
window.vLog=function(cid){const p=G.pros.find(x=>x.cid===cid);if(!p)return;const V=p.vlog||[];
 const rows=V.map((v,i)=>{const pv=i?V[i-1]:null;const d=pv?gi(pv.g)-gi(v.g):0;
  return '<tr><td>'+esc(bname(v.bn).replace(/^\d+年 /,''))+(v.wk?'<br><span class="mute">第'+v.wk+'週</span>':'')+'</td><td>'+esc(v.who)+(v.first?'':'<br><span class="mute">目利き '+Math.round(v.mk)+'・'+biasW(v.b)+'</span>')+'</td><td><b class="kin">'+v.g+'</b>'+(d>0?' <span class="vup">↑</span>':d<0?' <span class="vdn">↓</span>':'')+'<br><span class="mute">'+v.plo+'〜'+v.phi+'</span></td><td>'+v.lo+'〜'+v.hi+'</td><td>'+(v.st?esc(v.st):'?')+(v.per?'・'+esc(v.per):'')+'</td><td style="font-size:12px">'+esc(v.note||'')+'</td></tr>';}).join('');
 openM('<h2>'+esc(p.n)+'の見立ての記録</h2><div style="overflow-x:auto"><table class="tb vlt"><tr><th>いつ</th><th>見た人</th><th>素質</th><th>今の力</th><th>取り口・性格</th><th>ひとこと</th></tr>'+(rows||'<tr><td colspan="6" class="mute">まだ会いに行っていません</td></tr>')+'</table></div>'+
  '<p class="mute" style="font-size:12px">目利きが低い人は素質を甘め(高め)に見がちです。何人かで見比べると確かになります。親方が会った回数 '+(p.visOyN||(p.visOy?1:0))+' 回。</p><button class="btn main" onclick="closeM()">閉じる</button>');};
/* カード:変わったところの矢印・記録のボタン・親方の回数。会いに行く人の目利き */
const sh0=scoutHTML;scoutHTML=function(){const d=document.createElement('div');d.innerHTML=sh0();
 d.querySelectorAll('.cards.sc .card').forEach((c,i)=>{const p=G.pros[i];if(!p)return;const V=p.vlog||[];const a=V[V.length-2],b=V[V.length-1];
  const divs=[...c.querySelectorAll('.info > div')];
  if(a&&b&&!b.first){const dd=gi(a.g)-gi(b.g);const sd=divs.find(x=>x.textContent.startsWith('素質'));
   const tag=dd>0?'<span class="vtg vup">↑ '+a.g+'から上がった</span>':dd<0?'<span class="vtg vdn">↓ '+a.g+'から下がった</span>':'<span class="vtg">幅が狭まった</span>';
   if(sd)sd.insertAdjacentHTML('beforeend',' '+tag);
   const td=divs.find(x=>x.textContent.startsWith('取り口'));if(td&&((b.st&&!a.st)||(b.per&&!a.per)))td.insertAdjacentHTML('beforeend',' <span class="vtg vnw">新しくわかった</span>');}
  const cnt=divs.find(x=>x.textContent.startsWith('見に行った回数'));
  if(cnt){const n=p.visOyN||(p.visOy?1:0);cnt.insertAdjacentHTML('beforeend',(n?'・親方 '+n+' 回':'')+(isFar(p)?'・遠方(親方は 2 週空ける)':'')+' <button class="btn sm vlb" onclick="vLog(\''+p.cid+'\')">見立ての記録'+(V.length>1?'('+(V.length-1)+')':'')+'</button>');}
  const sel=c.querySelector('select[id^="vis_"]');if(sel)[...sel.options].forEach(o=>{const v=visitors().find(x=>String(x.k)===o.value);if(v)o.textContent=(v.k==='oy'?'親方'+(oyFame()[1]?'('+oyFame()[1]+')':''):v.n)+'・目利き '+Math.round(v.mk);});
  if(sel)sel.style.maxWidth='16em';});
 return d.innerHTML;};
window.oyFame=oyFame;window.vBias=vBias;
document.head.insertAdjacentHTML('beforeend','<style>.vtg{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid currentColor;margin-left:4px;opacity:.9}.vup{color:#3d8a4a}.vdn{color:#b0402a}.vnw{color:#2c6aa0}'+
 '.vlb{margin-left:6px;padding:2px 8px!important;font-size:12px!important}.vdf div{margin:3px 0}.vlt td,.vlt th{font-size:13px;vertical-align:top;white-space:nowrap}.vlt td:last-child{white-space:normal;min-width:12em}'+
 'body.sk-urushik .vup,body.sk-urushi .vup,body.sk-urushig .vup,body.sk-yoru .vup{color:#7fd08a}body.sk-urushik .vdn,body.sk-urushi .vdn,body.sk-urushig .vdn,body.sk-yoru .vdn{color:#f08a6a}body.sk-urushik .vnw,body.sk-urushi .vnw,body.sk-urushig .vnw,body.sk-yoru .vnw{color:#8fb0e0}</style>');
})();
