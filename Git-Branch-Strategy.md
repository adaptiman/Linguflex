# Git Branch Management Strategy

## Recommended Approach: Feature Branch + Selective Commits

Given your specific needs to keep instapaper module changes separate while maintaining a full fork, here's the recommended workflow:

### 1. Create Two Tracking Branches

```bash
# Create branch for clean instapaper-only changes
git checkout -b instapaper-module-only

# Create branch for your complete fork with all changes  
git checkout -b david-full-fork
```

### 2. Daily Development Workflow

**Work in `david-full-fork` for everything:**
```bash
git checkout david-full-fork
# Make all your changes here - instapaper + other modules
```

**When you make instapaper changes, commit them separately:**
```bash
# Stage only instapaper files
git add lingu/modules/instapaper/
git commit -m "instapaper: add new feature X"

# Then commit other changes separately
git add .
git commit -m "other: update weather handler, fix UI issues, etc."
```

### 3. Sync Instapaper Branch

**Extract instapaper commits to clean branch:**
```bash
# Switch to clean instapaper branch
git checkout instapaper-module-only

# Cherry-pick only the instapaper commits
git cherry-pick <instapaper-commit-hash>
```

### 4. Push Appropriately

```bash
# Push instapaper-only changes to upstream instapaper branch
git push origin instapaper-module-only:instapaper

# Push your complete fork to your own branch
git push origin david-full-fork
```

### 5. Alternative: Use Git Aliases for Efficiency

Add these to your `.gitconfig` for easier workflow:
```bash
git config alias.add-instapaper "add lingu/modules/instapaper/"
git config alias.commit-instapaper "commit -m"
```

Then use:
```bash
git add-instapaper
git commit-instapaper "instapaper: your message"
```

### Benefits of This Approach

- ✅ **Clean separation** of instapaper vs. other changes
- ✅ **Full control** of both codebases  
- ✅ **Easy to maintain** upstream compatibility
- ✅ **Preserves commit history** for both branches
- ✅ **Flexible workflow** - work on everything in one place, selectively sync

## Alternative Strategies (If Needed)

### Strategy 2: Use Git Worktrees (Advanced)

Set up separate working directories:
```bash
# Create worktrees for different purposes
git worktree add ../linguflex-instapaper instapaper
git worktree add ../linguflex-full main

# Work in appropriate directories
cd ../linguflex-instapaper      # Only commit instapaper changes here
cd ../linguflex-full            # All changes here
```

### Strategy 3: Selective Staging (Manual)

Daily workflow:
```bash
# Stage only instapaper files for instapaper branch
git checkout instapaper
git add lingu/modules/instapaper/
git commit -m "instapaper: your changes"

# Keep all other changes in your main development branch
git checkout my-main-branch
git add .
git commit -m "all changes including instapaper and others"
```

## Quick Reference Commands

### Initial Setup
```bash
git checkout -b instapaper-module-only
git checkout -b david-full-fork
```

### Daily Work
```bash
# Work in david-full-fork
git checkout david-full-fork

# Separate commits
git add lingu/modules/instapaper/
git commit -m "instapaper: feature description"
git add .
git commit -m "other: changes description"

# Sync to clean branch
git checkout instapaper-module-only
git cherry-pick <commit-hash>
```

### Push Changes
```bash
git push origin instapaper-module-only:instapaper
git push origin david-full-fork
```

## Notes

- Always commit instapaper changes separately from other changes
- Use descriptive commit messages with "instapaper:" prefix for easy identification
- Cherry-pick preserves commit history and authorship
- Your fork maintains full control while keeping upstream compatibility