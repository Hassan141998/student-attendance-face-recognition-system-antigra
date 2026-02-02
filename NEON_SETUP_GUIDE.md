# Neon Database Setup Guide

## Why Neon?
- ✅ **Free tier never pauses** (unlike Supabase)
- ✅ Perfect for Vercel serverless
- ✅ PostgreSQL compatible
- ✅ Auto-scaling

## Step-by-Step Setup

### 1. Create Neon Account
1. Go to: https://neon.tech
2. Click **"Sign Up"** (use GitHub for quick signup)
3. Verify your email

### 2. Create New Project
1. Click **"Create Project"**
2. **Project Name:** `attendance-system`
3. **Region:** Choose closest to you (e.g., AWS US East for best Vercel compatibility)
4. **PostgreSQL Version:** 16 (default)
5. Click **"Create Project"**

### 3. Get Connection String
After project creation, you'll see a dashboard with connection details.

1. Look for **"Connection Details"** section
2. **Database:** `neondb` (default)
3. **Role:** `neondb_owner` (default)
4. Click **"Connection string"** tab
5. Select **"Pooled connection"** (important for Vercel!)
6. Copy the connection string - it looks like:
   ```
   postgresql://neondb_owner:XXXXX@ep-XXXXX.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### 4. Update Vercel Environment Variable

1. Go to: https://vercel.com/dashboard
2. Select your project: `student-attendance-face-recognition-system-antigra`
3. Click **Settings** → **Environment Variables**
4. Find `DATABASE_URL` and click **Edit** (or delete and add new)
5. **Name:** `DATABASE_URL`
6. **Value:** Paste your Neon connection string from step 3
7. **Environments:** Check all (Production, Preview, Development)
8. Click **Save**

### 5. Redeploy on Vercel

1. Go to **Deployments** tab
2. Click the **"..."** menu on the latest deployment
3. Click **"Redeploy"**
4. Wait 2-3 minutes

### 6. Initialize Database

Once redeployed, visit:
```
https://your-app.vercel.app/init-db
```

You should see:
```json
{"message": "Database initialized successfully! Admin user created (admin/admin123)"}
```

### 7. Test Login

Visit your app:
```
https://your-app.vercel.app/login
```

Login with:
- **Username:** `admin`
- **Password:** `admin123`

## ✅ Done!

Your app is now running on Neon database which won't pause!

---

## Troubleshooting

**If you get "password authentication failed":**
- Make sure you copied the **pooled connection** string (not direct)
- Check that the password in the connection string is correct
- Verify you selected the right database name

**If connection times out:**
- Make sure you selected **"Pooled connection"** in Neon dashboard
- Try a different region closer to your Vercel deployment

**Need help?**
Just let me know what error you see!
