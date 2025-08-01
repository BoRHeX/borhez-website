// Persist dark/light theme across page loads and sync with the theme toggle
(function() {
  // Determine the default theme from the site config
  const defaultTheme = (function() {
    // This placeholder will be replaced by Hugo at render time if you
    // choose to inject a default theme here via templating.  Otherwise
    // fallback to 'light'.
    return 'dark';
  })();
  const saved = localStorage.getItem('theme');
  const theme = saved || defaultTheme;
  document.documentElement.setAttribute('data-theme', theme);
  document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', current);
        localStorage.setItem('theme', current);
      });
    }
  });
})();