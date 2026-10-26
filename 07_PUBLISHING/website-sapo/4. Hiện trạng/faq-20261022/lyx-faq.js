/* Louis Yoga — Câu hỏi thường gặp (22/10/2026). Đi kèm assets/lyx-faq.css.
   Mọi khối .lyxq: hiệu ứng mở câu, mở câu theo #id trên địa chỉ.
   Trang FAQ (.lyxq-page): tìm kiếm không dấu, mục lục theo dõi nhóm đang xem, dữ liệu có cấu trúc FAQPage (JSON-LD) dựng từ nội dung trang. */
(() => {
  'use strict';
  const d = document, $ = (s, r = d) => r.querySelector(s), $$ = (s, r = d) => [...r.querySelectorAll(s)];
  const roots = $$('.lyxq');
  if (!roots.length) return;

  /* Hiệu ứng mở (chỉ khi người dùng bấm) */
  roots.forEach(root => root.addEventListener('toggle', e => {
    const q = e.target;
    if (!q.classList || !q.classList.contains('lyxq-q') || !q.open) return;
    q.classList.remove('is-anim'); void q.offsetWidth; q.classList.add('is-anim');
  }, true));

  /* Mở câu theo #id */
  const openHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const q = d.getElementById(id);
    if (q && q.classList.contains('lyxq-q')) { q.open = true; setTimeout(() => q.scrollIntoView({ block: 'start' }), 60); }
  };
  openHash();
  addEventListener('hashchange', openHash);

  const page = $('.lyxq-page');
  if (!page) return;
  const items = $$('.lyxq-q', page), grps = $$('[data-lyxq-grp]', page);

  /* JSON-LD FAQPage */
  try {
    const ld = { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: items.map(q => ({
      '@type': 'Question', name: $('summary span', q).textContent.trim(),
      acceptedAnswer: { '@type': 'Answer', text: $('.lyxq-a', q).innerText.replace(/\s+\n/g, '\n').trim() }
    })) };
    const s = d.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(ld); d.head.append(s);
  } catch (e) {}

  /* Tìm kiếm (bỏ dấu, không phân biệt hoa thường) */
  const norm = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'D').toLowerCase();
  const inp = $('.lyxq-search input', page), clr = $('.lyxq-clear', page), cnt = $('.lyxq-count', page), empty = $('.lyxq-empty', page);
  const navLinks = $$('.lyxq-nav a', page);
  const idx = items.map(q => ({ q, sum: $('summary span', q), raw: $('summary span', q).textContent, t: norm(q.textContent) }));
  const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  let wasOpen = null;
  const run = () => {
    const v = norm(inp.value.trim());
    clr.hidden = !v;
    if (!v) {
      idx.forEach(o => { o.q.hidden = false; o.sum.textContent = o.raw; });
      if (wasOpen) { idx.forEach(o => { o.q.open = wasOpen.has(o.q); }); wasOpen = null; }
      grps.forEach(g => { g.hidden = false; });
      navLinks.forEach(a => a.classList.remove('is-empty'));
      cnt.textContent = ''; empty.hidden = true;
      return;
    }
    if (!wasOpen) wasOpen = new Set(items.filter(q => q.open));
    const words = v.split(/\s+/).filter(Boolean);
    let n = 0;
    idx.forEach(o => {
      const hit = words.every(w => o.t.includes(w));
      o.q.hidden = !hit; o.q.open = hit && v.length > 1;
      /* tô đậm từ khoá trong câu hỏi (so khớp không dấu trên cùng vị trí ký tự) */
      if (hit) {
        const nr = Array.from(o.raw, c => norm(c).charAt(0) || c).join(''); let out = '', i = 0;
        const marks = [];
        words.forEach(w => { let k = nr.indexOf(w); while (k > -1) { marks.push([k, k + w.length]); k = nr.indexOf(w, k + w.length); } });
        marks.sort((a, b) => a[0] - b[0]).forEach(([a, b]) => { if (a < i) return; out += esc(o.raw.slice(i, a)) + '<mark>' + esc(o.raw.slice(a, b)) + '</mark>'; i = b; });
        o.sum.innerHTML = out + esc(o.raw.slice(i));
        n++;
      } else o.sum.textContent = o.raw;
    });
    grps.forEach(g => { g.hidden = !$$('.lyxq-q:not([hidden])', g).length; });
    navLinks.forEach(a => { const g = d.getElementById(a.hash.slice(1)); a.classList.toggle('is-empty', !g || g.hidden); });
    cnt.textContent = n ? n + ' câu hỏi phù hợp' : '';
    empty.hidden = n > 0;
  };
  if (inp) {
    let t; inp.addEventListener('input', () => { clearTimeout(t); t = setTimeout(run, 120); });
    inp.addEventListener('keydown', e => { if (e.key === 'Escape') { inp.value = ''; run(); } });
    clr.addEventListener('click', () => { inp.value = ''; run(); inp.focus(); });
  }

  /* Mục lục: nhóm đang xem */
  if ('IntersectionObserver' in window && navLinks.length) {
    const vis = new Map();
    const io = new IntersectionObserver(es => {
      es.forEach(e => vis.set(e.target.id, e.isIntersecting ? e.boundingClientRect.top : null));
      let best = null, top = Infinity;
      grps.forEach(g => { const v = vis.get(g.id); if (v != null && !g.hidden && v < top) { top = v; best = g.id; } });
      if (!best) return;
      navLinks.forEach(a => {
        const on = a.hash === '#' + best;
        a.classList.toggle('is-on', on);
        if (on && matchMedia('(max-width:1023px)').matches) { const ul = a.closest('ul'); ul.scrollTo({ left: Math.max(0, ul.scrollLeft + a.getBoundingClientRect().left - ul.getBoundingClientRect().left - 16), behavior: 'smooth' }); }
      });
    }, { rootMargin: '-120px 0px -55% 0px' });
    grps.forEach(g => io.observe(g));
  }
  navLinks.forEach(a => a.addEventListener('click', e => {
    const g = d.getElementById(a.hash.slice(1)); if (!g) return;
    e.preventDefault(); g.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion:reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    history.replaceState(null, '', a.hash);
  }));
})();
