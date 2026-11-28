<style>/* v195:部屋の画面を iPad で 1 画面に(見本 fv1)。横幅 900px 以上・高さ 600px 以上のときだけ */
@media (min-width:900px) and (min-height:600px){
body.vh1 #hdr{padding:6px 14px!important}
body.vh1 #hdr .row{flex-wrap:nowrap!important;gap:10px!important}
body.vh1 #hdr .title{font-size:19px!important;letter-spacing:.06em!important}
body.vh1 #hdr .title small{font-size:11px!important}
body.vh1 #hdr .cal{font-size:13px!important;padding:2px 8px!important}
body.vh1 #hdr .hbtns{white-space:nowrap;display:flex;gap:4px}
body.vh1 #hdr .hbtns button,body.vh1 #hdr .hbtns .btn{white-space:nowrap;font-size:12px!important;padding:3px 8px!important;min-height:0!important}
body.vh1 #hdr .stat{margin-left:auto!important;font-size:13px!important;gap:10px!important;width:auto!important;flex:none}
body.vh1 #nav{margin:6px 0!important}
body.vh1 #nav button{min-height:34px!important;padding:4px 2px!important;font-size:14px!important}
body.vh1 .hbs{height:calc(100vh - 150px)!important;margin-bottom:8px!important}
body.vh1 .hbs .hbimg{left:0!important;top:0!important;width:100%!important;height:100%!important;background-size:cover!important;background-position:center 40%!important}
body.vh1 .hbslot.hbleft{top:8px!important;bottom:8px!important;height:auto!important;max-height:none!important;overflow:hidden!important}
body.vh1 .hbslot.hbright{top:8px!important;bottom:8px!important;height:auto!important;max-height:none!important;overflow:hidden!important}
body.vh1 .hbslot.hbleft>.hbp,body.vh1 .hbslot.hbright>.hbp{overflow:auto;min-height:0}
body.vh1 .hbslot.hbleft>.hbp.hbv,body.vh1 .hbslot.hbright>.hbp.hbo{flex:1 1 auto}
body.vh1 .hbslot.hbleft>.hbp.hbdy,body.vh1 .hbslot.hbright>.hbp.hby{flex:0 1 auto;max-height:38%}

body.vh1 .hbout{margin:0 0 6px!important}.hbout>.hbp{padding:4px 10px!important}.hbout .hbk{display:none}
body.vh1 .hbs~*{display:none!important}
body.vh1 #app{padding-bottom:0!important;margin-bottom:0!important}body.vh1 .hbs{margin-bottom:0!important}
}</style>
<script>(function(){const R0=render;render=function(){const x=R0.apply(this,arguments);try{document.body.classList.toggle('vh1',UI.view==='home');}catch(e){}return x;};})();</script>
