/* ========== v129:取り口を作る長い計画(型づくり) ==========
 ・プレイヤーの部屋の力士ごとに「目指す型」r.tk={p:型,v:完成度 0〜100}。型:O 押し相撲/R 右四つ/L 左四つ/W 業師/X 押してから四つ。
   おまかせ(r.tkP なし)なら担当の親方が決める(入門 3 年以内で親方の型が押しなら押し=鳴戸親方〈元隆の里〉が稀勢の里に
   10 年「まわしを取るな」と言った例、Number 2022/7/14)。ほかは体格と今の取り口から。
 ・段階:土台(0〜30)→ 型の柱(30〜65)→ 二の矢(65〜90)→ 完成(90〜)。段階ごとに伸びやすい分野が変わる(tkTilt。全体の伸びはほぼ同じ)。
 ・完成度は稽古の週ごとに上がる(休み・けがの週は上がらない)。体格と合う型ほど速い。順調で 3〜4 年で完成(推定)。
   型を変えると完成度は 4 割に下がる。
 ・取組:自分の形(押し合い/四つ、四つなら差す側)になると、完成度に応じて攻めが少し強い(最大 +0.45、tkB)。
   ほかの部屋の力士も、いまの取り口を型として、入門からの場所数で完成度が上がる(全体が同じように強くなる)。数字はすべて推定。 */
const TKPN={O:'押し相撲',R:'右四つ',L:'左四つ',W:'業師',X:'押してから四つ'};
const TKPS=['土台','型の柱','二の矢','完成'];
const TKPSD=['四股・すり足・てっぽうで体と腰を作る','型の中心の技を磨く','型を補う二の矢を覚える','型が身についた'];
function tkStage(v){return v>=90?3:v>=65?2:v>=30?1:0;}
function tkNat(r){const p=prefOf(r);if(r.sty==='技'&&(r.w||140)<135)return 'W';return p==='O'?'O':sideOf(r)==='右'?'R':'L';}
function tkFit(r,p){const w=r.w||140,h=r.ht||180;let f=1;
 if(p==='O')f=w>=150?1.1:w<120?.8:1;else if(p==='R'||p==='L')f=(h>=183?1.1:h<175?.85:1)*(w<115?.85:1);else if(p==='W')f=w<130?1.15:w>165?.75:1;
 const n=tkNat(r);if(n===p||(p==='X'&&n!=='W'))f*=1.1;else if((p==='R'&&n==='L')||(p==='L'&&n==='R'))f*=.9;return f;}
function tkAuto(r){if((G.bnum-(r.join||0))<=18){try{const c=kcCoach(r);if(c&&c.st==='押')return 'O';}catch(e){}}return tkNat(r);}
function tkBase(r){return Math.min(100,Math.max(((r.age||18)-17)*18,(G.bnum-(r.join||G.bnum))*2.6));}
function tkOf(r){if(!r.tk){const p=r.tkP||tkAuto(r);r.tk={p:p,v:Math.round(tkBase(r)*(p===tkNat(r)?1:.4))};}return r.tk;}
function tkSet(r,p){const t=tkOf(r);r.tkP=p||null;const np=p||tkAuto(r);if(np!==t.p){t.p=np;t.v=Math.round(t.v*.4);t.ch=G.bnum;}}
/* 週ごと(プレイヤーの部屋)。稽古の週に完成度が上がる */
function tkWeek(){own().forEach(r=>{const t=tkOf(r);if(!r.tkP){const a=tkAuto(r);if(a!==t.p&&(G.bnum-(t.ch||0))>=12&&t.v<30){t.p=a;t.ch=G.bnum;}}
 if(r.inj&&r.inj.s>=2)return;if(r.lw==='休')return;
 const age=r.age<=22?1.15:r.age<=27?1:r.age<=31?.8:.6;let k=1;try{const c=kcCoach(r).kc;const s=tkStage(t.v);if(c==='kiso'&&s===0)k=1.2;else if(c==='jis'&&s>=1)k=1.15;else if(c==='mou')k=1.05;}catch(e){}
 t.v=Math.min(100,t.v+.75*tkFit(r,t.p)*age*k*(r.lw==='基'?(tkStage(t.v)===0?1.3:.8):1));});}
/* 伸びやすさ:段階ごと(プレイヤーの部屋の力士だけ) */
function tkTilt(r,k){const t=r.tk;if(!t||!isPH(r.h))return 1;const s=tkStage(t.v),c=CAT[k],p=t.p;
 const main=p==='O'?(c==='osh'):p==='R'?(k==='mig'||k==='yor'):p==='L'?(k==='hid'||k==='yor'):p==='W'?(c==='waz'):(c==='osh'||k==='yor');
 const sub=p==='O'?(k==='hik'||k==='ash'):p==='W'?(k==='flx'||k==='hik'||k==='tac'):(k==='nag'||k==='mae');
 if(c==='sei')return 1;
 if(s===0)return (c==='tai')?1.08:.97;
 if(s===1)return main?1.1:c==='tai'?1:.96;
 if(s===2)return sub?1.1:main?1.03:.98;
 return main||sub?1.03:.99;}
/* 取組:自分の形になったときの攻めの上乗せ */
function tkB(r,form,gS){let p,v;if(r.tk){p=r.tk.p;v=r.tk.v;}else{p=tkNat(r);v=tkBase(r);}
 if(v<=0)return 0;const m=.45*v/100;
 if(p==='O')return form==='O'?m:0;if(p==='R'||p==='L')return form==='Y'&&gS===(p==='R'?'右':'左')?m:form==='Y'?m*.3:0;
 if(p==='W')return m*.5;return m*.65;}
