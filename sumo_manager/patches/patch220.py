# v216 -> v217:スカウトの争奪戦と、素質 B・C・D の弟子の役目(ダルマさん「素質Sをスカウトしてしまいがち」「素質bcdをとる必要性は?」→ 案 →「実施」)。
#   ① 注目の候補(A の上・S)は、よその部屋も声をかける(p.riv)。S は支度金の効き目が半分、縁(同郷・母校・親方が会いに行く・一門)が 1.6 倍。
#      勧誘は 2 回まで。断られると A・S は、ほかの部屋に決まることがある(S 4 割・A 2.5 割)。見込みの % は見立ての素質で出す(本当の素質が漏れないように)。
#   ② 関取の申し合い相手:番付が下の幕下・三段目の弟子の数で、関取の伸びが 0.95〜1.03 倍(出稽古・巡業・休みの週は関係なし)。
#   ③ 部屋の活気:幕下以下の弟子が 6 人より少ないと 1 人 0.8 下がり、多いと 1 人 0.35 上がる(2 まで)。
#   ④ 叩き上げ(画面の部品 patches/tk220_ui.js):入門のとき素質 C・D の弟子が関取・幕内に上がると、物語と人気・後援会。数字はどれも推定。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=216;\nconst SAVE='sumoManager216',SAVE215", "const APPV=217;\nconst SAVE='sumoManager217',SAVE216='sumoManager216',SAVE215")
rep('[SAVE215,SAVE214', '[SAVE216,SAVE215,SAVE214')
rep('<title>Grand Sumo Manager v216', '<title>Grand Sumo Manager v217')
# ① 争奪戦
rep("function offerP(p,lv){const sc=offerBonus(p);return cl(.5+G.rep*.004+lv*.17-(potOf(p.r)-9)*.035-p.int*.003+sc+((G.jin==null?50:G.jin)-50)*.002+(G.fac.shuku>=3?.03:0),.05,.95);}",
    "function prosRiv(p){if(p.riv==null){const pt=potOf(p.r);p.riv=pt>=16?RI(2,6):pt>=14.5?RI(1,4):pt>=13?RI(0,2):(Math.random()<.1?1:0);}return p.riv;}\n"
    "function offerP(p,lv,pv){const pt=pv!=null?pv:potOf(p.r);const S=pt>=16;const tie=offerBonus(p,pt)+Math.max(0,pt-12)*.08;\n"
    " return cl(.5+G.rep*.004+lv*.17*(S?.5:1)-(pt-9)*.035-p.int*.003+tie*(S&&tie>0?1.6:1)-Math.max(0,pt-12)*.08-prosRiv(p)*.05+((G.jin==null?50:G.jin)-50)*.002+(G.fac.shuku>=3?.03:0),.05,.95);}\n"
    "function offerPv(p,lv){return offerP(p,lv,p.ep==null?10:p.ep);}")
rep("function offerBonus(p){let b=0;", "function offerBonus(p,pv){let b=0;")
rep(" b-=Math.max(0,potOf(p.r)-12)*.08;\n if(own().some(r=>r.home===p.r.home))b+=.03;return b;}",
    " b-=Math.max(0,(pv!=null?pv:potOf(p.r))-12)*.08;\n if(own().some(r=>r.home===p.r.home))b+=.03;if(me().ic>=0&&/一門/.test(p.src||''))b+=.04;return b;}")
rep(" if(p.cool>G.wn)return '断られたばかりです。少し時間をおいたほうがよさそうです。';",
    " if((p.ng||0)>=2)return '2 回断られています。この候補はあきらめるしかなさそうです。';\n if(p.cool>G.wn)return '断られたばかりです。少し時間をおいたほうがよさそうです。';")
rep("G.money-=c;const r=p.r;r.n=shikona(me().pre);", "G.money-=c;const r=p.r;r.pot0=potOf(r);r.ep0=p.ep;r.n=shikona(me().pre);")
rep(" {const pt=potOf(p.r);if(pt>=13&&Math.random()<(pt-12)*.25){p.int=100;addNews(p.n+'は、ほかの部屋からも誘われていて、そちらに入門を決めそうです。');return p.n+'には断られました。ほかの部屋からも声がかかっていて、そちらに決めそうです。';}}\n p.int+=20;p.cool=G.wn+2;return p.n+'には今回は断られました。2 週たてばまた話ができます。';",
    " p.ng=(p.ng||0)+1;\n {const pt=potOf(p.r);const rv=prosRiv(p);if(rv>0&&pt>=13&&Math.random()<(pt>=16?.4:.25)){p.int=100;addNews(p.n+'は、ほかの部屋からも誘われていて、そちらに入門を決めそうです。');return p.n+'には断られました。ほかに '+rv+' 部屋が声をかけていて、そちらに決めそうです。';}}\n"
    " if(p.ng>=2){p.int=100;addNews(p.n+'には 2 度断られました。ほかの道を選ぶようです。');return p.n+'には 2 度断られました。この候補はあきらめます。';}\n"
    " p.int+=20;p.cool=G.wn+2;return p.n+'には今回は断られました(あと 1 回だけ話ができます)。2 週たてばまた話ができます。';")
# 札:よその部屋の声かけ・断られた回数・見込みは見立てで
rep("'<div class=\"sts\" style=\"grid-template-columns:7em 1fr\"><span>他部屋の関心</span>'+gg(p.int,p.int>=70?'r':p.int>=40?'y':'g2')+'</div>'+",
    "'<div class=\"sts\" style=\"grid-template-columns:7em 1fr\"><span>他部屋の関心</span>'+gg(p.int,p.int>=70?'r':p.int>=40?'y':'g2')+'</div>'+(prosRiv(p)?'<div class=\"riv\">ほかに '+p.riv+' 部屋が声をかけています</div>':'')+(p.ng?'<div class=\"shu\" style=\"font-size:12px\">断られた回数 '+p.ng+'/2</div>':'')+")
rep("'+man(offerCost(p,lv))+'・見込み '+Math.round(offerP(p,lv)*10)*10+'%</div></button>'", "'+man(offerCost(p,lv))+'・見込み '+Math.round(offerPv(p,lv)*10)*10+'%</div></button>'")
rep("(G.phase==='basho'||ng||p.cool>G.wn?'disabled':'')", "(G.phase==='basho'||ng||p.cool>G.wn||(p.ng||0)>=2?'disabled':'')")
# ② 関取の申し合い相手
rep("function hasPartner(r){", "function mshN(r){let n=0;for(const x of own())if(x.id!==r.id&&(x.d===2||x.d===3)&&x.pos>r.pos&&!x.inj)n++;return n;}\n"
    "function mshF(r,mk){if(r.d>1||mk==='休'||mk==='巡'||mk==='出')return 1;const n=mshN(r);return n>=8?1.03:n>=4?1+(n-4)*.0075:.95+n*.0125;}\nfunction hasPartner(r){")
rep(" if(isOwn)gm*=coMul(r);gm*=kcG(r)", " if(isOwn)gm*=coMul(r)*mshF(r,mk);gm*=kcG(r)")
# ③ 部屋の活気
rep("return Math.min(100,s/w+Math.min(4,o.filter(r=>r.per==='明るい').length*1.5))-mgPen();",
    "const yg=o.filter(r=>r.d>=2).length;return Math.min(100,s/w+Math.min(4,o.filter(r=>r.per==='明るい').length*1.5)+(yg>=6?Math.min(2,(yg-6)*.35):-(6-yg)*.8))-mgPen();")
ui = open(os.path.join(here, 'tk220_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
