<script>
/* v127 画面:弟子の物語(稽古の札に目標、力士の画面に「目標と歩み」) */
var ST_V=window.ST_V||3;
const STK={in:['#8a7a5a','入'],up:['#b5361f','昇'],yu:['#c9a24a','優'],sh:['#3f6b4a','賞'],ok:['#2e7d4f','達'],ng:['#888','逃'],kb:['#2c3e5c','壁'],dn:['#555','落'],fk:['#d0641c','復'],dk:['#6a4c9c','晩'],tk:['#6a4c9c','転']};
function stBar(r){const g=r.mk;if(!g)return '';const el=Math.min(g.n,G.bnum-g.b0),p=Math.round(el*100/g.n);return '<span class="stbar"><i style="width:'+p+'%"></i></span>';}
function stChip(r){if(!r||r.h!==ME()||r.ret)return '';stInit(r);if(!r.mk)stSet(r);const g=r.mk,L=stLeft(r);
 return '<div class="stc"><b>目標</b> '+esc(g.tx.replace('(じっくり)',''))+' <span class="'+(L<=1?'shu':'mute')+'">'+(g.k==='keep'?'あと '+L+' 場所守る':'あと '+L+' 場所')+'</span>'+(r.kb&&G.bnum-r.kb.b<3?' <span class="stk">壁を破る手 '+['出稽古','基本の見直し','気分転換','見守る'][r.kb.c]+'</span>':'')+'</div>';}
function stPick(id,p){const r=G.R[id];if(!r)return;r.mkP=p||null;stSet(r,true);showR(id);}
function stGoalBox(r){const g=r.mk,C=stCand(r),L=stLeft(r),a=r.mkP?null:(g.pk||0);
 const b=(p,i,lb)=>'<button class="pc'+((r.mkP||null)===p?' on':'')+'" onclick="stPick('+r.id+','+(p?'\''+p+'\'':'null')+')">'+lb+'</button>';
 return '<div class="stg"><div><b class="stgt">'+esc(g.tx)+'</b> '+stBar(r)+' <span class="'+(L<=1?'shu':'mute')+'">'+(g.k==='keep'?'あと '+L+' 場所守る':'期限まで あと '+L+' 場所')+'</span></div>'+
  '<div class="stpk">'+b(null,0,'親方にまかせる'+(a!=null?'(いまは'+(a?'じっくり':'高め')+')':''))+b('h',0,'高め:'+esc(C[0].tx))+b('j',1,'じっくり:'+esc(C[1].tx))+'</div>'+
  '<p class="mute" style="font-size:12px;margin:4px 0 0">届けば 気力 +10・信頼 +4、届かなければ 気力 −4・信頼 −1(推定)。これまで 達成 '+(r.mkW||0)+' 回・届かず '+(r.mkF||0)+' 回。</p></div>';}
function stRow(x){const k=STK[x.k]||['#888','・'];return '<li><span class="std" style="background:'+k[0]+'">'+k[1]+'</span><span class="mute stb">'+esc(bname(x.b))+'</span> '+esc(x.t)+'</li>';}
function stStory(r){const S=r.sto||[];const f=S[0];const last=k=>S.filter(x=>x.k===k).slice(-1)[0];const P=[];
 const up=last('up'),kb=last('kb'),fk=last('fk'),dk=last('dk');
 if(up){let t=up.t.replace(/\(.*\)/,'');t=/に上がる$/.test(t)?t.replace('に上がる','に上がった'):(t==='大関'||t==='横綱')?t+'に昇進した':t+'を果たした';P.push([up.b,bname(up.b)+'、'+t+'。']);}if(kb)P.push([kb.b,bname(kb.b)+'には壁にぶつかった。']);
 if(fk)P.push([fk.b,bname(fk.b)+'、'+fk.t.replace('復活:','').replace('返り咲き','返り咲いた')+'。']);if(dk)P.push([dk.b,bname(dk.b)+'ごろから急に力をつけた。']);
 P.sort((x,y)=>x[0]-y[0]);const yu=S.filter(x=>x.k==='yu').length;
 return r.n+'は'+(f?bname(f.b)+'に初土俵を踏んだ。':'この部屋で土俵に上がっている。')+P.map(x=>x[1]).join('')+(yu?'これまでに優勝 '+yu+' 回。':'')+'いまの目標は「'+r.mk.tx.replace('(じっくり)','')+'」。';}
function stHTML(r){if(r.h!==ME()||r.ret)return '';stInit(r);if(!r.mk)stSet(r);const S=(r.sto||[]).slice().reverse();
 const list='<ul class="stl">'+S.slice(0,UI.stAll?40:8).map(stRow).join('')+'</ul>'+(S.length>8&&!UI.stAll?'<button class="btn sm" onclick="UI.stAll=1;showR('+r.id+')">すべて見る('+S.length+' 件)</button>':'');
 if(ST_V===2)return '<div class="stp"><h3>目標と歩み</h3><div class="grid2"><div>'+stGoalBox(r)+'</div><div>'+list+'</div></div></div>';
 if(ST_V===3)return '<div class="stp"><h3>目標と歩み</h3><p class="stst">'+esc(stStory(r))+'</p>'+stGoalBox(r)+'<details><summary>年表</summary>'+list+'</details></div>';
 return '<div class="stp"><h3>目標と歩み</h3>'+stGoalBox(r)+'<h4 style="margin:8px 0 2px">歩み</h4>'+list+'</div>';}
const stK0=kcCard;kcCard=function(r){return stK0(r)+stChip(r);};
const stCM0=closeM;closeM=function(){UI.stAll=0;return stCM0.apply(this,arguments);};
</script><style>
.stc{font:12px sans-serif;margin:3px 0;padding:2px 6px;border-radius:4px;background:#c9a24a22}.stc .shu{color:#b5361f;font-weight:bold}.stk{background:#2c3e5c;color:#fff;border-radius:8px;padding:0 6px}
.stp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 10px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important;white-space:normal!important;text-align:left!important}.stp .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
.stg{border:1px solid var(--line);border-radius:8px;padding:8px;margin:4px 0}.stgt{font-size:16px;color:var(--ai)}.stpk{margin-top:4px}
.stbar{display:inline-block;width:80px;height:8px;background:#0002;border-radius:4px;overflow:hidden;vertical-align:middle}.stbar i{display:block;height:100%;background:#b5361f}
.stl{list-style:none;padding:0;margin:4px 0;font-size:13px}.stl li{padding:3px 0;border-bottom:1px dotted var(--line)}.std{display:inline-block;width:20px;height:20px;line-height:20px;border-radius:50%;color:#fff;text-align:center;font-size:11px;margin-right:4px}.stb{font-size:11px;margin-right:4px}
.stst{background:#fff8e6;border-left:4px solid #c9a24a;padding:6px 10px;margin:4px 0;font-size:14px;line-height:1.7;color:#1a140c}
</style>
