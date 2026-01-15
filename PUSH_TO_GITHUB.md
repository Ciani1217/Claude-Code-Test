# Push to GitHub - Instructions

Your code is ready and committed locally. To push to GitHub, you have a few options:

## Option 1: Using GitHub CLI (Easiest)

If you have GitHub CLI installed:

```bash
cd "/Users/cianiherbert/Desktop/CLAUDE CODE TEST"
gh auth login
git push -u origin main
```

## Option 2: Using Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name it: "Neural Interface"
   - Select scopes: `repo` (all checkboxes under "repo")
   - Click "Generate token"
   - Copy the token (you'll only see it once!)

2. **Push using the token:**
   ```bash
   cd "/Users/cianiherbert/Desktop/CLAUDE CODE TEST"
   git push -u origin main
   ```
   - When prompted for username: `Ciani1217`
   - When prompted for password: paste your Personal Access Token (not your GitHub password!)

## Option 3: Set Up SSH Keys (For Future)

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add to SSH agent:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. Copy public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

4. Add to GitHub:
   - Go to: https://github.com/settings/ssh/new
   - Paste your public key
   - Save

5. Update remote and push:
   ```bash
   cd "/Users/cianiherbert/Desktop/CLAUDE CODE TEST"
   git remote set-url origin git@github.com:Ciani1217/Claude-Code-Test.git
   git push -u origin main
   ```

## Quick Command (After getting token)

```bash
cd "/Users/cianiherbert/Desktop/CLAUDE CODE TEST"
git push -u origin main
# Username: Ciani1217
# Password: [paste your Personal Access Token]
```
