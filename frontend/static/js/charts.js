// Chart.js helpers for dashboard
function createMonthlyChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `$${context.parsed.toLocaleString()}`;
            }
          }
        }
      }
    }
  });
}

function createBalanceChart(canvasId) {
  // Bar chart for balance over time
}

function animateBalance(elementId, value) {
  const el = document.getElementById(elementId);
  const start = 0;
  const duration = 600;
  const startTime = performance.now();
  
  function step(currentTime) {
    const progress = Math.min((currentTime - startTime) / duration, 1);
    el.textContent = `$${(start + progress * value).toFixed(0)}`;
    
    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }
  
  requestAnimationFrame(step);
}

