function oRes(b){const W=G.R[b.w],L=G.R[b.l];const m=W.h===0?W:L,o=m===W?L:W,win=m===W;const c=G.B.rec[m.id];const half=Math.floor(c.nb/2)+1;
 let st=0;for(let i=c.res.length-1;i>=0;i--){const x=c.res[i];if(!x)continue;if(x.r==='や')break;const ww=x.r==='○'||x.r==='□';if(st===0||(st>0)===ww){st+=ww?1:-1;}else break;}
 let tag='';if(win&&c.w===half)tag='勝ち越し!';else if(!win&&c.l===half)tag='負け越し';else if(st>=3)tag=st+'連勝';else if(st<=-3)tag=(-st)+'連敗';
 if(win&&o.t==='Y'&&m.d===0&&!m.t)tag='金星!';
 const left=c.nb-c.w-c.l-c.ab;let need='';if(!tag&&left>0){if(c.w<half&&c.l<half)need='勝ち越しまであと '+(half-c.w);}
 return {m,o,win,c,tag,need};}
function wlBadge(win,fus){return '<span class="wlb '+(win?'wn':'ls')+'">'+(fus?(win?'不戦勝':'不戦敗'):(win?'勝ち':'負け'))+'</span>';}
