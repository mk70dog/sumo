/* ========== v131:部屋付き親方を探して来てもらう ==========
 ①部屋付き親方の人柄(s.hito 1〜20、人望)と教え方(s.tch 1〜20、指導力が弟子に届く度合い)。前の版の親方は名前から決まる(推定)。
   教え方:育つ環境の指導力に ×(0.85+0.015×教え方)。人柄:場所ごとに弟子の信頼 +(人柄−10)×0.03(担当の弟子は 2 倍)、
   相談事(悩み)のときに人柄 14 以上の親方がいれば「○○親方に話を聞いてもらう」が選べる。
 ②「こんな親方に来てほしい」(G.coReq {k,b}、20 万円、2 場所):押し・四つ・技・体作り・人柄・若い衆の担当。場所ごとの「雇える人」に条件に合う候補が 1〜2 人。
   実在の部屋で始めたときは、同じ一門の年寄から(いなければほかの一門から)。
 ③来てもらう交渉(部屋付き親方):来てくれる見込み coAcc = 0.5 +(評判−50)×0.006 + 関取 ×0.03 + 同じ一門 0.15/ほかの一門 −0.2
   + 型の合う弟子 2 人以上 0.1 + 人柄・教え方が高い人ほど選り好み −0.05(0.1〜0.95)。断られると候補から消える。
   実際も所属の変更は理事会の承認が要り、閉鎖した部屋の親方は同じ一門の部屋付きになる例が多い(デイリー 2018/10/1・2020/7/14、時事 2024/3/28)。
 ④型との相性:担当の親方の取り口(押し・四つ・技)と、弟子の目指す型(v129)が合うと型づくり ×1.15。数字はすべて推定。 */
const COREQ={osh:['押しを教えられる親方','osh'],yot:['四つを教えられる親方','yot'],waz:['技を教えられる親方','waz'],tai:['体作りの上手な親方','tai'],hito:['人望のある相談相手','hito'],waka:['若い衆を任せられる親方','waka']};
function coInit(s){if(s.role!=='co')return s;if(s.hito==null){const h=kcHash('hito|'+s.n);s.hito=Math.round(cl(10+((h%1000)/1000-.5)*12+(((s.sk&&s.sk.sei)||10)-10)*.2,3,18));s.tch=Math.round(cl(10+(((h>>>10)%1000)/1000-.5)*12,3,18));}return s;}
function coTch(s){coInit(s);return .85+.015*s.tch;}
function coHitoCycle(){const co=G.staff.filter(s=>s.role==='co').map(coInit);if(!co.length)return;own().forEach(r=>{let d=0;co.forEach(s=>{const a=coA(s);const mine=(a.t==='one'&&a.r===r.id)||(a.t==='seki'&&r.d<=1)||(a.t==='waka'&&r.d>=2);d+=(s.hito-10)*.03*(mine?2:1);});r.tr=cl((r.tr==null?50:r.tr)+d,0,100);});}
function coGoodHito(){return G.staff.filter(s=>s.role==='co').map(coInit).filter(s=>s.hito>=14).sort((a,b)=>b.hito-a.hito)[0]||null;}
function coStyleN(s){const t=kcStyleS(s);return {押:'押し相撲',四:'四つ相撲',技:'技能派'}[t];}
function coTkFit(r,p){try{const c=kcCoach(r);if(!c.co)return 1;const st=c.st;return (st==='押'&&(p==='O'||p==='X'))||(st==='四'&&(p==='R'||p==='L'||p==='X'))||(st==='技'&&p==='W')?1.15:1;}catch(e){return 1;}}
function coAcc(s){coInit(s);const sek=own().filter(r=>r.d<=1).length;const fromH=s.from?G.heya.find(h=>h.n===s.from):null;
 const ic=fromH?(fromH.ic===me().ic&&me().ic>=0?.15:-.2):0;const st=kcStyleS(s);const fit=own().filter(r=>r.tk&&((st==='押'&&r.tk.p==='O')||(st==='四'&&(r.tk.p==='R'||r.tk.p==='L'))||(st==='技'&&r.tk.p==='W')||r.tk.p==='X')).length;
 return cl(.5+((G.rep==null?50:G.rep)-50)*.006+sek*.03+ic+(fit>=2?.1:0)-(s.hito+s.tch>=30?.05:0),.1,.95);}
function coReqSet(k){if(!COREQ[k])return '';if(G.money<20)return '資金が足りません。';G.money-=20;G.coReq={k:k,b:G.bnum};addNews('一門の親方衆に「'+COREQ[k][0]+'」を探していると声をかけました(交際費 20 万円)。次の場所から、雇える人に候補が出ます。');return 'OK';}
function coReqMake(){const q=G.coReq;if(!q)return;if(G.bnum-q.b>2){G.coReq=null;addNews('部屋付き親方探しの声かけは、いったん終わりました。');return;}
 const k=q.k;const n=Math.random()<.5?1:2;const fix=s=>{coInit(s);s.req=k;if(k==='hito'){s.hito=RI(14,18);s.sk.sei=Math.max(s.sk.sei,RI(12,16));}else if(k==='waka'){s.hito=Math.max(s.hito,RI(12,16));s.tch=Math.max(s.tch,RI(12,16));s.sk.tai=Math.max(s.sk.tai,RI(11,15));}else s.sk[k]=Math.max(s.sk[k],RI(14,17));s.tch=Math.max(s.tch,RI(10,15));return s;};
 let added=0;if(G.toshi){const C=G.toshi.map((t,i)=>[t,i]).filter(([t])=>!t.left&&!t.shi&&t.heya!==me().n&&t.post!=='参与'&&ageOf(t.b)<62&&tHeya(t.heya)>0&&!G.market.some(m=>m.tid!=null&&G.toshi[m.tid]===t));
  const same=C.filter(([t])=>G.heya[tHeya(t.heya)].ic===me().ic),L=(same.length?same:C).sort(()=>Math.random()-.5).slice(0,n);
  L.forEach(([t,i])=>{const sf=fix(staffFromToshi(t,i));sf.from=t.heya;G.market.push(sf);added++;});}
 else for(let i=0;i<n;i++){G.market.push(fix(mkStaff('co',R(9,13))));added++;}}
function coEvt(){const so=EVT.soudan;if(!so||so._co)return;so._co=1;const c0=so.c,a0=so.ap;
 so.c=e=>{const L=c0(e).slice();const g=coGoodHito();if(e.tp==='nayami'&&g)L.push(g.n.replace(/^元・/,'')+'親方に話を聞いてもらう(人柄 '+g.hito+')');return L;};
 so.ap=(e,i)=>{if(e.tp==='nayami'&&i===2){const g=coGoodHito(),r=G.R[e.rid];if(!g||!r||r.ret)return '';trAdd(r,4,'部屋付き親方が話を聞いてくれた');r.mor=cl(r.mor+8,0,100);r.kn=Math.min(100,r.kn+3);return g.n.replace(/^元・/,'')+'親方がじっくり話を聞き、'+r.n+'は気持ちが軽くなったようです。';}return a0(e,i);};}
