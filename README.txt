<<<<<<< HEAD
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
=======

Firebase Email/Password Auth Setup for Hugo (PaperMod)
-----------------------------------------------------

This package provides the files needed to add client-side email/password authentication to a Hugo site using Firebase.

Files:
  /static/js/firebase-config.js   – Placeholder for your Firebase project config.  Replace the values with your project’s credentials.
  /static/js/auth.js              – Authentication logic for register, login, logout and session handling.
  /layouts/partials/user-auth.html – An HTML partial you can include in any page via `{{ partial "user-auth.html" . }}`.

Setup Steps:
1. **Create/Select a Firebase Project**
   • Go to https://console.firebase.google.com and create a project (or use an existing one).

2. **Enable Email/Password Auth**
   • Navigate to *Build → Authentication → Sign-in method*.
   • Enable the Email/Password provider.

3. **Register a Web App**
   • In *Project settings → General → Your apps*, click “Add app” and choose the Web icon.
   • You do not need Firebase Hosting; just register the app.
   • Copy the config snippet shown (apiKey, authDomain, projectId, etc.).
   • Paste these values into `static/js/firebase-config.js`.

4. **Include the Scripts in your Hugo Layout**
   • Add the following tags to your `layouts/_default/baseof.html` (just before `</body>`):
     ```html
     <script type="module" src="/js/firebase-config.js"></script>
     <script type="module" src="/js/auth.js"></script>
     ```
   • Insert the user auth partial wherever you want the login UI (e.g., in your navbar or footer):
     ```go
     {{ partial "user-auth.html" . }}
     ```

5. **Enable Comments in config (Optional)**
   • If you want to control whether the auth widget appears site-wide, you can expose a parameter in `config.toml` such as `[params] auth = true` and conditionally render the partial in your templates.

Notes:
- This uses Firebase JS SDK v10 (modular API) loaded via ES modules from Google’s CDN.  Make sure your site does not block these scripts.
- All authentication happens client-side; the Hugo site remains fully static.
- No third-party providers (Google, GitHub) are configured here; only email/password.

Once set up, users can register, log in, and log out using the auth widget.  The current user’s email is displayed when signed in.
>>>>>>> parent of e31aab2 (auth patch)
