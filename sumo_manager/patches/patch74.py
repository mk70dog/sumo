# v70 -> v71:身のこなし(隠れた資質)+ほかの競技からの新弟子+新弟子運動能力検査(見本 mino1・ta1・ken1、ダルマさん「お任せ」)
# 出典:デイリー 2026/8/3・8/4、共同通信 2026/8/3(体格基準 167cm・67kg、3 月場所の中学卒業見込みは 165cm・65kg。
#       基準に届かない人は背筋力・握力・反復横跳びなど 7 項目の運動能力検査。新道〈高田川〉は柔術・MMA 出身で 164cm・55kg で通過)
#       Number 2026/8/28(安青錦の低い姿勢と体幹は幼少期からのレスリング経験が支え)
# 数値はすべて推定(合格の見込み、身のこなしの効き方、ほかの競技の新弟子の数・特徴)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

rep('<title>Sumo Manager v70</title>', '<title>Sumo Manager v71</title>')
rep("const APPV=70;\nconst SAVE='sumoManager70',SAVE69", "const APPV=71;\nconst SAVE='sumoManager71',SAVE70='sumoManager70',SAVE69")
rep('[SAVE69,SAVE68', '[SAVE70,SAVE69,SAVE68')
rep(" if(g.v===69){g.v=70;}\n return g.v===70?g:null;}", " if(g.v===69){g.v=70;}\n if(g.v===70){mig71(g);g.v=71;}\n return g.v===71?g:null;}")
rep('G={v:70,', 'G={v:71,')

# ---- 身のこなし ----
CORE = r'''
/* v71:身のこなし(運動神経・体幹。生まれつき 1〜20、10 がふつう)。数値はすべて推定 */
function minoOf(r){return r.mino==null?10:r.mino;}
function taiOf(r){return cl((minoOf(r)-10)*.2,-1,2);}
function setMino(r,m,f){m=Math.round(cl(m,1,20));const d=(m-minoOf(r))/10;['exp','flx','tgw'].forEach(k=>{if(r.cap&&r.cap[k]!=null)r.cap[k]=cl(r.cap[k]+d*f,r.a[k],20);});r.mino=m;}
const MINOX={'安青錦':4,'欧勝馬':3,'魁勝':2};
function realMino(g,f){const L=Object.values(g.R).filter(r=>r&&r.a&&r.cap&&!r.ret&&r.w).map(r=>[r,ovr(r)]).sort((a,b)=>b[1]-a[1]);if(L.length<10)return;
 L.forEach(([r],i)=>{if(f<1&&r.mino!=null)return;const P=L.slice(Math.max(0,i-20),i+21);const mw=P.reduce((a,x)=>a+x[0].w,0)/P.length;const X=(typeof REALX!=='undefined'&&REALX[r.n])||{};
  setMino(r,10+(mw-r.w)*.12+(hhR(r.id,3)-.5)*4+(MINOX[r.n]||0)+(X.iki?1:0),f);});}
function mig71(g){realMino(g,.6);for(const id in g.R){const r=g.R[id];if(r&&r.mino==null)r.mino=10;}(g.pros||[]).forEach(p=>{if(p.r&&p.r.mino==null)p.r.mino=Math.round(cl(10+randn()*3,1,20));});}
function minoTxt(r){const m=minoOf(r);return (m>=15?'体幹が強く、運動神経がいい':m>=12?'身のこなしが良い':m<=5?'体が硬く、動きがぎこちない':m<=8?'身のこなしはいまひとつ':'ふつう')+
 (m>=12?'<div class="mute" style="font-size:12px">腰の重さ(体幹)・瞬発力・柔軟性・土俵際が少し高い。引き技・足技・逆転が決まりやすい</div>':m<=8?'<div class="mute" style="font-size:12px">体幹の分で腰の重さが少し低い。引き技・足技・逆転はやや決まりにくい</div>':'');}
function minoStar(m){const n=cl(Math.round(m/4),1,5);return '<span class="stars">'+'★'.repeat(n)+'<i>'+'★'.repeat(5-n)+'</i></span>';}
function chipH(r,k){const c=(lb,v)=>'<em class="atp '+(v>=.5?'pu':v<=-.5?'mi':'')+'">'+lb+(v>=0?'+':'−')+Math.abs(v).toFixed(1)+'</em>';
 if(k==='mae')return c('器用さ',mgOf(r));return c('体格',kbOf(r))+(kn(r)>=40?' '+c('体幹',taiOf(r)):'');}
'''
rep("function inb(r,k){return k==='kos'?kbOf(r):k==='mae'?mgOf(r):0;}", CORE + "function inb(r,k){return k==='kos'?kbOf(r)+taiOf(r):k==='mae'?mgOf(r):0;}")
# 引き技・足技・土俵際は身のこなしで少し強く(最大 +0.5、推定)
rep("function E(r,k){return Math.max(.5,((k==='kos'||k==='mae'?atTot(r,k):r.a[k])-injPen(r,k))*r._f+r._pr);}",
    "function E(r,k){return Math.max(.5,((k==='kos'||k==='mae'?atTot(r,k):r.a[k])-injPen(r,k)+(k==='hik'||k==='ash'||k==='tgw'?(minoOf(r)-10)*.05:0))*r._f+r._pr);}")
# 新しく生まれる力士(新弟子・アマチュアなど)は 1〜20 のばらつき
rep(" return r;\n}\nfunction ovrOf", " setMino(r,10+randn()*3,1);\n return r;\n}\nfunction ovrOf")
# 実在の力士:同じくらいの力(番付)の力士より軽いほど高い(体重 1kg あたり 0.12)+経歴にレスリング・柔道(推定)
rep(" buildRanks();\n const o=own();const sek=", " realMino(G,1);\n buildRanks();\n const o=own();const sek=")
# 画面:腰の重さの札を 2 つ(体格・体幹)
rep("'+x[1]+' <em class=\"atp '+(ib>=.5?'pu':ib<=-.5?'mi':'')+'\">'+lb+sg+'</em></span>", "'+x[1]+' '+chipH(r,x[0])+'</span>")
rep("'ふつう')+\n  '</dl><p class=\"mute kaku\" style=\"font-size:12px\">一緒に過ごす週", "'ふつう')+hidRow(r,'身のこなし',40,minoTxt(r))+\n  '</dl><p class=\"mute kaku\" style=\"font-size:12px\">一緒に過ごす週")

# ---- ほかの競技からの新弟子 ----
OSP = r'''
/* v71:ほかの競技からの新弟子(名前は架空。特徴・人数は推定) */
const OSP={
 '柔道':{c:'j',age:[18,22],ht:[168,192],w:[85,140],T:[2.8,4.6],st:[['右',35],['左',35],['技',30]],a:{nag:2,ash:2,flx:1.5,mig:1,hid:1,str:.5,tsk:-1.5,tac:-1.5,mae:-1.5},
  f:'投げ・足技・柔軟性が高め。組むのが得意で、突き押しは低め',
  h:{高校:['高校柔道部・県大会 優勝','高校柔道部・インターハイ 出場','高校柔道部・インターハイ ベスト8'],大学:['大学柔道部・全日本学生 ベスト16','大学柔道部・全日本学生 3 位','大学柔道部・地区学生大会 優勝'],社会人:['実業団柔道部・全日本実業団 出場','実業団柔道部・全日本実業団 3 位']}},
 'レスリング':{c:'w',age:[18,22],ht:[168,190],w:[80,130],T:[2.8,4.6],st:[['押',30],['技',40],['右',15],['左',15]],a:{exp:2,ash:2,kos:1,str:1,gam:.5,tac:-1,tsk:-1.5,mae:-1.5},
  f:'低い姿勢・体幹・瞬発力が高め。足取りが得意',
  h:{高校:['高校レスリング部・インターハイ 出場','高校レスリング部・インターハイ 3 位','高校レスリング部・全国高校選抜 ベスト8'],大学:['大学レスリング部・全日本学生 5 位','大学レスリング部・全日本学生 3 位','大学レスリング部・学生リーグ戦 出場'],社会人:['社会人・全日本選手権 出場','社会人・全日本社会人 3 位']}},
 '柔術・総合':{c:'b',age:[15,22],ht:[164,186],w:[55,105],T:[2.4,4],st:[['技',60],['右',20],['左',20]],a:{flx:2.5,tgw:2,gam:2,ash:1,tac:-1.5,tsk:-1.5,mae:-1.5},
  f:'柔軟性・土俵際・我慢強さが高め。体は小さめ',
  h:{中学:['ブラジリアン柔術・地区大会 優勝','総合格闘技・アマチュア大会 1 勝'],高校:['ブラジリアン柔術(青帯)・全日本 3 位','総合格闘技・アマチュア大会 優勝'],大学:['ブラジリアン柔術(紫帯)','総合格闘技・アマチュア大会 優勝'],社会人:['ブラジリアン柔術(茶帯)','総合格闘技・アマチュア戦 3 勝']}}};
function mkOsp(){const s=wpick([['柔道',45],['レスリング',30],['柔術・総合',25]]);const O=OSP[s];const age=RI(O.age[0],O.age[1]);
 const kind=age<=15?'中学':age<=18?'高校':Math.random()<.7?'大学':'社会人';const reg=RI(0,5);
 const r=mkR({T:R(O.T[0],O.T[1]),room:R(5,11),age:age,h:0,home:pick(REG[reg].p),fr:false,style:wpick(O.st)});
 for(const k in O.a){const v=O.a[k];r.a[k]=cl(r.a[k]+v,1,19.5);r.cap[k]=cl(r.cap[k]+Math.max(0,v)*.6,r.a[k],20);}
 r.ht=RI(O.ht[0],O.ht[1]);r.w=Math.round(R(O.w[0],O.w[1]));r.wT=Math.round(Math.max(r.w+R(15,45),115));
 setMino(r,13+randn()*2.5,1);const hl=(O.h[kind]||O.h['大学']);r.osp={s:s,h:pick(hl)};r.kind=kind;
 return {cid:Math.random().toString(36).slice(2,8),n:personName(reg),kind:kind,reg:reg,age:age,r:r,v:0,mk:0,eo:null,ep:null,err:6,int:R(0,15),wk:G.wn,cool:0,ama:null,star:false,lv:-1,sch:'',src:'',osp:r.osp};}
function ospH(p){const o=p.osp||(p.r&&p.r.osp);if(!o)return '';return '<div class="mn"><b>前の競技:'+esc(o.s)+'('+esc(o.h)+')</b><br>'+OSP[o.s].f+'(推定)<br>相撲は未経験:立ち合い・突き押し・前さばきは低めから始まり、最初の 1〜2 年は伸びがゆっくり。'+(p.v>=2?'身のこなし '+minoStar(minoOf(p.r)):'')+'</div>';}
/* 新弟子運動能力検査:体格基準(167cm・67kg、中学卒業見込みは 165cm・65kg)に届かない人が受ける。合格の見込みは推定 */
function bodyStd(p){return p.kind==='中学'?[165,65]:[167,67];}
function needTest(p){const s=bodyStd(p);return p.r.ht<s[0]||p.r.w<s[1];}
function testP(r){return cl(sig((minoOf(r)*.45+r.a.str*.25+r.a.exp*.2-4.5)*.9),.05,.97);}
function testH(p){if(!needTest(p))return '';const s=bodyStd(p),t=testP(p.r);return '<div class="shu" style="font-size:12px">体格基準('+s[0]+'cm・'+s[1]+'kg)に届きません → 運動能力検査を受けます'+(p.v>=2?'。見込み:'+(t>=.7?'合格しそう':t>=.4?'五分五分':'厳しそう'):'')+'</div>';}
'''
rep("function mkProspect(reg,star){", OSP + "function mkProspect(reg,star){")
# 情報源:親方の人脈・一門から年に数人ほど(推定)
rep("if(Math.random()<.012+net*.5)add(mkProspect(6),'海外の相撲関係者の紹介');",
    "if(Math.random()<.012+net*.5)add(mkProspect(6),'海外の相撲関係者の紹介');\n if(Math.random()<(.05+net*.3)*spring){const p=mkOsp();add(p,me().ic>=0&&Math.random()<.4?IC[me().ic]+'一門の紹介('+p.osp.s+')':'親方の人脈('+p.osp.s+'の指導者)');}")
# 最初の 1 年半(9 場所)は伸びがゆっくり(推定 0.85 倍)
rep("if(r.fast&&r.age<26)gm*=r.fast;", "if(r.fast&&r.age<26)gm*=r.fast;if(r.osp&&G.bnum-(r.join||0)<9)gm*=.85;")
# 候補カード
rep("(p.nisei?'<span class=\"tag kin\">二世</span>':'')", "(p.nisei?'<span class=\"tag kin\">二世</span>':'')+(p.osp?'<span class=\"spt '+OSP[p.osp.s].c+'\">'+esc(p.osp.s)+'</span>':'')")
rep("'<div class=\"nm\" style=\"font-size:15px\">'+esc(p.n)+'</div>'", "'<div class=\"nm\" style=\"font-size:15px\">'+esc(p.n)+'</div>'+ospH(p)")
rep("'<div>'+Math.round(r.ht)+'cm・'+Math.round(r.w)+'kg'+(ng?", "'<div>'+Math.round(r.ht)+'cm・'+Math.round(r.w)+'kg'+testH(p)+(ng?")
rep("(身長・体重の基準は 2023 年に撤廃されました)", "(身長 167cm・体重 67kg〈3 月場所の中学卒業見込みは 165cm・65kg〉に届かない人は、背筋力・握力・反復横跳びなど 7 項目の運動能力検査を受けます)")
# 力士の画面:前の競技
rep("<dl class=\"kv\" style=\"margin-top:6px\"><dt>部屋</dt><dd>'+esc(G.heya[r.h].n)+'部屋</dd>'", "<dl class=\"kv\" style=\"margin-top:6px\"><dt>部屋</dt><dd>'+esc(G.heya[r.h].n)+'部屋</dd>'+(r.osp?'<dt>前の競技</dt><dd>'+esc(r.osp.s)+'('+esc(r.osp.h)+')</dd>':'')")
# 運動能力検査(勧誘がまとまったあと。落ちたら支度金は払わず、入門は見送り)
rep(" if(Math.random()<offerP(p,lv)){",
    " if(Math.random()<offerP(p,lv)){\n  if(needTest(p)){if(Math.random()>testP(p.r)){G.pros=G.pros.filter(x=>x.cid!==cid);addNews(p.n+'は入門を決めましたが、新弟子運動能力検査に合格できず、入門を見送りました。');return p.n+'は入門を決めましたが、体格基準に届かず受けた新弟子運動能力検査(背筋力・握力・反復横跳びなど 7 項目)に合格できませんでした。今回は入門を見送ります。';}\n   addNews(p.n+'は体格基準に届かなかったため新弟子運動能力検査を受け、合格しました。');}")
rep("  if(p.int>=100){", "  if(p.int>=100){if(needTest(p)&&Math.random()>testP(p.r))return false;")
CSS = ".spt{display:inline-block;font-size:11px;padding:0 6px;border-radius:3px;margin-left:4px;background:#2c3e5c;color:#fff;vertical-align:1px;font-family:sans-serif}.spt.w{background:#7a4a1e}.spt.b{background:#3d6b4f}" \
      ".mn{font-size:12px;line-height:1.5;margin-top:3px}.mn b{color:var(--ai)}.stars{color:var(--kin);letter-spacing:1px}.stars i{font-style:normal;opacity:.3}"
rep(".atw5{display:grid;", CSS + ".atw5{display:grid;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
