/* 見本 dg1〜dg5:取組の動画(真上から見た土俵)の絵の見直し。動き(dhPlan・dhPlay)はそのまま、絵だけ差しかえる。
   #dg0=今のまま / #dg1 本物に近い土俵 / #dg2 錦絵風 / #dg3 中継風(斜め上から) / #dg4 見やすさ重視 / #dg5 夜の国技館 */
(function(){
const V=+((location.hash.match(/dg(\d)/)||[])[1]||1);window.DGV=V;if(V===0)return;
const _pose=dhPose;
const SK={1:'#e8b88c',2:'#f2d2a8',3:'#e8b88c',4:'#f0c998',5:'#e9b88a'}[V];
const INK=V===2?'#1a1410':'#5a3a1a';
/* 真上から見た力士:胴(.bd)・腹・まわし(背中に結び目)・頭と髷・腕 */
function body(cls,col,nm,kg){
 const sc=V===4?1:1.05;const s=dhSide(kg)*sc,h=s/2;const aw=Math.max(6,s*.2).toFixed(1),hr=Math.max(5,s*.13).toFixed(1);
 const arm='<line class="a1" stroke="'+SK+'" stroke-width="'+aw+'" stroke-linecap="round"/><line class="a2" stroke="'+SK+'" stroke-width="'+aw+'" stroke-linecap="round"/>'+
  (V===2?'':'')+'<circle class="h1" r="'+hr+'" fill="'+SK+'" stroke="'+INK+'" stroke-width="1.5"/><circle class="h2" r="'+hr+'" fill="'+SK+'" stroke="'+INK+'" stroke-width="1.5"/><g class="bst" opacity="0"></g>';
 let core;
 if(V===4){/* 見やすさ重視:色の丸+向きの三角 */
  core='<circle class="aura" r="'+(h+8)+'" fill="none" stroke="#ff8a1f" stroke-width="5" opacity="0"/>'+
   '<circle class="bd" r="'+h+'" fill="'+col+'" stroke="#fff" stroke-width="3"/>'+
   '<path d="M'+(h*.15)+','+(-h*.42)+' L'+(h*.78)+',0 L'+(h*.15)+','+(h*.42)+'Z" fill="#fff"/>';
 }else{
  const sw=V===2?2.6:1.6;const grad=V===2?'':'<ellipse cx="'+(-h*.1)+'" cy="'+(-h*.25)+'" rx="'+(s*.24)+'" ry="'+(s*.2)+'" fill="#fff" opacity=".22"/>';
  core='<ellipse cx="'+(-h*.1)+'" cy="'+(h*.14)+'" rx="'+(s*.48)+'" ry="'+(s*.58)+'" fill="#000" opacity="'+(V===5?.45:.2)+'"/>'+/* 影 */
   '<ellipse class="aura" rx="'+(s*.5+7)+'" ry="'+(s*.58+7)+'" fill="none" stroke="#ff8a1f" stroke-width="5" opacity="0"/>'+
   '<ellipse cx="'+(-h*.28)+'" rx="'+(s*.34)+'" ry="'+(s*.42)+'" fill="'+col+'" stroke="'+INK+'" stroke-width="'+sw+'"/>'+/* まわし(腰から後ろが見える) */
   '<path d="M'+(-h*.62)+','+(-s*.42)+' Q'+(-h*.9)+',0 '+(-h*.62)+','+(s*.42)+'" fill="none" stroke="'+INK+'" stroke-width="'+(sw*.7)+'" opacity=".5"/>'+
   '<rect x="'+(-h*1.02)+'" y="'+(-s*.09)+'" width="'+(s*.17)+'" height="'+(s*.18)+'" rx="2" fill="'+col+'" stroke="'+INK+'" stroke-width="'+sw+'"/>'+/* 背中の結び目 */
   '<ellipse class="bd" cx="'+(h*.1)+'" rx="'+(s*.3)+'" ry="'+(s*.5)+'" fill="'+SK+'" stroke="'+INK+'" stroke-width="'+sw+'"/>'+/* 肩と胴 */
   (V===2?'':'<ellipse cx="'+(-h*.02)+'" cy="'+(-h*.38)+'" rx="'+(s*.14)+'" ry="'+(s*.1)+'" fill="#fff" opacity=".18"/>')+
   '<circle cx="'+(h*.48)+'" r="'+(s*.15)+'" fill="#231a14" stroke="'+INK+'" stroke-width="1"/>'+/* 頭(髪) */
   '<ellipse cx="'+(h*.4)+'" rx="'+(s*.08)+'" ry="'+(s*.045)+'" fill="#000" stroke="#555" stroke-width=".6"/>'+/* 髷 */
   (V===2?'<path d="M'+(-h*.1)+','+(-h*.75)+' Q'+(h*.35)+','+(-h*.9)+' '+(h*.55)+','+(-h*.45)+'" fill="none" stroke="'+INK+'" stroke-width="1.2" opacity=".6"/>':'');
 }
 const w=[...String(nm)].length*12.5+14;
 const nmc=V===2?'<g class="nm" transform="translate(0,'+(-h-14)+')"><rect x="'+(-w/2).toFixed(1)+'" y="-11" width="'+w.toFixed(1)+'" height="19" fill="#f6ecd2" stroke="'+col+'" stroke-width="2"/><text y="4" text-anchor="middle" font-size="13" font-weight="bold" fill="'+col+'" font-family="serif">'+esc(nm)+'</text></g>'
  :'<g class="nm" transform="translate(0,'+(-h-14)+')"><rect x="'+(-w/2).toFixed(1)+'" y="-11" width="'+w.toFixed(1)+'" height="18" rx="9" fill="'+col+'" stroke="'+(V===5?'#ffe9a8':'#fff8ea')+'" stroke-width="1.5"/><text y="3" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">'+esc(nm)+'</text></g>';
 return '<g class="'+cls+'" data-h="'+h.toFixed(1)+'"'+(V===5?' style="filter:drop-shadow(0 0 3px rgba(255,236,180,.55))"':'')+'><g class="rot"><g class="arms">'+arm+'</g>'+core+'</g>'+nmc+
  '<text class="tg" y="'+(h+22)+'" text-anchor="middle" font-size="12" font-weight="bold" fill="'+(V===5?'#ffd75a':'#8a5a00')+'" stroke="'+(V===5?'#1a1410':'#fff8ea')+'" stroke-width="3" paint-order="stroke"></text></g>';}
dhRik=body;
/* 行司:装束の色・烏帽子・軍配 */
const _gy=dhGyoji;
dhGyoji=function(){let s=_gy();if(V===1||V===3||V===5)s=s.replace('class="gsc" transform="scale(1.3)"','class="gsc" transform="scale(.95)"');if(V===2)s=s.replace(/#6b3b8a/g,'#5b2f7a').replace(/stroke-width="1.5"/,'stroke-width="2.6"').replace('#2b1a3a','#1a1410');if(V===4)s=s.replace(/#6b3b8a/g,'#7b4bb0');if(V===5)s=s.replace('fill="#6b3b8a" stroke="#2b1a3a"','fill="#7a46a0" stroke="#e8c870"');return s;};
/* 観客 */
function crowd(R0,R1,G,pal,head,extra){let h='';let sd=11;const r=()=>{sd=(sd*1103515245+12345)>>>0;return (sd>>>8)/16777216;};
 for(let y=-R1;y<=R1;y+=G)for(let x=-R1;x<=R1;x+=G){const jx=x+(r()-.5)*3,jy=y+(r()-.5)*3;if(Math.abs(jx)<R0&&Math.abs(jy)<R0)continue;if(Math.abs(jx)>R1-2||Math.abs(jy)>R1-2)continue;
  const c=pal[Math.floor(r()*pal.length)],hd=head[Math.floor(r()*head.length)];const fl=extra&&r()<.12;
  h+='<g class="fan" transform="translate('+jx.toFixed(1)+','+jy.toFixed(1)+')"><g style="animation-delay:-'+(r()*.6).toFixed(2)+'s"><circle r="'+(G*.52).toFixed(1)+'" fill="'+c+'" cy="2.2"'+(V===2?' stroke="#1a1410" stroke-width="1"':'')+'/><circle r="'+(G*.34).toFixed(1)+'" fill="'+hd+'" cy="-1.4"/>'+(fl?'<circle class="fsh" r="3.2" cy="-1" fill="#fff" style="animation-delay:'+(r()*2.4).toFixed(2)+'s"/>':'')+'</g></g>';}
 return '<g class="crowd">'+h+'</g>';}
/* 本物の寸法:土俵の内径 4.55m を半径 135 にする → 1m=59.3。台(6.7m 四方)=±199、仕切り線は内側どうし 70cm・長さ 90cm・幅 6cm */
const M=135/2.275;
function realRing(o){o=o||{};const sand=o.sand||'#d8c193',clay=o.clay||'#c9a86e',bale=o.bale||'#b89a5e',line=o.line||'#6e5530';let h='';
 const SQ=3.35*M;/* 台の半分 */
 h+='<rect x="'+(-SQ-8)+'" y="'+(-SQ-8)+'" width="'+(2*SQ+16)+'" height="'+(2*SQ+16)+'" fill="'+(o.edge||'#a8865a')+'"/>';/* 台の斜面 */
 h+='<rect x="'+(-SQ)+'" y="'+(-SQ)+'" width="'+(2*SQ)+'" height="'+(2*SQ)+'" fill="'+clay+'"/>';
 /* 角俵(四角)と上げ俵(角) */
 const kb=SQ-9;for(let i=0;i<4;i++){const rot=i*90;h+='<g transform="rotate('+rot+')"><rect x="'+(-kb)+'" y="'+(kb-5)+'" width="'+(2*kb)+'" height="10" rx="5" fill="'+bale+'" stroke="'+line+'" stroke-width="1.2"/>';for(let k=1;k<7;k++)h+='<line x1="'+(-kb+2*kb*k/7)+'" y1="'+(kb-5)+'" x2="'+(-kb+2*kb*k/7)+'" y2="'+(kb+5)+'" stroke="'+line+'" stroke-width="1"/>';h+='</g>';}
 /* 蛇の目の砂(俵の外 約 25cm) */
 h+='<circle r="'+(135+5+.25*M)+'" fill="'+(o.janome||'#e9dcbc')+'"/><circle r="'+(135+5)+'" fill="'+clay+'"/>';
 h+='<circle r="135" fill="url(#'+o.id+'g)"/>';
 /* 勝負俵 16+徳俵 4(東西南北で外へずらす) */
 for(let i=0;i<20;i++){const a0=(i*18-9+1.2)*Math.PI/180,a1=(i*18+9-1.2)*Math.PI/180;const mid=i*18;const toku=mid%90===0;const R=toku?135+8:135;
  const p=(a)=>[(R*Math.cos(a)).toFixed(1),(R*Math.sin(a)).toFixed(1)];const A=p(a0),B=p(a1);h+='<path d="M'+A+' A'+R+','+R+' 0 0 1 '+B+'" fill="none" stroke="'+bale+'" stroke-width="9" stroke-linecap="round"/><path d="M'+A+' A'+R+','+R+' 0 0 1 '+B+'" fill="none" stroke="'+line+'" stroke-width="1" stroke-dasharray="3 4" opacity=".7"/>';}
 h+='<circle class="tw" r="135" fill="none" stroke="'+bale+'" stroke-width="2"/>';
 /* 仕切り線 */
 const gx=(.35+.03)*M,gl=.45*M,gw=.06*M;h+='<rect x="'+(-gx-gw/2)+'" y="'+(-gl)+'" width="'+gw+'" height="'+(2*gl)+'" fill="#fff"/><rect x="'+(gx-gw/2)+'" y="'+(-gl)+'" width="'+gw+'" height="'+(2*gl)+'" fill="#fff"/>';
 return h;}
function fusa(R,len){/* 四房:正面(下)から見て 東=左。青房=正面東、黒房=正面西、赤房=向正面東、白房=向正面西 */
 const F=[[-1,1,'#2a6fb5','青房'],[1,1,'#1d1d1d','黒房'],[-1,-1,'#c2341f','赤房'],[1,-1,'#f4f1e6','白房']];
 return F.map(f=>'<g transform="translate('+(f[0]*R)+','+(f[1]*R)+')"><circle r="'+len+'" fill="'+f[2]+'" stroke="#c9a24a" stroke-width="2"/><circle r="'+(len*.45)+'" fill="none" stroke="'+(f[2]==='#f4f1e6'?'#999':'#fff')+'" stroke-width="1" opacity=".6"/></g>').join('');}
function person(x,y,col,rot,lab){return '<g transform="translate('+x+','+y+') rotate('+(rot||0)+')"><ellipse rx="9" ry="12" fill="'+col+'"/><circle cx="3" r="5.5" fill="#1d1d1d"/></g>';}
function judges(R){/* 審判 5 人(黒の紋付)・控え力士(東西)・呼出(簡略) */
 return person(0,R,'#2a2a2a',-90)+person(-62,-R,'#2a2a2a',90)+person(62,-R,'#2a2a2a',90)+person(-R,72,'#2a2a2a',0)+person(R,72,'#2a2a2a',180)+
  '<g transform="translate('+(-R)+',-60)"><ellipse rx="11" ry="14" fill="#e8b88c" stroke="#5a3a1a"/><circle cx="3" r="6" fill="#231a14"/></g><g transform="translate('+R+',-60) rotate(180)"><ellipse rx="11" ry="14" fill="#e8b88c" stroke="#5a3a1a"/><circle cx="3" r="6" fill="#231a14"/></g>';}
const lab=(x,y,t,c,sc)=>'<text x="'+x+'" y="'+y+'" text-anchor="middle" font-size="12" fill="'+(c||'#fff8ea')+'" stroke="'+(sc||'#3a2a1a')+'" stroke-width="3" paint-order="stroke">'+t+'</text>';
const _svg=dhSVG;
dhSVG=function(id,nE,nW,kE,kW){let s=_svg(id,nE,nW,kE,kW);
 const a=s.indexOf('<rect x="-215" y="-215"'),b=s.indexOf('<g class="gyo">');if(a<0||b<0)return s;
 let bg='',vb='-215 -215 430 430',defs='';
 const E=V===4?'#e0452b':'#b5361f',W=V===4?'#2f6fd0':'#2d4d7a';
 if(V===1||V===3){vb='-232 -232 464 464';
  defs='<radialGradient id="'+id+'g"><stop offset="0" stop-color="#e2cc9c"/><stop offset=".85" stop-color="#d6bc88"/><stop offset="1" stop-color="#c9ab73"/></radialGradient>';
  bg='<rect x="-250" y="-250" width="500" height="500" fill="#7a2f2a"/>'+crowd(232,252,12,['#3a4a6a','#6a3a3a','#4a5a3a','#5a4a6a','#2d4d7a','#ddd','#c9a24a','#e9e2d0','#8a8a8a'],['#2b2420','#1d1d1d','#4a3a2a','#6b5a4a','#8a8a8a'])+
   '<rect x="-232" y="-232" width="464" height="464" fill="#8e3a33"/>'+/* 溜席の座布団(臙脂) */
   realRing({id})+judges(214)+fusa(206,9)+lab(0,229,'正面')+lab(0,-222,'向正面')+lab(-222,4,'東')+lab(222,4,'西');}
 else if(V===2){
  defs='<radialGradient id="'+id+'g"><stop offset="0" stop-color="#ecd9ae"/><stop offset="1" stop-color="#ddc595"/></radialGradient><pattern id="'+id+'w" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#efe2c4"/><path d="M0,20 Q10,8 20,20 T40,20" fill="none" stroke="#c9b48a" stroke-width="1"/><path d="M0,40 Q10,28 20,40 T40,40" fill="none" stroke="#c9b48a" stroke-width="1"/></pattern><filter id="'+id+'f"><feTurbulence baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .35  0 0 0 0 .2  0 0 0 .10 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>';
  bg='<rect x="-215" y="-215" width="430" height="430" fill="url(#'+id+'w)"/>'+crowd(170,215,14,['#2e4a7a','#b5361f','#3f5f3a','#6b3b8a','#c98a2a','#1d2a44','#e6d3a8'],['#1a1410'])+
   '<rect x="-163" y="-163" width="326" height="326" fill="#cfae74" stroke="#1a1410" stroke-width="3"/><circle r="150" fill="#cfae74" stroke="#1a1410" stroke-width="1.5"/><circle r="135" fill="url(#'+id+'g)"/>'+
   '<circle class="tw" r="135" fill="none" stroke="#8a6a3a" stroke-width="10"/><circle r="140" fill="none" stroke="#1a1410" stroke-width="2"/><circle r="130" fill="none" stroke="#1a1410" stroke-width="2"/>'+
   '<rect x="-215" y="-215" width="430" height="430" filter="url(#'+id+'f)" fill="#fff"/>'+
   '<line x1="-20" y1="-24" x2="-20" y2="24" stroke="#fff" stroke-width="4"/><line x1="20" y1="-24" x2="20" y2="24" stroke="#fff" stroke-width="4"/>'+
   fusa(185,10)+
   lab(0,207,'正面','#1a1410','#efe2c4')+lab(0,-199,'向正面','#1a1410','#efe2c4')+'<rect x="-212" y="-10" width="20" height="20" fill="#efe2c4" stroke="#1a1410"/><rect x="192" y="-10" width="20" height="20" fill="#efe2c4" stroke="#1a1410"/>'+lab(-202,5,'東','#b5361f','#efe2c4')+lab(202,5,'西','#2e4a7a','#efe2c4');}
 else if(V===4){
  defs='<radialGradient id="'+id+'g"><stop offset="0" stop-color="#f1e2bd"/><stop offset="1" stop-color="#ead6a6"/></radialGradient>';
  bg='<rect x="-215" y="-215" width="430" height="430" fill="#24324a" rx="10"/>'+
   '<rect x="-170" y="-170" width="340" height="340" rx="6" fill="#d9c08c"/><circle r="135" fill="url(#'+id+'g)"/><circle r="152" fill="none" stroke="#c94a3a" stroke-width="2" stroke-dasharray="4 6" opacity=".7"/>'+
   '<circle class="tw" r="135" fill="none" stroke="#7a5a32" stroke-width="7"/>'+
   '<line x1="-20" y1="-24" x2="-20" y2="24" stroke="#fff" stroke-width="4"/><line x1="20" y1="-24" x2="20" y2="24" stroke="#fff" stroke-width="4"/>'+
   '<text y="206" text-anchor="middle" font-size="13" font-weight="bold" fill="#cfd8ea">正面</text><text x="-196" y="5" font-size="16" font-weight="bold" fill="'+E+'">東</text><text x="182" y="5" font-size="16" font-weight="bold" fill="'+W+'">西</text>';}
 else if(V===5){vb='-232 -232 464 464';
  defs='<radialGradient id="'+id+'g"><stop offset="0" stop-color="#f6e2b0"/><stop offset=".8" stop-color="#e3c68e"/><stop offset="1" stop-color="#c9a466"/></radialGradient><radialGradient id="'+id+'L"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".72"/></radialGradient>';
  bg='<rect x="-250" y="-250" width="500" height="500" fill="#0d0b10"/>'+crowd(232,252,12,['#2a2630','#3a2a2a','#262c38','#3a3424','#4a4450'],['#141014','#1c1818'],1)+
   '<rect x="-232" y="-232" width="464" height="464" fill="#3a1a1c"/>'+
   realRing({id,clay:'#d4b072',sand:'#e3c68e',bale:'#c9a466',line:'#6e5530',janome:'#f1e4c2',edge:'#8a6a40'})+judges(214)+
   '<rect x="-250" y="-250" width="500" height="500" fill="url(#'+id+'L)" pointer-events="none"/>'+
   '<rect x="-212" y="-212" width="424" height="424" fill="none" stroke="#c9a24a" stroke-width="1.5" stroke-dasharray="2 5" opacity=".55"/>'+/* 吊り屋根のふち(真上から) */
   fusa(212,10)+lab(0,229,'正面','#e9d8b0','#000')+lab(0,-222,'向正面','#e9d8b0','#000')+lab(-222,4,'東','#ff8a6a','#000')+lab(222,4,'西','#8ab8ff','#000');}
 s=s.slice(0,a)+bg+s.slice(b);
 s=s.replace(/<defs>[\s\S]*?<\/defs>/,'<defs>'+defs+'</defs>').replace('viewBox="-215 -215 430 430"','viewBox="'+vb+'"');
  if(V===4)s=s.replace(/fill="#b5361f"/g,'fill="'+E+'"');
 if(V===3)s=s.replace('<div class="dhw"','<div class="dhw dg3"').replace('</svg>','</svg><svg class="dgroof" viewBox="0 0 400 70" preserveAspectRatio="none"><path d="M0,0 H400 V30 Q200,44 0,30Z" fill="#2a1d14"/><path d="M0,28 Q200,42 400,28 V44 Q200,58 0,44Z" fill="#5b2f7a"/><path d="M0,40 Q200,54 400,40" stroke="#c9a24a" stroke-width="2" fill="none"/><g><rect x="70" y="40" width="10" height="18" fill="#c2341f"/><circle cx="75" cy="60" r="6" fill="#c2341f"/></g><g><rect x="320" y="40" width="10" height="18" fill="#f4f1e6"/><circle cx="325" cy="60" r="6" fill="#f4f1e6" stroke="#bbb"/></g><g><rect x="4" y="0" width="14" height="52" fill="#2a6fb5"/><circle cx="11" cy="58" r="10" fill="#2a6fb5"/></g><g><rect x="382" y="0" width="14" height="52" fill="#1d1d1d"/><circle cx="389" cy="58" r="10" fill="#1d1d1d"/></g></svg>');
 return s;};
/* 色:胴の色(勢い)と手の色を絵柄にあわせる */
dhPose=function(g,p,q,stance,ph,pushing,fallen,fx){_pose(g,p,q,stance,ph,pushing,fallen,fx);
 const bd=g.querySelector('.bd');if(!bd)return;const heat=fx.heat||0;
 if(V===4){const col=g.classList.contains('ge')?'#e0452b':'#2f6fd0';bd.setAttribute('fill',col);}
 else bd.setAttribute('fill',dhMix(SK,'#ff9a5a',heat*.8));
 g.querySelectorAll('.h1,.h2').forEach(c=>{if(c.getAttribute('fill')==='#f0c998')c.setAttribute('fill',SK);if(V===2&&c.getAttribute('stroke')==='#5a3a1a')c.setAttribute('stroke',INK);});};
/* 見た目の CSS */
let css='';
if(V===3)css='.dhw.dg3{perspective:900px;padding-top:10%;background:linear-gradient(#1c130d,#3a2418 30%,#5a2a24);overflow:hidden;border-radius:8px}.dhw.dg3 .dhbar,.dhw.dg3 .dhlg{background:#fffaf0;padding:2px 4px}.dhw.dg3 .dhy{transform:rotateX(38deg) scale(1.08);transform-origin:50% 55%}.dhw.dg3.shake .dhy{animation:dhs3 .26s}@keyframes dhs3{0%,100%{transform:rotateX(38deg) scale(1.08)}25%{transform:rotateX(38deg) scale(1.08) translate(-4px,2px)}50%{transform:rotateX(38deg) scale(1.08) translate(4px,-2px)}}.dhw .dgroof{position:absolute;left:-2%;top:0;width:104%;height:14%;pointer-events:none;z-index:1}';
if(V===2)css='.dhw .dhy{border:4px solid #1a1410;box-sizing:border-box;background:#efe2c4}.dhbar,.dhlg{font-family:serif!important}';
if(V===4)css='.dhw .dhy{border-radius:10px}.dhw .dhy .tg{font-size:14px}';
if(V===5)css='.dhw .dhy{background:#0d0b10;border-radius:8px}.dhw .crowd .fsh{opacity:0}.dhw.cheer .crowd .fsh,.dhw.roar .crowd .fsh{animation:fsh 1.2s steps(1) infinite}@keyframes fsh{0%{opacity:0}8%{opacity:1}16%{opacity:0}}';
document.head.insertAdjacentHTML('beforeend','<style>'+css+'</style>');
})();
