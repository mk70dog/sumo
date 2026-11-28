# v197 -> v198:マネージャーの能力を 4 つに
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=197;\nconst SAVE='sumoManager197',SAVE196", "const APPV=198;\nconst SAVE='sumoManager198',SAVE197='sumoManager197',SAVE196")
rep('[SAVE196,SAVE195', '[SAVE197,SAVE196,SAVE195')
rep('<title>Grand Sumo Manager v197', '<title>Grand Sumo Manager v198')

# v198:マネージャーの能力を 4 つに(目利き・人脈+事務・営業)。得意な分野と前の仕事
rep("sc:{n:'マネージャー',max:3,sk:['meki','net'],b:6,m:1.4}}","sc:{n:'マネージャー',max:3,sk:['meki','net','jim','eig'],b:6,m:1.4}}")
rep("meki:'目利き',iry:'医療',cnd:'調整',eiy:'栄養',net:'人脈'}","meki:'目利き',iry:'医療',cnd:'調整',eiy:'栄養',net:'人脈',jim:'事務',eig:'営業'}")
rep(" if(role==='sc')s.reg=RI(0,6);"," if(role==='sc'){s.reg=RI(0,6);mgSpec(s,1);}")
rep("function refreshMarket(){","""/* v198:マネージャーの得意な分野。実際の部屋のマネージャーは元力士が多く、事務・後援会との連絡・新弟子探しなどを受け持つ(効き目の大きさは推定) */
const MGT={meki:['スカウト上手',['元幕下','元三段目','元高校の相撲部の監督']],net:['顔が広い',['元力士','元相撲記者','元タニマチの会社員']],jim:['事務が得意',['元銀行員','元会社の経理','元役所の職員']],eig:['後援会に強い',['元営業マン','元旅行会社の社員','元百貨店の外商']]};
function mgSpec(s,boost){if(s.role!=='sc')return s;if(s.sk.jim==null){s.sk.jim=Math.round(cl((s.sk.meki+s.sk.net)/2+randn()*3.2,1,20));s.sk.eig=Math.round(cl((s.sk.meki+s.sk.net)/2+randn()*3.2,1,20));}
 if(!s.tok){const ks=['meki','net','jim','eig'];let k=ks.reduce((a,b)=>s.sk[b]>s.sk[a]?b:a);if(boost){k=pick(ks);s.sk[k]=Math.min(18,Math.max(s.sk[k],Math.max(...ks.map(x=>s.sk[x])))+RI(1,3));}s.tok=k;s.bg=pick(MGT[k][1]);
  if(boost){const av=ks.reduce((t,x)=>t+s.sk[x],0)/4;s.sal=Math.round(ROLE.sc.b+av*ROLE.sc.m);}}
 return s;}
function mgFix(){(G.staff||[]).concat(G.market||[]).forEach(s=>mgSpec(s,0));}
function mgEff(){const M=(G.staff||[]).filter(s=>s.role==='sc');M.forEach(s=>mgSpec(s,0));return {jim:M.reduce((t,s)=>t+Math.max(0,s.sk.jim-6),0),eig:M.reduce((t,s)=>t+(s.sk.eig-8),0),M:M};}
function refreshMarket(){""")
# 事務:出費の見直し(出費の合計 × 事務の力 × 0.4%、最大 5%)
rep("const tin=F.in.reduce((s,x)=>s+x[1],0),tout=F.out.reduce((s,x)=>s+x[1],0);","{const E=mgEff();if(E.jim>0){const o0=F.out.reduce((s,x)=>s+x[1],0);const v=Math.round(o0*Math.min(.05,E.jim*.004));if(v>0)F.in.push(['マネージャーの事務(むだな出費の見直し)',v]);}} const tin=F.in.reduce((s,x)=>s+x[1],0),tout=F.out.reduce((s,x)=>s+x[1],0);")
# 営業:後援会(場所ごと、営業の力−8 の合計 × 0.35 人。法人の会員も少し)
rep("G.sup+=(G._psup||0);});","G.sup+=(G._psup||0);{const E=mgEff();if(E.M.length){G.sup=Math.max(30,G.sup+Math.round(E.eig*.35));if(E.eig>=8&&Math.random()<Math.min(.25,E.eig*.012)){G.supC=(G.supC||0)+1;addNews('マネージャーの営業で、地元の会社が後援会に法人で入ってくれました。');}}}});")
# 部屋の声:マネージャーの言葉を得意な分野で
rep("add(1,['経理の書類をまとめておきました。','後援会の名簿を新しくしました。']);","{const M=(G.staff||[]).filter(s=>s.role==='sc');const tk=M.map(s=>(mgSpec(s,0),s.tok));if(tk.includes('jim'))add(2,['今月の帳簿をまとめました。ちゃんこの材料費が少し下がっています。','光熱費の契約を見直しました。','領収書の整理が終わりました。']);if(tk.includes('eig'))add(2,['後援会の新しい会員さんを '+RI(2,5)+' 人ご紹介いただきました。','地元の商店街に、番付表を配って回りました。','千秋楽パーティーの案内状を出しました。']);if(tk.includes('net'))add(1,['知り合いの記者から、ほかの部屋の話を聞いてきました。']);add(1,['経理の書類をまとめておきました。','後援会の名簿を新しくしました。']);}")
# 雇える人の札・今のスタッフの札に「得意」と前の仕事
rep("function skH(s){return ROLE[s.role].sk.map(","function skH(s){mgSpec(s,0);return (s.tok&&MGT[s.tok]?'<div class=\"mgt\"><span class=\"mgtk\">'+MGT[s.tok][0]+'</span> '+esc(s.bg||'')+'</div>':'')+ROLE[s.role].sk.map(")
rep("(rk==='sc'?'・担当 '+REG[s.reg].n:'')","(rk==='sc'?'・担当 '+REG[s.reg].n+(mgSpec(s,0).tok?'・'+MGT[s.tok][0]+'('+esc(s.bg)+')':''):'')")
rep("候補に会いに行けて(目利きで見立てが正確に)、人脈で情報が少し増える。</p></div>';","候補に会いに行けて(目利きで見立てが正確に)、人脈で情報が少し増える。事務が高いとむだな出費が減り、営業が高いと後援会の会員が増えやすい。</p></div>';")
ui = '<style>.mgt{flex:0 0 100%;width:100%;font-size:13px;margin:2px 0 4px;color:var(--mute,#aaa)}.mgtk{display:inline-block;background:var(--kin,#c9a24a);color:#1a1611;border-radius:9px;padding:0 8px;font-size:12px;font-weight:700;margin-right:4px}</style>\n'

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
