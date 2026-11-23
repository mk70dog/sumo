/* ========== v137:保存の直し(ダルマさん「途中からが書きかわらない」) ==========
 原因:保存データは 1 つで 0.7〜1.9MB の文字。版が上がるたびに新しい名前(sumoManagerNN)で保存し、前の版の分を消していなかったので、
 iPad の保存の上限(約 5MB)を超えて、新しい版の保存が黙って失敗していた。「続きから」は前の版の保存を読み直していた。
 直し:①保存を縮める(LZW。'LZ1:' で始まる文字。だいたい 1/5〜1/8)。②保存できたら、前の版の保存(sumoManagerNN・sumoHeyaMonogatariNN)を消す。
 ③保存に失敗したら前の版の保存を消してもう一度。それでもだめなら知らせる(G._svErr)。 */
function lzBits(n){let b=1;while((1<<b)<=n)b++;return b;}
function lzc(str){const out=[];let acc=0,an=0;const put=(v,w)=>{for(let i=w-1;i>=0;i--){acc=(acc<<1)|((v>>i)&1);an++;if(an===15){out.push(String.fromCharCode(acc+32));acc=0;an=0;}}};
 const dict=new Map(),one=new Map();let next=2,wc=-1;
 for(let i=0;i<str.length;i++){const cc=str.charCodeAt(i);
  if(wc>=0){const k=wc*65536+cc;const n=dict.get(k);if(n!==undefined){wc=n;continue;}put(wc,lzBits(next));dict.set(k,next++);}
  const sc=one.get(cc);if(sc===undefined){put(0,lzBits(next));put(cc,16);one.set(cc,next++);wc=-1;}else wc=sc;}
 if(wc>=0)put(wc,lzBits(next));
 put(1,lzBits(next+(wc>=0?1:0)));if(an>0){acc<<=15-an;out.push(String.fromCharCode(acc+32));}
 return out.join('');}
function lzd(data){let pos=0,acc=0,an=0;const get=w=>{let v=0;for(let i=0;i<w;i++){if(an===0){acc=data.charCodeAt(pos++)-32;an=15;}an--;v=(v<<1)|((acc>>an)&1);}return v;};
 const dict=[null,null];let prev=null,prevLit=true;const out=[];
 for(;;){const code=get(lzBits(dict.length+(prevLit?0:1)));
  if(code===1)break;
  let cur;
  if(code===0){cur=String.fromCharCode(get(16));if(!prevLit)dict.push(prev+cur[0]);dict.push(cur);prevLit=true;}
  else{cur=code<dict.length?dict[code]:(code===dict.length&&!prevLit?prev+prev[0]:null);if(cur==null)throw new Error('lz');if(!prevLit)dict.push(prev+cur[0]);prevLit=false;}
  out.push(cur);prev=cur;}
 return out.join('');}
function lsGet(k){const s=localStorage.getItem(k);if(s&&s.slice(0,4)==='LZ1:')return lzd(s.slice(4));return s;}
function lsOld(keep){try{for(let i=localStorage.length-1;i>=0;i--){const key=localStorage.key(i);if(key!==keep&&/^(sumoManager\d+|sumoHeyaMonogatari\d+)$/.test(key))localStorage.removeItem(key);}}catch(e){}}
function lsPut(k,str){const d='LZ1:'+lzc(str);try{localStorage.setItem(k,d);if(k===SAVE)lsOld(SAVE);if(G)G._svErr=0;return true;}catch(e){lsOld(SAVE);try{localStorage.setItem(k,d);if(G)G._svErr=0;return true;}catch(e2){if(G)G._svErr=1;try{if(typeof toast==='function')toast('保存できませんでした(保存の場所がいっぱいです)。設定の「保存データ」から「ファイルで保存」をしてください');}catch(z){}return false;}}}
