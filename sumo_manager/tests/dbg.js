const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2],'utf8');let code=html.slice(html.indexOf("'use strict';"),html.indexOf('/* ========== 画面'));
const store={};const ctx={console,localStorage:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=v;}},document:{documentElement:{style:{setProperty(){}}},querySelector:()=>null,getElementById:()=>null},setTimeout};ctx.window=ctx;
vm.createContext(ctx);vm.runInContext(code+';globalThis.__get=()=>G;globalThis.__X={own,ownAll,EVT};',ctx);
module.exports=ctx;
