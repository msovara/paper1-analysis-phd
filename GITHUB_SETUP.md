# GitHub Repository Setup Guide

## ✅ Why Create a GitHub Repo?

**Yes, creating a GitHub repo is the right thing to do!** Here's why:

### Benefits:
1. **Version Control**: Track all changes to your code and analysis
2. **Backup**: Cloud backup of your work - never lose your code
3. **Collaboration**: Share with colleagues, supervisors, or collaborators
4. **Portfolio**: Showcase your research and coding skills
5. **Reproducibility**: Others can reproduce your analysis
6. **Documentation**: Centralized place for all project documentation
7. **Issue Tracking**: Track bugs, feature requests, and tasks
8. **Professional**: Standard practice in scientific computing

### What Gets Committed:
- ✅ All Python scripts and code
- ✅ Configuration files
- ✅ Documentation (Markdown files)
- ✅ Small sample data files (CSV)
- ✅ Requirements files
- ✅ README and guides

### What Gets Excluded (via .gitignore):
- ❌ Large data files (NetCDF, GRIB, Zarr)
- ❌ Output plots and results
- ❌ Model checkpoints
- ❌ Virtual environments
- ❌ SSH keys and credentials
- ❌ Temporary files

## 🚀 Setup Steps

### Step 1: Review Your Current Status

You already have a Git repository initialized! Check status:
```bash
git status
```

You're currently on branch `paper-draft-1` connected to remote `paper-repo`.

### Step 2: Add .gitignore (Already Created)

I've created a comprehensive `.gitignore` file that excludes:
- Large data files (*.nc, *.grib, *.zarr)
- Output directories
- Images and plots
- Virtual environments
- Credentials

### Step 3: Stage Your New Files

Add the new Streamlit files and .gitignore:
```bash
# Add the .gitignore first
git add .gitignore

# Add new Streamlit files
git add streamlit_data_visualizer.py
git add requirements_streamlit.txt
git add README_STREAMLIT.md
git add run_streamlit.bat
git add run_streamlit.sh

# Add the project README
git add README_PROJECT.md
git add GITHUB_SETUP.md

# Review what will be committed
git status
```

### Step 4: Commit Your Changes

```bash
git commit -m "Add Streamlit data visualization dashboard and project documentation"
```

### Step 5: Push to GitHub

**Option A: Push to Existing Remote**
```bash
git push paper-repo paper-draft-1
```

**Option B: Create New GitHub Repository**

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `iod-drought-analysis` (or your preferred name)
4. Description: "Analysis of Indian Ocean Dipole and African drought relationships (1980-2020)"
5. Choose: Public (recommended for research) or Private
6. **DO NOT** initialize with README (you already have files)
7. Click "Create repository"

Then connect your local repo:
```bash
# Add new remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Or if you prefer SSH:
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git push -u origin paper-draft-1
```

### Step 6: Create Main Branch (Optional)

If you want to use `main` as your primary branch:
```bash
# Create and switch to main branch
git checkout -b main

# Push main branch
git push -u origin main

# Set main as default branch on GitHub (via web interface)
```

## 📋 Recommended Repository Structure

Your repository should have:
```
├── README.md (or README_PROJECT.md)  # Main project description
├── .gitignore                        # Excludes large files
├── requirements_*.txt                # Dependencies
├── streamlit_data_visualizer.py      # Interactive dashboard
├── *.py                              # Analysis scripts
├── *.md                              # Documentation
├── configs/                          # Configuration files
├── utils/                            # Utility modules
└── [data/ and output/ excluded]      # Large files not in repo
```

## 🔒 Security Best Practices

1. **Never commit**:
   - API keys or passwords
   - SSH private keys
   - Personal data
   - Large binary files

2. **Use .gitignore** for:
   - Data files (*.nc, *.grib)
   - Output directories
   - Virtual environments
   - IDE settings

3. **If you accidentally commit sensitive data**:
   ```bash
   # Remove from history (use with caution!)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH_TO_FILE" \
     --prune-empty --tag-name-filter cat -- --all
   ```

## 📝 Commit Best Practices

Write clear commit messages:
```bash
# Good commit messages
git commit -m "Add Streamlit dashboard for data visualization"
git commit -m "Fix correlation calculation in composite analysis"
git commit -m "Update documentation for cluster setup"

# Avoid vague messages
git commit -m "updates"  # ❌ Too vague
git commit -m "fix"      # ❌ Not descriptive
```

## 🌿 Branch Strategy

Consider using branches for different work:
```bash
# Create feature branch
git checkout -b feature/streamlit-dashboard

# Work on feature
# ... make changes ...

# Commit and push
git add .
git commit -m "Add new visualization feature"
git push origin feature/streamlit-dashboard

# Merge to main (via GitHub Pull Request or locally)
git checkout main
git merge feature/streamlit-dashboard
```

## 📊 GitHub Features to Use

1. **Issues**: Track bugs, feature requests, tasks
2. **Projects**: Kanban boards for project management
3. **Wiki**: Additional documentation
4. **Releases**: Tag versions of your code
5. **Actions**: CI/CD automation (optional)

## 🎯 Next Steps

1. ✅ Review `.gitignore` - ensure it covers your needs
2. ✅ Stage and commit your new files
3. ✅ Push to GitHub (existing or new repo)
4. ✅ Update README with repository link
5. ✅ Add a license file (if sharing publicly)
6. ✅ Consider adding a `CONTRIBUTING.md` if collaborating

## ❓ Common Questions

**Q: Should I make the repo public or private?**
A: For research, public is often preferred (open science). Use private if you have sensitive data or unpublished work.

**Q: What if my data is too large?**
A: Use Git LFS (Large File Storage) for files >100MB, or host data separately (Zenodo, Figshare, etc.)

**Q: Can I delete the repo later?**
A: Yes, you can delete or make it private at any time.

**Q: Should I commit the paper draft?**
A: Your choice - some prefer to keep drafts private until publication.

---

**Ready to push?** Follow Step 3-5 above to get your code on GitHub! 🚀

