# LetsK AI — Website

Personal business site for [www.letskai.com](https://www.letskai.com), built with [Astro 5](https://astro.build).

---

## Running the Site Locally

Before you deploy, you can preview the site on your own computer.

**Requirements:** You need [Node.js](https://nodejs.org) installed (version 18 or higher).

```bash
# 1. Open a terminal in this folder, then install dependencies
npm install

# 2. Start the local development server
npm run dev
```

Open your browser and go to `http://localhost:4321` — you'll see the live site. Any changes you make to files will update instantly.

---

## Deploying to GitHub Pages

This site is configured to deploy automatically to GitHub Pages using GitHub Actions. Here's the full setup, step by step.

---

### Step 1: Create a GitHub Account

If you don't have one, go to [github.com](https://github.com) and sign up. It's free.

---

### Step 2: Install Git

Git is the tool that lets you upload code to GitHub.

- **Mac:** Open Terminal and run `git --version`. If it's not installed, it will prompt you to install it.
- **Windows:** Download from [git-scm.com](https://git-scm.com) and install it.

---

### Step 3: Create a New GitHub Repository

1. Log in to GitHub
2. Click the **+** icon in the top right → **New repository**
3. Name it something like `letskai-site` (or whatever you prefer)
4. Set it to **Public** (required for free GitHub Pages)
5. **Do NOT** check "Add a README file" — leave it empty
6. Click **Create repository**

---

### Step 4: Connect Your Local Folder to GitHub

Open a terminal **inside the `letskai-site` folder** and run these commands one at a time:

```bash
# Initialize a git repository in this folder
git init

# Stage all files
git add .

# Create your first commit
git commit -m "Initial commit"

# Rename the default branch to 'main'
git branch -M main

# Connect to GitHub — replace YOUR_USERNAME and YOUR_REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push your code to GitHub
git push -u origin main
```

> **Example:** If your GitHub username is `kai` and you named the repo `letskai-site`, the remote URL would be:
> `https://github.com/kai/letskai-site.git`

---

### Step 5: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (tab near the top)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Click **Save**

That's it. GitHub will now automatically build and deploy your site every time you push code to the `main` branch. You can watch the progress under the **Actions** tab.

---

### Step 6: Set Up Your Custom Domain (www.letskai.com)

#### Part A — Tell GitHub about your domain

1. In your repo, go to **Settings → Pages**
2. Under **Custom domain**, type `www.letskai.com` and click **Save**

> Note: A file called `CNAME` is already included in the `public/` folder with your domain. GitHub Pages uses this file automatically.

#### Part B — Point your domain to GitHub

Log in to wherever you bought your domain (e.g., GoDaddy, Namecheap, Google Domains) and update your DNS settings:

**For `www.letskai.com` (CNAME record):**

| Type  | Name | Value                       |
|-------|------|-----------------------------|
| CNAME | www  | YOUR_USERNAME.github.io     |

> Replace `YOUR_USERNAME` with your actual GitHub username.

**For the apex domain `letskai.com` (A records) — optional but recommended:**

| Type | Name | Value          |
|------|------|----------------|
| A    | @    | 185.199.108.153 |
| A    | @    | 185.199.109.153 |
| A    | @    | 185.199.110.153 |
| A    | @    | 185.199.111.153 |

DNS changes can take anywhere from a few minutes to 48 hours to fully propagate. Once it's ready, GitHub will also automatically enable **HTTPS** for your domain.

---

## Making Updates

Every time you want to update the website:

1. Edit the files in your code editor
2. Run these three commands in the terminal:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

GitHub Actions will automatically rebuild and redeploy the site. You'll see it live at [www.letskai.com](https://www.letskai.com) within a minute or two.

---

## Customizing the Site

All the page content lives in one file:

```
src/pages/index.astro
```

- **Calendly link:** Search for `calendly.com` in `index.astro` and replace it with your actual Calendly booking URL.
- **Email:** Search for `hello@letskai.com` and update it.
- **Stats & copy:** Edit any text directly in the file.

The layout (HTML head, meta tags) is in:

```
src/layouts/Layout.astro
```

---

## Project Structure

```
letskai-site/
├── public/
│   ├── CNAME              ← Custom domain config
│   └── favicon.svg
├── src/
│   ├── layouts/
│   │   └── Layout.astro   ← HTML head, fonts, global styles
│   └── pages/
│       └── index.astro    ← All page content and styles
├── .github/
│   └── workflows/
│       └── deploy.yml     ← Auto-deploy to GitHub Pages
├── astro.config.mjs
├── package.json
└── tsconfig.json
```
