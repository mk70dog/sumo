/* v113 育つ環境を力士のまど(能力・状態)と稽古の画面に出す(見本 ev1 くわしく) */
(function(){
const V=1;
function envParts(r){const mk=r.menu,it=r.it;let pa=envPa(r);if(mk==='出')pa=Math.max(pa,.8);
 return {sh:envSh(),pa:pa,fa:envFa(),ke:envKe(r,mk,it)};}
function envTot(p){const W=ENV.w;return Math.round((W.sh*p.sh+W.pa*p.pa+W.fa*p.fa+W.ke*p.ke)*100)/100;}
function young(r){return (G.bnum-(r.join==null?-99:r.join))<ENV.yrs||r.age<=ENV.age;}
const PN={sh:'指導力',pa:'稽古相手',fa:'施設と体づくり',ke:'稽古の中身'};
function word(e){return e>=.7?'とても良い':e>=.56?'良い':e>=.42?'ふつう':e>=.28?'悪い':'とても悪い';}
function mark(v){return v>=.7?'◎':v>=.5?'○':v>=.3?'△':'×';}
function col(e){return e>=.56?'#2f7d32':e>=.42?'#a8823c':'#b5361f';}
function hint(r,p){const k=Object.keys(PN).sort((a,b)=>p[a]-p[b])[0];
 if(k==='sh')return '指導力の高い部屋付き親方を雇うと伸びます(スタッフ)。';
 if(k==='pa')return '番付の近い兄弟子が少ない。出稽古で補えます。';
 if(k==='fa')return '稽古場・食堂・医務室を広げる、ジムや管理栄養士と契約すると伸びます(経営)。';
 if(r.fat>75)return '疲れがたまっています。少し軽くして疲れを抜きましょう。';
 if((r.it||0)===0)return '稽古が軽めです。強めにすると伸びます(けがに注意)。';
 return '気力と師匠への信頼を上げると伸びます。';}
function bar(v,c){return '<span style="display:inline-block;vertical-align:middle;width:min(110px,24vw);height:9px;background:#0001;border-radius:5px;overflow:hidden"><span style="display:block;height:100%;width:'+Math.round(v*100)+'%;background:'+(c||'#a8823c')+'"></span></span>';}
function envBox(r){if(r.h!==ME()||G.pend.includes(r.id))return '';const p=envParts(r),e=envTot(p),yg=young(r);
 const up=e>=ENV.E0;const arrow=yg?(up?'<b style="color:#2f7d32">↑ 素質の上限が伸びています</b>':'<b style="color:#b5361f">↓ 素質の上限が下がっています</b>'):'<span class="mute">育つ時期を過ぎたので、上限は動きません(伸びる速さだけ変わります)</span>';
 if(V===1)return '<div class="pn" style="margin:8px 0;padding:8px 10px"><h3 style="margin:0 0 4px">育つ環境 <b style="color:'+col(e)+'">'+Math.round(e*100)+' 点</b> <small>'+word(e)+'</small></h3><div style="font-size:13px">'+arrow+'</div>'+
  '<table class="tb" style="margin:4px 0;font-size:13px">'+Object.keys(PN).map(k=>'<tr><td style="white-space:nowrap">'+PN[k]+' <small class="mute">'+Math.round(ENV.w[k]*100)+'%</small></td><td>'+bar(p[k],col(p[k]))+' '+Math.round(p[k]*100)+'</td></tr>').join('')+'</table><div class="kaku" style="font-size:13px">伸ばすには:'+hint(r,p)+'</div></div>';
 if(V===2)return '<p class="kaku" style="margin:6px 0">育つ環境 <b style="color:'+col(e)+'">'+Math.round(e*100)+' 点(' +word(e)+')</b> '+(yg?(up?'<span style="color:#2f7d32">↑</span>':'<span style="color:#b5361f">↓</span>'):'')+'<br><small>'+hint(r,p)+'</small></p>';
 return '<p class="kaku" style="margin:6px 0">育つ環境 <b style="font-size:18px;color:'+col(e)+'">'+mark(e)+'</b> '+Object.keys(PN).map(k=>PN[k]+' '+mark(p[k])).join('・')+(yg?' '+(up?'<span style="color:#2f7d32">↑</span>':'<span style="color:#b5361f">↓</span>'):'')+'<br><small>'+hint(r,p)+'</small></p>';}
const _tb=trustBox;trustBox=function(r){return _tb(r)+envBox(r);};
function cell(r){if(G.pend.includes(r.id))return '<span class="mute">—</span>';const p=envParts(r),e=envTot(p);const yg=young(r);const ar=yg?(e>=ENV.E0?'↑':'↓'):'';
 if(V===3)return '<b style="color:'+col(e)+'">'+mark(e)+'</b>'+ar;return '<b style="color:'+col(e)+'">'+Math.round(e*100)+'</b>'+ar;}
const _kh=keikoHTML;keikoHTML=function(){let h=_kh();
 h=h.replace('<th>見立て</th>','<th>見立て</th><th>育つ環境</th>');
 h=h.replace(/(<td class="nm" onclick="showR\((\d+)\)" style="cursor:pointer">[^<]*<\/td><td class="num">[^<]*(?:<[^>]*>[^<]*)*?<\/td>)/g,(m,a,id)=>a+'<td class="num">'+cell(G.R[id])+'</td>');
 h=h.replace(/(<b class="nm" onclick="showR\((\d+)\)">[^<]*<\/b>)/g,(m,a,id)=>a+' <span class="kaku">環境 '+cell(G.R[id])+'</span>');
 if(V===1||V===3){const L=ownAll().filter(r=>!G.pend.includes(r.id));if(L.length){const avg=k=>L.reduce((s,r)=>s+envParts(r)[k],0)/L.length;const p={sh:avg('sh'),pa:avg('pa'),fa:avg('fa'),ke:avg('ke')};const e=envTot(p);
  const low=Object.keys(PN).sort((a,b)=>p[a]-p[b])[0];
  const panel=V===1?'<div class="pn"><h2>部屋の育つ環境 <span class="sub">弟子の平均 '+Math.round(e*100)+' 点・'+word(e)+'</span></h2><table class="tb" style="font-size:13px">'+Object.keys(PN).map(k=>'<tr><td>'+PN[k]+'</td><td>'+bar(p[k],col(p[k]))+' '+Math.round(p[k]*100)+(k===low?' <b style="color:#b5361f;white-space:nowrap">← いちばん弱い</b>':'')+'</td></tr>').join('')+'</table><p class="kaku mute" style="font-size:12px;margin:4px 0 0">入門 6 年まで(または 24 歳まで)は、56 点より上なら素質の上限が伸び、下なら下がります。</p></div>'
   :'<div class="pn"><h2>部屋の育つ環境 <span class="sub">'+mark(e)+'</span></h2><p class="kaku" style="margin:0">'+Object.keys(PN).map(k=>PN[k]+' <b>'+mark(p[k])+'</b>').join(' ・ ')+'</p></div>';
  h=h.replace('<div class="btns" style="margin:8px 0">全員:',panel+'<div class="btns" style="margin:8px 0">全員:');}}
 return h;};
})();
