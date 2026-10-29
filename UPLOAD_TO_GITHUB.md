# Upload GuardKit to GitHub — no coding needed

This guide is written for someone who has never used GitHub before. You do not need to install anything, and you do not need to use a terminal.

## Before you start

- You need the `guardkit/` folder from this project (all files inside it, not just the README).
- If you are using Muse, ask it to give you the `guardkit/` folder as a download / zip. Keep the folder structure exactly as it is — do not move files out of their subfolders.

## Step 1: Create a GitHub account (if you don't have one)

1. Go to github.com
2. Click **Sign up**, enter an email and a password you will remember
3. Verify your email when GitHub asks

## Step 2: Create a new repository

1. On github.com, click the **+** in the top-right, then **New repository**
2. Repository name: `guardkit` (lowercase, one word)
3. Description (copy this):
   > Verify before you trust. Make pipelines faster, greener, reproducible. Seven working tools: SemVer-Diff, TraceLock, WattShift, ShmPipe, SafeOffer, CheckFirst, SecretScan.
4. Choose **Public**
5. Tick **Add a README file** — no, do NOT tick it if you are uploading your own files (you already have a README). Leave it unticked.
6. Click **Create repository**

## Step 3: Upload the files (web upload, no terminal)

1. On your new empty repository page, click **uploading an existing file** (the link in the middle of the page)
2. Drag the *contents* of the `guardkit/` folder into the upload area — or click **choose your files** and select all files and folders inside `guardkit/`
   - Important: upload the contents, not a folder called `guardkit` inside `guardkit`. The top level of the repo should show `README.md`, `kit.py`, `web/`, `checkfirst/`, etc.
   - If GitHub says "too many files", upload in two batches: first the top-level files, then one subfolder at a time.
3. At the bottom, in the commit message box, write: `Initial GuardKit v0.3.0`
4. Click **Commit changes**

## Step 4: Check it worked

1. Go back to the repository main page. You should see the GuardKit README with the seven tools listed.
2. Click `web/index.html` — GitHub will show the file, but it will not run it as a website yet (see Step 5).
3. Click `SUITE_REPORT.md` — this is your proof that all seven tools passed.

## Step 5 (optional, but impressive): Turn on GitHub Pages for the web app

1. In your repository, click **Settings** (top-right tab)
2. On the left, click **Pages**
3. Under **Build and deployment**, Source: choose **Deploy from a branch**
4. Branch: `main`, Folder: `/ (root)` — then Save
5. Wait a minute, then visit `https://<your-username>.github.io/guardkit/web/index.html`
   - That is a live, working CheckFirst + SafeOffer app anyone can try, with no install.

## Step 6: What to write in your submission / portfolio

Copy this, and adjust if you need to:

> GuardKit is a suite of seven Python tools I built and tested as one project. It has two themes: Trust (verify code changes, forwarded messages, job offers, and secrets before you trust them) and Efficiency (provenance, carbon-aware scheduling, and shared-memory data pipes). Each tool works alone, and `python kit.py demo` runs all seven proofs and writes a report. The web app works in a browser with no upload and no install, in English and Bengali.

## Common problems

- **"I uploaded a zip, now I see one zip file"** — GitHub web upload does not unzip. Upload the extracted files, not the zip.
- **"My README looks plain"** — that's normal on first upload. It will render after the page reloads.
- **"Pages shows a 404"** — wait 2 minutes and reload. Check you chose branch `main`, not `master`.
- **"Someone says my code is AI-generated"** — be honest: say you designed and tested it with an AI assistant, and that every demo result in SUITE_REPORT.md was actually run. That is a strength, not a secret.

## What NOT to upload

- Do not upload any file containing a real password, API key, or OTP. Run SecretScan first: `python kit.py secretscan scan .` from the guardkit folder, and fix any finding before you upload.
