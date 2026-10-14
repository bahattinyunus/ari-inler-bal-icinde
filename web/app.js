/**
 * 🍯 ari-inler-bal-icinde: İnteraktif Simülasyon, Ses Sentezleyici ve İrfan Antolojisi
 */

// Dahili Yedek Veriler (Statik Dosya Olarak Açıldığında da Çalışması İçin)
const DEFAULT_MATRIX = [
  {
    parametre: "Fail Kimdir?",
    zahir: "Balı arı yapar; emek, maharet ve mülkiyet arınındır.",
    batin: "Bal ilahi kudrettendir; arı yalnızca tecelli tezgâhı ve perdedir.",
    temel: "Enfâl 17 / Pir Sultan Abdal (Tevhid-i Ef'âl) / Spinoza"
  },
  {
    parametre: "İnlemenin Sebebi",
    zahir: "Arı yapışkan bala batmış, kanatları kilitlenmiş, çaresizce acı çekmektedir.",
    batin: "Sonsuz vuslatın lezzetinden sarhoş olmuş, ilahi nefesin vecdiyle mesttir.",
    temel: "Fuzûlî / Mevlânâ (Mesnevî 1-3) / San Juan de la Cruz"
  },
  {
    parametre: "Varlık İlişkisi",
    zahir: "Arı ayrı bir özne, bal ayrı bir nesnedir (Dualizm / Kesret).",
    batin: "Arı balın içinde erimiş, ikilik perdesi yırtılmıştır (Vahdet-i Vücûd / Non-Dualizm).",
    temel: "Niyâzî-i Mısrî (Katrenin Ummân Oluşu) / Chandogya Upanishad (Tat Tvam Asi)"
  },
  {
    parametre: "Sesin Anlamı",
    zahir: "Şikâyet, sızlanma, ölüm korkusu ve acı çığlığı.",
    batin: "Zikir, vecd, hayret ve sonlu kabın taşmasından doğan sır nidası.",
    temel: "İbnü'l-Arabî (Tahayyür) / Şeyh Galip / Meister Eckhart"
  },
  {
    parametre: "Bitiş Noktası",
    zahir: "Yok oluş bir felaket, hezimet ve trajedidir.",
    batin: "Fenâ, ebedi dirilişin (Bekābillâh / Samadhi) yegâne eşiğidir.",
    temel: "Hallâc-ı Mansûr / Ferîdüddîn Attâr (Simurg) / Sri Ramakrishna (Tuz Bebek)"
  }
];

// --- Web Audio Sentezleyici ---
class ZarSesSentezleyici {
  constructor() {
    this.ctx = null;
    this.oscCarrier = null;
    this.oscHarmonic = null;
    this.lfo = null;
    this.filter = null;
    this.gainNode = null;
    this.lfoGain = null;
    this.calisiyor = false;
  }

  baslat() {
    if (this.calisiyor) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    this.ctx = new AudioCtx();

    // Taşıyıcı ve Harmonik Osilatör
    this.oscCarrier = this.ctx.createOscillator();
    this.oscHarmonic = this.ctx.createOscillator();
    this.oscCarrier.type = "sawtooth";
    this.oscHarmonic.type = "sine";

    // Alçak Geçiren Filtre (Viskozite Sönümlemesi)
    this.filter = this.ctx.createBiquadFilter();
    this.filter.type = "lowpass";
    this.filter.frequency.setValueAtTime(1200, this.ctx.currentTime);
    this.filter.Q.setValueAtTime(4.0, this.ctx.currentTime);

    // LFO (Vızıltı / Titreşim Modülasyonu)
    this.lfo = this.ctx.createOscillator();
    this.lfoGain = this.ctx.createGain();
    this.lfo.frequency.setValueAtTime(18.0, this.ctx.currentTime);
    this.lfoGain.gain.setValueAtTime(25.0, this.ctx.currentTime);

    this.lfo.connect(this.lfoGain);
    this.lfoGain.connect(this.oscCarrier.frequency);

    // Ana Ses Kazancı (Gain)
    this.gainNode = this.ctx.createGain();
    this.gainNode.gain.setValueAtTime(0.001, this.ctx.currentTime);
    this.gainNode.gain.exponentialRampToValueAtTime(0.12, this.ctx.currentTime + 0.3);

    // Bağlantılar
    this.oscCarrier.connect(this.filter);
    this.oscHarmonic.connect(this.filter);
    this.filter.connect(this.gainNode);
    this.gainNode.connect(this.ctx.destination);

    this.oscCarrier.start();
    this.oscHarmonic.start();
    this.lfo.start();
    this.calisiyor = true;
  }

  durdur() {
    if (!this.calisiyor || !this.ctx) return;
    this.gainNode.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 0.2);
    setTimeout(() => {
      if (this.ctx) {
        this.ctx.close();
        this.calisiyor = false;
        this.ctx = null;
      }
    }, 250);
  }

  guncelle(frekans, benlikOrani) {
    if (!this.calisiyor || !this.ctx) return;
    const now = this.ctx.currentTime;

    this.oscCarrier.frequency.setTargetAtTime(frekans, now, 0.1);
    this.oscHarmonic.frequency.setTargetAtTime(frekans * 1.618, now, 0.1);

    const filtreHedef = 200 + (benlikOrani * 1400);
    this.filter.frequency.setTargetAtTime(filtreHedef, now, 0.15);

    const lfoHedef = 2.0 + (benlikOrani * 20.0);
    this.lfo.frequency.setTargetAtTime(lfoHedef, now, 0.2);
  }
}

// --- Canvas Animasyonu ve Sıvı Fiziği ---
class HoneySimulationCanvas {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.width = canvas.width;
    this.height = canvas.height;

    this.bee = {
      x: 70,
      y: 70,
      size: 14,
      wingAngle: 0,
      wingSpeed: 0.8,
      alpha: 1.0,
      dissolvedParticles: []
    };

    this.ripples = [];
    this.time = 0;
    this.benlik = 1.0;
    this.viskozite = 1.618;

    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  setBenlik(val) {
    this.benlik = Math.max(0.0, Math.min(1.0, val));
    this.bee.alpha = 0.1 + (this.benlik * 0.9);
    this.bee.wingSpeed = 0.1 + (this.benlik * 0.7);

    if (this.benlik < 0.9 && Math.random() < (1.0 - this.benlik) * 0.7) {
      this.bee.dissolvedParticles.push({
        x: this.bee.x + (Math.random() - 0.5) * 16,
        y: this.bee.y + (Math.random() - 0.5) * 16,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        size: Math.random() * 3 + 1,
        life: 1.0,
        decay: Math.random() * 0.02 + 0.01
      });
    }
  }

  setPos(t) {
    const startX = 70, startY = 70;
    const endX = this.width / 2, endY = this.height / 2;
    this.bee.x = startX + (endX - startX) * t;
    this.bee.y = startY + (endY - startY) * t;

    if (t > 0.4 && Math.random() < 0.15) {
      this.ripples.push({
        x: this.bee.x,
        y: this.bee.y,
        radius: 5,
        maxRadius: 80 + (1.0 - this.benlik) * 120,
        alpha: 0.8
      });
    }
  }

  reset() {
    this.bee.x = 70;
    this.bee.y = 70;
    this.bee.alpha = 1.0;
    this.bee.dissolvedParticles = [];
    this.ripples = [];
    this.benlik = 1.0;
  }

  animate() {
    this.time += 0.03;
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    const centerX = this.width / 2;
    const centerY = this.height / 2;

    const grad = ctx.createRadialGradient(centerX, centerY, 20, centerX, centerY, this.width * 0.6);
    grad.addColorStop(0, "rgba(245, 158, 11, 0.45)");
    grad.addColorStop(0.5, "rgba(180, 83, 9, 0.25)");
    grad.addColorStop(1, "rgba(12, 10, 9, 0.95)");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, this.width, this.height);

    ctx.strokeStyle = "rgba(251, 191, 36, 0.12)";
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 4; i++) {
      ctx.beginPath();
      const r = 50 + i * 35 + Math.sin(this.time + i) * 6;
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    for (let i = this.ripples.length - 1; i >= 0; i--) {
      const rip = this.ripples[i];
      rip.radius += 1.2;
      rip.alpha -= 0.009;
      if (rip.alpha <= 0 || rip.radius >= rip.maxRadius) {
        this.ripples.splice(i, 1);
        continue;
      }
      ctx.beginPath();
      ctx.arc(rip.x, rip.y, rip.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(251, 191, 36, ${rip.alpha * 0.4})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    for (let i = this.bee.dissolvedParticles.length - 1; i >= 0; i--) {
      const p = this.bee.dissolvedParticles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= p.decay;
      if (p.life <= 0) {
        this.bee.dissolvedParticles.splice(i, 1);
        continue;
      }
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(251, 191, 36, ${p.life})`;
      ctx.shadowColor = "#f59e0b";
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    ctx.save();
    ctx.translate(this.bee.x, this.bee.y);
    ctx.globalAlpha = this.bee.alpha;

    this.bee.wingAngle += this.bee.wingSpeed;
    const wingFlap = Math.sin(this.bee.wingAngle) * 0.45;

    ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
    ctx.beginPath();
    ctx.ellipse(-6, -8, 4, 10, -0.4 + wingFlap, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(6, -8, 4, 10, 0.4 - wingFlap, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.ellipse(0, 0, 7, 11, 0, 0, Math.PI * 2);
    ctx.fillStyle = "#fbbf24";
    ctx.fill();
    ctx.strokeStyle = "#1c1917";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-6, -2);
    ctx.lineTo(6, -2);
    ctx.moveTo(-6, 3);
    ctx.lineTo(6, 3);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(0, -9, 4, 0, Math.PI * 2);
    ctx.fillStyle = "#78350f";
    ctx.fill();

    if (this.benlik < 0.6) {
      ctx.beginPath();
      ctx.arc(0, 0, 18, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(245, 158, 11, ${(1.0 - this.benlik) * 0.4})`;
      ctx.fill();
    }

    ctx.restore();
    requestAnimationFrame(this.animate);
  }
}

// --- Ana Uygulama ---
class App {
  constructor() {
    this.canvas = new HoneySimulationCanvas(document.getElementById("honey-canvas"));
    this.audio = new ZarSesSentezleyici();
    this.matrixData = DEFAULT_MATRIX;
    this.corpusData = [];

    this.activeTradition = "all";
    this.activeMotif = "all";
    this.searchTerm = "";

    this.steps = [];
    this.currentStepIdx = 0;
    this.timer = null;

    this.initDOM();
    this.initEvents();
    this.loadData();
  }

  initDOM() {
    this.btnStart = document.getElementById("btn-start");
    this.btnReset = document.getElementById("btn-reset");
    this.btnAudio = document.getElementById("btn-audio");
    this.btnRandomInsight = document.getElementById("btn-random-insight");

    this.badgeMakam = document.getElementById("badge-makam");
    this.zarText = document.getElementById("zar-text");

    this.barBenlik = document.getElementById("bar-benlik");
    this.valBenlik = document.getElementById("val-benlik");
    this.barDirenc = document.getElementById("bar-direnc");
    this.valDirenc = document.getElementById("val-direnc");
    this.barHayret = document.getElementById("bar-hayret");
    this.valHayret = document.getElementById("val-hayret");
    this.valFrekans = document.getElementById("val-frekans");
    this.valKarakter = document.getElementById("val-karakter");

    this.timelineContainer = document.getElementById("steps-timeline");
    this.finalTecelli = document.getElementById("final-tecelli");
    this.tecelliHukum = document.getElementById("tecelli-hukum");
    this.tecelliHal = document.getElementById("tecelli-hal");

    this.rangeViskozite = document.getElementById("range-viskozite");
    this.lblViskozite = document.getElementById("lbl-viskozite");
    this.rangeHiz = document.getElementById("range-hiz");
    this.lblHiz = document.getElementById("lbl-hiz");
    this.inputSalik = document.getElementById("input-salik");

    this.matrixTbody = document.getElementById("matrix-tbody");
    this.corpusGrid = document.getElementById("corpus-grid");
    this.corpusSearch = document.getElementById("corpus-search");

    this.bannerQuote = document.getElementById("contemplation-quote");
    this.bannerAuthor = document.getElementById("contemplation-author");
    this.bannerWork = document.getElementById("contemplation-work");
    this.bannerTradition = document.getElementById("contemplation-tradition");
  }

  initEvents() {
    this.btnStart.addEventListener("click", () => this.startSimulation());
    this.btnReset.addEventListener("click", () => this.resetSimulation());
    this.btnAudio.addEventListener("click", () => this.toggleAudio());
    this.btnRandomInsight.addEventListener("click", () => this.showRandomInsight());

    this.rangeViskozite.addEventListener("input", (e) => {
      this.lblViskozite.textContent = e.target.value;
      this.canvas.viskozite = parseFloat(e.target.value);
    });

    this.rangeHiz.addEventListener("input", (e) => {
      this.lblHiz.textContent = e.target.value;
    });

    this.corpusSearch.addEventListener("input", (e) => {
      this.searchTerm = e.target.value;
      this.renderFilteredCorpus();
    });

    // Matrix Filtre Sekmeleri
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
        e.target.classList.add("active");
        this.renderMatrix(e.target.id);
      });
    });

    // Gelenek Filtre Butonları
    document.querySelectorAll("#tradition-filters .pill").forEach((pill) => {
      pill.addEventListener("click", (e) => {
        document.querySelectorAll("#tradition-filters .pill").forEach((p) => p.classList.remove("active"));
        e.target.classList.add("active");
        this.activeTradition = e.target.getAttribute("data-value");
        this.renderFilteredCorpus();
      });
    });

    // Motif Filtre Butonları
    document.querySelectorAll("#motif-filters .pill").forEach((pill) => {
      pill.addEventListener("click", (e) => {
        document.querySelectorAll("#motif-filters .pill").forEach((p) => p.classList.remove("active"));
        e.target.classList.add("active");
        this.activeMotif = e.target.getAttribute("data-value");
        this.renderFilteredCorpus();
      });
    });
  }

  async loadData() {
    try {
      const mRes = await fetch("/api/matrix");
      if (mRes.ok) this.matrixData = await mRes.json();
    } catch (_) {}

    try {
      const cRes = await fetch("/api/corpus");
      if (cRes.ok) {
        this.corpusData = await cRes.json();
      }
    } catch (_) {}

    this.renderMatrix("tab-all");
    this.renderFilteredCorpus();
    this.showRandomInsight();
  }

  showRandomInsight() {
    if (!this.corpusData || this.corpusData.length === 0) return;
    const item = this.corpusData[Math.floor(Math.random() * this.corpusData.length)];
    this.bannerQuote.textContent = `"${item.orijinal_metin.replace(/\n/g, ' / ')}"`;
    this.bannerAuthor.textContent = item.muellif;
    this.bannerWork.textContent = item.eser;
    this.bannerTradition.textContent = item.gelenek || "İrfan Geleneği";
  }

  renderMatrix(filterId) {
    this.matrixTbody.innerHTML = "";
    this.matrixData.forEach((row) => {
      const tr = document.createElement("tr");

      let zahirStyle = filterId === "tab-batin" ? "opacity: 0.35;" : "";
      let batinStyle = filterId === "tab-zahir" ? "opacity: 0.35;" : "";

      tr.innerHTML = `
        <td><strong>${row.parametre}</strong></td>
        <td class="col-zahir" style="${zahirStyle}">${row.zahir}</td>
        <td class="col-batin" style="${batinStyle}">${row.batin}</td>
        <td><small style="color: var(--text-muted);">${row.temel}</small></td>
      `;
      this.matrixTbody.appendChild(tr);
    });
  }

  renderFilteredCorpus() {
    this.corpusGrid.innerHTML = "";
    const q = (this.searchTerm || "").toLowerCase();

    const filtered = this.corpusData.filter((item) => {
      // Gelenek filtresi
      if (this.activeTradition !== "all" && item.gelenek !== this.activeTradition) {
        return false;
      }
      // Motif filtresi
      if (this.activeMotif !== "all" && item.motif !== this.activeMotif) {
        return false;
      }
      // Metin araması
      if (q) {
        const match =
          item.muellif.toLowerCase().includes(q) ||
          item.eser.toLowerCase().includes(q) ||
          item.orijinal_metin.toLowerCase().includes(q) ||
          item.serh.toLowerCase().includes(q) ||
          (item.gelenek && item.gelenek.toLowerCase().includes(q)) ||
          (item.motif && item.motif.toLowerCase().includes(q)) ||
          item.temalar.some((t) => t.toLowerCase().includes(q));
        if (!match) return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      this.corpusGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 30px;">
          Seçilen kriterlere uygun irfani kayıt bulunamadı.
        </div>
      `;
      return;
    }

    filtered.forEach((item) => {
      const card = document.createElement("div");
      card.className = "corpus-card";
      card.innerHTML = `
        <div class="corpus-header">
          <div class="corpus-author-meta">
            <span class="corpus-author">${item.muellif}</span>
            <span class="corpus-meta">${item.donem} &middot; ${item.eser}</span>
          </div>
          <span class="corpus-motif-badge">${item.motif || "ari-ve-bal"}</span>
        </div>
        <div class="corpus-verse">${item.orijinal_metin}</div>
        <div class="corpus-serh"><strong>Şerh:</strong> ${item.serh}</div>
        <div class="corpus-tags">
          <span class="corpus-tag" style="background: rgba(56, 189, 248, 0.15); color: var(--accent-cyan);">${item.gelenek}</span>
          ${item.temalar.map((t) => `<span class="corpus-tag">#${t}</span>`).join("")}
        </div>
      `;
      this.corpusGrid.appendChild(card);
    });
  }

  toggleAudio() {
    if (!this.audio.calisiyor) {
      this.audio.baslat();
      this.btnAudio.textContent = "🔇 Vecd Sesini Sustur";
      this.btnAudio.classList.add("active");
    } else {
      this.audio.durdur();
      this.btnAudio.textContent = "🔊 Vecd Sesini Aç";
      this.btnAudio.classList.remove("active");
    }
  }

  async startSimulation() {
    this.resetSimulation();
    this.btnStart.disabled = true;

    const salik = this.inputSalik.value || "Derviş / Arı";
    const viskozite = this.rangeViskozite.value;
    const hiz = this.rangeHiz.value;

    try {
      const res = await fetch(`/api/simulate?salik=${encodeURIComponent(salik)}&viskozite=${viskozite}&hiz=${hiz}`);
      if (res.ok) {
        const data = await res.json();
        this.runStepByStep(data.adimlar, data.zar_tecellisi);
        return;
      }
    } catch (_) {}

    this.runLocalSimulation(salik, parseFloat(viskozite), parseFloat(hiz));
  }

  runLocalSimulation(salik, viskozite, hiz) {
    const makamlar = [
      { ad: "Talep (Arayış)", benlik: 1.0, frekans: 440.0, msg: "Balı kendi eseri zanneder." },
      { ad: "Terk-i Dünya", benlik: 0.72, frekans: 380.0, msg: "Maddi bağlılıkların deryada erimesi." },
      { ad: "Terk-i Ukbâ", benlik: 0.48, frekans: 290.0, msg: "Ahiret menfaatinin terk edilmesi." },
      { ad: "Terk-i Hestî", benlik: 0.24, frekans: 195.0, msg: "Varlığın ve egonun çözülüşü." },
      { ad: "Terk-i Terk", benlik: 0.08, frekans: 155.0, msg: "Terk ettiğinin dahi unutulması." },
      { ad: "Fenâfillâh", benlik: 0.0, frekans: 136.1, msg: "Arı balda eridi, ikilik kalktı." },
      { ad: "Bekābillâh", benlik: 0.0, frekans: 136.1, msg: "Hakk ile bâkî kalış, ebedi zâr." }
    ];

    const adimlar = makamlar.map((m, idx) => ({
      adim_no: idx,
      durum: {
        makam: m.ad,
        benlik_orani: m.benlik,
        viskozite_direnci: Math.pow(m.benlik, 1.2),
        hayret_katsayisi: (1.0 - m.benlik) * 4.2,
        rezonans_frekansi: m.frekans,
        ses_karakteri: m.benlik === 0 ? "Vahdet Sükûtu" : "Zâr Uğultusu"
      },
      mesaj: m.msg,
      zar_metni: `Zâr (${m.frekans} Hz): ${m.msg}`
    }));

    const tecelli = {
      hukum: "Kudretten verdi balı / Bahanesi oldu arı / Dinle imdi âh u zârı / Arı inler bal içinde.",
      hal: `'${salik}' artık bağımsız bir fail değildir; Mutlak Kudret deryasında garktır.`
    };

    this.runStepByStep(adimlar, tecelli);
  }

  runStepByStep(adimlar, tecelli) {
    this.steps = adimlar;
    this.currentStepIdx = 0;
    this.renderTimelineShell();

    this.timer = setInterval(() => {
      if (this.currentStepIdx >= this.steps.length) {
        clearInterval(this.timer);
        this.btnStart.disabled = false;
        this.showFinalTecelli(tecelli);
        return;
      }

      const step = this.steps[this.currentStepIdx];
      this.applyStep(step, this.currentStepIdx, this.steps.length);
      this.currentStepIdx++;
    }, 1200);
  }

  renderTimelineShell() {
    this.timelineContainer.innerHTML = "";
    this.steps.forEach((step, idx) => {
      const item = document.createElement("div");
      item.id = `step-item-${idx}`;
      item.className = "timeline-step";
      item.innerHTML = `
        <div class="timeline-step-header">
          <span>${step.durum.makam}</span>
          <span>#${step.adim_no}</span>
        </div>
        <div class="timeline-step-msg">${step.mesaj}</div>
      `;
      this.timelineContainer.appendChild(item);
    });
  }

  applyStep(step, idx, total) {
    document.querySelectorAll(".timeline-step").forEach((el) => el.classList.remove("active"));
    const activeEl = document.getElementById(`step-item-${idx}`);
    if (activeEl) {
      activeEl.classList.add("active");
      activeEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    const progress = (idx + 1) / total;
    this.canvas.setPos(progress);
    this.canvas.setBenlik(step.durum.benlik_orani);

    this.badgeMakam.textContent = `Makam: ${step.durum.makam}`;
    this.zarText.textContent = step.zar_metni;

    const benlikYuzde = (step.durum.benlik_orani * 100).toFixed(1);
    this.valBenlik.textContent = `%${benlikYuzde}`;
    this.barBenlik.style.width = `${benlikYuzde}%`;

    const direncVal = step.durum.viskozite_direnci.toFixed(3);
    this.valDirenc.textContent = direncVal;
    this.barDirenc.style.width = `${step.durum.viskozite_direnci * 100}%`;

    const hayretVal = step.durum.hayret_katsayisi.toFixed(3);
    this.valHayret.textContent = hayretVal;
    this.barHayret.style.width = `${Math.min(100, step.durum.hayret_katsayisi * 20)}%`;

    this.valFrekans.textContent = `${step.durum.rezonans_frekansi.toFixed(1)} Hz`;
    this.valKarakter.textContent = step.durum.ses_karakteri;

    this.audio.guncelle(step.durum.rezonans_frekansi, step.durum.benlik_orani);
  }

  showFinalTecelli(tecelli) {
    this.finalTecelli.classList.remove("hidden");
    this.tecelliHukum.textContent = tecelli.hukum;
    this.tecelliHal.textContent = tecelli.hal;
  }

  resetSimulation() {
    if (this.timer) clearInterval(this.timer);
    this.btnStart.disabled = false;
    this.finalTecelli.classList.add("hidden");
    this.canvas.reset();

    this.badgeMakam.textContent = "Makam: Talep";
    this.zarText.textContent = "Vızıltı: Ayrılık ve kesret telaşı...";

    this.valBenlik.textContent = "%100.0";
    this.barBenlik.style.width = "100%";
    this.valDirenc.textContent = "1.000";
    this.barDirenc.style.width = "100%";
    this.valHayret.textContent = "0.000";
    this.barHayret.style.width = "0%";
    this.valFrekans.textContent = "440.0 Hz";
    this.valKarakter.textContent = "Kesret Feryadı";

    this.timelineContainer.innerHTML = "";
    this.audio.guncelle(440.0, 1.0);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  new App();
});
