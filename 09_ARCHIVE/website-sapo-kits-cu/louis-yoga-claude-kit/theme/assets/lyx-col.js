/* Louis Yoga — trang danh mục theo bản thiết kế 15/10/2026 (templates/collection.bwt).
   Ngăn bộ lọc (điện thoại) dùng đúng cơ chế cũ: lớp .openf trên #open-filters, .dqdt-sidebar, .opacity_sidebar (ly-filter.js tự đóng sau khi lọc).
   Thêm: nút đóng, Esc, bẫy focus, bảng "Sắp xếp" dạng tấm dưới, ô màu cho nhóm "Màu", "Xem thêm", hàng sale cuộn ngang. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const side = $('#lyxc-side'), dim = $('.opacity_sidebar'), btn = $('[data-lyxc-filter]');
  let last = null;
  const isOpen = () => side && side.classList.contains('openf');
  const setOpen = (v, from) => {
    if (!side) return;
    [side, dim, $('#open-filters')].forEach(el => el && el.classList.toggle('openf', v));
    document.documentElement.classList.toggle('lyx-lock', v);
    if (btn) btn.setAttribute('aria-expanded', String(v));
    if (v) { last = from || document.activeElement; setTimeout(() => { const f = $('[data-lyxc-close]', side); if (f) f.focus(); }, 60); }
    else if (last) { last.focus(); last = null; }
  };
  btn && btn.addEventListener('click', () => setOpen(!isOpen(), btn));
  $('[data-lyxc-close]')?.addEventListener('click', () => setOpen(false));
  dim && dim.addEventListener('click', () => setOpen(false));
  // ly-filter.js gỡ .openf sau khi lọc → đồng bộ khóa cuộn
  if (side && 'MutationObserver' in window) new MutationObserver(() => { if (!isOpen()) { document.documentElement.classList.remove('lyx-lock'); if (btn) btn.setAttribute('aria-expanded', 'false'); } }).observe(side, { attributes: true, attributeFilter: ['class'] });
  document.addEventListener('keydown', e => {
    if (!isOpen()) return;
    if (e.key === 'Escape') { setOpen(false); return; }
    if (e.key === 'Tab') {
      const f = $$('a[href],button,input:not([type=hidden]),summary', side).filter(x => x.offsetParent !== null);
      if (!f.length) return; const a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    }
  });

  // Sắp xếp: PC = menu thả; điện thoại = tấm dưới
  const sort = $('#sort-by'), sbtn = $('[data-lyxc-sort]');
  if (sort) {
    const li = $('#sortBy > li', sort);
    if (li) { li.tabIndex = 0; li.addEventListener('click', e => { if (!e.target.closest('a')) li.classList.toggle('is-open'); }); document.addEventListener('click', e => { if (!li.contains(e.target)) li.classList.remove('is-open'); }); }
    const close = () => { sort.classList.remove('is-open'); sbtn && sbtn.setAttribute('aria-expanded', 'false'); };
    sbtn && sbtn.addEventListener('click', e => { e.stopPropagation(); const v = !sort.classList.contains('is-open'); sort.classList.toggle('is-open', v); sbtn.setAttribute('aria-expanded', String(v)); });
    document.addEventListener('click', e => { if (sort.classList.contains('is-open') && !sort.contains(e.target) && e.target !== sbtn) close(); });
    sort.addEventListener('click', e => { if (e.target.closest('#sortBy a')) { close(); li && li.classList.remove('is-open'); const t = e.target.closest('a'); const s = $('#sortBy > li > span', sort); if (s && t) s.textContent = t.textContent; } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  // Ô màu cho nhóm có tiêu đề chứa "Màu"
  const COLORS = { 'xanh rêu': '#0f6b3a', 'ghi đậm': '#5d5f62', 'đen': '#111', 'tím đậm': '#5b2a6e', 'xanh cốm': '#8cc63f', 'cafe': '#6f4e37', 'trắng': '#f7f4ee', 'ghi khói': '#a39f97', 'đỏ': '#d0312d', 'vàng': '#f2b705', 'hồng': '#f78ab0', 'xanh đậm': '#2f4858', 'xanh coban': '#0047ab', 'xanh lá': '#2e7d32', 'tím huế': '#7d4b8f', 'hồng nhạt': '#f6bfd0', 'cam': '#f07f2d', 'xanh ngọc': '#1aa39a', 'tím': '#8e44ad', 'xanh': '#2f4858', 'ghi': '#8a8a8a', 'nâu': '#7a4b2a', 'be': '#e8dcc6' };
  $$('.ly-filters .aside-item').forEach(box => {
    const t = ($('.title-head', box)?.textContent || '').toLowerCase();
    if (!/màu/.test(t)) return;
    box.classList.add('lyx-swatch-list');
    $$('.filter-item label', box).forEach(l => {
      const inp = $('input', l); if (!inp || l.querySelector('.lyx-sw')) return;
      const name = (inp.dataset.text || l.textContent).trim().toLowerCase();
      const sw = document.createElement('span'); sw.className = 'lyx-sw'; sw.style.setProperty('--sw', COLORS[name] || '#ccc');
      inp.after(sw);
    });
  });
  // "Xem thêm" mở rộng nhóm
  $$('.ly-filters .filter-item-toggle').forEach(t => { t.setAttribute('role', 'button'); t.tabIndex = 0; const go = () => { const box = t.closest('.aside-content') || t.closest('ul'); box.classList.toggle('is-expand'); t.textContent = box.classList.contains('is-expand') ? 'Thu gọn' : 'Xem thêm'; }; t.addEventListener('click', go); t.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } }); });

  // Hàng sale cuộn ngang: thanh tiến độ
  $$('[data-lyxh-track]').forEach(track => {
    const row = $('.lyxh-row', track), bar = $('.lyxh-bar i', track);
    if (!row || !bar) return;
    const paint = () => { const max = row.scrollWidth - row.clientWidth, vis = row.scrollWidth ? Math.min(1, row.clientWidth / row.scrollWidth) : 1; bar.style.width = vis * 100 + '%'; bar.style.transform = `translateX(${max > 0 ? (row.scrollLeft / max) * ((1 - vis) / vis) * 100 : 0}%)`; };
    row.addEventListener('scroll', () => requestAnimationFrame(paint), { passive: true }); window.addEventListener('resize', paint); paint();
  });
})();