---
title: "Minimum Viable System"
description: "The core prototype implementing KBC"
---

The Minimum Viable System (MVS) demonstrates the core mechanics of KBC and the KnowledgeChain.  It currently consists of a local **FastAPI** backend with a **SQLite** database and a **Streamlit** frontend for interacting with users.

### Components

- **K‑Chain database** – Stores knowledge blocks (“neurons”) with statements, tags, certainty levels and explicit links to related blocks.
- **Users & Ledger** – Keeps track of user profiles and their KBC balances.  Each time a validated knowledge block is added, the contributor’s balance increases.
- **Validator & Oracle placeholders** – Validation logic is rudimentary in v2.1: blocks are marked as pending; future iterations will integrate Oracle AI and Proof‑of‑Knowledge【599027023887502†L175-L181】.
- **Teodora AI (Y‑Engine)** – A planned module that will assist in knowledge validation, synthesis and KBC assignment.

### How to run locally

1. Install Python 3.8+ and clone the repository (or use the `KBC` folder in this site’s source).
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Initialize the database:

   ```bash
   python init_db.py
   ```

4. Start the backend and frontend:

   ```bash
   uvicorn main:app --reload
   streamlit run app.py
   ```

5. Open your browser to the Streamlit URL (default is <http://localhost:8501>) and start adding knowledge.

The current MVS is a local prototype; in the future it will become a decentralized network of validators and AI agents【599027023887502†L191-L198】.

For source code and ongoing development, see the `KBC` directory in this repository.