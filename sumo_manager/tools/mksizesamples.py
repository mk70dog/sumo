# 見本 sz1〜5:スタート画面の「一人相撲」「二人相撲」を小さく、題字を大きく(ダルマさん「サイズダウン タイトルアップ サンプル x5」)。v80 に CSS を足すだけ。
base=open('sumo_manager_v80.html',encoding='utf-8').read()
V={
'sz1':('題字 1.3 倍・ボタンを横に細長く(高さ半分)',
 '.t1 b{font-size:clamp(60px,13vw,136px)}.t1 small{font-size:clamp(14px,2.8vw,26px)}.t1{padding:14px 44px 16px}'
 '.st-go button.big{padding:10px 12px}.st-go button.big b{font-size:clamp(22px,4vw,34px);margin:0}.st-go button.big small{font-size:12px}'),
'sz2':('題字を画面の真ん中に大きく・ボタンは下に小さく並べる',
 '.st-title{top:50%!important;transform:translate(-50%,-62%)!important}.t1 b{font-size:clamp(70px,15vw,160px)}.t1 small{font-size:clamp(15px,3vw,28px)}.t1{padding:16px 50px 18px}'
 '.st-go{bottom:4%!important;width:min(560px,90vw)!important;gap:10px!important}.st-go button.big{padding:8px 10px}.st-go button.big b{font-size:clamp(20px,3.6vw,28px);margin:0}.st-go button.big small{display:none}'),
'sz3':('題字 1.5 倍(枠を広く)・ボタンは文字だけの小さな札',
 '.t1 b{font-size:clamp(70px,16vw,170px)}.t1 small{font-size:clamp(15px,3vw,28px)}.t1{padding:16px 60px 18px}'
 '.st-go{width:min(480px,86vw)!important}.st-go button.big{padding:8px 10px;background:rgba(10,8,6,.75)!important}.st-go button.big b{font-size:clamp(20px,3.4vw,26px);margin:0;letter-spacing:.3em}.st-go button.big small{display:none}'),
'sz4':('題字 1.4 倍・ボタンを縦に 2 段、細く',
 '.t1 b{font-size:clamp(64px,14vw,150px)}.t1 small{font-size:clamp(14px,2.8vw,26px)}.t1{padding:14px 50px 16px}'
 '.st-go{flex-direction:column!important;width:min(380px,80vw)!important;gap:8px!important}.st-go button.big{padding:8px 10px}.st-go button.big b{font-size:clamp(20px,3.4vw,26px);margin:0}.st-go button.big small{font-size:11px}'),
'sz5':('題字を横幅いっぱい・ボタンは丸い小さな札',
 '.st-title{width:96vw!important}.t1{display:block;padding:16px 10px 18px}.t1 b{font-size:clamp(72px,17vw,190px)}.t1 small{font-size:clamp(16px,3.2vw,30px)}'
 '.st-go{width:min(520px,90vw)!important;gap:14px!important}.st-go button.big{padding:8px 10px;border-radius:40px}.st-go button.big b{font-size:clamp(20px,3.4vw,26px);margin:0}.st-go button.big small{display:none}'),
}
for k,(n,css) in V.items():
    s=base.replace('</body>','<style>'+css+'</style><div style="position:fixed;left:6px;top:46px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+k+':'+n+'</div></body>',1).replace('<title>Grand Sumo Manager v80</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
