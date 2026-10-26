/* Louis Yoga — 20/10/2026: ô màu trên thẻ sản phẩm (.lyx-card, snippets/ly-home-card.bwt).
   1. Bấm ô màu → ảnh thẻ đổi sang ảnh của màu đó, dòng "Màu …", giá + nhãn Sale theo biến thể.
   2. Ô màu chưa có mã trong cài đặt theme (color_N) → tô theo tên màu.
   3. Bấm giỏ / Mua ngay (hộp chọn phân loại của ly-design.js) → chọn sẵn đúng màu đang xem.
   4. 21/10/2026 (anh Công báo ô chọn không khớp ảnh): khi thẻ hiện, ô đang chọn luôn khớp ảnh — ảnh là ảnh của một màu → chọn ô đó (đưa lên đầu);
      ảnh đại diện không thuộc màu nào (vd QUEEN ảnh xanh, ô chọn đen) → đổi ảnh sang ảnh của màu đang chọn; màu đó không có ảnh → bỏ chọn, ẩn dòng "Màu …".
      Bản trước: assets/zz-backup-lyx-card-20261021-mau.js
   5. 22/10/2026 (anh Công): trang lọc theo màu — khối "Tìm màu sắc" trang chủ dẫn tới /collections/all?q=tags:((Xanh Đậm) OR (Xanh Coban) OR (Xanh Ngọc)),
      ô tick màu ở bộ lọc danh mục, hoặc link ?mau=xanh-dam → mọi thẻ tự chọn ô màu khớp (đúng tên trước, chứa tên sau) → ảnh thẻ hiện đúng màu đã chọn.
      Thẻ in đủ các màu (ly-home-card.bwt), ô ngoài 6/4 ô đầu bị ẩn bằng CSS → ô khớp được đưa lên đầu hàng.
      Bản trước: assets/zz-backup-lyx-card-20261022-loc.js */
(function () {
  if (window.__lyxCard) return;
  window.__lyxCard = 1;

  var COLORS = { 'xanh rêu': '#255e3b', 'xanh cốm': '#707e41', 'xanh đậm': '#4b708b', 'xanh coban': '#0047ab', 'xanh ngọc': '#1aa39a', 'xanh lá': '#2e7d32', 'xanh dương': '#4b708b', 'xanh navy': '#24314f', 'rêu': '#255e3b', 'xanh': '#4b708b',
    'tím huế': '#ddace1', 'tím đậm': '#945985', 'tím': '#8e6bb0', 'ghi đậm': '#6a6a6a', 'ghi khói': '#a39f97', 'ghi': '#8a8a8a', 'xám': '#8f8d8a',
    'đen': '#1d1d1d', 'trắng': '#f7f4ee', 'kem': '#efe6d6', 'be': '#e8dcc6', 'cafe': '#6f4e37', 'nâu': '#7a4b2a', 'đỏ đô': '#7a1f2b', 'đỏ': '#d0312d',
    'vàng': '#f2b705', 'cam': '#f07f2d', 'hồng nhạt': '#f6bfd0', 'hồng phấn': '#f3c6cf', 'hồng': '#f78ab0' };
  var KEYS = Object.keys(COLORS).sort(function (a, b) { return b.length - a.length; });

  function hex(name) {
    name = (name || '').toLowerCase().replace(/\s+/g, ' ').trim();
    if (COLORS[name]) return COLORS[name];
    for (var i = 0; i < KEYS.length; i++) if (name.indexOf(KEYS[i]) > -1) return COLORS[KEYS[i]];
    return '';
  }
  function paint(root) {
    var list = (root || document).querySelectorAll('.lyx-sw:not([style])');
    for (var i = 0; i < list.length; i++) {
      var c = hex(list[i].getAttribute('data-c'));
      list[i].style.setProperty('--c', c || '#d8d2ca');
    }
  }
  function num(s) { return parseInt(String(s || '').replace(/\D/g, ''), 10) || 0; }
  function file(s) { return String(s || '').split('?')[0].split('/').pop(); }

  function pick(sw, instant) {
    var card = sw.closest('.lyx-card');
    if (!card) return;
    if (sw.offsetParent === null && sw.parentNode && sw.parentNode.firstElementChild !== sw) sw.parentNode.insertBefore(sw, sw.parentNode.firstElementChild);
    var all = card.querySelectorAll('.lyx-sw');
    for (var i = 0; i < all.length; i++) { all[i].classList.toggle('is-on', all[i] === sw); all[i].setAttribute('aria-pressed', String(all[i] === sw)); }
    var line = card.querySelector('.lyx-card-color');
    if (line) line.style.visibility = '';
    var name = card.querySelector('.lyx-card-color span');
    if (name) name.textContent = sw.getAttribute('data-c') || '';
    var src = sw.getAttribute('data-img'), img = card.querySelector('.lyx-card-img img');
    if (src && img && img.getAttribute('src') !== src && instant) { img.src = src; img.removeAttribute('srcset'); }
    else if (src && img && img.getAttribute('src') !== src) {
      var pre = new Image();
      /* chỉ gán nếu ô vẫn đang được chọn (tránh ảnh tải chậm đè lên màu chọn sau, vd bước 5) */
      pre.onload = pre.onerror = function () { if (!sw.classList.contains('is-on')) return; img.src = src; img.removeAttribute('srcset'); };
      img.classList.add('is-swap');
      pre.src = src;
      setTimeout(function () { img.classList.remove('is-swap'); }, 260);
    }
    var p = sw.getAttribute('data-p'), cp = sw.getAttribute('data-cp');
    var box = card.querySelector('.lyx-card-price'), strong = box && box.querySelector('strong');
    if (p && strong && strong.querySelector('u')) {
      strong.innerHTML = p + ' <u>đ</u>';
      var del = box.querySelector('del');
      if (cp) {
        if (!del) { del = document.createElement('del'); box.insertBefore(del, strong); }
        del.innerHTML = cp + ' <u>đ</u>';
      } else if (del) del.remove();
      var sale = card.querySelector('.lyx-card-sale:not(.is-out)');
      if (sale) {
        var pct = cp ? Math.round((num(cp) - num(p)) * 100 / num(cp)) : 0;
        sale.hidden = !(pct > 0);
        if (pct > 0) sale.innerHTML = 'Sale<br> ' + pct + '%';
      }
    }
  }

  // 4. Ô đang chọn khớp ảnh (chạy 1 lần mỗi thẻ)
  function match(root) {
    var cards = (root || document).querySelectorAll('.lyx-card:not([data-lyc-ok])');
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      card.setAttribute('data-lyc-ok', '1');
      var img = card.querySelector('.lyx-card-img img'), sws = card.querySelectorAll('.lyx-sws .lyx-sw');
      if (!img || !sws.length) continue;
      var cur = file(img.getAttribute('src')), on = card.querySelector('.lyx-sws .lyx-sw.is-on'), hit = null;
      if (on && file(on.getAttribute('data-img')) === cur) continue;
      for (var j = 0; j < sws.length && !hit; j++) if (file(sws[j].getAttribute('data-img')) === cur) hit = sws[j];
      if (hit) { if (hit.parentNode.firstElementChild !== hit) hit.parentNode.insertBefore(hit, hit.parentNode.firstElementChild); pick(hit); }
      else if (on && on.getAttribute('data-img')) pick(on);
      else if (on) {
        on.classList.remove('is-on'); on.setAttribute('aria-pressed', 'false');
        var line = card.querySelector('.lyx-card-color');
        if (line) line.style.visibility = 'hidden';
      }
    }
  }

  // 5. Trang lọc theo màu → mọi thẻ hiện ảnh đúng màu (chạy 1 lần mỗi thẻ, sau bước 4)
  function norm(s) { return String(s || '').toLowerCase().replace(/[()]/g, '').replace(/[-_+]+/g, ' ').replace(/\s+/g, ' ').trim(); }
  function wanted() {
    var out = [], q = '';
    var ck = document.querySelectorAll('.filter-item--check-box input:checked');
    for (var c = 0; c < ck.length; c++) out.push(ck[c].getAttribute('data-text') || ck[c].value);
    try { var u = new URLSearchParams(location.search); q = u.get('q') || ''; if (u.get('mau')) out.push(u.get('mau')); } catch (e) {}
    var t = q.match(/tags\s*:\s*\((.*)\)/i);
    if (t) t[1].split(/\)\s*or\s*\(|[()]/i).forEach(function (s) { if (s && !/[:<>]|\band\b/i.test(s)) out.push(s); });
    return out.map(norm).filter(Boolean);
  }
  function applyWanted() {
    var want = wanted();
    if (!want.length) return;
    var cards = document.querySelectorAll('.lyx-card:not([data-lyx-cf])');
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i], all = card.querySelectorAll('.lyx-sws .lyx-sw[data-img]'), sws = [], hit = null, on = card.querySelector('.lyx-sws .lyx-sw.is-on');
      card.setAttribute('data-lyx-cf', '1');
      for (var a = 0; a < all.length; a++) sws.push({ el: all[a], c: norm(all[a].getAttribute('data-c')) });
      if (!sws.length) continue;
      if (on && on.getAttribute('data-img') && want.indexOf(norm(on.getAttribute('data-c'))) > -1) continue;
      /* chỉ xét ô có ảnh; khớp: đúng tên → tên ô chứa tên lọc ("vàng - mã q5" ⊃ "vàng") → tên lọc chứa tên ô ("ghi đậm" ⊃ "ghi", "xanh rêu" ⊃ "rêu") */
      for (var w = 0; w < want.length && !hit; w++) for (var k = 0; k < sws.length && !hit; k++) if (sws[k].c === want[w]) hit = sws[k].el;
      for (var w2 = 0; w2 < want.length && !hit; w2++) for (var k2 = 0; k2 < sws.length && !hit; k2++) if (sws[k2].c.indexOf(want[w2]) > -1) hit = sws[k2].el;
      for (var w3 = 0; w3 < want.length && !hit; w3++) for (var k3 = 0; k3 < sws.length && !hit; k3++) if (sws[k3].c.length > 2 && want[w3].indexOf(sws[k3].c) > -1) hit = sws[k3].el;
      if (hit) { if (hit.parentNode.firstElementChild !== hit) hit.parentNode.insertBefore(hit, hit.parentNode.firstElementChild); pick(hit, true); }
    }
  }

  document.addEventListener('click', function (e) {
    var sw = e.target.closest && e.target.closest('.lyx-card .lyx-sw');
    if (sw) { e.preventDefault(); pick(sw); return; }
    var btn = e.target.closest && e.target.closest('.lyx-card [data-pick]');
    if (!btn) return;
    var on = btn.closest('.lyx-card').querySelector('.lyx-sw.is-on');
    if (!on) return;
    var c = (on.getAttribute('data-c') || '').trim();
    setTimeout(function () {
      var dlg = document.querySelector('dialog.ly-pick[open]');
      if (!dlg || !c) return;
      var opts = dlg.querySelectorAll('.ly-pick-opts button'), hit = null;
      for (var i = 0; i < opts.length && !hit; i++) if (!opts[i].disabled && opts[i].textContent.toLowerCase().indexOf(c) === 0) hit = opts[i];
      if (!hit) return;
      for (var j = 0; j < opts.length; j++) opts[j].setAttribute('aria-checked', String(opts[j] === hit));
      var pr = dlg.querySelector('.ly-pick-price');
      if (pr) pr.textContent = hit.getAttribute('data-price') || '';
      hit.focus();
    }, 0);
  });

  function boot() {
    paint(); match(); applyWanted();
    if (!window.MutationObserver) return;
    var t;
    new MutationObserver(function () { clearTimeout(t); t = setTimeout(function () { paint(); match(); applyWanted(); }, 150); }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();