# v168 -> v169:小さい部屋のお金を本物に近づける(ダルマさん「実施」)。数値の多くは推定。
#   A 千秋楽の打ち上げのご祝儀を東京場所でも(後援会・法人・関取・勝ち越しで決まる。推定)。
#   B 後援者からの差し入れ:後援会の人数で食費が 5〜30% 減る(推定)。幕内優勝の副賞(米・肉など)で次の場所の食費がさらに減る。
#   C 地方場所の宿舎・稽古場:つながり 30 以上は用意してもらえる/15〜29 は一門・後援会のつてで半額/15 未満は全額。
#   D 食費 1 人 22→18 万円、光熱費 15+4×人数 → 8+2.5×人数(推定)。
#   出典:moneypost 1465571(地方場所は後援会が宿舎・稽古場、差し入れ、激励会・打ち上げの祝儀、5 人で黒字)、
#         moneypost 1181396(米 月 500kg 近く・月 30 万円前後、平均 15 人の部屋)、moneypost 1153439(人数が増えると 1 人あたりが下がる)、
#         moneypost 1134707(優勝の副賞の米や肉に助けられた)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=168;\nconst SAVE='sumoManager168',SAVE167", "const APPV=169;\nconst SAVE='sumoManager169',SAVE168='sumoManager168',SAVE167")
rep('[SAVE167,SAVE166', '[SAVE168,SAVE167,SAVE166')
rep('<title>Grand Sumo Manager v168', '<title>Grand Sumo Manager v169')
# 食費(D・B)
rep(" F.out.push(['ちゃんこの食費('+mealName()+')'+(chiB&&cv>=30?'・地方の差し入れあり':''),Math.round(nn*22*mealCost()*(chiB?(cv>=30?.75:.9):1))]);\n F.out.push(['水道光熱費',15+nn*4]);",
    " {const sa=Math.min(.3,.05+(G.sup||0)/3000);const rice=G.riceB===G.bnum;let f=(chiB?(cv>=30?.75:.9):1)*(1-sa)*(rice?.75:1);f=Math.max(.5,f);"
    "F.out.push(['ちゃんこの食費('+mealName()+'・後援者の差し入れ −'+Math.round(sa*100)+'%'+(chiB&&cv>=30?'・地方の差し入れあり':'')+(rice?'・優勝の副賞の米や肉':'')+')',Math.round(nn*18*mealCost()*f)]);}\n"
    " F.out.push(['水道光熱費',Math.round(8+nn*2.5)]);")
# 地方の宿舎(C)と打ち上げ(A)
rep("if(cv<30)F.out.push([chiB.n+'場所の宿舎・稽古場(自前で手配)',60+2*nn]);",
    "if(cv<15)F.out.push([chiB.n+'場所の宿舎・稽古場(自前で手配)',60+2*nn]);else if(cv<30)F.out.push([chiB.n+'場所の宿舎・稽古場(一門・後援会のつてで半額)',Math.round((60+2*nn)/2)]);")
rep(" if(G.acc.dek)F.out.push(['出稽古の費用',G.acc.dek]);",
    " if(!chiB){const kk=o.filter(r=>{const c=B.rec[r.id];return c&&c.w>c.l+(c.ab||0);}).length;const sek=o.filter(r=>r.d<=1).length;const u=Math.round((G.sup||0)*.06+(G.supC||0)*2+sek*8+kk);if(u)F.in.push(['千秋楽の打ち上げのご祝儀',u]);}\n"
    " {const my=sum.yu.some(y=>y.h===ME()&&y.d===0);if(my)G.riceB=G.bnum+1;}\n"
    " if(G.acc.dek)F.out.push(['出稽古の費用',G.acc.dek]);")
# 説明
rep("いちばん大きな支出は食費です。借金には利息がかかります。",
    "いちばん大きな支出は食費です。後援会が大きいほど米・肉・野菜の差し入れが増えて食費が減り、幕内優勝の副賞(米や肉)でも次の場所の食費が減ります。どの場所でも千秋楽の打ち上げでご祝儀が入ります(地方場所は激励会も)。借金には利息がかかります。")
rep("地方の後援会とのつながりが 30 以上なら宿舎と稽古場を用意してもらえ、",
    "地方の後援会とのつながりが 30 以上なら宿舎と稽古場を用意してもらえ(15 以上なら一門や後援会のつてで半額)、")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
