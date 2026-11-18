# v61 -> v62:土俵の見やすさ(見本 nb1+sh1)・部屋付き親方の担当(見本 co1)
import sys
sys.path.insert(0, 'patches')
import nb66, sh67
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v61</title>', '<title>Sumo Manager v62</title>')
rep("const APPV=61;\nconst SAVE='sumoManager61',SAVE60", "const APPV=62;\nconst SAVE='sumoManager62',SAVE61='sumoManager61',SAVE60")
rep('[SAVE60,SAVE59', '[SAVE61,SAVE60,SAVE59')
rep(" if(g.v===60){g.v=61;}\n return g.v===61?g:null;}", " if(g.v===60){g.v=61;}\n if(g.v===61){g.v=62;}\n return g.v===62?g:null;}")
rep('G={v:61,', 'G={v:62,')
# 土俵:名前のバッジ・土俵の中の文字なし・行司は離れた側(nb1)、勝負ありは行司の横に縦書きの筆文字(sh1)
s = nb66.apply(s, 1)
s = sh67.apply(s, 1)
# ===== 部屋付き親方の担当(数字は推定) =====
CORE = r'''/* 部屋付き親方の担当 G.coAs[sid]={t:'all'|'seki'|'waka'|'one'|'sk', r:弟子の id, s:稽古の種類}。数字は推定 */
const COT=[['all','全体'],['seki','関取担当'],['waka','若い衆担当'],['one','付きっきり'],['sk','得意分野にしぼる']];
const COEFF={all:'得意分野の指導を全員に',seki:'関取の伸び +6%・場所ごとの調子の波が小さく',waka:'幕下以下の伸び +5%・入門 2 年以内にやめる人 −10%',one:'選んだ弟子の伸び +12%・信頼が少しずつ上がる(全体の指導からは外れる)',sk:'その種類の稽古の効き +10%(ほかの種類の指導からは外れる)'};
function coA(s){const a=(G.coAs||{})[s.sid];return a&&a.t?a:{t:'all'};}
function coL(t){return G.staff.filter(s=>s.role==='co'&&coA(s).t===t);}
function coMul(r){if(r.h!==0)return 1;let m=1;G.staff.forEach(s=>{if(s.role!=='co')return;const a=coA(s);
 if(a.t==='seki'&&r.d<=1)m*=1.06;else if(a.t==='waka'&&r.d>=2)m*=1.05;else if(a.t==='one'&&a.r===r.id)m*=1.12;});return m;}
function coWeek(){G.staff.forEach(s=>{if(s.role!=='co')return;const a=coA(s);if(a.t!=='one')return;const r=G.R[a.r];if(!r||r.h!==0||r.ret){delete G.coAs[s.sid];return;}r.tr=cl((r.tr==null?50:r.tr)+.5,0,100);});
 Object.keys(G.coAs||{}).forEach(k=>{if(!G.staff.some(s=>String(s.sid)===k))delete G.coAs[k];});}
'''
rep("function heyaH(h){", CORE + "function heyaH(h){")
# 指導力:付きっきりの親方は全体の指導から外れ、得意分野にしぼった親方はその種類だけを教えて効きが上がる
rep(" const co=G.staff.filter(s=>s.role==='co');const OY=me().oy;\n const best=k=>Math.max(OY[k],...co.map(s=>s.sk[k]));",
    " const co=G.staff.filter(s=>s.role==='co'&&coA(s).t!=='one');const OY=me().oy;\n const best=k=>Math.max(OY[k],...co.filter(s=>coA(s).t!=='sk'||coA(s).s===k).map(s=>s.sk[k]));")
rep("['tai','osh','yot','waz','sei'].forEach(k=>cf[k]=(.7+.03*best(k))*lf);", "['tai','osh','yot','waz','sei'].forEach(k=>cf[k]=(.7+.03*best(k))*lf*(co.some(s=>coA(s).t==='sk'&&coA(s).s===k)?1.1:1));")
# 伸び:担当の上乗せ
rep("for(const k in M.w)grow(r,k,gm*M.w[k]*H.cf[CAT[k]]*(r.per==='職人肌'&&CAT[k]==='waz'?1.2:1));",
    "if(isOwn)gm*=coMul(r);for(const k in M.w)grow(r,k,gm*M.w[k]*H.cf[CAT[k]]*(r.per==='職人肌'&&CAT[k]==='waz'?1.2:1));")
# 若い衆担当:入門 2 年以内にやめる確率 ×0.9
rep("  if(G.wkg)p*=.85;\n", "  if(G.wkg)p*=.85;\n  if(coL('waka').length)p*=.9;\n")
# 関取担当:場所ごとの調子の波を小さく
rep("r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);}", "r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);if(r.h===0&&r.d<=1&&coL('seki').length)r.bfm*=.6;}")
# 週ごと
rep("function wkgBasho(){", "function wkgBasho(){coWeek();")
# 週ごとの付きっきりの信頼(週の初めに)
rep("function doWeek(){\n if(G.phase!=='train')return;\n mWeek();oshiWeek();", "function doWeek(){\n if(G.phase!=='train')return;\n mWeek();oshiWeek();coWeek();")
rep("function wkgBasho(){coWeek();", "function wkgBasho(){")
# 画面:稽古の画面の「師弟」の上に担当の表(見本 co1)
UI = r'''function coPanel(){const L=G.staff.filter(s=>s.role==='co');if(!L.length)return '';G.coAs=G.coAs||{};const o=own().slice().sort((x,y)=>x.pos-y.pos);
 const SKL=[['osh','押し'],['yot','四つ'],['waz','技'],['tai','体作り'],['sei','心']];
 const best=s=>SKL.slice().sort((x,y)=>s.sk[y[0]]-s.sk[x[0]]).slice(0,2).map(([k,n])=>n+' '+s.sk[k]).join('・');
 return '<div class="pn"><h2>部屋付き親方の担当<span class="sub">'+L.length+' 人</span></h2><table class="cot">'+L.map(s=>{const a=coA(s);
  let sub='';if(a.t==='one')sub='<select onchange="coPick('+s.sid+',\'r\',+this.value)">'+o.map(r=>'<option value="'+r.id+'"'+(a.r===r.id?' selected':'')+'>'+esc(r.n)+'('+esc(r.rkS)+')</option>').join('')+'</select>';
  if(a.t==='sk')sub='<select onchange="coPick('+s.sid+',\'s\',this.value)">'+SKL.map(([k,n])=>'<option value="'+k+'"'+(a.s===k?' selected':'')+'>'+n+'('+s.sk[k]+')</option>').join('')+'</select>';
  const one=a.t==='one'&&G.R[a.r]?'(いま:'+esc(G.R[a.r].n)+')':'';
  return '<tr><td><b>'+esc(s.n)+'</b><br><span class="mute" style="font-size:12px">得意 '+best(s)+'</span></td><td><select onchange="coPick('+s.sid+',\'t\',this.value)">'+COT.map(([k,n])=>'<option value="'+k+'"'+(a.t===k?' selected':'')+'>'+n+'</option>').join('')+'</select> '+sub+'<div class="coe">'+COEFF[a.t]+one+'</div></td></tr>';}).join('')+'</table><p class="kaku mute" style="font-size:12px;margin-top:6px">担当を決めない親方は「全体」のまま。効き目の数字は推定。</p></div>';}
function coPick(sid,k,v){G.coAs=G.coAs||{};const a=Object.assign({t:'all'},G.coAs[sid]||{});a[k]=v;if(k==='t'){if(v==='one'&&a.r==null){const o=own().filter(r=>r.d>=2).sort((x,y)=>x.pos-y.pos);a.r=(o[0]||own()[0]||{}).id;}if(v==='sk'&&!a.s){const s=G.staff.find(x=>x.sid===sid);a.s=s?['osh','yot','waz','tai','sei'].sort((x,y)=>s.sk[y]-s.sk[x])[0]:'osh';}}G.coAs[sid]=a;save();render();}
'''
rep("function shiteiPanel(){", UI + "function shiteiPanel(){")
rep(" h+=shiteiPanel();\n", " h+=coPanel();\n h+=shiteiPanel();\n")
CSS = '.cot{width:100%;border-collapse:collapse;font-size:14px}.cot td{padding:6px;border-bottom:1px dashed var(--line);vertical-align:middle}.cot select{font-size:14px;max-width:100%}.coe{font-size:12px;color:var(--mute);margin-top:5px}\n</style>'
k = s.index('</style>'); s = s[:k] + CSS + s[k+len('</style>'):]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
