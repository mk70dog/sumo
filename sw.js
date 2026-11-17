// Sumo Manager のオフライン用(サービスワーカー)。v38 から。
// ネットにつながっているときはいつもネットの最新を使い、取れたものを保存しておく。つながらないときだけ保存したものを出す。
// Sumo Manager のファイル(入口・設定・sumo_manager/ の中。見本 samples/ は除く)だけを扱い、judge/ などほかには何もしない。
const CACHE='sumo-manager-1';
const BASE=new URL('./',self.location).pathname; // 例:/sumo/
const mine=p=>p===BASE||p===BASE+'index.html'||p===BASE+'manifest.webmanifest'||(p.startsWith(BASE+'sumo_manager/')&&!p.startsWith(BASE+'sumo_manager/samples/'));
const key=u=>{const x=new URL(u,self.location);return x.origin+x.pathname;};
self.addEventListener('install',e=>{e.waitUntil((async()=>{const c=await caches.open(CACHE);
 const list=[BASE,BASE+'index.html',BASE+'manifest.webmanifest',BASE+'sumo_manager/index.html',BASE+'sumo_manager/latest.json',BASE+'sumo_manager/img/icon180.png',BASE+'sumo_manager/img/icon512.png'];
 for(const u of list){try{const r=await fetch(u,{cache:'no-store'});if(r.ok)await c.put(key(u),r);}catch(_){}}
 try{const j=await (await fetch(BASE+'sumo_manager/latest.json',{cache:'no-store'})).json();if(j&&j.file){const u=BASE+'sumo_manager/'+j.file;const r=await fetch(u,{cache:'no-store'});if(r.ok)await c.put(key(u),r);}}catch(_){}
 await self.skipWaiting();})());});
self.addEventListener('activate',e=>{e.waitUntil((async()=>{for(const k of await caches.keys())if(k.startsWith('sumo-manager-')&&k!==CACHE)await caches.delete(k);await self.clients.claim();})());});
self.addEventListener('fetch',e=>{const q=e.request;if(q.method!=='GET')return;const u=new URL(q.url);if(u.origin!==self.location.origin||!mine(u.pathname))return;
 e.respondWith((async()=>{const c=await caches.open(CACHE);
  try{const r=await fetch(q,{cache:'no-store'});if(r.ok&&r.type==='basic')c.put(key(q.url),r.clone());return r;}
  catch(err){const m=await c.match(key(q.url));if(m)return m;if(q.mode==='navigate'){const i=await c.match(key(BASE+'index.html'))||await c.match(key(BASE));if(i)return i;}throw err;}})());});
