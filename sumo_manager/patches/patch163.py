# v159 -> v160:稽古の週のホーム「弟子の様子」を小さなカードを並べる形に(見本 tw3。ダルマさん「全体的に下にスクロールが多いので改良する」→「tw3」)。
#   上に「関取・けが・疲れ(疲労 70 以上)・不調(調子 35 未満)」の人数。全員を小さなカードで並べる(iPad 横は 6 列、スマホは 2 列)。
#   カード:番付・四股名(ふつうの字)・けが/角番の札・調子と疲労の点(緑=良い・金=注意・朱=悪い)。けが・疲れ・不調・角番は金の枠。
#   押すと今までどおり力士の詳しい画面。v115 の札(ws2)の上から差し替える。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=159;\nconst SAVE='sumoManager159',SAVE158", "const APPV=160;\nconst SAVE='sumoManager160',SAVE159='sumoManager159',SAVE158")
rep('[SAVE158,SAVE157', '[SAVE159,SAVE158,SAVE157')
rep('<title>Grand Sumo Manager v159', '<title>Grand Sumo Manager v160')
BLOCK = r"""<style>
/* v160 弟子の様子=小さなカード(見本 tw3) */
.twx .sm4{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 8px}
.twx .sm4 div{flex:1;min-width:64px;background:var(--washi2);border:1px solid var(--line);border-radius:8px;padding:5px 8px;text-align:center;font-size:12px;color:var(--mute)}
.twx .sm4 b{display:block;font-size:20px;color:var(--sumi)}
.twx .sm4 .r b{color:var(--shu)}.twx .sm4 .y b{color:var(--kin)}
.twx .tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:6px}
.twx .tl{background:var(--washi2);border:1px solid var(--line);border-radius:6px;padding:5px 8px;cursor:pointer;display:grid;grid-template-columns:1fr auto;gap:0 6px;align-items:center}
.twx .tl:hover{border-color:var(--kin)}
.twx .tl.warn{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.twx .tl .rk{font-size:11px;color:var(--mute)}
.twx .tl .n{font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--sumi)}
.twx .tl .mt{grid-column:1/3;display:flex;gap:4px;align-items:center;font-size:11px;color:var(--mute);white-space:nowrap}
.twx .tl .tg{text-align:right}.twx .tl .tag{font-size:10px;padding:0 4px;margin:0 0 0 2px}
.twx .dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#888;flex:none}
.twx .dot.g{background:var(--midori)}.twx .dot.r{background:var(--shu)}.twx .dot.y{background:var(--kin)}
.twx .lg{font-size:12px;margin-top:6px}
@media (max-width:760px){.twx .tiles{grid-template-columns:1fr 1fr}}
</style>
<script>
(function(){
const _ot=ownTable;
const warn=r=>r.inj||r.fat>=70||r.cond<35||r.kad;
ownTable=function(){const o=ownAll();if(!o.length)return _ot();
 const cnt='<div class="sm4"><div><b>'+o.filter(r=>r.d<=1).length+'</b>関取</div><div class="r"><b>'+o.filter(r=>r.inj).length+'</b>けが</div><div class="y"><b>'+o.filter(r=>r.fat>=70).length+'</b>疲れ</div><div class="r"><b>'+o.filter(r=>r.cond<35).length+'</b>不調</div></div>';
 return '<div class="twx">'+cnt+'<div class="tiles">'+o.map(r=>{const pd=G.pend.includes(r.id);const c=r.cond>=70?'g':r.cond<35?'r':'',fz=r.fat>=70?'r':r.fat>=45?'y':'g';
  return '<div class="tl'+(warn(r)?' warn':'')+'" onclick="showR('+r.id+')"><div><div class="rk">'+esc(pd?(r.tsuke?'付出予定':'前相撲'):r.rkS)+'</div><div class="n">'+esc(r.n)+'</div></div><div class="tg">'+(injTag(r)||'')+(r.kad?'<span class="tag shu">角番</span>':'')+'</div><div class="mt"><span class="dot '+c+'"></span>調子 '+Math.round(r.cond)+' <span class="dot '+fz+'"></span>疲労 '+Math.round(r.fat)+'</div></div>';}).join('')+
  '</div><p class="mute kaku lg">● 緑=良い・金=注意・朱=悪い。金の枠=けが・疲れ・不調・角番</p></div>';};
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
