/* CQC site-wide JS — header scroll state */
(function () {
  var header = document.querySelector('.site-header');
  if (!header) return;

  var SCROLL_THRESHOLD = 60;  // ヒーロー透過 → 白背景 切替閾値（px）
  var ticking = false;

  function update() {
    var scrolled = window.scrollY > SCROLL_THRESHOLD;
    header.classList.toggle('is-scrolled', scrolled);
    ticking = false;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  update();  // 初期化
})();

/* CQC site-wide JS — hamburger nav toggle */
(function () {
  var toggle = document.querySelector('.site-nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (!toggle || !nav) return;

  function setOpen(open) {
    toggle.classList.toggle('is-open', open);
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
  }

  toggle.addEventListener('click', function () {
    setOpen(!toggle.classList.contains('is-open'));
  });

  // ナビ内リンクをタップしたら閉じる
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') setOpen(false);
  });

  // ESC で閉じる
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && toggle.classList.contains('is-open')) setOpen(false);
  });

  // デスクトップ幅に戻ったら強制クローズ
  var mq = window.matchMedia('(min-width: 769px)');
  mq.addEventListener && mq.addEventListener('change', function (e) {
    if (e.matches) setOpen(false);
  });
})();
