# Google OAuth Setup Instructions

This guide will help you set up Google OAuth authentication for the admin dashboard.

## Step 1: Google Cloud Console Setup

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Create a new project or select an existing one
   - Project name suggestion: "Personal Website"

3. **Enable Google+ API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" or "Google People API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Name: "Personal Website Auth"

5. **Configure Authorized Redirect URIs**
   Add these URIs (replace with your actual domains):

   **For Development:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```

   **For Production:**
   ```
   https://yourdomain.com/accounts/google/login/callback/
   ```

6. **Get Your Client Credentials**
   - After creating, you'll get:
     - Client ID (starts with numbers)
     - Client Secret
   - Keep these safe!

## Step 2: Django Configuration

1. **Set Environment Variable**
   Add to your `.env` file:
   ```
   ALLOWED_ADMIN_EMAIL=your-email@gmail.com
   ```
   Replace with the exact Gmail address you want to grant admin access to.

2. **Add Google OAuth App in Django Admin**
   - Start your development server: `uv run python manage.py runserver`
   - Go to: http://localhost:8000/admin/
   - Login with Django superuser
   - Navigate to "Social Applications" > "Add Social Application"
   - Fill in:
     - Provider: Google
     - Name: Google OAuth
     - Client ID: (from Google Console)
     - Secret: (from Google Console)
     - Sites: Select your site (usually "example.com")

## Step 3: Testing

1. **Test Login Flow**
   - Go to: http://localhost:8000/accounts/google/login/
   - Should redirect to Google
   - Login with your Gmail account
   - Should redirect back to your dashboard

2. **Test Access Control**
   - Only the email specified in `ALLOWED_ADMIN_EMAIL` should access `/dashboard/`
   - Other emails should see "Access Denied"

## Step 4: Production Deployment

1. **Update OAuth Settings**
   - Add production domain to authorized redirect URIs
   - Update `ALLOWED_HOSTS` in Django settings

2. **Security Considerations**
   - Use environment variables for secrets
   - Enable HTTPS in production
   - Set secure CSRF settings

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Check that your redirect URI exactly matches what's in Google Console
- Make sure to include the trailing slash

### Error: "Access Denied" for your email
- Verify `ALLOWED_ADMIN_EMAIL` matches your Google account email exactly
- Check for typos or extra spaces

### Error: "OAuth app not found"
- Make sure you created the Social Application in Django admin
- Verify the Client ID and Secret are correct

## Security Notes

- Only one email address can access admin (your Gmail)
- Users with other emails will be denied access
- Google handles all authentication security
- No passwords to manage or store

## Next Steps

After OAuth is working:
- Week 2: Project Management Interface
- Week 3: Blog Management Interface
- Week 4: Advanced Features & Polish
