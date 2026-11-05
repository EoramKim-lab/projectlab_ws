"""Standalone canvas report with time seeking, pause/play and playback speed."""
import json
from pathlib import Path


def save_animation(path, payload):
    # Keep log/model text inside JSON; never insert it into markup as HTML.
    data = json.dumps(payload, allow_nan=False).replace('<', '\\u003c')
    Path(path).write_text(HTML.replace('__FLIGHT_DATA__', data), encoding='utf-8')


HTML = r'''<!doctype html>
<html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flight obstacle playback</title>
<style>
body{font:15px system-ui,sans-serif;margin:24px;background:#f3f5f7;color:#182330}h1{font-size:21px}button,select{font:inherit;padding:7px 12px}button:focus,input:focus,select:focus{outline:2px solid #087cb9}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;background:white;padding:14px;border-radius:10px}input[type=range]{flex:1;min-width:220px}.plots{display:grid;grid-template-columns:1fr 1.5fr;gap:16px;margin-top:16px}canvas{width:100%;background:white;border-radius:10px}p{line-height:1.6}.note{color:#536171;font-size:13px}@media(max-width:850px){.plots{grid-template-columns:1fr}}
</style>
<h1 id="title"></h1>
<div class="controls"><button id="play">재생 ▶</button><button id="reset">처음으로</button><label for="speed">재생 속도</label><select id="speed"><option value="0.25">0.25×</option><option value="0.5">0.5×</option><option selected value="1">1×</option><option value="2">2×</option><option value="4">4×</option><option value="8">8×</option><option value="16">16×</option></select><label for="seek">시간</label><input id="seek" type="range" min="0" step="0.01" value="0"><output id="time"></output></div>
<div class="plots"><canvas id="body" width="720" height="560" aria-label="Body FRD LiDAR"></canvas><canvas id="world" width="1080" height="560" aria-label="Gazebo ENU reference trajectory and obstacles"></canvas></div>
<p>파랑: 비행 궤적 · 초록 점선: 레퍼런스 · 회색: 저장된 월드 장애물 · 주황 원: LiDAR 추정 장애물 · 빨강 점선: 추정 안전 반경</p>
<p class="note" id="note"></p>
<script>
'use strict';
const data=__FLIGHT_DATA__;
const seek=document.getElementById('seek'),play=document.getElementById('play'),speed=document.getElementById('speed');
let t=0,playing=false,last=null;
document.getElementById('title').textContent=data.name;
document.getElementById('note').textContent=data.note;
seek.max=data.duration;
function panel(id,bounds,title,xlabel,ylabel){
 const canvas=document.getElementById(id),ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height;
 ctx.clearRect(0,0,W,H);ctx.fillStyle='#fff';ctx.fillRect(0,0,W,H);
 const [xmin,xmax,ymin,ymax]=bounds,s=Math.min((W-100)/(xmax-xmin),(H-100)/(ymax-ymin)),ox=(W-s*(xmax-xmin))/2,oy=(H-s*(ymax-ymin))/2;
 const point=p=>[ox+(p[0]-xmin)*s,H-oy-(p[1]-ymin)*s];
 ctx.font='17px sans-serif';ctx.fillStyle='#182330';ctx.fillText(title,20,25);ctx.font='13px sans-serif';ctx.fillText(xlabel,W/2-35,H-10);ctx.fillText(ylabel,10,46);
 ctx.strokeStyle='#e5e9ed';ctx.lineWidth=1;
 const step=Math.max(1,Math.ceil((xmax-xmin)/14));
 for(let x=Math.ceil(xmin/step)*step;x<=xmax;x+=step){let a=point([x,ymin]),b=point([x,ymax]);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.fillText(x.toFixed(0),a[0]-5,a[1]+18);}
 for(let y=Math.ceil(ymin);y<=ymax;y++){let a=point([xmin,y]),b=point([xmax,y]);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.fillText(y.toFixed(0),a[0]-30,a[1]+4);}
 ctx.save();ctx.beginPath();ctx.rect(ox,oy,(xmax-xmin)*s,(ymax-ymin)*s);ctx.clip();
 return {ctx,point,s};
}
function line(p,points,color,width=2,dash=[]){if(!points.length)return;p.ctx.strokeStyle=color;p.ctx.lineWidth=width;p.ctx.setLineDash(dash);p.ctx.beginPath();points.forEach((q,i)=>{const a=p.point(q);if(i)p.ctx.lineTo(...a);else p.ctx.moveTo(...a);});p.ctx.stroke();p.ctx.setLineDash([]);}
function dots(p,points,color,size=2){p.ctx.fillStyle=color;for(const q of points){const a=p.point(q);p.ctx.fillRect(a[0]-size/2,a[1]-size/2,size,size);}}
function circle(p,center,r,color,dash=[]){p.ctx.strokeStyle=color;p.ctx.lineWidth=2;p.ctx.setLineDash(dash);p.ctx.beginPath();p.ctx.arc(...p.point(center),r*p.s,0,2*Math.PI);p.ctx.stroke();p.ctx.setLineDash([]);}
function render(){
 let index=0;while(index+1<data.frames.length&&data.frames[index+1].t<=t)index++;
 const f=data.frames[index];seek.value=t;document.getElementById('time').textContent=`${t.toFixed(2)} / ${data.duration.toFixed(2)} s`;
 const body=panel('body',[-8,8,-8,8],`LiDAR (body FRD) — ${f.body.length} points`,'Forward [m]','Right [m]');dots(body,f.body,'#327a9e');dots(body,[[0,0]],'#dc3545',8);body.ctx.restore();
 const world=panel('world',data.bounds,`World ENU — sample ${f.t.toFixed(2)} s, ${f.obstacles.length} detections`,'East [m]','North [m]');
 for(const shape of data.shapes){world.ctx.beginPath();shape.points.forEach((q,i)=>{const a=world.point(q);if(i)world.ctx.lineTo(...a);else world.ctx.moveTo(...a);});world.ctx.closePath();world.ctx.fillStyle='#a7afb8';world.ctx.fill();world.ctx.strokeStyle='#66727f';world.ctx.stroke();}
 for(const segment of data.references)line(world,segment,'#198754',3,[8,5]);
 line(world,data.trajectory.filter(q=>q.t<=t).map(q=>q.xy),'#1278bd',2);
 dots(world,f.world,'#7d8790');
 for(const ob of f.obstacles){circle(world,ob.center,ob.radius,'#ee8510');circle(world,ob.center,ob.safe,'#d34444',[5,4]);}
 if(f.drone)dots(world,[f.drone],'#d62c40',9);
 world.ctx.restore();
}
play.onclick=()=>{if(!playing&&t>=data.duration)t=0;playing=!playing;play.textContent=playing?'일시정지 ❚❚':'재생 ▶';last=null;};
document.getElementById('reset').onclick=()=>{t=0;playing=false;last=null;play.textContent='재생 ▶';render();};
seek.oninput=()=>{t=Number(seek.value);last=null;render();};
function tick(now){if(playing&&last!==null){t=Math.min(data.duration,t+(now-last)/1000*Number(speed.value));render();if(t>=data.duration){playing=false;play.textContent='재생 ▶';}}last=now;requestAnimationFrame(tick);}
render();requestAnimationFrame(tick);
</script></html>'''
