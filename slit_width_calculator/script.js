document.addEventListener('DOMContentLoaded', () => {
    // --- 1. UI Elements & State ---
    const calculateBtn = document.getElementById('calculate-btn');
    const resultsContainer = document.getElementById('results-container');
    const resultsBody = document.getElementById('results-body');
    const wInput = document.getElementById('wavelength');
    const colorIndicator = document.getElementById('color-indicator');
    const collapsibleCard = document.querySelector('.collapsible-card');
    const graphHeader = document.getElementById('graph-header');
    
    let chartInstance = null;

    // --- 2. Particle Background System ---
    const initParticles = () => {
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouse = { x: -100, y: -100 };

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };

        window.addEventListener('resize', resize);
        resize();

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        class Particle {
            constructor() {
                this.reset();
            }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.homeX = this.x;
                this.homeY = this.y;
                this.vx = (Math.random() - 0.5) * 0.2;
                this.vy = (Math.random() - 0.5) * 0.2;
                this.size = Math.random() * 2 + 1;
                this.baseOpacity = Math.random() * 0.5 + 0.1;
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;

                // Infinite screen loop
                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;
                if (this.y < 0) this.y = canvas.height;
                if (this.y > canvas.height) this.y = 0;

                // Mouse interaction - Smoother repulsion
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 200) {
                    const force = Math.pow((200 - dist) / 200, 2);
                    this.vx -= dx * force * 0.015;
                    this.vy -= dy * force * 0.015;
                }

                // Home seeking - gentle spring force
                const dhx = this.homeX - this.x;
                const dhy = this.homeY - this.y;
                this.vx += dhx * 0.005;
                this.vy += dhy * 0.005;

                // Friction - balanced for smoothness
                this.vx *= 0.94;
                this.vy *= 0.94;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(190, 100%, 50%, ${this.baseOpacity + 0.2})`;
                ctx.fill();
            }
        }

        for (let i = 0; i < 200; i++) particles.push(new Particle());

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        };
        animate();
    };
    initParticles();

    // --- 3. Wavelength to Color Helper ---
    function wavelengthToColor(wavelengthNm) {
        let R = 0, G = 0, B = 0, alpha = 1;
        let wl = wavelengthNm;
        
        if (wl >= 380 && wl < 440) {
            R = -(wl - 440) / (440 - 380);
            B = 1.0;
        } else if (wl >= 440 && wl < 490) {
            G = (wl - 440) / (490 - 440);
            B = 1.0;
        } else if (wl >= 490 && wl < 510) {
            G = 1.0;
            B = -(wl - 510) / (510 - 490);
        } else if (wl >= 510 && wl < 580) {
            R = (wl - 510) / (580 - 510);
            G = 1.0;
        } else if (wl >= 580 && wl < 645) {
            R = 1.0;
            G = -(wl - 645) / (645 - 580);
        } else if (wl >= 645 && wl <= 780) {
            R = 1.0;
        }

        if (wl >= 380 && wl < 420) alpha = 0.3 + 0.7 * (wl - 380) / (420 - 380);
        else if (wl >= 420 && wl < 701) alpha = 1.0;
        else if (wl >= 701 && wl <= 780) alpha = 0.3 + 0.7 * (780 - wl) / (780 - 700);
        else { alpha = 0.0; R = 1; G = 1; B = 1; }

        return {
            r: Math.round(R * 255),
            g: Math.round(G * 255),
            b: Math.round(B * 255),
            a: Math.max(0.1, alpha),
            toString: function() { return `rgba(${this.r}, ${this.g}, ${this.b}, ${this.a})`; }
        };
    }

    function updateColorIndicator() {
        const wl = parseFloat(wInput.value) || 532;
        const color = wavelengthToColor(wl);
        colorIndicator.style.backgroundColor = color.toString();
        colorIndicator.style.boxShadow = `0 0 20px ${color.toString()}`;
    }

    wInput.addEventListener('input', updateColorIndicator);
    updateColorIndicator();

    // --- 4. Core Calculations ---
    calculateBtn.addEventListener('click', () => {
        calculateSlitWidth();
        // Reveal graph automatically on first calculation
        if (!collapsibleCard.classList.contains('active')) {
            collapsibleCard.classList.add('active');
        }
    });
    
    // Initial calculation
    calculateSlitWidth();

    function calculateSlitWidth() {
        const centralWidthCm = parseFloat(document.getElementById('central-width').value);
        const distanceCm = parseFloat(document.getElementById('distance').value);
        const wavelengthNm = parseFloat(document.getElementById('wavelength').value);

        if (isNaN(centralWidthCm) || isNaN(distanceCm) || isNaN(wavelengthNm)) {
            return;
        }

        const centralWidthM = centralWidthCm / 100;
        const distanceM = distanceCm / 100;
        const wavelengthM = wavelengthNm * 1e-9;
        const slitWidthM = (2 * wavelengthM * distanceM) / centralWidthM;
        const slitWidthMm = slitWidthM * 1000;
        const slitWidthUm = slitWidthM * 1e6;

        function formatScientific(num) {
            let [base, exponent] = num.toExponential(6).split('e');
            if (!exponent.startsWith('-')) exponent = '+' + exponent.replace('+', '').padStart(2, '0');
            else exponent = '-' + exponent.replace('-', '').padStart(2, '0');
            return `${base}e${exponent}`;
        }

        resultsBody.innerHTML = `
            <tr><td>Central Width (m)</td><td>${formatScientific(centralWidthM)}</td></tr>
            <tr><td>Distance (m)</td><td>${formatScientific(distanceM)}</td></tr>
            <tr><td>Wavelength (m)</td><td>${formatScientific(wavelengthM)}</td></tr>
            <tr><td>Slit Width (m)</td><td>${formatScientific(slitWidthM)}</td></tr>
            <tr><td>Slit Width (mm)</td><td>${formatScientific(slitWidthMm)}</td></tr>
            <tr><td>Slit Width (μm)</td><td>${formatScientific(slitWidthUm)}</td></tr>
        `;
        
        let distanceHtml = "";
        for (let L = 0.3; L <= 3.05; L += 0.3) {
            const W_m = (2 * wavelengthM * L) / slitWidthM;
            const W_mm = W_m * 1000;
            distanceHtml += `<tr><td>${L.toFixed(1)}</td><td>${W_mm.toFixed(1)}</td></tr>`;
        }
        document.getElementById('distance-body').innerHTML = distanceHtml;

        resultsContainer.style.display = 'block';
        
        const displayColor = wavelengthToColor(wavelengthNm);
        render1DDiffraction(wavelengthM, slitWidthM, displayColor);
        renderLineChart(centralWidthM, distanceM, wavelengthM, slitWidthM, displayColor);
    }

    // --- 5. Visual Rendering ---
    function render1DDiffraction(lambda_m, a_m, colorObj) {
        const canvas = document.getElementById('diffraction-visual');
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, width, height);
        
        const imgData = ctx.createImageData(width, height);
        const data = imgData.data;

        for (let x = 0; x < width; x++) {
            const theta = -Math.PI/2 + (x / width) * Math.PI;
            let intensity;
            if (Math.abs(theta) < 1e-10) {
                intensity = 1.0;
            } else {
                const beta = (Math.PI * a_m / lambda_m) * Math.sin(theta);
                intensity = Math.pow(Math.sin(beta) / beta, 2);
            }

            let visualIntensity = Math.pow(intensity, 0.4);
            const iA = visualIntensity * colorObj.a;

            for (let y = 0; y < height; y++) {
                const index = (y * width + x) * 4;
                const isPeak = intensity > 0.95;
                data[index + 0] = isPeak ? Math.min(255, colorObj.r + 150) : colorObj.r * iA;
                data[index + 1] = isPeak ? Math.min(255, colorObj.g + 150) : colorObj.g * iA;
                data[index + 2] = isPeak ? Math.min(255, colorObj.b + 150) : colorObj.b * iA;
                data[index + 3] = 255;
            }
        }
        ctx.putImageData(imgData, 0, 0);
    }

    function renderLineChart(W_m, L_m, lambda_m, a_m, baseColor) {
        const canvas = document.getElementById('diffraction-chart');
        const ctx = canvas.getContext('2d');
        const dataPoints = [];
        const labels = [];
        
        for (let L = 0.3; L <= 3.05; L += 0.3) {
            labels.push(L.toFixed(1));
            const W_current_m = (2 * lambda_m * L) / a_m;
            dataPoints.push(W_current_m * 1000);
        }
        
        if (chartInstance) chartInstance.destroy();
        
        const color = baseColor.toString();
        const glowColor = `rgba(${baseColor.r}, ${baseColor.g}, ${baseColor.b}, 0.2)`;

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Central Fringe Width (mm)',
                    data: dataPoints,
                    borderColor: color,
                    backgroundColor: glowColor,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 8,
                    pointBackgroundColor: color,
                    pointBorderColor: '#fff',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: color,
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Distance (m)', color: '#94a3b8', font: { family: 'Outfit', size: 12 } },
                        ticks: { color: '#64748b' },
                        grid: { color: 'rgba(255,255,255,0.05)' }
                    },
                    y: {
                        title: { display: true, text: 'Width (mm)', color: '#94a3b8', font: { family: 'Outfit', size: 12 } },
                        ticks: { color: '#64748b' },
                        grid: { color: 'rgba(255,255,255,0.05)' }
                    }
                }
            }
        });
    }

    // --- 6. Interactivity ---
    graphHeader.addEventListener('click', () => {
        collapsibleCard.classList.toggle('active');
    });
});
