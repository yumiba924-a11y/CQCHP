/* CQC site-wide JS — scroll reveal (IntersectionObserver) */
(function () {
  if (!('IntersectionObserver' in window)) return;

  /* 監視対象セレクタ（写真は除外） */
  var selectors = [
    '.section-header',
    '.chairman__pull',
    '.chairman__body',
    '.president__pull',
    '.president__body',
    '.gap-network__h2',
    '.gap-network__lead',
    '.gap-network__map',
    '.gap-network__cta',
    '.transactions__cta',
    '.track-record__note',
    '.pillar-card',
    '.person-card',
    '.track-grid .tx-card',
    '.leader-mini',
    '.group-card',
    '.about-table',
    '.access__info',
    '.access__map',
    '.gap-stat',
    '.track-stats__item',
    '.track-tabs'
  ];

  var targets = document.querySelectorAll(selectors.join(','));
  if (!targets.length) return;

  targets.forEach(function (t) { t.setAttribute('data-anim', ''); });

  /* 同一セクション内のスタガード（出現順に 0.1s 遅延） */
  var sections = document.querySelectorAll(
    '.section, .chairman, .president, .transactions, .gap-network, ' +
    '.access, .team-section, .members-section, .track-section'
  );
  sections.forEach(function (sec) {
    var inSec = sec.querySelectorAll('[data-anim]');
    inSec.forEach(function (el, idx) {
      if (idx > 0 && idx <= 4) el.setAttribute('data-anim-delay', String(idx));
    });
  });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

  targets.forEach(function (t) { observer.observe(t); });
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
