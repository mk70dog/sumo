# 見本 staff1〜3:若者頭・世話人・マネージャーの見せ方(v58 の本体に見本用の script を足す)
import sys
src='sumo_manager_v58.html'
base=open(src,encoding='utf-8').read()
JS=r'''
<style>
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin-top:6px}
.sc2{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper)}
.sc2 .rl{font-weight:700;font-size:17px}.sc2 .who{margin:4px 0;font-size:14px}
.pay{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;margin-left:6px;vertical-align:2px;border:1px solid}
.pay.k{color:var(--ai);border-color:var(--ai)}.pay.h{color:var(--shu);border-color:var(--shu)}
.eff{display:inline-block;font-size:12px;padding:1px 7px;border-radius:6px;background:rgba(0,0,0,.05);margin:2px 4px 0 0}
.yk{font-size:13px;color:var(--mute);margin-top:4px}
.org{position:relative;padding:6px 0}
.org .top{text-align:center;margin:0 auto 6px;max-width:260px}
.org .bx{border:1.5px solid var(--sumi);border-radius:8px;padding:6px 8px;background:var(--paper);text-align:center;font-size:14px}
.org .bx b{display:block;font-size:15px}.org .bx.h{border-color:var(--shu)}
.org .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-top:10px}
.org .ln{height:14px;border-left:2px solid var(--line);width:0;margin:0 auto}
.org .sub2{margin-top:6px;font-size:12px;color:var(--mute)}
</style>
<script>
(function(){
const V=__V__;
const R0=G0=>0;
function people(){const U=uraOf(me().n);const co=G.staff.filter(s=>s.role==='co');const sc=G.staff.filter(s=>s.role==='sc');
 const wk={n:'若翔(架空)',mo:'幕下 5 枚目',age:41};
 const sw=U.filter(u=>u.k==='世話人');const yb=U.filter(u=>u.k!=='世話人');
 const own0=own();const young=own0.filter(r=>r.d>=2).length;
 return {co,sc,wk,sw,yb,young};}
const ROLES=P=>[
 {k:'co',n:'部屋付き親方',pay:'k',who:P.co.length?P.co.map(s=>esc(s.n)+(s.myo?'(年寄 '+esc(s.myo)+')':'')).join('、'):'いません',yk:'稽古場で弟子を指導する。名跡があれば跡継ぎ・独立の候補。本場所では審判や警備などの協会の仕事も。',eff:['稽古の伸び(得意分野)','素質の見極め','新弟子に会いに行ける']},
 {k:'wk',n:'若者頭',pay:'k',who:esc(P.wk.n)+'・元'+P.wk.mo+'・'+P.wk.age+'歳',yk:'幕下以下の若い衆('+P.young+' 人)の生活と稽古を見張る監督役。本場所の進行の手伝いも。',eff:['入門 2 年以内にやめる人 −15%','兄弟子の暴力の芽が見つかりやすい']},
 {k:'sw',n:'世話人',pay:'k',who:P.sw.length?P.sw.map(u=>esc(u.n)).join('、'):'いません',yk:'用具の運び・保管と部屋の雑務。若者頭の助手。本場所では木戸(入口)や役員室の係。',eff:['若い衆の雑用が減る(疲れ −3%)']},
 {k:'sc',n:'マネージャー',pay:'h',who:P.sc.length?P.sc.map(s=>esc(s.n)).join('、'):'いません',yk:'部屋が自分で契約する人(協会員ではない)。事務・後援会との連絡・新弟子探しの手伝い。',eff:['新弟子の情報が少し増える','後援会の連絡(後援会員 +2%)']}];
const payL=p=>p==='k'?'<span class="pay k">給料は協会</span>':'<span class="pay h">給料は部屋</span>';
const note='<p class="kaku mute" style="font-size:13px;margin-top:8px">新弟子探しの主役は親方と部屋付き親方の人脈(後援会・学校の監督・同郷・先輩のつながり)。若者頭・世話人は、自分の部屋で十両・幕下まで上がって引退した力士から、師匠の推薦でなれます。効き目の数字は推定。若者頭の名前は架空(実在の一覧が見つからないため)。</p>';
const os=staffHTML;
staffHTML=function(){let h=os();const P=people();const L=ROLES(P);
 // 元の「部屋の裏方」と「部屋のスタッフ」の欄を外して、新しい欄にする
 const d=document.createElement('div');d.innerHTML=h;const pn=[...d.querySelectorAll('.pn')];
 const ura=pn.find(x=>/部屋の裏方/.test(x.textContent));const stf=pn.find(x=>/部屋のスタッフ/.test(x.textContent));
 let nw='';
 if(V===1){
  const blk=(t,s,arr)=>'<div class="pn"><h2>'+t+'<span class="sub">'+s+'</span></h2>'+arr.map(r=>'<div class="stf"><div><b class="nm">'+r.n+'</b>'+payL(r.pay)+'<span class="mute kaku" style="font-size:12px;margin-left:6px">'+r.who+'</span></div><div class="yk">'+r.yk+'</div><div>'+r.eff.map(e=>'<span class="eff">'+e+'</span>').join('')+'</div></div>').join('')+'</div>';
  nw=blk('協会の人','この部屋に所属・給料は協会から',L.filter(r=>r.pay==='k'))+'<div class="pn"><h2>行司・呼出・床山<span class="sub">この部屋に所属</span></h2><div class="kaku">'+P.yb.map(u=>'<b>'+u.k+'</b> '+esc(u.n)).join('、')+'</div></div>'+blk('部屋が雇う人','給料は部屋から',L.filter(r=>r.pay==='h'))+note;}
 if(V===2){
  nw='<div class="pn"><h2>部屋を支える人<span class="sub">役目と効き目</span></h2><div class="sg">'+L.map(r=>'<div class="sc2"><div class="rl">'+r.n+payL(r.pay)+'</div><div class="who">'+r.who+'</div><div class="yk">'+r.yk+'</div><div style="margin-top:4px">'+r.eff.map(e=>'<span class="eff">'+e+'</span>').join('')+'</div></div>').join('')+
   '<div class="sc2"><div class="rl">行司・呼出・床山'+payL('k')+'</div><div class="who">'+P.yb.map(u=>u.k+' '+esc(u.n)).join('<br>')+'</div><div class="yk">本場所の進行・番付の発送や後援会への連絡(行司)・髷を結う(床山)。</div></div></div>'+note+'</div>';}
 if(V===3){
  const bx=(r)=>'<div class="bx'+(r.pay==='h'?' h':'')+'"><b>'+r.n+'</b>'+r.who+'<div class="sub2">'+r.eff[0]+'</div></div>';
  nw='<div class="pn"><h2>部屋の人の図<span class="sub">枠が赤=部屋が雇う人</span></h2><div class="org"><div class="top bx"><b>師匠</b>'+esc(me().o)+'</div><div class="ln"></div>'+
   '<div class="row">'+bx(L[0])+'<div class="bx"><b>おかみさん</b>'+(G.okami?esc(G.okami.n):'いません')+'<div class="sub2">後援会・お金・弟子の相談</div></div>'+bx(L[3])+'</div><div class="ln" style="margin-top:6px"></div>'+
   '<div class="row">'+bx(L[1])+bx(L[2])+'<div class="bx"><b>行司・呼出・床山</b>'+P.yb.map(u=>esc(u.n)).join('・')+'<div class="sub2">本場所の仕事</div></div></div><div class="ln" style="margin-top:6px"></div>'+
   '<div class="top bx"><b>力士 '+own().length+' 人</b>関取 '+own().filter(r=>r.d<=1).length+'・若い衆 '+P.young+'</div></div>'+
   '<ul class="kaku" style="font-size:13px;padding-left:18px;margin:6px 0 0">'+L.map(r=>'<li><b>'+r.n+'</b>:'+r.yk+'('+r.eff.join('・')+')</li>').join('')+'</ul>'+note+'</div>';}
 const first=ura||stf;if(first){const t=document.createElement('div');t.innerHTML=nw;first.replaceWith(...t.childNodes);}
 if(stf&&stf.parentNode)stf.remove();
 // おかみさんの欄はそのまま。雇える人の欄から部屋付き親方以外はそのまま
 return d.innerHTML;};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('春日野');UI.title=0;UI.start=0;go('staff');}catch(e){console.error(e)}},50);});
})();
</script>
'''
for v in (1,2,3):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'</body>',1)
    s=s.replace('<title>Sumo Manager v58</title>','<title>見本 staff%d</title>'%v,1)
    open('samples/staff%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
