// Pipeline Animation
// Full 12-second cycle with clear stage labels and annotations
(function() {
  var canvas = document.getElementById('pipeline-canvas');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var dpr = window.devicePixelRatio || 1;
  var W, H;
  var mono = 'JetBrains Mono, monospace';
  var CYCLE = 12000;
  var startTime = performance.now();

  var userTxns = [];
  var bundles = [];
  var bids = [];
  var bidCount = 0;

  // Stage positions (fraction of width)
  var SX = {
    users:     0.06,
    searchers: 0.24,
    builders:  0.44,
    relay:     0.64,
    validator: 0.80,
    chain:     0.94
  };

  // Vertical positions
  var nodeYs = { searchers: [], builders: [] };

  function resize() {
    var rect = canvas.parentElement.getBoundingClientRect();
    W = rect.width;
    H = rect.height;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    var cy = H * 0.52;
    nodeYs.searchers = [cy - 16, cy + 16];
    nodeYs.builders = [cy - 24, cy, cy + 24];
  }

  function ease(t) { return t * (2 - t); }

  function drawStageLabel(text, x, y, alpha) {
    ctx.font = '10px ' + mono;
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(255,255,255,' + alpha + ')';
    ctx.fillText(text, x, y);
  }

  function drawAnnotation(text, x, y, alpha) {
    ctx.font = '8px ' + mono;
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(255,255,255,' + alpha + ')';
    ctx.fillText(text, x, y);
  }

  function drawNode(x, y, r, alpha) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255,255,255,' + alpha + ')';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  function drawArrowZone(x1, x2, y, alpha) {
    // Subtle dashed line between stages
    ctx.setLineDash([3, 4]);
    ctx.beginPath();
    ctx.moveTo(x1, y);
    ctx.lineTo(x2, y);
    ctx.strokeStyle = 'rgba(255,255,255,' + alpha + ')';
    ctx.lineWidth = 0.5;
    ctx.stroke();
    ctx.setLineDash([]);
    // Arrowhead
    ctx.beginPath();
    ctx.moveTo(x2 - 5, y - 3);
    ctx.lineTo(x2, y);
    ctx.lineTo(x2 - 5, y + 3);
    ctx.strokeStyle = 'rgba(255,255,255,' + alpha + ')';
    ctx.lineWidth = 0.8;
    ctx.stroke();
  }

  function updateParticles(arr, now) {
    for (var i = arr.length - 1; i >= 0; i--) {
      var p = arr[i];
      var t = Math.min(1, (now - p.born) / p.duration);
      if (t >= 1) { arr.splice(i, 1); continue; }
      var et = ease(t);
      var x = p.sx + (p.tx - p.sx) * et;
      var y = p.sy + (p.ty - p.sy) * et;
      var alpha = p.opacity;
      if (t < 0.1) alpha *= t / 0.1;
      if (t > 0.8) alpha *= (1 - t) / 0.2;
      ctx.beginPath();
      ctx.arc(x, y, p.size || 1.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,' + alpha + ')';
      ctx.fill();
    }
  }

  function draw(now) {
    if (!animating) return;
    var elapsed = (now - startTime) % CYCLE;
    var progress = elapsed / CYCLE;
    var cy = H * 0.52;

    ctx.clearRect(0, 0, W, H);

    // -- Spawn particles by phase

    // Users -> Searchers (throughout)
    if (progress < 0.88 && Math.random() < 0.35) {
      var sIdx = Math.floor(Math.random() * 2);
      userTxns.push({
        born: now, duration: 600 + Math.random() * 400,
        sx: W * SX.users + Math.random() * 10,
        sy: cy + (Math.random() - 0.5) * 50,
        tx: W * SX.searchers - 8,
        ty: nodeYs.searchers[sIdx] + (Math.random() - 0.5) * 8,
        opacity: 0.3 + Math.random() * 0.3,
        size: 1.5
      });
    }

    // Searchers -> Builders (after 5%)
    if (progress > 0.05 && progress < 0.85 && Math.random() < 0.12 + progress * 0.12) {
      var bIdx = Math.floor(Math.random() * 3);
      bundles.push({
        born: now, duration: 450 + Math.random() * 300,
        sx: W * SX.searchers + 8,
        sy: nodeYs.searchers[Math.floor(Math.random() * 2)],
        tx: W * SX.builders - 8,
        ty: nodeYs.builders[bIdx] + (Math.random() - 0.5) * 6,
        opacity: 0.35 + Math.random() * 0.3,
        size: 2.5
      });
    }

    // Builders -> Relay (ramping hard)
    var bidRate;
    if (progress < 0.1) bidRate = 0.02;
    else if (progress < 0.4) bidRate = 0.06 + progress * 0.2;
    else if (progress < 0.75) bidRate = 0.15 + (progress - 0.4) * 0.6;
    else if (progress < 0.9) bidRate = 0.4 + (progress - 0.75) * 2.5;
    else bidRate = 0;

    if (Math.random() < bidRate) {
      var fromB = Math.floor(Math.random() * 3);
      bids.push({
        born: now, duration: 350 + Math.random() * 350,
        sx: W * SX.builders + 8,
        sy: nodeYs.builders[fromB] + (Math.random() - 0.5) * 8,
        tx: W * SX.relay,
        ty: cy + (Math.random() - 0.5) * 12,
        opacity: 0.25 + Math.random() * 0.3,
        size: 1.5
      });
      // Each visible particle represents a burst of bids
      bidCount += 8 + Math.floor(Math.random() * 12);
    }

    // -- Draw wallet icon (source of user txns)
    var walletX = W * SX.users + 5;
    var walletY = cy;
    var ww = 16, wh = 12;
    ctx.strokeStyle = 'rgba(255,255,255,0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(walletX - ww/2, walletY - wh/2, ww, wh);
    // Wallet flap
    ctx.beginPath();
    ctx.moveTo(walletX - ww/2, walletY - wh/2);
    ctx.lineTo(walletX - ww/2 + 4, walletY - wh/2 - 4);
    ctx.lineTo(walletX + ww/2 - 2, walletY - wh/2 - 4);
    ctx.lineTo(walletX + ww/2, walletY - wh/2);
    ctx.strokeStyle = 'rgba(255,255,255,0.4)';
    ctx.stroke();

    // -- Draw stage flow arrows (background)
    var arrowAlpha = 0.08;
    var arrowY = cy;
    drawArrowZone(W * SX.users + 15, W * SX.searchers - 12, arrowY, arrowAlpha);
    drawArrowZone(W * SX.searchers + 12, W * SX.builders - 12, arrowY, arrowAlpha);
    drawArrowZone(W * SX.builders + 12, W * SX.relay - 18, arrowY, arrowAlpha);
    drawArrowZone(W * SX.relay + 18, W * SX.validator - 14, arrowY, arrowAlpha);
    drawArrowZone(W * SX.validator + 14, W * SX.chain - 20, arrowY, arrowAlpha);

    // -- Draw stage labels (top)
    var labelY = H * 0.12;
    drawStageLabel('users', W * SX.users + 5, labelY, 0.55);
    drawStageLabel('searchers', W * SX.searchers, labelY, 0.55);
    drawStageLabel('builders', W * SX.builders, labelY, 0.55);
    drawStageLabel('relay', W * SX.relay, labelY, 0.55);
    drawStageLabel('validator', W * SX.validator, labelY, 0.55);

    // -- Draw annotation descriptions (below labels)
    var descY = labelY + 14;
    drawAnnotation('submit txns', W * SX.users + 5, descY, 0.25);
    drawAnnotation('bundle txns', W * SX.searchers, descY, 0.25);
    drawAnnotation('build blocks', W * SX.builders, descY, 0.25);
    drawAnnotation('select best', W * SX.relay, descY, 0.25);
    drawAnnotation('propose', W * SX.validator, descY, 0.25);

    // -- Draw searcher nodes
    for (var s = 0; s < nodeYs.searchers.length; s++) {
      drawNode(W * SX.searchers, nodeYs.searchers[s], 5, 0.35);
    }

    // -- Draw builder nodes
    for (var b = 0; b < nodeYs.builders.length; b++) {
      drawNode(W * SX.builders, nodeYs.builders[b], 5, 0.35);
    }

    // -- Draw relay (glows with activity)
    var relayGlow = Math.min(0.4, bidCount * 0.00004);
    var relayR = 14 + relayGlow * 8;
    var relayX = W * SX.relay;

    if (relayGlow > 0.05) {
      var grad = ctx.createRadialGradient(relayX, cy, relayR, relayX, cy, relayR + 20);
      grad.addColorStop(0, 'rgba(255,255,255,' + relayGlow * 0.15 + ')');
      grad.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.beginPath();
      ctx.arc(relayX, cy, relayR + 20, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
    }
    drawNode(relayX, cy, relayR, 0.45 + relayGlow);

    // -- Draw validator
    var valX = W * SX.validator;
    drawNode(valX, cy, 9, 0.4);

    // -- Draw particles
    updateParticles(userTxns, now);
    updateParticles(bundles, now);
    updateParticles(bids, now);

    // -- Proposal phase (last 10%)
    var isProposing = progress > 0.9;
    if (isProposing) {
      var pp = (progress - 0.9) / 0.1;

      // Relay -> Validator
      if (pp < 0.5) {
        var lp = pp / 0.5;
        var lx = relayX + relayR + (valX - relayX - relayR - 9) * ease(lp);
        ctx.beginPath();
        ctx.moveTo(relayX + relayR, cy);
        ctx.lineTo(lx, cy);
        ctx.strokeStyle = 'rgba(255,255,255,' + lp * 0.6 + ')';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // Validator -> Chain block
      if (pp > 0.35) {
        var cp = (pp - 0.35) / 0.65;
        var chainX = W * SX.chain;
        var lx2 = valX + 9 + (chainX - 22 - valX - 9) * ease(Math.min(1, cp));
        ctx.beginPath();
        ctx.moveTo(valX + 9, cy);
        ctx.lineTo(lx2, cy);
        ctx.strokeStyle = 'rgba(255,255,255,' + Math.min(1, cp) * 0.5 + ')';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Block
        var ba = Math.min(1, cp * 1.5);
        var bw = 30, bh = 24;
        ctx.strokeStyle = 'rgba(255,255,255,' + ba * 0.8 + ')';
        ctx.lineWidth = ba > 0.5 ? 1.5 : 1;
        ctx.strokeRect(chainX - bw/2, cy - bh/2, bw, bh);

        ctx.font = '8px ' + mono;
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(255,255,255,' + ba * 0.7 + ')';
        ctx.fillText('block', chainX, cy + 3);
      }
    }

    // -- Bottom stats
    var sec = elapsed / 1000;
    ctx.font = '10px ' + mono;
    ctx.fillStyle = 'rgba(255,255,255,0.45)';
    ctx.textAlign = 'left';
    ctx.fillText(sec.toFixed(1) + 's / 12s', 10, H - 12);
    ctx.textAlign = 'right';
    ctx.fillText(bidCount.toLocaleString() + ' builder bids', W - 10, H - 12);

    // -- Reset each cycle
    if (progress < 0.01) {
      userTxns = [];
      bundles = [];
      bids = [];
      bidCount = 0;
    }

    requestAnimationFrame(draw);
  }

  var animating = false;
  var observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting && !animating) {
      animating = true;
      startTime = performance.now();
      userTxns = []; bundles = []; bids = [];
      bidCount = 0;
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
