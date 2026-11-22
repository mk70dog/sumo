/* 見本 kt1〜kt3:稽古タブをわかりやすく使いやすく。#kt1 札とボタン / #kt2 まとめて決める / #kt3 すっきりした表 */
(function(){
const V=+((location.hash.match(/kt(\d)/)||[])[1]||1);window.KTV=V;
const MK=Object.keys(MENU);const PK=Object.keys(PM);
const short={基:'四股',ぶ:'ぶつかり',申:'申し合い',三:'三番',筋:'筋トレ',出:'出稽古',休:'休養'};
const sn=k=>short[k]||MENU[k].n;
const isP=r=>G.pend.includes(r.id);
const rk=r=>isP(r)?'新弟子':r.rkS;
const injOK=r=>!(r.inj&&r.inj.s>=2);
function envN(r){try{if(typeof envE!=='function'||isP(r))return '';const e=Math.round(envE(r,r.menu,r.it)*100);return '<span style="color:'+(e>=56?'#6fbf73':e>=42?'#c9a24a':'#e07a5a')+'">'+e+'</span>';}catch(e){return '';}}
/* 今週の稽古で疲れがどうなるか(おおまか:稽古の疲れ×強さ+午後) */
function fatF(r){const m=MENU[injOK(r)?r.menu:'休']||MENU['基'];return Math.round((m.f||0)*INT[r.it||1].f+(PM[r.pm||'昼']||{f:0}).f-12);}
function fatTxt(r){const d=fatF(r),v=r.fat+d;return v>75?'<b style="color:#e07a5a">疲れすぎ</b>':d>4?'<span style="color:#e0a05a">疲れがたまる</span>':d<-4?'<span style="color:#6fbf73">疲れが抜ける</span>':'<span class="mute">ほぼ同じ</span>';}
function seg(id,k,list,cur,num){return '<div class="kseg">'+list.map(([v,t])=>'<button class="'+(String(v)===String(cur)?'on':'')+'" onclick="ktSet('+id+',\''+k+'\','+(num?v:'\''+v+'\'')+')">'+t+'</button>').join('')+'</div>';}
window.ktSet=function(id,k,v){const ids=id==='all'?ownAll().map(r=>r.id):Array.isArray(id)?id:[id];ids.forEach(i=>{G.R[i][k]=v;});save();const y=scrollY;render();scrollTo(0,y);};
window.ktGrp=function(g,k,v){ktSet(GRP[g].f().map(r=>r.id),k,v);};
window.ktPre=function(p){const L=ownAll();L.forEach(r=>{if(p==='go'){r.menu=r.d<=2?'申':'基';r.it=2;r.pm='筋';}if(p==='fin'){r.menu='基';r.it=0;r.pm='昼';}if(p==='rest'){r.menu='休';r.it=0;r.pm='治';}if(p==='std'){r.menu='申';r.it=1;r.pm='昼';}});save();const y=scrollY;render();scrollTo(0,y);};
const GRP={sk:{n:'関取',f:()=>ownAll().filter(r=>!isP(r)&&r.d<=1&&injOK(r))},ms:{n:'幕下',f:()=>ownAll().filter(r=>!isP(r)&&r.d===2&&injOK(r))},lo:{n:'三段目以下・新弟子',f:()=>ownAll().filter(r=>(isP(r)||r.d>=3)&&injOK(r))},ij:{n:'けがをしている',f:()=>ownAll().filter(r=>!injOK(r))}};
function hint(){const wk=G.wk||1;return wk<=WEEKS-2?'<b>今は「鍛える時期」</b>(第 '+wk+' 週)。しっかり稽古して力を伸ばしましょう。':'<b>今は「仕上げの時期」</b>(初日まであと '+(WEEKS-wk+1)+' 週)。軽めにして疲れを抜くと、初日の調子が上がります。';}
const help='<details class="khelp"><summary>稽古のしくみ(押すと開きます)</summary><div class="hl">・稽古は 1 週ごとに効きます。強いほど伸びますが、疲労とけがが増えます。疲労が 75 を超えると伸びが落ちます。<br>・調子は実戦的な稽古(申し合い・三番稽古・出稽古)で上がり、休むと下がります。前半の 4 週はしっかり稽古し、初日前の 2 週を軽めにして疲れを抜く「仕上げ」がうまくいくと、初日の調子が上がります。<br>・体重は「筋肉」と「脂肪」に分かれます。筋肉は稽古・筋トレ・たんぱく質で付き、脂肪は食べ過ぎ・昼寝で付きます。<br>・けがをしている力士は、軽傷なら軽い稽古だけ、中程度以上は休養になります。</div></details>';
function top(){let h='<div class="pn"><h2>稽古<span class="sub">'+(G.phase==='train'?'第'+G.wk+'週/'+WEEKS+'週':'本場所の後に再開')+'</span></h2>';
 if(G.phase==='train')h+=weekDots()+'<div class="khint">'+hint()+'</div><div class="btns" style="margin:6px 0 10px"><button class="btn main" onclick="doWeekUI()">1 週間を過ごす</button><button class="btn ai" onclick="doToBasho()">初日まで進める</button></div>';
 return h;}
function card(r){const ij=!injOK(r);
 return '<div class="kc'+(r.d<=1&&!isP(r)?' sk':'')+(ij?' ij':'')+'"><div class="kch"><span class="wsr">'+esc(rk(r))+'</span><b class="wsnm" onclick="showR('+r.id+')">'+esc(r.n)+'</b>'+(injTag(r)||'')+'<span class="kenv">環境 '+envN(r)+'</span></div>'+
 '<div class="kst">調子 '+condG(r)+' 疲労 '+fatG(r)+' <small>'+Math.round(r.w)+'kg</small></div>'+
 (ij?'<div class="mute" style="font-size:13px;margin:6px 0">けがのため休養します</div>':
 '<div class="krow"><span>稽古</span>'+seg(r.id,'menu',MK.map(k=>[k,sn(k)]),r.menu)+'</div><div class="krow"><span>強さ</span>'+seg(r.id,'it',INT.map((x,i)=>[i,x.n]),r.it,1)+'</div>')+
 '<div class="krow"><span>午後</span>'+seg(r.id,'pm',PK.map(k=>[k,PM[k].n]),r.pm||'昼')+'</div><div class="krow"><span>体重</span>'+seg(r.id,'wplan',WPL.map((x,i)=>[i,x]),r.wplan,1)+'</div>'+
 '<div class="kfoot">今週:'+fatTxt(r)+'</div></div>';}
function grpRow(g){const L=GRP[g].f();if(!L.length)return '';const one=k=>{const v=L[0][k];return L.every(r=>r[k]===v)?v:null;};
 return '<div class="kg"><div class="kgh"><b>'+GRP[g].n+'</b> <small>'+L.length+' 人</small></div>'+(g==='ij'?'<div class="mute" style="font-size:13px">けがの重さに合わせて自動で休ませます。</div>':
  '<div class="krow"><span>稽古</span>'+seg('\''+g+'\'','menu',MK.map(k=>[k,sn(k)]),one('menu')).replace(/ktSet\('(\w+)'/g,"ktGrp('$1'")+'</div><div class="krow"><span>強さ</span>'+seg('\''+g+'\'','it',INT.map((x,i)=>[i,x.n]),one('it'),1).replace(/ktSet\('(\w+)'/g,"ktGrp('$1'")+'</div><div class="krow"><span>午後</span>'+seg('\''+g+'\'','pm',PK.map(k=>[k,PM[k].n]),one('pm')).replace(/ktSet\('(\w+)'/g,"ktGrp('$1'")+'</div>')+
  '<div class="kgl">'+L.map(r=>'<span onclick="showR('+r.id+')">'+esc(r.n)+' <small>'+(r.fat>75?'<b style="color:#e07a5a">疲'+Math.round(r.fat)+'</b>':'疲'+Math.round(r.fat))+'</small></span>').join('')+'</div></div>';}
const _kh=keikoHTML;
keikoHTML=function(){const full=_kh();const cut=full.indexOf(coPanel());const rest=cut>=0?full.slice(cut):'';const o=ownAll();let h=top();
 if(V===1){h+=help+'<div class="btns" style="margin:6px 0">全員まとめて:<button class="btn sm" onclick="ktPre(\'std\')">ふつうに稽古</button><button class="btn sm" onclick="ktPre(\'go\')">しっかり鍛える</button><button class="btn sm" onclick="ktPre(\'fin\')">仕上げ(軽め)</button><button class="btn sm" onclick="ktPre(\'rest\')">全員休ませる</button></div><div class="kcs">'+o.map(card).join('')+'</div></div>';}
 if(V===2){h+='<div class="kpre"><b>おすすめをまとめて選ぶ</b><button onclick="ktPre(\'go\')"><b>しっかり鍛える</b><small>幕下以上は申し合い・下は四股、強め、午後は筋トレ</small></button><button onclick="ktPre(\'std\')"><b>ふつう</b><small>申し合い・ふつう・昼寝</small></button><button onclick="ktPre(\'fin\')"><b>仕上げ</b><small>四股・軽め・昼寝。初日前の 2 週に</small></button><button onclick="ktPre(\'rest\')"><b>休ませる</b><small>休養・治療</small></button></div>'+help+
  '<h3 style="margin:10px 0 4px">番付ごとに決める</h3>'+['sk','ms','lo','ij'].map(grpRow).join('')+'<p class="kaku mute" style="font-size:13px">ひとりずつ変えたいときは、名前を押して力士の画面から変えるか、「力士」タブを使います。</p></div>';}
 if(V===3){h+=help+'<div class="btns" style="margin:6px 0">全員:'+selH([['','稽古']].concat(MK.map(k=>[k,MENU[k].n])),'','if(this.value)setAll(\'menu\',this.value)')+selH([['','強さ']].concat(INT.map((x,i)=>[i,x.n])),'','if(this.value!==\'\')setAll(\'it\',+this.value)')+selH([['','午後']].concat(PK.map(k=>[k,PM[k].n])),'','if(this.value)setAll(\'pm\',this.value)')+'</div>'+
  '<div style="overflow-x:auto"><table class="tb kt3"><tr><th>力士</th><th>調子・疲労</th><th>稽古</th><th>強さ</th><th>午後</th><th>体重</th><th>今週</th></tr>'+o.map((r,i)=>{const ij=!injOK(r);return '<tr class="'+(ij?'ij':'')+'"><td onclick="showR('+r.id+')" style="cursor:pointer"><div class="wsr">'+esc(rk(r))+' '+(injTag(r)||'')+'</div><div class="wsnm" style="white-space:nowrap">'+esc(r.n)+'</div><div style="font-size:12px">'+hyOW(r)+' ・環境 '+envN(r)+'</div></td><td style="white-space:nowrap">'+condG(r)+'<br>'+fatG(r)+' <small>'+Math.round(r.fat)+'</small></td><td>'+(ij?'<span class="mute">休養</span>':selH(MK.map(k=>[k,MENU[k].n]),r.menu,'setR('+r.id+',\'menu\',this.value)'))+'</td><td>'+(ij?'':seg(r.id,'it',INT.map((x,i)=>[i,x.n]),r.it,1))+'</td><td>'+selH(PK.map(k=>[k,PM[k].n]),r.pm||'昼','setR('+r.id+',\'pm\',this.value)')+'</td><td>'+seg(r.id,'wplan',WPL.map((x,i)=>[i,x]),r.wplan,1)+'<div style="font-size:11px" class="mute">'+Math.round(r.w)+'kg '+Math.round((r.bf||.25)*100)+'%</div></td><td style="font-size:13px">'+fatTxt(r)+'</td></tr>';}).join('')+'</table></div></div>';}
 return h+rest;};
document.head.insertAdjacentHTML('beforeend','<style>'+
 '.kseg{display:inline-flex;flex-wrap:wrap;gap:3px}.kseg button{font-size:12px;padding:3px 7px;border-radius:5px;border:1px solid rgba(127,127,127,.4);background:rgba(127,127,127,.12);color:inherit;cursor:pointer;white-space:nowrap}.kseg button.on{background:#9a2b1d;border-color:#9a2b1d;color:#fff}'+
 '.krow{display:flex;align-items:flex-start;gap:6px;margin:4px 0}.krow>span:first-child{width:2.5em;flex:none;font-size:12px;opacity:.75;padding-top:4px}'+
 '.kcs{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:8px}.kc{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:8px 10px;background:rgba(127,127,127,.06)}.kc.sk{border-color:#c9a24a}.kc.ij{opacity:.8}.kch{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.kch .wsnm{cursor:pointer}.kenv{margin-left:auto;font-size:12px}.kst{font-size:12px;margin:2px 0 4px}.kfoot{font-size:12px;margin-top:4px;border-top:1px dashed rgba(127,127,127,.3);padding-top:4px}'+
 '.wsr{font-size:12px;color:#8fa9d8}.wsnm{font-family:Dela,sans-serif;font-size:18px;letter-spacing:.04em}'+
 '.khint{margin:6px 0;padding:6px 10px;border-left:4px solid #c9a24a;background:rgba(201,162,74,.1);font-size:14px}.khelp summary{cursor:pointer;font-size:13px;opacity:.8;margin:4px 0}'+
 '.kpre{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:6px;margin:6px 0}.kpre>b{grid-column:1/-1}.kpre button{text-align:left;padding:8px 10px;border-radius:8px;border:1px solid rgba(201,162,74,.6);background:rgba(127,127,127,.1);color:inherit;cursor:pointer}.kpre button small{display:block;font-size:11px;opacity:.75;margin-top:2px}'+
 '.kg{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:8px 10px;margin:6px 0}.kgh{margin-bottom:2px}.kgl{display:flex;flex-wrap:wrap;gap:4px 10px;font-size:13px;margin-top:6px}.kgl span{cursor:pointer;text-decoration:underline dotted}'+
 '.kt3 td{vertical-align:middle}.kt3 tr.ij td{opacity:.75}.kt3 tr:nth-child(even) td{background:rgba(127,127,127,.06)}'+
 '</style>');
})();
