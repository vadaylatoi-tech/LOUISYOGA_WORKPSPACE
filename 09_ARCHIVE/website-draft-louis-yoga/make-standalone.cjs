const fs=require('fs');const path=require('path');
const source=path.join(__dirname,'louis-yoga','dist');
const mime={'.png':'image/png','.svg':'image/svg+xml','.ttf':'font/ttf'};
const assets={};
for(const name of fs.readdirSync(path.join(source,'assets'))){const type=mime[path.extname(name)];if(type)assets['assets/'+name]='data:'+type+';base64,'+fs.readFileSync(path.join(source,'assets',name)).toString('base64');}
let html=fs.readFileSync(path.join(source,'index.html'),'utf8');
let css=fs.readFileSync(path.join(source,'styles.css'),'utf8');
let js=fs.readFileSync(path.join(source,'app.js'),'utf8');
for(const [key,data] of Object.entries(assets)){html=html.split('src="'+key+'"').join('src="'+data+'"');css=css.split("url('"+key+"')").join("url('"+data+"')");}
js=js.replace('const imageFor=(p,color=p.color)=>`assets/${p.asset || colors[color]?.asset || colors.rose.asset}`;', 'const imageFor=(p,color=p.color)=>ASSETS[`assets/${p.asset || colors[color]?.asset || colors.rose.asset}`];');
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>');
html=html.replace('<script src="app.js" defer></script>','');
html=html.replace('</body>','<script>const ASSETS='+JSON.stringify(assets)+';\n'+js+'</script></body>');
fs.writeFileSync(path.join(__dirname,'Louis-Yoga-mo-truc-tiep.html'),html);
console.log('Đã tạo HTML tự chứa: '+fs.statSync(path.join(__dirname,'Louis-Yoga-mo-truc-tiep.html')).size+' bytes');
