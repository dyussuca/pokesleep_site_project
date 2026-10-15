// 全ページ共通のテーマ制御: 保存値 (pokesleep_theme) > OS設定。Ctrl+Shift+L で切替。
// <head> で同期読み込みし、描画前にテーマを確定させてチラつきを防ぐ。
(function () {
  const KEY = 'pokesleep_theme';
  const LEGACY_KEY = 'exp_sim_theme';
  const root = document.documentElement;
  const media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function savedTheme() {
    try {
      const v = localStorage.getItem(KEY) || localStorage.getItem(LEGACY_KEY);
      return v === 'dark' || v === 'light' ? v : null;
    } catch (e) {
      return null;
    }
  }

  function resolveTheme() {
    return savedTheme() || (media && media.matches ? 'dark' : 'light');
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  // テーマ以外の通知 (トップの備蓄セット完了など) からも使う
  function showThemeToast(msg) {
    const toast = document.getElementById('theme-toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => { toast.classList.remove('show'); }, 2000);
  }

  window.showThemeToast = showThemeToast;
  window.toggleTheme = function () {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(KEY, next); } catch (e) { /* 保存不可でも表示は切り替える */ }
    applyTheme(next);
    showThemeToast(next === 'dark' ? '🌙 ダークモードに切り替えました' : '☀️ ライトモードに切り替えました');
  };

  applyTheme(resolveTheme());
  if (media && media.addEventListener) {
    media.addEventListener('change', () => { if (!savedTheme()) applyTheme(resolveTheme()); });
  }
  document.addEventListener('DOMContentLoaded', () => applyTheme(root.getAttribute('data-theme')));
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 'L' || e.key === 'l' || e.code === 'KeyL')) {
      e.preventDefault();
      window.toggleTheme();
    }
  });
})();
