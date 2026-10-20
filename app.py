
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Stickman vs Zombie</title>
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;background:#14232c;color:white;font-family:Arial,sans-serif;touch-action:none}
canvas{display:block;width:100vw;height:100dvh}
#hud{position:fixed;top:12px;left:12px;right:12px;display:flex;justify-content:space-between;gap:10px;pointer-events:none}
.box{background:#09131ddd;border:1px solid #ffffff35;border-radius:12px;padding:10px;min-width:125px}
h3{margin:0 0 7px;color:#baff78;font-size:15px}
p{margin:4px 0;font-size:12px}
.bar{height:10px;background:#35434b;border-radius:8px;overflow:hidden}
.fill{height:100%;width:100%;background:#83f16b;transition:width .1s}
#buttons{position:fixed;bottom:18px;left:16px;right:16px;display:flex;justify-content:space-between;align-items:end}
.pad{display:grid;grid-template-columns:52px 52px 52px;grid-template-rows:52px 52px;gap:5px}
button{border:1px solid #ffffff55;background:#111f2be8;color:white;border-radius:13px;font-size:23px;font-weight:bold;touch-action:none;user-select:none}
button:active,.pressed{background:#4c743c}
#up{grid-column:2}#left{grid-column:1;grid-row:2}#down{grid-column:2;grid-row:2}#right{grid-column:3;grid-row:2}
#hit{width:88px;height:88px;border-radius:50%;background:#a7382c;border:2px solid #ffb27b;font-size:15px}
#hit b{display:block;font-size:29px}
#overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#02080bc9;padding:20px}
#card{background:#132630;border:1px solid #59716e;border-radius:20px;padding:25px;text-align:center;max-width:400px;width:100%}
#card h1{color:#baff78}
#start{background:#baff78;color:#17251b;border:0;padding:14px 24px;font-size:16px;border-radius:10px}
.hide{display:none!important}
</style>
</head>
<body>
<canvas id="game"></canvas>
<div id="hud">
 <div class="box"><h3>⚔ STICKMAN</h3><p>Máu: <span id="hp">100</span>/100</p><div class="bar"><div id="pbar" class="fill"></div></div></div>
 <div class="box"><h3>☠ ZOMBIES</h3><p>Đã hạ: <b id="score">0</b></p><p>Quái: <b id="count">0</b></p></div>
</div>
<div id="buttons">
 <div class="pad">
  <button id="up">▲</button><button id="left">◀</button>
  <button id="down">▼</button><button id="right">▶</button>
 </div>
 <button id="hit"><b>⚔</b> CHÉM</button>
</div>
<div id="overlay">
 <div id="card">
  <h1 id="title">STICKMAN<br>VS ZOMBIES</h1>
  <p id="desc">Sống sót giữa bầy zombie! Di chuyển, né đòn và chém để bảo vệ mình.</p>
  <p>📱 Dùng các nút trên màn hình<br>💻 Máy tính: WASD / phím mũi tên, Space để chém</p>
  <button id="start">BẮT ĐẦU CHƠI</button>
 </div>
</div>
<script>
(()=>{
const c=document.getElementById('game'),g=c.getContext('2d');
const $=id=>document.getElementById(id);
let w,h,dpr=1,last=0,state='menu',time=0,score=0,spawn=0;
let p,zombies=[],particles=[],texts=[],keys={};
const rnd=(a,b)=>a+Math.random()*(b-a);
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
function resize(){
 dpr=Math.min(devicePixelRatio||1,2);
 w=innerWidth;h=innerHeight;
 c.width=w*dpr;c.height=h*dpr;
 g.setTransform(dpr,0,0,dpr,0,0);
 if(p){p.x=clamp(p.x,20,w-20);p.y=clamp(p.y,90,h-25)}
}
addEventListener('resize',resize);
function reset(){
 score=0;time=0;spawn=.5;zombies=[];particles=[];texts=[];
 p={x:w/2,y:h/2,hp:100,fx:1,fy:0,walk:0,attack:0,cool:0,inv:0};
 for(let i=0;i<3;i++)makeZombie();
 hud();
}
function makeZombie(){
 let side=Math.floor(Math.random()*4),x,y;
 if(side===0){x=rnd(20,w-20);y=100}
 else if(side===1){x=w-20;y=rnd(100,h-25)}
 else if(side===2){x=rnd(20,w-20);y=h-25}
 else{x=20;y=rnd(100,h-25)}
 let hp=60+Math.min(score,20)*2;
 zombies.push({x,y,hp,max:hp,speed:rnd(43,59)+Math.min(score,20),fx:1,fy:0,walk:rnd(0,8),flash:0,cool:rnd(.2,1),dead:false,fade:0});
}
function hud(){
 $('hp').textContent=Math.ceil(p.hp);
 $('pbar').style.width=p.hp+'%';
 $('score').textContent=score;
 $('count').textContent=zombies.filter(z=>!z.dead).length;
}
function line(x,y,a,b,width,color){
 g.beginPath();g.moveTo(x,y);g.lineTo(a,b);g.lineWidth=width;
 g.strokeStyle=color;g.lineCap='round';g.stroke();
}
function circle(x,y,r,color){
 g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.fillStyle=color;g.fill();
}
function blood(x,y,fx,fy,n=12){
 for(let i=0;i<n;i++){
  let a=Math.atan2(fy,fx)+rnd(-1.3,1.3),v=rnd(40,190);
  particles.push({x:x+rnd(-4,4),y:y+rnd(-5,5),vx:Math.cos(a)*v,vy:Math.sin(a)*v-rnd(10,50),life:rnd(.25,.65),size:rnd(2,4),color:Math.random()<.25?'#ff9880':'#d93443'});
 }
}
function text(x,y,s,color){
 texts.push({x,y,s,color,life:.8});
}
function attack(){
 if(state!=='play'||p.cool>0)return;
 p.attack=.3;p.cool=.43;
 for(let z of zombies){
  if(z.dead)continue;
  let dx=z.x-p.x,dy=z.y-p.y,d=Math.hypot(dx,dy)||1;
  let dot=(dx*p.fx+dy*p.fy)/d;
  if(d<75&&dot>-.25){
   z.hp-=35;z.flash=.17;
   z.x+=p.fx*10;z.y+=p.fy*10;
   blood(z.x,z.y,p.fx,p.fy,14);
   text(z.x,z.y-27,'-35','#ffe2b7');
   if(z.hp<=0){z.dead=true;z.fade=.45;score++;text(z.x,z.y-35,'+1','#c6ff85')}
  }
 }
 hud();
}
function hurt(z){
 if(p.inv>0)return;
 p.hp=Math.max(0,p.hp-10);p.inv=.7;
 let dx=p.x-z.x,dy=p.y-z.y,d=Math.hypot(dx,dy)||1;
 p.x+=dx/d*14;p.y+=dy/d*14;
 text(p.x,p.y-25,'-10','#ff7777');
 blood(p.x,p.y,-dx/d,-dy/d,5);
 if(p.hp<=0){
  state='over';$('title').innerHTML='BẠN ĐÃ THUA!';
  $('desc').textContent='Bạn đã hạ '+score+' zombie. Thử lại nào!';
  $('start').textContent='CHƠI LẠI';
  $('overlay').classList.remove('hide');
 }
}
function update(dt){
 time+=dt;spawn-=dt;
 if(spawn<=0&&zombies.filter(z=>!z.dead).length<Math.min(14,3+Math.floor(score/2))){
  makeZombie();spawn=Math.max(.65,2-score*.03);
 }
 let x=(keys.right?1:0)-(keys.left?1:0);
 let y=(keys.down?1:0)-(keys.up?1:0),d=Math.hypot(x,y);
 if(d){
  x/=d;y/=d;p.fx=x;p.fy=y;
  p.x+=x*220*dt;p.y+=y*220*dt;p.walk+=dt*12;
 }else p.walk+=dt*3;
 p.x=clamp(p.x,18,w-18);p.y=clamp(p.y,95,h-25);
 p.attack=Math.max(0,p.attack-dt);
 p.cool=Math.max(0,p.cool-dt);p.inv=Math.max(0,p.inv-dt);
 for(let z of zombies){
  if(z.dead){z.fade-=dt;continue}
  z.flash=Math.max(0,z.flash-dt);z.cool-=dt;z.walk+=dt*7;
  let dx=p.x-z.x,dy=p.y-z.y,d=Math.hypot(dx,dy)||1;
  z.fx=dx/d;z.fy=dy/d;
  if(d>31){z.x+=z.fx*z.speed*dt;z.y+=z.fy*z.speed*dt}
  if(d<37&&z.cool<=0){z.cool=1;hurt(z)}
 }
 zombies=zombies.filter(z=>!z.dead||z.fade>0);
 for(let a of particles){
  a.life-=dt;a.vy+=260*dt;a.x+=a.vx*dt;a.y+=a.vy*dt;
  a.vx*=Math.pow(.2,dt);
 }
 particles=particles.filter(a=>a.life>0);
 for(let a of texts){a.life-=dt;a.y-=30*dt}
 texts=texts.filter(a=>a.life>0);
 hud();
}
function background(){
 let gr=g.createLinearGradient(0,0,0,h);
 gr.addColorStop(0,'#132938');gr.addColorStop(.65,'#30433d');gr.addColorStop(1,'#172322');
 g.fillStyle=gr;g.fillRect(0,0,w,h);
 g.fillStyle='#0c1923';
 for(let x=0;x<w;x+=55){
  let bh=30+(Math.sin(x*3)*.5+.5)*55;
  g.fillRect(x,90-bh,35,bh);
 }
 g.strokeStyle='#ffffff0b';g.lineWidth=1;
 for(let x=0;x<w;x+=48){g.beginPath();g.moveTo(x,90);g.lineTo(x,h);g.stroke()}
 for(let y=110;y<h;y+=48){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke()}
}
function drawPlayer(){
 let x=p.x,y=p.y+Math.sin(p.walk)*1.5,sw=Math.sin(p.walk)*7;
 g.save();g.translate(x,y);
 g.fillStyle='#0005';g.beginPath();g.ellipse(0,19,19,5,0,0,7);g.fill();
 if(p.inv>0&&Math.floor(p.inv*20)%2===0)g.globalAlpha=.4;
 const skin='#edf5f5',dark='#17242c';
 line(-2,4,-6+sw,14,5,dark);line(-6+sw,14,-10+sw,21,4,skin);
 line(2,4,6-sw,14,5,dark);line(6-sw,14,10-sw,21,4,skin);
 line(0,-7,0,7,6,dark);line(0,-7,0,7,3,skin);
 circle(0,-15,8,skin);circle(p.fx*3,-16+p.fy,1.5,dark);
 line(0,-5,-8+sw*.5,0,5,dark);
 line(-8+sw*.5,0,-12,5,4,skin);
 let a=Math.atan2(p.fy,p.fx);
 if(p.attack>0)a-=Math.sin((.3-p.attack)/.3*Math.PI)*1.7;
 let hx=8+p.fx*4,hy=-2+p.fy*5;
 line(0,-5,hx,hy,5,dark);circle(hx,hy,2.5,skin);
 g.save();g.translate(hx,hy);g.rotate(a);
 line(0,0,8,0,3,'#79502d');line(0,-4,0,4,2,'#e4c879');
 g.beginPath();g.moveTo(7,-2);g.lineTo(27,0);g.lineTo(7,2);g.closePath();
 g.fillStyle='#e7f4f8';g.fill();g.strokeStyle='#819aa6';g.stroke();
 g.restore();
 if(p.attack>0){
  g.globalAlpha=.5*p.attack/.3;g.strokeStyle='#fff';g.lineWidth=4;
  g.beginPath();g.arc(0,0,40,a-.8,a+.65);g.stroke();
 }
 g.restore();
}
function drawZombie(z){
 let x=z.x,y=z.y+Math.sin(z.walk)*2,sw=Math.sin(z.walk)*5;
 g.save();g.translate(x,y);
 g.fillStyle='#0005';g.beginPath();g.ellipse(0,18,18,5,0,0,7);g.fill();
 let skin=z.flash?'#ffaaa0':'#83a06e',shirt=z.flash?'#ffd0c6':'#435d4b',dark='#253c33';
 line(-4,4,-7+sw,14,5,dark);line(-7+sw,14,-11+sw,21,4,skin);
 line(4,4,7-sw,14,5,dark);line(7-sw,14,12-sw,20,4,skin);
 g.fillStyle=shirt;g.beginPath();g.moveTo(-8,-8);g.lineTo(8,-8);g.lineTo(10,7);g.lineTo(3,10);g.lineTo(-9,7);g.closePath();g.fill();
 line(-6,-5,-13,-1,5,dark);line(-13,-1,-16,5,4,skin);
 line(6,-5,13,0,5,dark);line(13,0,16,5,4,skin);
 line(0,-8,0,-12,4,dark);circle(0,-17,8.5,skin);
 g.fillStyle='#28382d';g.beginPath();g.moveTo(-8,-18);g.lineTo(-11,-25);g.lineTo(-4,-22);g.lineTo(-1,-27);g.lineTo(3,-22);g.lineTo(8,-25);g.lineTo(8,-17);g.fill();
 circle(-3,-18,2.2,'#e3ff91');circle(3,-18,2.2,'#e3ff91');
 line(-4,-12,4,-12,2,'#442929');
 g.restore();
 // health bar above head
 let bw=40,bx=x-bw/2,by=y-38;
 g.fillStyle='#101716';g.fillRect(bx-1,by-1,bw+2,7);
 g.fillStyle='#753a3b';g.fillRect(bx,by,bw,5);
 g.fillStyle=z.hp/z.max>.4?'#a9ef68':'#ff584e';
 g.fillRect(bx,by,bw*clamp(z.hp/z.max,0,1),5);
}
function draw(){
 background();
 let actors=[...zombies.filter(z=>!z.dead).map(z=>({y:z.y,z})),{y:p.y,p:true}].sort((a,b)=>a.y-b.y);
 for(let a of actors){if(a.p)drawPlayer();else drawZombie(a.z)}
 for(let a of particles){g.globalAlpha=clamp(a.life/.65,0,1);circle(a.x,a.y,a.size,a.color)}
 g.globalAlpha=1;
 for(let a of texts){
  g.globalAlpha=clamp(a.life/.8,0,1);g.font='bold 15px Arial';g.textAlign='center';
  g.lineWidth=3;g.strokeStyle='#111';g.strokeText(a.s,a.x,a.y);
  g.fillStyle=a.color;g.fillText(a.s,a.x,a.y);
 }
 g.globalAlpha=1;
}
function loop(t){
 let dt=Math.min(.035,(t-last)/1000||0);last=t;
 if(state==='play')update(dt);draw();requestAnimationFrame(loop);
}
function begin(){
 reset();state='play';$('overlay').classList.add('hide');
}
$('start').addEventListener('click',begin);
function set(k,v){keys[k]=v}
addEventListener('keydown',e=>{
 let k=e.key.toLowerCase();
 if(['arrowup','arrowdown','arrowleft','arrowright',' ','w','a','s','d'].includes(k))e.preventDefault();
 if(k==='w'||k==='arrowup')set('up',true);
 if(k==='s'||k==='arrowdown')set('down',true);
 if(k==='a'||k==='arrowleft')set('left',true);
 if(k==='d'||k==='arrowright')set('right',true);
 if(k===' '||k==='j')attack();
});
addEventListener('keyup',e=>{
 let k=e.key.toLowerCase();
 if(k==='w'||k==='arrowup')set('up',false);
 if(k==='s'||k==='arrowdown')set('down',false);
 if(k==='a'||k==='arrowleft')set('left',false);
 if(k==='d'||k==='arrowright')set('right',false);
});
addEventListener('blur',()=>keys={});
function hold(id,k){
 let b=$(id);
 b.addEventListener('pointerdown',e=>{
  e.preventDefault();set(k,true);b.classList.add('pressed');
  try{b.setPointerCapture(e.pointerId)}catch(_){}
 });
 let off=e=>{set(k,false);b.classList.remove('pressed')};
 b.addEventListener('pointerup',off);b.addEventListener('pointercancel',off);
 b.addEventListener('lostpointercapture',off);
}
hold('up','up');hold('down','down');hold('left','left');hold('right','right');
$('hit').addEventListener('pointerdown',e=>{e.preventDefault();attack();$('hit').classList.add('pressed')});
['pointerup','pointercancel','lostpointercapture'].forEach(ev=>$('hit').addEventListener(ev,()=>$('hit').classList.remove('pressed')));
resize();
p={x:w/2,y:h/2,hp:100,fx:1,fy:0,walk:0,attack:0,cool:0,inv:0};
requestAnimationFrame(loop);
})();
</script>
</body>
</html>
