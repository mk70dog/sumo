import sys,re
f=sys.argv[1];kw=sys.argv[2];w=int(sys.argv[3]) if len(sys.argv)>3 else 90;mx=int(sys.argv[4]) if len(sys.argv)>4 else 20
s=open(f,encoding='utf-8').read()
idx=[m.start() for m in re.finditer(re.escape(kw),s)]
print('==',kw,len(idx))
for i in idx[:mx]:print(s.count('\n',0,i)+1,'|',s[max(0,i-w):i+w].replace('\n',' '))
