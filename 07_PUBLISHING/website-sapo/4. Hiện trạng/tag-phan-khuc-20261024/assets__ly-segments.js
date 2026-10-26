/* Phân khúc thảm Harmony / Balance / Mastery (10/2026) + dòng thảm Du lịch / TPE (11/10/2026).
   Dữ liệu lấy từ snippets/ly-segments.bwt (in vào HTML qua data-ly-seg-v / data-ly-seg-name) — file này không khai báo lại danh sách.
   Việc làm: đánh dấu liên kết phân khúc đang xem (menu, chip danh mục), đổi tiêu đề trang /collections/all khi đang xem 1 phân khúc,
   gỡ trạng thái chờ (html.ly-qwait) khi bộ lọc Sapo đã thay xong lưới sản phẩm. */
(function () {
  'use strict';
  var d = document, html = d.documentElement;
  var decode = function (s) { try { return decodeURIComponent(s.replace(/\+/g, ' ')); } catch (e) { return s; } };
  var links = function () { return [].slice.call(d.querySelectorAll('a[data-ly-seg-v]')); };
  var boxes = function () { return [].slice.call(d.querySelectorAll('.ly-filters input[data-ly-seg-box]')); };

  // Phân khúc đang xem: ưu tiên ô đã tích trong bộ lọc; chưa có thì đọc từ đường dẫn (?q=id:(...)).
  function active() {
    var out = [], seen = {};
    var add = function (v, name) { if (v && !seen[v]) { seen[v] = 1; out.push({ v: v, name: name }); } };
    boxes().forEach(function (b) { if (b.checked) add(b.value, b.getAttribute('data-text')); });
    if (out.length) return out;
    var q = decode(location.search);
    if (q.indexOf('id:') < 0 && q.indexOf('tags:') < 0) return out; // 24/10/2026: phân khúc lọc theo tag
    links().forEach(function (a) { var v = a.getAttribute('data-ly-seg-v'); if (q.indexOf(v) > -1) add(v, a.getAttribute('data-ly-seg-name')); });
    return out;
  }

  var hero = d.querySelector('.ly-collection .ly-page-hero h1');
  var heroHTML = hero ? hero.innerHTML : '', titleOrig = d.title;
  var onAll = /^\/collections\/all\/?$/.test(location.pathname);
  var navOther = [].slice.call(d.querySelectorAll('.ly-category-nav a:not([data-ly-seg-v])'));
  var navOtherCur = navOther.map(function (a) { return a.getAttribute('aria-current'); });

  function paint() {
    var act = active(), one = act.length === 1 ? act[0].v : null;
    // Trang sản phẩm: phân khúc của sản phẩm đang xem (nếu có) cũng được đánh dấu trong menu.
    if (!one && !act.length) { var cur = d.querySelector('[data-ly-seg-current]'); if (cur) one = cur.getAttribute('data-ly-seg-current'); }
    links().forEach(function (a) {
      var on = !!one && a.getAttribute('data-ly-seg-v') === one;
      a.classList.toggle('is-current', on);
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    navOther.forEach(function (a, i) {
      if (act.length) a.removeAttribute('aria-current');
      else if (navOtherCur[i]) a.setAttribute('aria-current', navOtherCur[i]);
    });
    if (hero && onAll) {
      if (act.length === 1) {
        var nm = act[0].name;
        hero.textContent = ''; hero.append(nm.toUpperCase(), d.createElement('br'), 'LOUIS YOGA');
        // Dòng thảm đã có chữ "Thảm" trong tên (vd. "Thảm Du lịch") → không lặp "Thảm tập Yoga".
        d.title = (/^thảm\s/i.test(nm) ? nm : 'Thảm tập Yoga ' + nm) + ' – Louis Yoga';
      } else { hero.innerHTML = heroHTML; d.title = titleOrig; }
    }
  }

  // Trạng thái chờ khi mở link lọc sẵn: lưới tạm ẩn tới khi bộ lọc trả kết quả (tối đa 4 giây).
  var release = function () { html.classList.remove('ly-qwait'); };
  if (html.classList.contains('ly-qwait')) setTimeout(release, 4000);
  var box = d.querySelector('.category-products');
  if (box && 'MutationObserver' in window) {
    new MutationObserver(function () { release(); paint(); }).observe(box, { childList: true });
  }

  d.addEventListener('change', function (e) { if (e.target && e.target.closest && e.target.closest('.ly-filters')) setTimeout(paint, 0); });
  window.addEventListener('popstate', paint);
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', paint); else paint();
  window.addEventListener('load', paint);
})();