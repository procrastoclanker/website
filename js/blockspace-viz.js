// Blockspace Visualization
// Transactions fall from the sky into the current block. Block fills, appends to chain.
(function() {
  var canvas = document.getElementById('blockspace-canvas');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dpr = window.devicePixelRatio || 1;
  var W, H;
  var mono = 'JetBrains Mono, monospace';
  var CYCLE = 12000;
  var startTime = performance.now();
  var txns = [];
  var chainBlocks = [];
  var blockNum = 9907;
  var cycleCount = 0;

  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    W = rect.width;
    H = rect.height;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function ease(t) { return t < 0.5 ? 2*t*t : -1+(4-2*t)*t; }

  function draw(now) {
    if (!animating) return;

    var elapsed = (now - startTime) % CYCLE;
    var progress = elapsed / CYCLE;

    var currentCycle = Math.floor((now - startTime) / CYCLE);
    if (currentCycle > cycleCount) {
      chainBlocks.unshift({ num: blockNum, slideT: now });
      blockNum++;
      cycleCount = currentCycle;
      // Keep max 4 chain blocks, reset blockNum to prevent unbounded growth
      if (chainBlocks.length > 4) {
        chainBlocks.pop();
        blockNum = 9907 + chainBlocks.length + 1;
      }
      txns = [];
    }

    ctx.clearRect(0, 0, W, H);

    var blockW = Math.min(90, W * 0.15);
    var blockH = Math.min(70, H * 0.35);
    var curX = W * 0.65;
    var chainY = H * 0.55;
    var gap = blockW * 0.35;

    // -- Chain blocks (left of current)
    for (var c = 0; c < chainBlocks.length; c++) {
      var cb = chainBlocks[c];
      var slideAge = now - cb.slideT;
      var sp = ease(Math.min(1, slideAge / 600));
      var targetX = curX - (c + 1) * (blockW + gap);
      var bx = targetX + (blockW + gap) * (1 - sp);
      if (slideAge >= 600) bx = targetX;
      if (bx + blockW/2 < -10) continue;

      var age = Math.min(1, slideAge / 3000);
      var alpha = 0.6 - age * 0.4;

      ctx.strokeStyle = 'rgba(255,255,255,' + alpha + ')';
      ctx.lineWidth = 1;
      ctx.strokeRect(bx - blockW/2, chainY - blockH/2, blockW, blockH);

      ctx.fillStyle = 'rgba(255,255,255,' + alpha * 0.04 + ')';
      ctx.fillRect(bx - blockW/2 + 1, chainY - blockH/2 + 1, blockW - 2, blockH - 2);

      ctx.font = '9px ' + mono;
      ctx.textAlign = 'center';
      ctx.fillStyle = 'rgba(255,255,255,' + alpha * 0.8 + ')';
      ctx.fillText('#' + cb.num, bx, chainY + 3);

      // Arrow to next
      var arrowTo = c === 0 ? curX - blockW/2 : targetX + blockW + gap - blockW/2;
      var arrowFrom = bx + blockW/2;
      if (arrowTo - arrowFrom > 10) {
        ctx.beginPath();
        ctx.moveTo(arrowFrom + 4, chainY);
        ctx.lineTo(arrowTo - 4, chainY);
        ctx.strokeStyle = 'rgba(255,255,255,' + alpha * 0.3 + ')';
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(arrowTo - 8, chainY - 3);
        ctx.lineTo(arrowTo - 4, chainY);
        ctx.lineTo(arrowTo - 8, chainY + 3);
        ctx.stroke();
      }
    }

    // -- Current block
    var fillLevel = Math.min(1, progress / 0.82);
    var blockAlpha = 0.5 + fillLevel * 0.5;

    ctx.strokeStyle = 'rgba(255,255,255,' + blockAlpha + ')';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(curX - blockW/2, chainY - blockH/2, blockW, blockH);

    var fillH = (blockH - 2) * fillLevel;
    ctx.fillStyle = 'rgba(255,255,255,' + fillLevel * 0.06 + ')';
    ctx.fillRect(curX - blockW/2 + 1, chainY + blockH/2 - fillH - 1, blockW - 2, fillH);

    ctx.font = '10px ' + mono;
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(255,255,255,' + blockAlpha + ')';
    ctx.fillText('#' + blockNum, curX, chainY - 2);

    var txCount = Math.floor(fillLevel * 200);
    ctx.font = '9px ' + mono;
    ctx.fillStyle = 'rgba(255,255,255,' + blockAlpha * 0.6 + ')';
    ctx.fillText(txCount + ' txns', curX, chainY + 12);

    // "blockspace" label
    ctx.font = '9px ' + mono;
    ctx.fillStyle = 'rgba(255,255,255,' + Math.min(fillLevel, 0.45) + ')';
    ctx.fillText('blockspace', curX, chainY + blockH/2 + 16);

    // -- Transactions falling from above into the block
    var blockLeft = curX - blockW/2;
    var blockRight = curX + blockW/2;
    var blockTop = chainY - blockH/2;

    if (progress < 0.85 && Math.random() < 0.2 + progress * 0.15) {
      txns.push({
        born: now,
        duration: 900 + Math.random() * 700,
        x: blockLeft + 6 + Math.random() * (blockW - 12),
        sy: -5 - Math.random() * 20,
        ty: blockTop + 4 + Math.random() * (fillH > 4 ? fillH - 4 : blockH * 0.3),
        opacity: 0.3 + Math.random() * 0.35
      });
    }

    for (var i = txns.length - 1; i >= 0; i--) {
      var tx = txns[i];
      var age = now - tx.born;
      var t = Math.min(1, age / tx.duration);

      if (t >= 1) { txns.splice(i, 1); continue; }

      var et = ease(t);
      var y = tx.sy + (tx.ty - tx.sy) * et;

      var alpha2 = tx.opacity;
      if (t < 0.12) alpha2 *= t / 0.12;
      if (t > 0.85) alpha2 *= (1 - t) / 0.15;

      ctx.beginPath();
      ctx.arc(tx.x, y, 2, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,' + alpha2 + ')';
      ctx.fill();
    }

    // -- Timer bar at bottom
    var timerY = H - 20;
    var barW = W * 0.5;
    var barX = (W - barW) / 2;
    var sec = elapsed / 1000;

    // Track background
    ctx.fillStyle = 'rgba(255,255,255,0.06)';
    ctx.fillRect(barX, timerY, barW, 3);

    // Progress fill
    ctx.fillStyle = 'rgba(255,255,255,0.25)';
    ctx.fillRect(barX, timerY, barW * progress, 3);

    // Time label
    ctx.font = '10px ' + mono;
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(255,255,255,0.45)';
    ctx.fillText(sec.toFixed(1) + 's / 12s', W / 2, timerY - 6);

    requestAnimationFrame(draw);
  }

  function initChain() {
    // Start with 3 blocks already in the chain so it never looks empty
    blockNum = 9907;
    var now = performance.now();
    chainBlocks = [
      { num: blockNum - 1, slideT: now - 5000 },
      { num: blockNum - 2, slideT: now - 5000 },
      { num: blockNum - 3, slideT: now - 5000 },
    ];
    cycleCount = 0;
    txns = [];
  }

  var animating = false;
  var observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting && !animating) {
      animating = true;
      startTime = performance.now();
      initChain();
      resize();
      requestAnimationFrame(draw);
    } else if (!entries[0].isIntersecting) {
      animating = false;
    }
  }, { threshold: 0.1 });

  resize();
  window.addEventListener('resize', resize);
  observer.observe(canvas);
})();
