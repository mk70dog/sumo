const fs=require('fs'),vm=require('vm');const [,,file,yS,sS]=process.argv;const yrs=+yS||3;let seed=+sS||1;const rnd=()=>{seed=(seed*1103515245+12345)%2147483648;return seed/2147483648;};
const html=fs.readFileSync(file,'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,Math:Object.create(Math),localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
ctx.Math.random=rnd;vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__bn=bname;',ctx);
const C=ctx;C.newGameReal('高田川');let need=0,miss=0,yo=0,yom=0;const ex=[];
for(let b=0;b<yrs*6;b++){while(C.__get().phase==='train')C.doWeek();
 let G=C.__get();const top=G.order.map(i=>G.R[i]).filter(r=>r.d===0&&(r.t==='Y'||r.t==='O'||r.t==='S'||r.t==='K'));const met=new Set();let BB=null;
 while(C.__get().phase==='basho'){if(!BB)BB=C.__get().B;const bs=C.advanceDay();bs.forEach(x=>{if(x.fus)return;met.add(x.w+'|'+x.l);met.add(x.l+'|'+x.w);});}
 G=C.__get();
 for(let i=0;i<top.length;i++)for(let j=i+1;j<top.length;j++){const a=top[i],c=top[j];if(a.h===c.h)continue;const ha=a.hist[a.hist.length-1],hc=c.hist[c.hist.length-1];if(!ha||!hc||ha.b!==G.bnum||hc.b!==G.bnum||ha.ab||hc.ab)continue;if(b===0)continue;need++;const isT=r=>r.t==='Y'||r.t==='O';if(isT(a)&&isT(c)){yo++;if(!met.has(a.id+'|'+c.id))yom++;}if(!met.has(a.id+'|'+c.id)){miss++;if(ex.length<12)ex.push(C.__bn(G.bnum)+' '+a.n+'('+a.t+') - '+c.n+'('+c.t+')');}}
 while(G.ev.length)C.resolveEv(G.ev[0].id,0);C.nextCycle();}
console.log('横綱・大関どうし',yo,'抜け',yom);console.log('役力士どうし(休場なし・別部屋)の組み合わせ',need,'当たらなかった',miss);console.log(ex.join('\n'));
