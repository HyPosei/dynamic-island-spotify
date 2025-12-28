# Security Policy

## 🔐 Handling Secrets

**NEVER commit sensitive data to the repository!**

### Protected Files
The following files contain secrets and are excluded via `.gitignore`:
- `.env` - Contains your Spotify API credentials
- `.spotify_cache` - Contains authentication tokens

### What to Keep Secret
- `SPOTIPY_CLIENT_ID` - Your Spotify application client ID
- `SPOTIPY_CLIENT_SECRET` - Your Spotify application secret key
- OAuth tokens and refresh tokens

## ⚠️ If Credentials Are Leaked

If you accidentally exposed your Spotify API credentials:

### 1. Immediately Rotate Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Select your application
3. Click "Settings" → "Reset client secret"
4. Copy the new secret
5. Update your local `.env` file with the new secret

### 2. Revoke Existing Tokens
1. Delete the `.spotify_cache` file from your project
2. Re-authenticate with the new credentials

### 3. Check for Unauthorized Access
1. Review your Spotify account activity
2. Check for any unusual API calls in your dashboard

## 🛡️ Best Practices

1. **Use environment variables** - Never hardcode credentials
2. **Check before commits** - Use `git diff --cached` to review staged changes
3. **Use .gitignore** - Ensure secret files are always ignored
4. **Separate environments** - Use different credentials for development/production
5. **Regular rotation** - Rotate API secrets periodically

## 📧 Reporting Security Issues

If you discover a security vulnerability in this project:
1. **DO NOT** open a public GitHub issue
2. Contact the maintainer privately
3. Provide detailed information about the vulnerability

## 🔗 Resources

- [Spotify API Terms of Service](https://developer.spotify.com/terms/)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/rfc6819)
