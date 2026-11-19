# 見本 dfa・dfb:字を Dela Gothic One(OFL)にした画面。dfa=画面の字をすべて、dfb=見出し・四股名・番付・ボタン・数字だけ(説明の文はそのまま)
# 取組の前の画像(見本 int1)もいっしょに入れる。
import base64
src=open('samples/int1.html',encoding='utf-8').read()
F=base64.b64encode(open('fonts/Dela-sub.woff2','rb').read()).decode()
FACE='@font-face{font-family:Dela;src:url(data:font/woff2;base64,'+F+') format("woff2")}'
CSS={'dfa':'<style>'+FACE+'body,body *{font-family:Dela,sans-serif!important;font-weight:400!important;letter-spacing:.02em}</style>',
     'dfb':'<style>'+FACE+'h1,h2,h3,h4,.nm,.fuda,.rk,.btn,button,th,.num,b,.tag,.itt,.itm,.it2,.atg,.kin,.ai,.sub{font-family:Dela,sans-serif!important;font-weight:400!important}</style>'}
NOTE={'dfa':'dfa:字をすべて Dela Gothic One に','dfb':'dfb:見出し・四股名・番付・ボタン・数字だけ Dela Gothic One に'}
for k in CSS:
    s=src.replace('</body>',CSS[k]+'</body>',1).replace('見本 int1:','見本 '+NOTE[k]+'(取組の前の画像は int1)/',1).replace('<title>見本 int1</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
