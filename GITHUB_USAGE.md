# How to Use Your GitHub Repository

## 🔗 Your Repository

**Repository URL**: https://github.com/msovara/paper1-analysis-phd

**Current Setup**:
- Remote name: `paper-repo`
- Current branch: `paper-draft-1`
- Main branch: `main`

## 📋 Quick Reference Commands

### Check Status
```bash
git status
```

### Add Files
```bash
# Add specific files
git add filename.py

# Add all changes
git add .

# Add with pattern
git add *.py
```

### Commit Changes
```bash
git commit -m "Description of your changes"
```

### Push to GitHub
```bash
# Push current branch to paper-repo
git push paper-repo paper-draft-1

# Or if branch is already tracking
git push
```

### Pull Latest Changes
```bash
git pull paper-repo paper-draft-1
```

## 🚀 Common Workflows

### 1. Daily Workflow (Making Changes)

```bash
# 1. Check what changed
git status

# 2. See what changed in files
git diff

# 3. Add your changes
git add .

# 4. Commit with message
git commit -m "Add Streamlit dashboard for data visualization"

# 5. Push to GitHub
git push paper-repo paper-draft-1
```

### 2. Starting Fresh (Pull Latest)

```bash
# Pull latest changes from GitHub
git pull paper-repo paper-draft-1

# If there are conflicts, resolve them, then:
git add .
git commit -m "Merge remote changes"
git push paper-repo paper-draft-1
```

### 3. Creating a New Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-analysis

# Make changes, commit
git add .
git commit -m "Add new analysis feature"

# Push new branch
git push paper-repo feature/new-analysis
```

### 4. Switching Branches

```bash
# List all branches
git branch -a

# Switch to main branch
git checkout main

# Switch back to paper-draft-1
git checkout paper-draft-1
```

### 5. Viewing History

```bash
# See commit history
git log

# See changes in a file
git log -p filename.py

# See who changed what
git blame filename.py
```

## 🔄 Working with Remotes

### Your Current Remotes
- `origin`: https://github.com/msovara/tiny_media_analysis_api.git
- `paper-repo`: https://github.com/msovara/paper1-analysis-phd.git ← **Use this one**

### Push to paper-repo (Your Main Repo)
```bash
git push paper-repo <branch-name>
```

### Pull from paper-repo
```bash
git pull paper-repo <branch-name>
```

## 📦 First Time Setup (If Starting Fresh)

If you're cloning this repo on a new machine:

```bash
# Clone the repository
git clone https://github.com/msovara/paper1-analysis-phd.git

# Navigate into directory
cd paper1-analysis-phd

# Check current branch
git branch

# Switch to your working branch
git checkout paper-draft-1
```

## 🎯 Recommended Workflow for Your Project

### For Regular Development:
```bash
# 1. Start your work session
git pull paper-repo paper-draft-1

# 2. Make your changes
# ... edit files ...

# 3. Check what changed
git status
git diff

# 4. Stage changes
git add .

# 5. Commit
git commit -m "Clear description of changes"

# 6. Push
git push paper-repo paper-draft-1
```

### For Major Features:
```bash
# 1. Create feature branch
git checkout -b feature/streamlit-dashboard

# 2. Work on feature
# ... make changes ...

# 3. Commit frequently
git add .
git commit -m "Add Streamlit visualization"

# 4. Push feature branch
git push paper-repo feature/streamlit-dashboard

# 5. When done, merge to main branch
git checkout paper-draft-1
git merge feature/streamlit-dashboard
git push paper-repo paper-draft-1
```

## 🔍 Useful Git Commands

### See What's Different
```bash
# Unstaged changes
git diff

# Staged changes
git diff --staged

# Compare with remote
git diff paper-repo/paper-draft-1
```

### Undo Changes
```bash
# Discard changes to a file (not committed)
git restore filename.py

# Unstage a file
git restore --staged filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - USE CAREFULLY
git reset --hard HEAD~1
```

### View Information
```bash
# Show remote URLs
git remote -v

# Show branch info
git branch -a

# Show commit log
git log --oneline --graph --all
```

## 🌐 GitHub Web Interface

You can also:
- View files: https://github.com/msovara/paper1-analysis-phd
- Create issues
- View commit history
- Create pull requests
- Manage branches
- Download files

## ⚠️ Important Notes

1. **Always commit before pushing**: Changes must be committed before they can be pushed
2. **Write clear commit messages**: Helps you and others understand changes
3. **Pull before push**: If others are working on the repo, pull first
4. **Don't commit large files**: Use `.gitignore` (already set up)
5. **Backup important work**: Git is great, but keep local backups too

## 🆘 Troubleshooting

### "Your branch is ahead of origin"
```bash
# Just push your changes
git push paper-repo paper-draft-1
```

### "Your branch is behind origin"
```bash
# Pull latest changes first
git pull paper-repo paper-draft-1
```

### Merge Conflicts
```bash
# Git will show conflicted files
# Edit files to resolve conflicts
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push paper-repo paper-draft-1
```

### Accidentally committed large file
```bash
# Remove from last commit (but keep file locally)
git reset --soft HEAD~1
git restore --staged large_file.nc
# Add large_file.nc to .gitignore
git add .gitignore
git commit -m "Remove large file and update gitignore"
```

## 📚 Additional Resources

- GitHub Docs: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Desktop (GUI alternative): https://desktop.github.com

---

**Quick Start**: Just remember these three commands:
1. `git add .` - Stage changes
2. `git commit -m "message"` - Save changes
3. `git push paper-repo paper-draft-1` - Upload to GitHub

