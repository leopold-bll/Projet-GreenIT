function startGame(questions) {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const sprite = new Image();
    sprite.src = '/static/sprites/hero.png';
    let frame = 0;
    let current = 0;
  
    sprite.onload = () => animate();
  
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const sw = 64, sh = 64; // taille d'un cadre
      const sx = frame * sw;
      ctx.drawImage(sprite, sx, 0, sw, sh, 50 + current * 200, 300, sw, sh);
      requestAnimationFrame(animate);
    }
  
    // changement de question/sprite toutes les 3s
    setInterval(() => {
      current = Math.floor(Math.random() * questions.length);
      frame = (frame + 1) % 4;
    }, 3000);
  }