// v133 結婚・縁談・婿の継承の確認。usage: node fm133.js file.html
const fs=require('fs'),vm=require('vm');const html=fs.readFileSync(process.argv[2],'utf8');
const code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));const store={};
const ctx={console,localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;},removeItem:k=>{delete store[k];}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,EVT,fmCycle,spInit};',ctx);const X=ctx.__X;
ctx.newGameReal('木瀬');const G=()=>ctx.__get();X.spInit();const out={};
X.own().forEach(x=>{delete x.kk;});const r=X.own().filter(x=>x.d<=1).sort((a,b)=>a.pos-b.pos)[0];
G().ev.push({k:'kekkon',rid:r.id,id:'k1'});out.k=ctx.resolveEv('k1',0);out.mar=r.mar;
G().sp.fam.kids=[{rel:'長女',boy:0,age:26}];const c=X.own().filter(x=>x.d<=1&&x!==r)[0];c.tr=80;
G().ev.push({k:'endan',rid:c.id,rel:'長女',age:26,id:'e1'});out.e=ctx.resolveEv('e1',0);out.muko=c.muko;
const e=ctx.mkShokei();out.sc=X.EVT.shokei.c(e);G().ev.push(e);out.s=ctx.resolveEv(e.id,0);out.ret=!!c.ret;out.oy=G().heya[0].o;out.okami=G().okami&&G().okami.n;
console.log(JSON.stringify(out,null,1));
