/* v217 叩き上げの物語と、稽古の画面の「関取の申し合い相手」。数字は推定。
   入門のとき素質 C・D(見立てか本当の素質のどちらか)だった弟子が関取・幕内に上がると、物語の行・人気・後援会。 */
(function(){
const g0=r=>{const v=r.ep0!=null?Math.max(r.ep0,r.pot0||0):r.pot0;return v==null?null:gradeOf(v);};
const nc0=nextCycle;nextCycle=function(){const old={};try{own().forEach(r=>{if(r.pot0==null)r.pot0=potOf(r);old[r.id]=r.d;});}catch(e){}
 const res=nc0.apply(this,arguments);
 try{if(res!==false)Object.keys(old).forEach(id=>{const r=G.R[id];if(!r||r.ret||r.h!==ME())return;const o=old[id];const gr=g0(r);if(gr!=='C'&&gr!=='D')return;
  if(r.d===1&&o>1&&!r.tkS){r.tkS=1;r.pop=cl((r.pop||20)+6,0,100);G.sup=(G.sup||0)+15;
   storySx(r,'入門のときは素質 '+gr+' の見立て。叩き上げで関取に',75);
   addNews(r.n+'が新十両。入門のときは期待されていなかった叩き上げです。地元から祝いの声が届き、後援会も増えました。');}
  if(r.d===0&&o>0&&!r.tkM){r.tkM=1;r.pop=cl((r.pop||20)+6,0,100);G.sup=(G.sup||0)+10;
   storySx(r,'叩き上げで幕内へ。素質 '+gr+' から番付を上りつめる',85);
   addNews(r.n+'が新入幕。素質 '+gr+' の見立てから上がってきた叩き上げに、館内の声援が集まっています。');}});}catch(e){console.error(e);}
 return res;};
/* 稽古の画面:関取の申し合い相手 */
const kh0=keikoHTML;keikoHTML=function(){let h=kh0.apply(this,arguments);try{const S=own().filter(r=>r.d<=1);if(!S.length)return h;
 const rows=S.map(r=>{const n=mshN(r);const f=mshF(r,'申');const t=n>=8?['ok','十分']:n>=4?['near','ふつう']:['far','少ない'];
  return '<span class="msh"><b>'+esc(r.n)+'</b> 相手 '+n+' 人 <span class="st '+t[0]+'">'+t[1]+'</span> <span class="mute">伸び ×'+f.toFixed(2)+'</span></span>';}).join('');
 const p='<div class="pn mshp"><h3>関取の申し合い相手<span class="mute kaku" style="font-size:12px;margin-left:8px">番付が下の幕下・三段目の弟子(けがの人をのぞく)。8 人いれば十分、3 人以下だと伸びが落ちます。出稽古の週は関係ありません</span></h3><div class="mshl">'+rows+'</div></div>';
 return p+h;}catch(e){console.error(e);return h;}};
document.head.insertAdjacentHTML('beforeend','<style>.riv{font-size:12px;color:#d9763a;margin-top:2px}.mshp h3{margin:0 0 6px}.mshl{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px}.msh{white-space:nowrap}</style>');
})();
