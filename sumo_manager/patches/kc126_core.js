/* v126:親方の「指導の色」と「親方におまかせ」(数字はすべて推定)。
   指導の色 KC:猛稽古派 mou(伸び ×1.05・けが ×1.2)/基本重視 kiso(腰の重さ・体の伸び ×1.1・けが ×0.9)/実戦派 jis(技・押し・四つの伸び ×1.04・調子 +)/理論派 riro(伸び ×0.97・けが ×0.85)。
   実在の部屋で記事がある部屋:伊勢ヶ濱=猛稽古派(日刊ゲンダイ:若い衆は 1 日 100 番、5 時間)、二所ノ関=理論派(Number:基礎運動の徹底と週 2 のウェイト・映像研究)、春日野=基本重視(日刊ゲンダイ:低く当たっておっつける教え)。ほかは推定(部屋と親方の名前から決まる。厳しい部屋は猛稽古派に寄る)。
   部屋の型 KCTRAD:春日野・高砂は押し(日刊ゲンダイ)。ない部屋は担当する親方の現役の取り口。入門 3 年(18 場所)以内の力士は、型の分野の伸びが ×1.08(本人の型と合えば)/×1.04、ほかの分野は ×0.98。
   おまかせ(G.kAuto、既定 オン):毎週、担当の親方(付きっきり・関取担当・若い衆担当の部屋付き親方、ほかは師匠)が力士ごとに稽古・強さ・午後を決め、理由を r.kWhy に。
   r.kMan(口を出した力士)はそのまま。場所中の朝稽古・午後(v125)も毎日決める。 */
const KC={mou:{n:'猛稽古派',g:1.05,i:1.2,d:'稽古の量で鍛える。強めが多く、伸びるがけがも多い'},kiso:{n:'基本重視',g:1,i:.9,d:'四股・すり足・てっぽうを徹底。腰の重さと体が伸び、けがが少ない'},jis:{n:'実戦派',g:1.02,i:1,d:'申し合い・三番・出稽古で相撲を取らせる。技が伸び、調子が上がる'},riro:{n:'理論派',g:.97,i:.85,d:'研究・休養・ウェイトを計画的に。けがが少ない'}};
const KCV={'伊勢ヶ濱':'mou','二所ノ関':'riro','春日野':'kiso'};
const KCTRAD={'春日野':'押','高砂':'押'};
function kcHash(s){let h=7;for(const c of String(s))h=(h*31+c.charCodeAt(0))>>>0;return h;}
function kcPickBy(seed,hard){const x=kcHash(seed)%100;if(hard)return x<60?'mou':x<80?'jis':'kiso';return x<25?'mou':x<55?'kiso':x<85?'jis':'riro';}
function kcOfH(h){const H=G.heya[h];if(!H)return 'jis';if(H.kc&&H.kcO===H.o)return H.kc;H.kc=(H.gen||1)<=1&&KCV[H.n]&&!H.kcSet?KCV[H.n]:kcPickBy(H.n+'|'+(H.o||''),H.hard);H.kcO=H.o;return H.kc;}
function kcOfS(s){if(!s.kc)s.kc=kcPickBy('co|'+s.n,false);return s.kc;}
function kcStyleH(h){const H=G.heya[h];if(!H)return '四';if(H.oyT)return H.oyT;const R=(typeof REALH!=='undefined')?REALH.find(x=>x[0]===H.n):null;return R&&OYAB[R[5]]?R[5]:['押','四','技'][kcHash(H.n)%3];}
function kcStyleS(s){const k=s.sk||{};const a=[['押',k.osh||0],['四',k.yot||0],['技',k.waz||0]].sort((x,y)=>y[1]-x[1]);return a[0][0];}
/* 力士を受け持つ人:プレイヤーの部屋なら担当の部屋付き親方、いなければ師匠 */
let _KCC={};
function kcCoach(r){const ck=r.id+'|'+r.h+'|'+r.d;if(_KCC[ck])return _KCC[ck];const v=kcCoach0(r);_KCC[ck]=v;return v;}
function kcCoach0(r){if(isPH(r.h)){let c=null;inP(r.h,()=>{G.staff.forEach(s=>{if(s.role!=='co'||c)return;const a=coA(s);if((a.t==='one'&&a.r===r.id)||(a.t==='seki'&&r.d<=1)||(a.t==='waka'&&r.d>=2))c=s;});});
  if(c)return {kc:kcOfS(c),st:kcStyleS(c),n:c.n.replace(/^元・/,'')+'親方',co:1};}
 const H=G.heya[r.h]||{};return {kc:kcOfH(r.h),st:KCTRAD[H.n]||kcStyleH(r.h),n:'師匠',co:0};}
/* 相撲界全体で平均が 1 になるようにならす(G._kcN、毎週 kcWeek で数え直す) */
function kcNorm(){let g=0,i=0,n=0;G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret)return;const c=kcCoach(r);g+=KC[c.kc].g;i+=KC[c.kc].i;n++;});G._kcN=n?{g:g/n,i:i/n}:{g:1,i:1};}
function kcG(r){const c=kcCoach(r);const N=G._kcN||{g:1};return KC[c.kc]?KC[c.kc].g/N.g:1;}
function kcI(r){const c=kcCoach(r);const N=G._kcN||{i:1};return KC[c.kc]?KC[c.kc].i/N.i:1;}
const KCSTC={押:'osh',四:'yot',技:'waz'};
function kcTilt(r,k){const c=kcCoach(r);let m=1;if(c.kc==='kiso'&&(CAT[k]==='tai'||k==='kos'))m*=1.1;else if(c.kc==='jis'&&(CAT[k]==='waz'||CAT[k]==='osh'||CAT[k]==='yot'))m*=1.04;
 if((G.bnum-(r.join||0))<=18){const t=KCSTC[c.st];if(t){if(CAT[k]===t){const p=prefOf(r);const fit=(c.st==='押'&&p==='O')||(c.st==='四'&&p==='Y')||c.st==='技';m*=fit?1.08:1.04;}else if(CAT[k]!=='tai'&&CAT[k]!=='sei')m*=.98;}}
 return m;}
/* おまかせ:担当の親方が決める。G.wk=いまの週(1〜6)。返り値 [稽古, 強さ 0〜3, 午後, 理由] */
function kcPlan(r){const c=kcCoach(r),k=c.kc,wk=G.wk||1,late=wk>=WEEKS-1,sek=r.d<=1,young=r.age<23&&r.d>=2;
 if(r.inj)return r.inj.s>=2?['休',0,'治','けがの治療を優先']:['基',0,'治','けがが治るまで基礎だけ軽めに'];
 if(r.fat>70)return ['休',0,'昼','疲れがたまっているので休ませる'];
 if(r.fat>58)return ['基',0,'昼','疲れが残っているので基礎を軽めに'];
 if(late){if(k==='mou')return [sek?'申':'ぶ',1,'昼','場所前も稽古の量は落とさない'];
  if(k==='jis'&&r.d<=2&&G._dek)return ['出',0,'昼','場所前の出稽古で仕上げる'];
  if(k==='kiso')return ['基',0,'昼','場所前は四股・すり足で整える'];
  return ['申',0,'昼','場所前は軽めにして疲れを抜く'];}
 if(k==='mou')return [r.d>=3?'ぶ':'申',2,'昼',r.d>=3?'ぶつかりで鍛える(強め)':'申し合いで鍛える(強め)'];
 if(k==='kiso')return [wk%2?'基':'申',1,'昼',wk%2?'四股・すり足・てっぽうを徹底':'基礎のあとは申し合い'];
 if(k==='jis')return [sek&&wk>=3&&G._dek?'出':(wk%2?'申':'三'),1,'昼',sek&&wk>=3&&G._dek?'出稽古で強い相手と':'相撲を取って覚えさせる'];
 return [sek&&wk%3===0?'研':(young?'基':'申'),1,sek&&wk%2?'筋':(young?'筋':'昼'),sek&&wk%3===0?'映像で相手を研究':young?'まず体づくり(基礎とウェイト)':'申し合いで実戦を'];}
function kcWeek(){_KCC={};kcNorm();forP(()=>{if(G.kAuto===false)return;own().forEach(r=>{if(r.kMan)return;const p=kcPlan(r);r.menu=MENU[p[0]]?p[0]:'申';r.it=p[1];r.pm=PM[p[2]]?p[2]:'昼';r.kWhy=p[3];});});}
/* 場所中:担当の親方が明日の朝稽古・午後を決める */
function kcBasho(){_KCC={};const B=G.B;if(!B)return;forP(()=>{if(G.kAuto===false)return;own().forEach(r=>{if(r.kMan)return;const c=B.rec[r.id];if(!c||c.ky)return;const k=kcCoach(r).kc;
 let a='軽',w='';if(r.fat>(k==='mou'?72:k==='riro'?50:60)){a='休';w='疲れを抜くため朝稽古は休ませる';}else if((k==='mou'&&r.d>=2)||(r.cond<45&&r.fat<40)){a='し';w=k==='mou'?'場所中も朝稽古はしっかり':'調子を上げるため朝稽古をしっかり';}else w='朝稽古は軽めに';
 r.bca=a;r.bcp=r.inj?'治':(k==='riro'&&r.fat>35?'治':(r.mor<40?'自':'昼'));r.kWhyB=w;});});}
