<script>
/* v130 画面:力士の画面に「引退について」(本人の様子・約束・親方から切り出す)、スタッフの画面に世話人 */
var RT_V=window.RT_V||1;
function rtUI(id,k){const m=rtTalk(id,k);UI.rtMsg=[id,m];save();showR(id);}
function rtState(r){if(r.rtLast)return '<b class="shu">この場所を最後に引退します。</b>';const c=r.rtC;if(!c)return '';
 return '<b class="shu">約束:'+(c.k==='kk'?(c.b===G.bnum?'この場所':'次の場所')+'で勝ち越せなければ引退':'3 場所のうちに関取に戻れなければ引退(あと '+Math.max(1,c.b+3-G.bnum)+' 場所)')+'</b>';}
function rtHTML(r){if(!isPH(r.h)||r.ret||r.h!==ME()||G.pend.includes(r.id))return '';const [lv,w]=rtMood(r);
 const mood=['<span style="color:#2e7d4f">まだまだやる気です</span>','<span style="color:#a8823c">先のことを考えはじめています</span>','<span class="shu">引退が頭をよぎっています</span>'][lv];
 const pa=rtAccept(r);const pw=pa>=.6?'受け入れそう':pa>=.35?'五分五分':'まだ続けたがりそう';
 const can=rtCanTalk(r);const msg=UI.rtMsg&&UI.rtMsg[0]===r.id?'<p class="rtm">'+esc(UI.rtMsg[1])+'</p>':'';
 const btn=can&&!r.rtC?'<div><button class="pc" onclick="rtUI('+r.id+',\'sus\')">引退を勧める<span class="tkf">'+pw+'</span></button><button class="pc" onclick="rtUI('+r.id+',\'kk\')">この場所で勝ち越せなければ引退と約束する</button><button class="pc" onclick="rtUI('+r.id+',\'hag\')">励ます</button></div>':
  '<p class="mute" style="font-size:12px;margin:2px 0">'+(G.phase!=='train'?'親方から話をするのは、稽古の期間だけです。':r.rtC||r.rtLast?'':'この場所はもう話をしました。')+'</p>';
 const body='<p class="kaku" style="margin:2px 0">本人の様子:'+mood+(lv?'<br><span class="mute" style="font-size:12px">思っていること:'+esc(w.join('・'))+'</span>':'')+'</p>'+(rtState(r)?'<p style="margin:2px 0">'+rtState(r)+'</p>':'')+msg+btn;
 if(RT_V===2)return '<div class="rtp"><details'+(lv>=2||r.rtC||r.rtLast||msg?' open':'')+'><summary><b>引退について</b> '+mood+'</summary>'+body+'</details></div>';
 return '<div class="rtp"><h3>引退について</h3>'+body+'</div>';}
const rtCM0=closeM;closeM=function(){UI.rtMsg=null;return rtCM0.apply(this,arguments);};
const rtS0=stHTML;stHTML=function(r){return rtS0(r)+rtHTML(r);};
const rtSt0=staffHTML;staffHTML=function(){const h=rtSt0();const L=G.sewa||[];if(!L.length)return h;
 return h+'<div class="pn"><h2>世話人<span class="sub">'+L.length+' 人(協会の嘱託・給与は協会から)</span></h2><table class="tb">'+L.map(s=>'<tr><td class="nm">'+esc(s.n)+'</td><td>元'+esc(s.rk||'')+'</td><td>'+Math.floor(s.age)+'歳</td></tr>').join('')+'</table><p class="mute kaku" style="font-size:12px">若い衆の面倒を見ています(幕下以下の気力・信頼が少しずつ上がる。推定)。65 歳で退きます。</p></div>';};
</script><style>
.rtp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 10px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important;white-space:normal!important}
.rtp summary{cursor:pointer;padding:4px 0}.rtm{background:#fff3cf;color:#1a140c;border-radius:6px;padding:4px 8px;margin:4px 0;font-size:13px}
</style>
