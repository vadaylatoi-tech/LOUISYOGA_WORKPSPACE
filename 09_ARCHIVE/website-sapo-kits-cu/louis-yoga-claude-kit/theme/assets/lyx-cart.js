/* Louis Yoga — giỏ trượt theo bản thiết kế 15/10/2026 (mobile trang 10–11). Gọi từ snippets/ly-cart-drawer.bwt.
   assets/ly-cart.js vẫn vẽ dòng sản phẩm/tổng tiền; tệp này chỉ: trạng thái trống theo thiết kế, ẩn gợi ý đã có trong giỏ,
   nút "+" thêm sản phẩm gợi ý (/cart/add.js như ly-cart.js) có chống nhấp lặp và báo lỗi. */
(() => {
  'use strict';
  const d = document, $ = (s, r = d) => r.querySelector(s), $$ = (s, r = d) => [...r.querySelectorAll(s)];
  const dlg = $('#ly-cart');
  if (!dlg || dlg.dataset.lyx) return;
  dlg.dataset.lyx = '1';
  const list = $('#ly-cart-items', dlg), up = $('[data-lyx-up]', dlg);
  const say = msg => {
    const t = $('#ly-toast');
    if (t) { t.textContent = msg; t.classList.add('is-visible'); setTimeout(() => t.classList.remove('is-visible'), 3500); }
  };
  const post = () => {
    const empty = $('.ly-cp-empty', list);
    dlg.classList.toggle('is-empty', !!empty);
    if (empty && !empty.dataset.lyx) {
      empty.dataset.lyx = '1';
      const a = $('a', empty);
      if (a) { a.textContent = 'Tiếp tục mua sắm'; a.classList.add('lyx-cart-cta'); }
      if (dlg.dataset.login) {
        const p = d.createElement('p'); p.className = 'lyx-cart-login';
        const l = d.createElement('a'); l.href = dlg.dataset.login; l.textContent = 'Đăng nhập';
        p.append(l, ' để thanh toán nhanh hơn');
        empty.append(p);
      }
    }
    if (up) {
      const inCart = new Set($$('.ly-line', list).map(l => l.dataset.vid));
      let n = 0;
      $$('.lyx-up-item', up).forEach(it => { const on = !inCart.has(it.dataset.vid) && n < 3; it.hidden = !on; if (on) n++; });
      up.hidden = !!empty || !list.children.length || n === 0;
    }
  };
  new MutationObserver(post).observe(list, { childList: true });
  post();

  if (up) up.addEventListener('click', async e => {
    const b = e.target.closest('[data-lyx-add]');
    if (!b) return;
    e.preventDefault();
    if (b.disabled) return;
    b.disabled = true; b.classList.add('is-busy');
    try {
      const r = await fetch('/cart/add.js', { method: 'POST', credentials: 'same-origin', headers: { Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' }, body: new URLSearchParams({ variantId: b.dataset.lyxAdd, quantity: 1 }) });
      if (!r.ok) { let m = ''; try { const j = await r.json(); m = j.description || j.message || ''; } catch (_) {} throw new Error(m || 'Không thêm được sản phẩm. Sản phẩm có thể đã hết hàng.'); }
      if (window.LYCart && window.LYCart.refresh) await window.LYCart.refresh();
      d.dispatchEvent(new CustomEvent('ly:cart-updated'));
    } catch (err) {
      say(err.message || 'Không thêm được sản phẩm, vui lòng thử lại.');
    } finally {
      b.disabled = false; b.classList.remove('is-busy');
    }
  });
})();
