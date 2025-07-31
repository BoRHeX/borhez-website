This patch adds a user authentication widget to your Hugo site without
overwriting your existing layout.  It contains a partial template
(`layouts/partials/user-auth.html`) that renders an email/password
login form with register, login and logout buttons.  To activate the
widget:

1. Copy the `layouts/partials/user-auth.html` file from this patch into
   your site's `layouts/partials/` directory.  For example:

       cp -R auth_form_patch/layouts/partials/* your-site/layouts/partials/

2. Open your site's `layouts/_default/baseof.html` (or the
   corresponding layout file from your theme) and insert the
   following snippet just before the closing `</body>` tag:

       {{ partial "user-auth.html" . }}
       <script type="module" src="/js/firebase-config.js"></script>
       <script type="module" src="/js/auth.js"></script>

   This will render the widget and load your Firebase scripts on every
   page.  If you wish to enable it conditionally, wrap the partial
   call in an `if` block using `{{ if .Site.Params.auth }}`.

3. Ensure you have populated `/static/js/firebase-config.js` with your
   Firebase project credentials and that `/static/js/auth.js` contains
   the authentication logic.

4. Set `params.auth = true` in your site's configuration (`config.toml`) if you
   plan to wrap the widget in an `if` block.

After applying these steps, rebuild your site.  The existing PaperMod
layout will remain intact, and the authentication form will appear
where you inserted it.