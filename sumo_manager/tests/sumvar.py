import json,statistics as st,sys
for k in sys.argv[1:]:
    D=[json.loads(open('/tmp/var/%s_%d.txt'%(k,sd)).read().strip().splitlines()[-1]) for sd in range(11,21)]
    f=lambda g:[float(g(d)) for d in D]
    print(k,{x:round(st.mean(f(lambda d:d['優勝'][x])),1) for x in ['横綱','大関','三役','平幕']},'決定戦',round(st.mean(f(lambda d:d['決定戦'])),1),'横綱数',round(st.mean(f(lambda d:d['横綱数'])),2),'金星',round(st.mean(f(lambda d:d['金星per横綱場所'])),2))
