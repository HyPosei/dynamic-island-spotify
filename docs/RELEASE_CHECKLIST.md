# Release Checklist

Pre-release verification steps for Dynamic Island Spotify Controller.

## 🔍 Before Release

### Code Quality
- [ ] Remove all debug print statements
- [ ] Remove any hardcoded test values
- [ ] Verify no secrets in code (search for API keys, tokens)
- [ ] Run the application and test all features

### Security
- [ ] `.env` is in `.gitignore`
- [ ] `.spotify_cache` is in `.gitignore`
- [ ] No credentials in commit history (`git log -p | grep -i secret`)
- [ ] `.env.example` has placeholder values only

### Documentation
- [ ] README.md is up to date
- [ ] All installation steps work on clean system
- [ ] Screenshots/demo are current
- [ ] License file exists

### Dependencies
- [ ] `requirements.txt` is current
- [ ] All dependencies have version specifiers
- [ ] Test fresh install: `pip install -r requirements.txt`

### Git
- [ ] No untracked secret files
- [ ] Clean working directory: `git status`
- [ ] All changes committed

## 🚀 Release Steps

1. **Final Test**
   ```bash
   # Clean environment test
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python dynamic_island.py
   ```

2. **Version Tag** (optional)
   ```bash
   git tag -a v1.0.0 -m "Initial public release"
   git push origin v1.0.0
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   ```

## ✅ Post-Release

- [ ] Verify repository is public
- [ ] Test clone and setup from scratch
- [ ] Update demo GIF if needed
