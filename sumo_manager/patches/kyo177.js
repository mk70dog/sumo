/* v177 協会の役員(理事 10 人・理事長)。2 年ごと(偶数年の初場所のあと)に理事を選び、理事の中から理事長を決める。
   2026 年の顔ぶれは本物(理事長 八角、理事 八角・浅香山・藤島・尾上・片男波・追手風・出羽海・高田川・佐渡ヶ嶽・伊勢ノ海)。
   選ばれやすさ(年齢・部屋の大きさと強さ・今の理事は続けやすい)と「選挙のとき 64 歳以上は出ない」は推定。65 歳の定年で必ず交代。 */
const KYO_R26=['八角','浅香山','藤島','尾上','片男波','追手風','出羽海','高田川','佐渡ヶ嶽','伊勢ノ海'];
function kyoName(i){const h=G.heya[i];if(!h)return '';if(i===ME())return me().o||(h.n+'親方');return h.n+(h.o2?'(元・'+h.o2+')':'親方');}
function kyoAge(i){return i===ME()?(me().age||50):(G.heya[i].oa||50);}
function kyoSeat(i){return {h:i,gen:G.heya[i].gen||1,o2:G.heya[i].o2||'',n:kyoName(i)};}
function kyoOk(s){const h=G.heya[s.h];if(!h||h.closed)return false;if(s.h===ME())return G.post>=1;return (h.gen||1)===s.gen&&(s.o2==null||(h.o2||'')===s.o2)&&kyoAge(s.h)<65;}
function kyoSc(i,inc){const h=G.heya[i];const a=kyoAge(i);const n=G.order.filter(id=>G.R[id].h===i&&!G.R[id].ret);const sk=n.filter(id=>G.R[id].d<=1).length;return (Math.min(a,62)-40)*.5+n.length*.15+sk*.8+(h.q||1)*8+(inc?8:0)+Math.random()*3;}
function kyoCand(){return openAI().filter(i=>kyoAge(i)>=40&&kyoAge(i)<64);}
function kyoFill(){const K=G.kyo;const has=new Set(K.rj.map(s=>s.h));const L=kyoCand().filter(i=>!has.has(i)).map(i=>[i,kyoSc(i,0)]).sort((a,b)=>b[1]-a[1]);while(K.rj.length<10&&L.length)K.rj.push(kyoSeat(L.shift()[0]));}
function kyoElect(){const K=G.kyo;const inc=new Set(K.rj.filter(kyoOk).map(s=>s.h));const sc=kyoCand().map(i=>[i,kyoSc(i,inc.has(i)),G.heya[i].ic]).sort((a,b)=>b[1]-a[1]);
 const pick=[];if(G.post>=1)pick.push(ME());
 for(let ic=0;ic<5;ic++){const c=sc.find(x=>x[2]===ic&&!pick.includes(x[0]));if(c&&pick.length<10)pick.push(c[0]);}
 for(const x of sc){if(pick.length>=10)break;if(!pick.includes(x[0]))pick.push(x[0]);}
 const nw=pick.filter(i=>!inc.has(i)&&i!==ME()).length;K.rj=pick.map(kyoSeat);
 addNews('協会の役員選挙で理事 10 人が決まりました('+(nw?'新しい理事 '+nw+' 人':'顔ぶれは変わらず')+')。');}
function kyoPickChair(el){const K=G.kyo;if(G.post===2)return ME();const c=K.ch;if(c&&c.h!==ME()&&kyoOk(c)&&K.rj.some(s=>s.h===c.h)&&!(el&&kyoAge(c.h)>=64))return c.h;
 const L=K.rj.filter(s=>s.h!==ME()&&kyoOk(s)).map(s=>[s.h,kyoSc(s.h,0)+Math.min(kyoAge(s.h),62)*.3]).sort((a,b)=>b[1]-a[1]);return L.length?L[0][0]:null;}
function kyoSetChair(i,why){const K=G.kyo;if(i==null)return;const y=curYear();const last=K.hist[K.hist.length-1];if(last&&!last.y1)last.y1=y;
 K.ch=Object.assign(kyoSeat(i),{since:y});K.hist.push({y0:y,n:K.ch.n,hn:G.heya[i].n});if(K.hist.length>40)K.hist.shift();
 hlog((i===ME()?'親方が':'')+'日本相撲協会の新しい理事長に、'+(i===ME()?'':K.ch.n+'が')+'選ばれました'+(why||'')+'。');}
function kyoInit(){if(G.kyo)return;const K=G.kyo={rj:[],hist:[],ly:curYear()-(curYear()%2),ch:null};
 if(G.real){KYO_R26.forEach(n=>{const i=G.heya.findIndex(h=>!h.closed&&h.n===n);if(i<0||isPH(i)&&i!==ME())return;if(i===ME()&&G.post<1)return;K.rj.push(kyoSeat(i));});}
 if(G.post>=1&&!K.rj.some(s=>s.h===ME()))K.rj.unshift(kyoSeat(ME()));kyoFill();if(K.rj.length>10)K.rj.length=10;
 let c=null;if(G.post===2)c=ME();else if(G.real){const i=G.heya.findIndex(h=>!h.closed&&h.n==='八角');if(i>=0&&K.rj.some(s=>s.h===i))c=i;}if(c==null)c=kyoPickChair(0);
 if(c!=null){K.ch=Object.assign(kyoSeat(c),{since:(G.real&&G.heya[c].n==='八角'&&c!==ME())?2015:curYear()});K.hist.push({y0:K.ch.since,n:K.ch.n,hn:G.heya[c].n});}}
function kyoBasho(){if(!G||!G.heya)return;kyoInit();const K=G.kyo;const y=curYear();
 const bad=K.rj.filter(s=>!kyoOk(s));if(bad.length){K.rj=K.rj.filter(s=>!bad.includes(s));kyoFill();}
 if(G.post>=1&&!K.rj.some(s=>s.h===ME())){K.rj.push(kyoSeat(ME()));while(K.rj.length>10){const L=K.rj.filter(s=>s.h!==ME()&&!(K.ch&&s.h===K.ch.h)).sort((a,b)=>kyoSc(a.h,1)-kyoSc(b.h,1));K.rj.splice(K.rj.indexOf(L[0]),1);}}
 let el=false;if((G.bnum-1)%6===0&&y%2===0&&K.ly!==y){K.ly=y;kyoElect();el=true;}
 const ok=K.ch&&kyoOk(K.ch)&&K.rj.some(s=>s.h===K.ch.h)&&!(K.ch.h===ME()&&G.post!==2);const c=kyoPickChair(el);
 if(!ok)kyoSetChair(c,K.ch?'(前の理事長の'+(K.ch.h===ME()?'任期が終わったため':'退任による')+')':'');else if(c!=null&&c!==K.ch.h)kyoSetChair(c,el?'(役員選挙のあとの理事会で)':'');}
