function oyN(){return me().o.replace(/[((].*$/,'')+'親方';}
function koePeople(){
 const o=own(),P=[];const L=(who,role,lines)=>{if(lines.length)P.push({who,role,lines});};
 const t=heyaTop(),inj=o.filter(r=>r.inj),fat=o.filter(r=>r.fat>70),down=o.filter(r=>(r.tr==null?50:r.tr)<35||r.mor<35);
 const a=[];
 a.push(G.money<0?'借金がかさんでいる…。なんとかしないとな。':G.money<500?'金のやりくりが苦しい。後援会に頭を下げに行くか…。':'お金の心配は、今のところない。');
 if(t)a.push('部屋頭の'+t.n+'('+t.rk+')には、もっと上を目指してほしいんだが。');
 if(inj.length)a.push('けが人が '+inj.length+' 人。無理はさせられん。');
 if(me().age>=60)a.push('定年まであと '+Math.max(0,65-Math.floor(me().age))+' 年か…。跡継ぎを考えないと。');
 L(oyN(),'師匠',a);
 if(G.okami){const b=[],at=atmo();b.push(at>=65?'みんな明るくやっています。ちゃんこもよく食べるし。':at<40?'若い子たちの元気がないのが気になります。':'部屋の雰囲気は落ち着いています。');
  b.push('後援会の方は '+G.sup+' 人。この前も差し入れをいただきました。');
  if(down[0])b.push(down[0].n+'が、このところ少し落ち込んでいるみたい。');
  L(G.okami.n,'おかみさん',b);}
 G.staff.filter(s=>s.role==='co').slice(0,1).forEach(s=>{const c=[];c.push(fat.length?fat.slice(0,3).map(r=>r.n).join('・')+'は疲れがたまっています。少し軽めにしましょう。':'稽古は順調です。みんなよく動けています。');
  const up=o.filter(r=>!r.inj&&r.mor>=70).slice(0,2);if(up.length)c.push(up.map(r=>r.n).join('・')+'は気合いが入っていますよ。');L(s.n,'部屋付き親方',c);});
 G.staff.filter(s=>s.role==='sc').slice(0,1).forEach(s=>{L(s.n,'マネージャー',['新弟子の候補は '+G.pros.length+' 人。'+(G.pros.length?'近いうちに会いに行きたいですね。':'今は情報が少ないです。')]);});
 if(inj.length&&Object.keys(G.con||{}).some(k=>G.con[k]))L('契約トレーナー','トレーナー',inj.slice(0,3).map(r=>r.n+'の'+r.inj.p+'は、あと '+r.inj.wk+' 週ほどみてください。'));
 const d=[];inj.slice(0,2).forEach(r=>d.push([r,r.inj.p+'が痛くて…。早く土俵に戻りたいです。']));
 fat.filter(r=>!r.inj).slice(0,1).forEach(r=>d.push([r,'体が重いっす…。']));
 o.filter(r=>!r.inj&&r.mor<35).slice(0,1).forEach(r=>d.push([r,'最近、うまくいかなくて…。']));
 o.filter(r=>!r.inj&&r.mor>=75).slice(0,1).forEach(r=>d.push([r,'調子いいです! 今場所は勝ち越したいです。']));
 d.slice(0,4).forEach(([r,x])=>L(r.n,'弟子・'+r.rk,[x]));
 return P;}
