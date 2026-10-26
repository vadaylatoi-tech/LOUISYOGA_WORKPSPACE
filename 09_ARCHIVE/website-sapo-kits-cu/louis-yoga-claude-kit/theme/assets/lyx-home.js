/* Louis Yoga — trang chủ editorial 16/10/2026 (snippets/lyx-home.bwt).
   1. Đồng hồ đếm ngược: ngày thật (data-mode="date", giờ +07:00) hoặc tới 23:59:59 cuối tháng hiện tại (data-mode="month")
   2. Hero video: MP4 (data-mp4-pc / data-mp4-mb) hoặc YouTube tắt tiếng (data-yt); tải sau khi trang xong, bỏ qua khi giảm chuyển động / tiết kiệm dữ liệu
   3. Tab phân khúc Harmony/Balance/Mastery + banner
   4. Hàng cuộn ngang: thanh tiến độ, mũi tên, kéo bằng chuột trên PC
   5. Nút "Xem câu chuyện" + khối Video (YouTube / Shorts / TikTok) trong hộp thoại; thẻ giữa + chấm trang trên điện thoại (16/10)
   Hero điện thoại (17/10): khung 5:4 — MP4 (bản riêng hoặc bản ngang PC), không nhúng YouTube. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  const ytOk = id => /^[A-Za-z0-9_-]{11}$/.test(id || '');

  // 1. Đếm ngược
  $$('[data-lyx-cd]').forEach(cd => {
    const pad = v => String(v).padStart(2, '0');
    const parse = (raw, endOfDay) => {
      const p = String(raw || '').trim().match(/^(\d{4})-(\d{1,2})-(\d{1,2})(?:[-T ](\d{1,2})[-:](\d{1,2})(?:[-:](\d{1,2}))?)?$/);
      if (!p) return NaN;
      const t = p[4] !== undefined ? `${pad(p[4])}:${pad(p[5])}:${pad(p[6] || 0)}` : (endOfDay ? '23:59:59' : '00:00:00');
      return new Date(`${p[1]}-${pad(p[2])}-${pad(p[3])}T${t}+07:00`).getTime();
    };
    // Cuối tháng theo giờ Việt Nam (+07:00), không phụ thuộc múi giờ máy khách
    const monthEnd = () => {
      const vn = new Date(Date.now() + 7 * 36e5);
      const y = vn.getUTCFullYear(), m = vn.getUTCMonth();
      const last = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
      return new Date(`${y}-${pad(m + 1)}-${pad(last)}T23:59:59+07:00`).getTime();
    };
    const mode = cd.dataset.mode;
    const start = mode === 'date' ? parse(cd.dataset.start, false) : NaN;
    let end = mode === 'date' ? parse(cd.dataset.end, true) : mode === 'month' ? monthEnd() : NaN;
    const set = (u, v) => { const el = $(`[data-u="${u}"]`, cd); if (el) el.textContent = pad(v); };
    const tick = () => {
      if (mode === 'month' && Date.now() > end) end = monthEnd();
      if (!Number.isFinite(end)) { cd.hidden = true; return false; }
      const now = Date.now(), before = Number.isFinite(start) && now < start, diff = (before ? start : end) - now;
      if (diff <= 0) { cd.hidden = true; return false; }
      cd.hidden = false;
      set('d', Math.min(99, Math.floor(diff / 864e5))); set('h', Math.floor(diff / 36e5) % 24); set('m', Math.floor(diff / 6e4) % 60); set('s', Math.floor(diff / 1e3) % 60);
      return true;
    };
    if (tick()) { const t = setInterval(() => { if (!tick()) clearInterval(t); }, 1000); }
  });

  // 2. Hero video
  const hero = $('[data-lyxh-hero]');
  if (hero && !reduce && !saveData) {
    const box = $('[data-lyxh-hero-video]', hero);
    const start = () => {
      const mb = matchMedia('(max-width:767px)').matches;
      // 17/10: điện thoại khung 5:4 — phát MP4 điện thoại, không có thì MP4 ngang PC (cắt phủ khung); không có MP4 thì giữ ảnh — không nhúng YouTube (lộ nút điều khiển)
      const mp4 = mb ? (hero.dataset.mp4Mb || hero.dataset.mp4Pc) : hero.dataset.mp4Pc;
      if (mb && !mp4) return;
      if (mp4) {
        const v = document.createElement('video');
        Object.assign(v, { muted: true, autoplay: true, loop: true, playsInline: true, preload: 'auto' });
        v.setAttribute('muted', ''); v.setAttribute('playsinline', ''); v.setAttribute('aria-hidden', 'true');
        v.src = mp4;
        v.addEventListener('playing', () => hero.classList.add('is-playing'), { once: true });
        box.append(v);
        v.play().catch(() => {});
      } else if (ytOk(hero.dataset.yt)) {
        const id = hero.dataset.yt;
        const f = document.createElement('iframe');
        f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&mute=1&loop=1&playlist=${id}&controls=0&disablekb=1&modestbranding=1&playsinline=1&rel=0&iv_load_policy=3&fs=0`;
        f.title = 'Video nền Louis Yoga'; f.tabIndex = -1;
        f.allow = 'autoplay; encrypted-media; picture-in-picture';
        f.setAttribute('aria-hidden', 'true');
        f.addEventListener('load', () => setTimeout(() => hero.classList.add('is-playing'), 1200), { once: true });
        box.append(f);
      }
    };
    if (document.readyState === 'complete') setTimeout(start, 600); else window.addEventListener('load', () => setTimeout(start, 600), { once: true });
  }

  // 5. Video có tiếng trong hộp thoại: nút "Xem câu chuyện" + khối Video (yt = YouTube, ys = Shorts, tt = TikTok)
  const ttId = u => { const m = String(u || '').match(/(?:video|v|embed\/v2|player\/v1)\/(\d{8,})/) || String(u || '').match(/^(\d{8,})$/); return m ? m[1] : ''; };
  const modal = $('[data-lyxh-modal]');
  if (modal && modal.showModal) {
    const frame = $('.lyxh-modal-frame', modal);
    const open = (src, title, tall) => {
      frame.innerHTML = '';
      const f = document.createElement('iframe');
      f.src = src; f.title = title || 'Video Louis Yoga';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true;
      frame.append(f);
      modal.classList.toggle('is-tall', !!tall);
      modal.showModal();
    };
    $$('[data-lyxh-play]').forEach(b => b.addEventListener('click', () => {
      const id = b.dataset.lyxhPlay; if (!ytOk(id)) return;
      open(`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`, 'Câu chuyện Louis Yoga', false);
    }));
    $$('[data-lyxh-vid]').forEach(b => b.addEventListener('click', () => {
      const kind = b.dataset.lyxhVid, src = b.dataset.src, t = (b.getAttribute('aria-label') || '').replace(/^Xem video:\s*/, '');
      if (kind === 'tt') { const id = ttId(src); if (id) open(`https://www.tiktok.com/player/v1/${id}?autoplay=1&loop=1&rel=0`, t, true); else window.open(src, '_blank', 'noopener'); return; }
      if (ytOk(src)) open(`https://www.youtube-nocookie.com/embed/${src}?autoplay=1&rel=0&playsinline=1`, t, kind === 'ys');
    }));
    $('.lyxh-modal-x', modal).addEventListener('click', () => modal.close());
    modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });
    modal.addEventListener('close', () => { frame.innerHTML = ''; });
  }
  // Ảnh bìa TikTok: lấy từ oEmbed công khai khi chưa khai báo ảnh bìa trong Assets
  $$('[data-lyxh-vid="tt"]').forEach(b => {
    if ($('img', b)) return;
    fetch('https://www.tiktok.com/oembed?url=' + encodeURIComponent(b.dataset.src)).then(r => r.ok ? r.json() : null).then(j => {
      if (!j || !/^https:\/\//.test(j.thumbnail_url || '')) return;
      const im = new Image(); im.src = j.thumbnail_url; im.alt = ''; im.loading = 'lazy'; im.width = 300; im.height = 533; b.prepend(im);
    }).catch(() => {});
  });

  // 3. Tab phân khúc
  const mat = $('[data-lyxh-mat]');
  if (mat) {
    const tabs = $$('[role="tab"][data-seg]', mat), panels = $$('.lyxh-mat-panel', mat), banners = $$('.lyxh-mat-banner [data-seg]', mat), all = $('[data-lyxh-mat-all]', mat);
    const select = (i, focusEl) => {
      tabs.forEach(t => { const on = Number(t.dataset.seg) === i; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
      panels.forEach(p => { p.hidden = Number(p.dataset.seg) !== i; if (!p.hidden && all && p.dataset.url) all.href = p.dataset.url; });
      banners.forEach(b => { b.hidden = Number(b.dataset.seg) !== i; });
      if (focusEl) focusEl.focus();
    };
    tabs.forEach(t => {
      t.addEventListener('click', () => select(Number(t.dataset.seg)));
      t.addEventListener('keydown', e => {
        const k = tabs.indexOf(t), n = tabs.length;
        const map = { ArrowRight: (k + 1) % n, ArrowDown: (k + 1) % n, ArrowLeft: (k + n - 1) % n, ArrowUp: (k + n - 1) % n, Home: 0, End: n - 1 };
        if (e.key in map) { e.preventDefault(); const nx = tabs[map[e.key]]; select(Number(nx.dataset.seg), nx); }
      });
    });
  }

  // 4. Hàng cuộn ngang
  $$('[data-lyxh-track]').forEach(track => {
    const row = $('.lyxh-row', track), bar = $('.lyxh-bar i', track), arrows = $$('.lyxh-arr', track);
    if (!row) return;
    const paint = () => {
      const max = row.scrollWidth - row.clientWidth;
      const vis = row.scrollWidth ? Math.min(1, row.clientWidth / row.scrollWidth) : 1;
      if (bar) {
        bar.style.width = (vis * 100) + '%';
        bar.style.transform = `translateX(${max > 0 ? (row.scrollLeft / max) * ((1 - vis) / vis) * 100 : 0}%)`;
      }
      const nav = $('.lyxh-track-nav', track); if (nav) nav.hidden = max <= 4;
      arrows.forEach(a => { a.disabled = Number(a.dataset.dir) < 0 ? row.scrollLeft <= 2 : row.scrollLeft >= max - 2; });
    };
    arrows.forEach(a => a.addEventListener('click', () => {
      const item = row.firstElementChild; const step = item ? item.getBoundingClientRect().width + parseFloat(getComputedStyle(row).columnGap || 16) : row.clientWidth * .8;
      row.scrollBy({ left: Number(a.dataset.dir) * step * (matchMedia('(max-width:767px)').matches ? 1 : 2), behavior: reduce ? 'auto' : 'smooth' });
    }));
    row.addEventListener('scroll', () => requestAnimationFrame(paint), { passive: true });
    window.addEventListener('resize', paint); window.addEventListener('load', paint); paint();
    let down = false, sx = 0, sl = 0, moved = false;
    row.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = row.scrollLeft; });
    window.addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 5) { moved = true; row.style.scrollSnapType = 'none'; row.scrollLeft = sl - dx; } });
    window.addEventListener('pointerup', () => { if (!down) return; down = false; row.style.scrollSnapType = ''; });
    row.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
    // Khối Video trên điện thoại: đánh dấu thẻ ở giữa (.is-center) + chấm trang (như bản thiết kế mobile)
    const dots = $('.lyxh-dots', track);
    if (dots) {
      const items = [...row.children];
      dots.innerHTML = items.map(() => '<i></i>').join('');
      const ds = [...dots.children];
      const mark = () => {
        const mid = row.getBoundingClientRect().left + row.clientWidth / 2;
        let best = 0, bd = Infinity;
        items.forEach((it, k) => { const r = it.getBoundingClientRect(), d = Math.abs(r.left + r.width / 2 - mid); if (d < bd) { bd = d; best = k; } });
        items.forEach((it, k) => it.classList.toggle('is-center', k === best));
        ds.forEach((d, k) => d.classList.toggle('is-on', k === best));
      };
      row.addEventListener('scroll', () => requestAnimationFrame(mark), { passive: true });
      window.addEventListener('resize', mark); mark();
    }
  });
})();
