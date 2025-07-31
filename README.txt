
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
