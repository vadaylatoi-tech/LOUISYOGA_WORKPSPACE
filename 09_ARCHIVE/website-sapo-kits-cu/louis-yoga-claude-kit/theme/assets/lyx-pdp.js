/* Louis Yoga — trang sản phẩm theo bản thiết kế 15/10/2026. Đi kèm assets/lyx-pdp.css, gọi từ snippets/tab_product.bwt.
   Chỉ thêm phần tử mới hoặc gom khối đánh giá; không di chuyển ô màu / số lượng / nút của form (ly-pdp.js dùng chúng trên mobile).
   Đánh giá: điểm và số lượng = web (app đánh giá Sapo, đã hiển thị trên trang) + Shopee (khối #lysr). Không ghi điểm Shopee vào schema. */
(() => {
  'use strict';
  const d = document, $ = (s, r = d) => r.querySelector(s), $$ = (s, r = d) => [...r.querySelectorAll(s)];
  const dp = $('.layout-product .details-pro');
  if (!dp || dp.dataset.lyxp) return;
  dp.dataset.lyxp = '1';
  const el = (tag, cls, html) => { const e = d.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const fmt = n => (Math.round(n * 10) / 10).toFixed(1);
  const ICON = {
    heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.3-9.4C1.4 7.6 3.6 4 7.2 4c2 0 3.5 1.1 4.8 2.8C13.3 5.1 14.8 4 16.8 4c3.6 0 5.8 3.6 4.5 7.1-1.8 4.8-9.3 9.4-9.3 9.4z"/></svg>',
    share: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.5 2.5 10.6 13.4M21.5 2.5l-6.9 19-4-8.1-8.1-4z"/></svg>'
  };
  /* Thông báo ngắn: dùng #ly-toast của site (ly-site.js, lớp is-visible), thiếu thì tự tạo */
  const toast = msg => {
    let t = $('#ly-toast');
    if (!t) { t = $('.lyxp-toast') || el('div', 'lyxp-toast'); t.setAttribute('role', 'status'); if (!t.isConnected) d.body.append(t); }
    t.textContent = msg; t.classList.add('is-visible');
    clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('is-visible'), 3500);
  };

  /* 1. Nhãn phân khúc + Chính hãng (PC). Mobile: chip trả về chỗ cũ cho lớp ly-pdp.js tự xếp */
  const mqd = matchMedia('(min-width:768px)');
  const title = $('.title-product', dp);
  const badges = el('div', 'lyxp-badges');
  const chip = $('.ly-seg-chip', dp), chipHome = chip && d.createComment('lyxp-chip');
  if (chip) chip.before(chipHome);
  badges.append(el('span', 'lyxp-genuine', 'Chính hãng'));
  if (title) title.before(badges); else dp.prepend(badges);
  const placeChip = () => { if (!chip) return; if (mqd.matches) badges.prepend(chip); else chipHome.after(chip); };
  placeChip();
  mqd.addEventListener ? mqd.addEventListener('change', placeChip) : mqd.addListener(placeChip);

  /* 2. Dòng sao dưới tên (điểm gộp, cập nhật khi đánh giá tải xong) */
  const rate = el('button', 'lyxp-rate');
  rate.type = 'button'; rate.hidden = true;
  rate.addEventListener('click', () => { const s = $('.ly-pd-reviews'); if (s) s.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  if (title) title.after(rate);

  /* 3. Tim + chia sẻ cạnh giá */
  const price = $('.form-product .price-box', dp);
  const wish = $('.setWishlist', dp);
  if (price) {
    const acts = el('div', 'lyxp-acts');
    if (wish) {
      const h = el('button', '', ICON.heart);
      h.type = 'button'; h.setAttribute('aria-label', 'Thêm vào yêu thích');
      const sync = () => h.setAttribute('aria-pressed', String(wish.getAttribute('aria-pressed') === 'true' || wish.classList.contains('active')));
      sync(); new MutationObserver(sync).observe(wish, { attributes: true, attributeFilter: ['class', 'aria-pressed'] });
      h.addEventListener('click', () => wish.click());
      acts.append(h);
    }
    const sh = el('button', '', ICON.share);
    sh.type = 'button'; sh.setAttribute('aria-label', 'Chia sẻ sản phẩm');
    sh.addEventListener('click', async () => {
      const data = { title: d.title, url: location.href.split('#')[0] };
      try {
        if (navigator.share) { await navigator.share(data); return; }
        await navigator.clipboard.writeText(data.url); toast('Đã sao chép liên kết sản phẩm');
      } catch (e) { if (e && e.name !== 'AbortError') toast('Không chia sẻ được, hãy sao chép địa chỉ trang'); }
    });
    acts.append(sh);
    price.append(acts);
  }

  /* 4. Bảng thông số: tách "Nhãn: giá trị" của mô tả ngắn thành hai cột; dòng không có nhãn giữ nguyên chữ */
  const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  $$('.product-summary li', dp).forEach(li => {
    const t = li.textContent.replace(/ /g, ' ').replace(/\s+/g, ' ').trim();
    const m = t.match(/^([^:]{1,40}):\s*(.+)$/);
    if (m) { li.classList.add('lyxp-kv'); li.innerHTML = '<span class="lyxp-k">' + esc(m[1]) + '</span><span class="lyxp-v">' + esc(m[2]) + '</span>'; }
    else li.classList.add('lyxp-line');
  });

  /* Dòng miễn phí vận chuyển dưới bảng thông số (lấy từ lớp mobile, cùng nguồn cài đặt) */
  const fp = $('.form-product', dp);
  const shipRow = $$('.lyp-row', dp).find(r => /vận chuyển/i.test(r.textContent));
  const shipTxt = shipRow && $('.lyp-row-v', shipRow) ? $('.lyp-row-v', shipRow).textContent.trim() : '';
  if (fp && shipTxt) { const p = el('p', 'lyxp-ship'); p.textContent = shipTxt; fp.append(p); }

  /* 5. Ảnh PC: lưới 2×2, chấm chuyển trang */
  const wrap = $('.gallery-top .swiper-wrapper');
  const slides = wrap ? $$('.swiper-slide', wrap) : [];
  const PER = 4, pages = Math.ceil(slides.length / PER);
  let page = 0, dots = null;
  const show = p => {
    page = Math.max(0, Math.min(pages - 1, p));
    slides.forEach((s, i) => s.classList.toggle('lyxp-off', mqd.matches && Math.floor(i / PER) !== page));
    if (dots) $$('button', dots).forEach((b, i) => b.setAttribute('aria-current', String(i === page)));
  };
  if (slides.length) {
    if (pages > 1) {
      dots = el('div', 'lyxp-gdots');
      dots.setAttribute('role', 'group'); dots.setAttribute('aria-label', 'Trang ảnh sản phẩm');
      for (let i = 0; i < pages; i++) {
        const b = el('button'); b.type = 'button';
        b.setAttribute('aria-label', 'Ảnh ' + (i * PER + 1) + '–' + Math.min(slides.length, (i + 1) * PER));
        b.addEventListener('click', () => show(i));
        dots.append(b);
      }
      $('.product-image-block').after(dots);
    }
    const apply = () => {
      if (dots) dots.hidden = !mqd.matches;
      const g = window.galleryTop;
      if (g && 'allowTouchMove' in g) g.allowTouchMove = !mqd.matches;
      show(page);
    };
    apply();
    mqd.addEventListener ? mqd.addEventListener('change', apply) : mqd.addListener(apply);
    /* Chọn màu có ảnh riêng → product.bwt gọi galleryTop.slideTo(i): đưa trang chứa ảnh đó lên */
    const hook = () => { const g = window.galleryTop; if (g && g.on) g.on('slideChange', () => { if (mqd.matches) show(Math.floor((g.activeIndex || 0) / PER)); }); };
    if (window.galleryTop) hook(); else window.addEventListener('load', hook, { once: true });
  }

  /* 6. Nút giỏ tròn: trạng thái đang thêm (chống nhấp lặp, giỏ AJAX gốc xử lý yêu cầu) */
  const mua = $('.btn-mua', dp), add = mua && $('.btn_add_cart', mua);
  if (add) {
    add.setAttribute('aria-label', 'Thêm vào giỏ hàng');
    add.setAttribute('title', 'Thêm vào giỏ hàng');
    add.addEventListener('click', () => { if (!mqd.matches) return; mua.classList.add('lyxp-busy'); setTimeout(() => mua.classList.remove('lyxp-busy'), 1500); });
  }

  /* 7. Đánh giá gộp web + Shopee */
  const sec = $('.ly-pd-reviews');
  if (!sec) return;
  const lyp = $('.lyp-rate-t');
  const read = () => {
    const web = [0, 0, 0, 0, 0, 0], shp = [0, 0, 0, 0, 0, 0];
    $$('.ly-rv-bar', sec).forEach(b => { const n = +b.dataset.n, m = (b.getAttribute('aria-label') || '').match(/\((\d+)\)/); if (n >= 1 && n <= 5 && m) web[n] = +m[1]; });
    $$('.lysr-bar', sec).forEach(b => { const n = parseInt(($('span', b) || {}).textContent, 10), c = parseInt(($('em', b) || {}).textContent, 10); if (n >= 1 && n <= 5 && c >= 0) shp[n] = c; });
    const sum = a => a.reduce((x, y) => x + y, 0), avg = a => { const t = sum(a); return t ? a.reduce((x, c, i) => x + c * i, 0) / t : 0; };
    let wT = sum(web), wA = avg(web);
    const bp = window.BPR && window.BPR.product;
    if (!wT && bp && bp.votes > 0) { wT = +bp.votes; wA = +bp.rating || 0; }
    const sT = sum(shp), sA = avg(shp), tot = wT + sT;
    const all = [0, 1, 2, 3, 4, 5].map(i => web[i] + shp[i]);
    return { web, shp, all, wT, sT, tot, avg: tot ? (wA * wT + sA * sT) / tot : 0, webList: $('#sapo-product-reviews', sec), shpBox: $('#lysr', sec) };
  };
  let score, bars, tabWeb, tabShp, selTab = null, picked = false, sig = '';
  /* Cập nhật số liệu (gọi lại mỗi khi app đánh giá đổi số; so chữ ký để không lặp vô hạn) */
  const update = () => {
    const r = read(), s = [r.wT, r.sT].concat(r.all).join(',');
    if (s === sig) return;
    sig = s;
    if (r.tot) score.innerHTML = '<b>' + fmt(r.avg) + '</b><span class="lyxp-stars" style="--v:' + (r.avg / 5 * 100).toFixed(1) + '%" aria-hidden="true">★★★★★</span><span>' + r.tot + ' Đánh giá</span>';
    else score.innerHTML = '<b>–</b><span class="lyxp-stars" style="--v:0%" aria-hidden="true">★★★★★</span><span>Chưa có đánh giá</span>';
    score.setAttribute('aria-label', r.tot ? 'Điểm trung bình ' + fmt(r.avg) + ' trên 5, ' + r.tot + ' đánh giá' : 'Chưa có đánh giá');
    $$('.lyxp-rv-bar', bars).forEach(b => {
      const n = +b.dataset.n, pc = r.tot ? Math.round(r.all[n] / r.tot * 100) : 0;
      $('b', b).style.width = pc + '%';
      b.setAttribute('aria-label', n + ' sao: ' + r.all[n] + ' đánh giá');
    });
    if (tabWeb) tabWeb.textContent = 'Đánh giá (' + r.wT + ')';
    if (tabShp) tabShp.textContent = 'Đánh giá shopee (' + r.sT + ')';
    if (!picked && selTab && tabWeb && r.wT > 0) selTab(0);
    if (r.tot) {
      rate.innerHTML = '<span>' + fmt(r.avg) + '</span><span class="lyxp-stars" style="--v:' + (r.avg / 5 * 100).toFixed(1) + '%" aria-hidden="true">★★★★★</span><i aria-hidden="true"></i><em><b>' + r.tot + '</b> Đánh giá</em>';
      rate.setAttribute('aria-label', 'Điểm ' + fmt(r.avg) + ' trên 5 từ ' + r.tot + ' đánh giá, xem đánh giá');
      rate.hidden = false;
      if (lyp) lyp.textContent = fmt(r.avg).replace('.', ',') + ' · ' + r.tot + ' đánh giá';
    }
  };
  const build = () => {
    if (sec.classList.contains('lyxp-rv-on')) return;
    const r = read();
    if (!r.webList && !r.shpBox) return;
    sec.classList.add('lyxp-rv-on');
    const h = $('.ly-pd-h', sec);
    const sumBox = el('div', 'lyxp-rv-sum');
    score = el('div', 'lyxp-rv-score');
    bars = el('div', 'lyxp-rv-bars');
    for (let n = 5; n >= 1; n--) { const b = el('div', 'lyxp-rv-bar', '<span>' + n + ' Sao</span><i><b style="width:0%"></b></i>'); b.dataset.n = n; bars.append(b); }
    sumBox.append(score, bars);
    const origWrite = $('.btn-new-review', sec);
    if (origWrite) {
      const w = el('button', 'lyxp-rv-write', 'Viết đánh giá'); w.type = 'button';
      w.addEventListener('click', () => {
        if (selTab && tabWeb) selTab(0); // form của app nằm trong tab web
        const cfg = window.BPR && window.BPR.config, $j = window.jQuery;
        if (cfg && cfg.type_form === 'popup' && !($j && $j.fn && $j.fn.jquerymodal)) { toast('Chức năng viết đánh giá của ứng dụng đang tạm gián đoạn. Vui lòng thử lại sau.'); return; }
        origWrite.click();
      });
      sumBox.append(w);
    }
    (h || sec.firstChild) && (h ? h.after(sumBox) : sec.prepend(sumBox));

    /* Hai tab: web / Shopee */
    const tabs = el('div', 'lyxp-rv-tabs'); tabs.setAttribute('role', 'tablist'); tabs.setAttribute('aria-label', 'Nguồn đánh giá');
    const panels = [];
    const mk = (key, label, nodes) => {
      const id = 'lyxp-rv-' + key;
      const t = el('button'); t.type = 'button'; t.id = id + '-t'; t.setAttribute('role', 'tab'); t.setAttribute('aria-controls', id); t.textContent = label;
      const p = el('div', 'lyxp-rv-panel'); p.id = id; p.setAttribute('role', 'tabpanel'); p.setAttribute('aria-labelledby', t.id);
      nodes.filter(Boolean).forEach(n => p.append(n));
      tabs.append(t); panels.push([t, p]);
    };
    if (r.webList) { mk('web', 'Đánh giá (' + r.wT + ')', [$('.lysr-web-h', sec), r.webList, $('.ly-rv-more', sec)]); tabWeb = panels[panels.length - 1][0]; }
    if (r.shpBox) { mk('shopee', 'Đánh giá shopee (' + r.sT + ')', [r.shpBox]); tabShp = panels[panels.length - 1][0]; }
    const sel = i => panels.forEach(([t, p], k) => { t.setAttribute('aria-selected', String(k === i)); t.tabIndex = k === i ? 0 : -1; p.hidden = k !== i; });
    selTab = sel;
    panels.forEach(([t], i) => {
      t.addEventListener('click', () => { picked = true; sel(i); });
      t.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const j = (i + (e.key === 'ArrowRight' ? 1 : panels.length - 1)) % panels.length; picked = true; sel(j); panels[j][0].focus(); } });
    });
    sumBox.after(tabs);
    let last = tabs;
    panels.forEach(([, p]) => { last.after(p); last = p; });
    const bp = window.BPR && window.BPR.product;
    sel(r.wT > 0 || (bp && +bp.votes > 0) || !r.shpBox ? 0 : panels.length - 1);
    update();
    /* App/ly-reviews.js có thể đổi số sau khi dựng: theo dõi 15 giây đầu */
    let tm;
    const mo = new MutationObserver(() => { clearTimeout(tm); tm = setTimeout(update, 200); });
    mo.observe(sec, { subtree: true, childList: true, attributes: true, attributeFilter: ['aria-label'] });
    setTimeout(() => { mo.disconnect(); update(); }, 15000);
  };
  /* App đánh giá tải bất đồng bộ: chờ ly-reviews.js dựng xong (ly-rv-ready + thanh sao) hoặc app báo số đánh giá; tối đa 10 giây */
  let tries = 0;
  const wait = () => {
    const bp = window.BPR && window.BPR.product;
    const ready = !$('#sapo-product-reviews', sec) || (sec.classList.contains('ly-rv-ready') && $('.ly-rv-bar', sec)) || (bp && 'votes' in bp && !(+bp.votes > 0));
    if (ready || ++tries > 40) build(); else setTimeout(wait, 250);
  };
  wait();
})();
