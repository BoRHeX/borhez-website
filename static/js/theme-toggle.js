/*
 * Theme toggle persistence
 *
 * This script restores the last chosen theme (dark or light) from
 * localStorage on page load and attaches a click handler to the theme
 * toggle button.  When the user changes the theme, the new value is
 * written back to localStorage so it persists across page reloads.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Restore theme from storage or apply default theme if none exists
  const stored = localStorage.getItem('theme');
  const defaultTheme = 'dark';
  const currentTheme = stored || document.documentElement.getAttribute('data-theme') || defaultTheme;
  document.documentElement.setAttribute('data-theme', currentTheme);
  // Attach toggle handler
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  }
});