This repository contains the sources for the borhez.com website built with
Hugo using the PaperMod theme. It includes custom styling, a Firebase
authentication widget and an automated blog generation workflow.

## Authentication and Theme

* **Firebase Email/Password auth** – The login/register form lives in
  `layouts/partials/user-auth.html`. The corresponding logic is in
  `static/js/auth.js`, which imports your Firebase project credentials
  from `static/js/firebase-config.js`. Make sure you have enabled
  Email/Password sign‑in in the Firebase console and that your site’s
  domain is authorised. The widget appears on every page when
  `params.auth = true` is set in `config.toml`.

* **Colour palette** – Custom CSS variables define a black/gold/red
  palette for both dark and light modes. These variables live in
  `assets/css/extended/custom.css`. A small script at
  `static/js/theme-toggle.js` persists the user’s theme preference using
  `localStorage`. The default is dark mode. You can toggle themes via
  the built‑in PaperMod switcher.

## Automated Blog Posts

* **GitHub Actions workflow** – The file
  `.github/workflows/blog_automation.yml` defines a job that runs twice
  daily (midnight and noon UTC) and on manual dispatch. It generates a
  ~600‑word blog post using the OpenAI API, builds the static site with
  Hugo and commits the results back to the repository.

* **Secrets required** – To use this automation, you **must** add a
  repository secret named `OPENAI_API_KEY` containing your OpenAI API
  key. Without this secret, the script will exit immediately and the
  workflow will fail. Optionally, you can set `CHAT_SUMMARY_PATH` to
  point to a text file containing your own summary to include in the
  prompt; if unset, the script chooses a random topic.

* **Write permissions** – The workflow includes
  `permissions: contents: write` so it can push commits. If your branch
  has protection rules, ensure that GitHub Actions is allowed to bypass
  them or adjust the settings accordingly.

* **Customising frequency** – The schedule is defined via cron in the
  workflow. Adjust these expressions to change how often posts are
  generated. For testing, you can trigger the workflow manually via
  the GitHub UI.

## Running Locally

To build the site locally, install Hugo extended (version 0.146.0 or
greater) and run:

```
hugo --minify
```

The generated site will appear in the `public/` directory. Use a
simple HTTP server to preview the pages.