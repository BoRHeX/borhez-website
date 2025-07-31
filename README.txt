This patch provides the necessary files to integrate Firebase email/password
authentication into your Hugo-based website.  Drop the contents of the
`auth_patch` directory into your site's root (merging with existing
`layouts` and `static` directories) and ensure your configuration
enables the authentication widget.

Files included:

* `layouts/_default/baseof.html` – A simple base layout that renders
  your page content and conditionally injects the user authentication
  widget when `params.auth` is true in your config.  It also loads
  the Firebase and auth scripts at the bottom of the page.

* `layouts/partials/user-auth.html` – The authentication widget.  It
  contains email and password fields, buttons for registration,
  login and logout, and status/error messages.  You can include this
  partial in any template with `{{ partial "user-auth.html" . }}`.

Usage:

1. Copy the files into your Hugo project:

       cp -R auth_patch/layouts/* your-site/layouts/
       cp -R auth_patch/static/js/* your-site/static/js/

2. In your `config.toml` or equivalent, enable the auth widget by
   setting `params.auth = true`.

3. Ensure that `firebase-config.js` and `auth.js` exist in your
   project's `static/js` directory and contain your Firebase
   configuration and authentication logic, respectively.

4. Build and deploy your site.  The authentication widget should
   appear at the bottom of each page if enabled in the configuration.