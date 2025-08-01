Knowledge‑Based Currency Website
This repository contains the official website of Knowledge‑Based Currency (KBC). The site is built with Hugo using the PaperMod theme and presents a comprehensive overview of the KBC project, its philosophy and its technical underpinnings. It includes custom pages, a client‑side authentication widget, automated blog generation and links to deeper resources.

Project overview
KBC is a novel economic system where verified knowledge acts as currency. Each token represents a piece of information that has been validated and recorded on the KnowledgeChain ledger. The KBC site introduces the main concepts and provides entry points into the wider ecosystem:

About – background on the project and its originator, Master BoRHeZ, along with the mission, values and history of KBC.

K‑Chain – explains the decentralized ledger that stores knowledge blocks; each block contains content, metadata and links to other blocks, and is validated via a Proof‑of‑Knowledge process
GitHub
.

LightWeb – outlines a future decentralized web layer built on top of the KnowledgeChain.

Oracle AI – introduces the AI system that validates submissions and synthesizes new insights from the chain
GitHub
.

MVS (Minimum Viable System) – details a prototype comprising a FastAPI backend, SQLite database and Streamlit frontend; it demonstrates the core mechanics of KBC and provides setup instructions for local development
GitHub
.

Resources – lists whitepapers and research documents in the KBC/Resources directory
GitHub
.

Blog – houses posts and daily updates; an automated workflow generates new posts via the OpenAI API.

The repository also includes a contact page and a Get Involved section encouraging collaboration.

Key features
Dark/light theme customisation – Additional CSS in assets/css/extended/custom.css overrides PaperMod colours, constrains the main content width and displays an “under construction” banner. These overrides are configured via config.toml.

Firebase‑powered authentication widget – A partial template (layouts/partials/user-auth.html) renders a simple email/password form. The accompanying JavaScript (static/js/auth.js) initialises Firebase, handles register/login/logout events and updates the UI based on authentication state
GitHub
. A placeholder configuration lives in static/js/firebase-config.js and should be filled with your Firebase project credentials. To enable the widget site‑wide, set params.auth = true in config.toml
GitHub
.

Under‑construction alert – The site-alert.html partial inserts a fixed message at the top of every page, signalling that the site is a work in progress.

Blog automation – A Python script (scripts/generate_blog_post.py) uses OpenAI to generate ~600‑word posts based on daily summaries or selected topics. A GitHub Actions workflow (.github/workflows/blog_automation.yml) runs twice daily to generate a post, rebuild the site and commit the results to the repository.

Custom menu and social links – The navigation bar is defined in config.toml and links to the various sections of the site. Social links for Twitter/X and YouTube are configured in the same file
GitHub
.

Content pages – All page content lives in the content/ directory as Markdown files with front matter. New pages can be added simply by creating additional files in this directory and updating the menu configuration if necessary.

Repository structure
bash
Copy
Edit
├── config.toml               # Site configuration – base URL, theme, menus and parameters
├── content/                  # Markdown source for pages and posts
│   ├── _index.md             # Home page
│   ├── about.md              # About the project and mission:contentReference[oaicite:7]{index=7}
│   ├── k-chain.md            # KnowledgeChain description:contentReference[oaicite:8]{index=8}
│   ├── lightweb.md           # LightWeb vision
│   ├── oracle-ai.md          # Oracle AI overview:contentReference[oaicite:9]{index=9}
│   ├── mvs.md                # Minimum Viable System details:contentReference[oaicite:10]{index=10}
│   ├── resources.md          # List of research documents:contentReference[oaicite:11]{index=11}
│   ├── get-involved.md       # How to participate
│   ├── contact.md            # Contact form
│   └── posts/                # Blog posts (e.g. what-is-kbc.md)
├── layouts/
│   ├── _default/
│   │   ├── baseof.html       # Master layout with header/footer and authentication widget slot
│   │   └── single.html       # Template for single pages
│   └── partials/
│       ├── site-alert.html   # “Under construction” notice
│       ├── extend_footer.html# Footer extension message
│       └── user-auth.html    # Authentication form partial
├── assets/css/extended/
│   ├── custom.css            # Theme overrides and banner styling
│   └── auth.css              # Authentication widget styles
├── static/js/
│   ├── auth.js               # Firebase auth logic:contentReference[oaicite:12]{index=12}
│   └── firebase-config.js    # Firebase config (update with your credentials)
├── static/images/            # Logo and favicon assets
├── scripts/
│   └── generate_blog_post.py # Automated blog post generator
├── .github/workflows/
│   └── blog_automation.yml   # CI workflow to run the blog generator
└── README.md                 # You are here
Running the site locally
Install Hugo – Download the Hugo extended version for your platform and add it to your PATH.

Clone this repository – Use git clone to obtain the source. Make sure submodules are fetched if you choose to add themes as submodules.

Configure Firebase (optional) – To enable the authentication widget, edit static/js/firebase-config.js with your project credentials. Set params.auth = true in config.toml to render the widget globally.

Start the development server – Run hugo server --buildDrafts to start a local server. Visit http://localhost:1313 to preview the site.

Generate and publish posts – The scripts/generate_blog_post.py script can be run manually by providing an OPENAI_API_KEY environment variable. The GitHub Actions workflow will run it automatically twice a day when deployed.

Working with the MVS
The Minimum Viable System (MVS) codebase is part of the broader KBC project and is referenced from this website. To experiment with it locally:

Ensure Python 3.8+ is installed.

Clone or navigate to the KBC directory in this repository (if present).

Create a virtual environment and install dependencies:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Initialise the database:

bash
Copy
Edit
python init_db.py
Start the backend and frontend:

bash
Copy
Edit
uvicorn main:app --reload
streamlit run app.py
Open your browser to the indicated Streamlit URL and begin adding knowledge blocks. Note that the current MVS is a local prototype; future versions will evolve into a decentralized network
GitHub
.

Resources
The content/resources.md page lists a number of research documents and whitepapers stored in the KBC/Resources directory. These include:

KBC.docx – comprehensive overview of KBC history, principles and technical backbone.

KBC Genesis Block Creation.docx – analysis of the initial tokenomics.

KnowledgeChain (K‑Chain) Whitepaper.docx – technical description of the ledger and Proof of Knowledge.

Building the LightWeb Research Plan.docx – roadmap for the decentralized web layer.

What is KBC_.docx – introduction to KBC (supplement to the blog post).

Next steps and roadmap (MVS v2.x Focus).docx – plan for the MVS evolution.

Teodora KBC MVS docx – documentation of the current MVS implementation.

Knowledge‑Based Currency – The Eternal Force of Value.docx – exploration of why knowledge‑backed currency endures.

Light of Knowledge.docx – study of information in the LightWeb ecosystem.

The Y‑Engine.docx – conceptual design of the Oracle AI subsystem.

Open Letter & Manifesto for Knowledge‑Based Currency.docx – call for collaboration and guiding principles.

These documents are not tracked in the website build but are valuable references for understanding the broader project.

Contributing
Contributions to KBC are welcome! Here are a few ways to get involved:

Improve the website – Edit or add pages in the content/ directory, enhance layouts, or refine the CSS.

Expand the MVS – Work on the FastAPI/Streamlit prototype. The MVS is the backbone of the knowledge ledger, and improvements here directly impact the project.

Write blog posts – Submit your own posts or refine the automated ones. Posts live under content/posts/ and follow Hugo’s Markdown front matter.

Review research documents – Read the whitepapers in KBC/Resources and provide feedback or propose changes.

Join the community – Reach out via the contact page or open an issue to introduce yourself and describe how you’d like to contribute.

Keeping this README up to date
This README aims to serve as the primary source of truth for the repository. Whenever you add new features, scripts or pages, update this file accordingly. Documenting processes here reduces cognitive overhead, makes it easier for new contributors to onboard and helps automate repetitive tasks.

Knowledge‑Based Currency unites economics with truth. By building this site and the tools around it, we invite the world to participate in a future where knowledge is the ultimate asset.