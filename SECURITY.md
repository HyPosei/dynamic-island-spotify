# Security Policy

## 🔐 Credential Management

This application uses Spotify OAuth credentials that must be kept private.

### Protected Files

The following files are excluded from version control via `.gitignore`:

| File | Contains |
|------|----------|
| `.env` | Spotify API credentials |
| `.spotify_cache` | OAuth access/refresh tokens |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SPOTIPY_CLIENT_ID` | Spotify App Client ID | ✅ |
| `SPOTIPY_CLIENT_SECRET` | Spotify App Secret Key | ✅ |
| `SPOTIPY_REDIRECT_URI` | OAuth callback URL | ✅ |

## ⚠️ If Credentials Are Exposed

### Immediate Actions

1. **Rotate Client Secret**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Select your application
   - Click **Settings** → **Reset client secret**
   - Update your local `.env` with the new secret

2. **Revoke Tokens**
   - Delete `.spotify_cache` file
   - Re-authenticate with new credentials

3. **Check for Abuse**
   - Review Spotify account activity
   - Check API usage in developer dashboard

### Git History Cleanup

If credentials were committed:

```bash
# Remove from history (requires force push)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (destructive!)
git push origin --force --all
```

## 🛡️ Best Practices

1. **Always use `.env`** — Never hardcode credentials
2. **Verify before commit** — Run `git diff --cached`
3. **Use `.gitignore`** — Ensure secret files are ignored
4. **Rotate periodically** — Change secrets every 90 days
5. **Separate environments** — Use different credentials for dev/prod

## 📧 Reporting Vulnerabilities

If you discover a security issue:
1. **Do not** open a public GitHub issue
2. Contact the maintainer privately
3. Allow 48 hours for initial response

## 🔗 References

- [Spotify Developer Terms](https://developer.spotify.com/terms/)
- [OAuth 2.0 Security RFC](https://datatracker.ietf.org/doc/html/rfc6819)
- [Git Secrets Prevention](https://git-scm.com/docs/gitignore)
