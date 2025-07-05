const canvas = document.getElementById('bg');
const ctx = canvas.getContext('2d');

let w, h;
let particles = [];

function init() {
  resize();
  for (let i = 0; i < 90; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 2 + 1,
      dx: (Math.random() - 0.5) * 1,
      dy: (Math.random() - 0.5) * 1,
      a: Math.random() * Math.PI * 2
    });
  }
  requestAnimationFrame(update);
}

function resize() {
  w = window.innerWidth;
  h = window.innerHeight;
  canvas.width = w;
  canvas.height = h;
}

function update() {
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#e50914';

  particles.forEach(p => {
    p.x += Math.cos(p.a) * 0.3;
    p.y += Math.sin(p.a) * 0.3;
    p.a += 0.01;

    if (p.x < 0) p.x = w;
    if (p.x > w) p.x = 0;
    if (p.y < 0) p.y = h;
    if (p.y > h) p.y = 0;

    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
  });

  requestAnimationFrame(update);
}

window.addEventListener('resize', resize);
init();
