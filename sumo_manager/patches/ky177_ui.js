<style>/* v177 協会の役員(見本 ky1) */
.kyr{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.kyr span{border:1px solid var(--line);border-radius:12px;padding:2px 9px;font-size:13px}.kyr span.me{border-color:#a8823c;color:#a8823c;font-weight:bold}
.kyt{width:100%;border-collapse:collapse;font-size:13px}.kyt td{padding:4px 6px;border-bottom:1px solid var(--line)}</style>
<script>
function kyoHTML(){if(!G||!G.heya)return '';kyoInit();const K=G.kyo;const ch=K.ch;const y=curYear();const ny=K.ly+2;
 const chips='<div class="kyr">'+K.rj.map(s=>'<span'+(s.h===ME()?' class="me"':'')+'>'+esc(G.heya[s.h]?G.heya[s.h].n:s.n)+'</span>').join('')+'</div>';
 const hist='<table class="kyt">'+K.hist.slice().reverse().map(x=>'<tr><td>'+x.y0+'〜'+(x.y1||'')+'</td><td>'+esc(x.n)+'</td><td class="mute">'+esc(x.hn)+'部屋</td></tr>').join('')+'</table>';
 return '<details class="kacc" id="kyacc"'+(UI.kyO?' open':'')+'><summary><b>協会の役員</b><small>'+(ch?'理事長 '+esc(ch.n)+'・'+ch.since+' 年〜':'')+'</small></summary><div class="pn"><div class="mute" style="font-size:13px">理事 10 人('+K.ly+' 年の選挙・任期 2 年。次は '+ny+' 年 初場所のあと)。親方が理事なら金色の枠です。</div>'+chips
  +'<h3 style="font-size:14px;margin:10px 0 4px">歴代の理事長(このゲームで)</h3>'+hist+'<p class="kaku mute" style="font-size:12px">理事は 2 年ごとに選び直し、理事の中から理事長を決めます。65 歳の定年で必ず交代します。選ばれやすさは推定です。</p></div></details>';}
(function(){const R0=render;render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='kiroku'&&G&&G.heya&&!document.getElementById('kyacc')){const pn=document.querySelector('.pn');if(pn){pn.insertAdjacentHTML('beforebegin',kyoHTML());const d=document.getElementById('kyacc');d.addEventListener('toggle',()=>{UI.kyO=d.open;});}}}catch(e){console.error(e);}return x;};})();
</script>
