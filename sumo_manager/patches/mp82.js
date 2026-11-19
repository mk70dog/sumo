<script>
/* v82:GitHub の鍵(Gist の設定)の読み込み・書き出し。ASL アプリの aslsk_gist_settings にも対応(鍵だけ使う) */
function gistKeyHTML(){const t=mpTok();
 return '<div class="pn"><h2>GitHub の鍵(二人相撲)<span class="sub">Gist の設定</span></h2><p class="kaku" style="font-size:13px">二人相撲のデータの受け渡しに使う鍵です。この端末の中だけに保存します。ファイルから読み込むと楽です(ASL アプリで書き出した設定ファイルも使えます)。</p>'+
 '<p class="kaku">今の鍵:'+(t?'<b>保存済み</b>(…'+esc(t.slice(-4))+')':'<span class="shu">まだありません</span>')+'</p>'+
 '<div class="btns"><label class="btn">ファイルから読み込む<input type="file" accept=".json,application/json" style="display:none" onchange="gistImportFile(this)"></label>'+
 '<button class="btn" onclick="gistPaste()">貼り付けて読み込む</button><button class="btn" '+(t?'':'disabled')+' onclick="gistExport()">書き出す</button><button class="btn" '+(t?'':'disabled')+' onclick="gistClear()">鍵を消す</button></div></div>';}
function gistApply(txt){let o;try{o=JSON.parse(txt);}catch(e){
  const v=(txt||'').trim();if(/^(ghp_|github_pat_)\S+$/.test(v))o={gistToken:v};else{alertM('読み込めませんでした','設定ファイル(JSON)か、ghp_ / github_pat_ で始まる鍵を入れてください。');return;}}
 const tok=(o.gistToken||o.token||'').trim();if(!/^(ghp_|github_pat_)\S+$/.test(tok)){alertM('読み込めませんでした','ファイルの中に GitHub の鍵(gistToken)が見つかりません。');return;}
 try{localStorage.setItem('gsmTok',tok);}catch(e){}
 const asl=o.type==='aslsk_gist_settings';
 if(!asl&&o.type==='gsm_gist_settings'&&o.gistId){const c=$('#mp_code');if(c)c.value=o.gistId;}
 alertM('鍵を読み込みました','鍵(…'+tok.slice(-4)+')を保存しました。'+(asl?'ASL アプリの設定ファイルなので、鍵だけを使います(ASL の Gist の ID は使いません。二人相撲は専用の Gist を新しく作ります)。':''));render();}
function gistImportFile(inp){const f=inp.files&&inp.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>gistApply(String(rd.result||''));rd.readAsText(f);inp.value='';}
function gistPaste(){openM('<button class="btn sm x" onclick="closeM()">閉じる</button><h2>鍵の読み込み</h2><p class="kaku">設定ファイルの中身か、鍵(ghp_ / github_pat_ で始まる文字)を貼り付けてください。</p><textarea id="gimp" style="width:100%;height:140px;font-size:12px"></textarea><div class="btns"><button class="btn main" onclick="const v=$(\'#gimp\').value;closeM();gistApply(v)">読み込む</button></div>');}
function gistExport(){const o={type:'gsm_gist_settings',version:1,exportedAt:new Date().toISOString(),gistToken:mpTok(),gistId:(G&&G.mp&&G.mp.id)||(mpJ(localStorage.getItem('gsmGuest')).id)||''};
 const b=new Blob([JSON.stringify(o,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='gsm_gist_settings.json';document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);
 toast('書き出しました。鍵が入っているので、人に渡さないでください');}
function gistClear(){try{localStorage.removeItem('gsmTok');}catch(e){}toast('鍵を消しました');render();}
const gkSys=sysHTML;sysHTML=function(){return gkSys()+gistKeyHTML();};
const gkTop=topHTML;topHTML=function(){let h=gkTop();if(UI.mode!=='two')return h;
 return h.replace('<label>GitHub の鍵(gist だけ書ける鍵。この端末の中だけに保存。ふたりとも同じ鍵を使います)</label>','<label>GitHub の鍵(gist だけ書ける鍵。この端末の中だけに保存。ふたりとも同じ鍵を使います)<span style="margin-left:8px">'+(mpTok()?'保存済み(…'+esc(mpTok().slice(-4))+')':'まだありません')+'</span></label><label class="btn sm" style="display:inline-block;margin:4px 0">設定ファイルから読み込む<input type="file" accept=".json,application/json" style="display:none" onchange="gistImportFile(this)"></label>');};
</script>
<style id="mpTopFlow">body.st-top:has(.st-go2){overflow:auto}body:has(.st-go2) .st-title{position:absolute}
body:has(.st-go2) .st-go2{position:relative!important;left:auto!important;bottom:auto!important;transform:none!important;margin:clamp(215px,26vw,330px) auto 50px!important}
body:has(.st-go2) .st-credit{position:absolute}</style>
