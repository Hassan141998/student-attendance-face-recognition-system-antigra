# Neon Database Setup via Vercel Integration (EASIEST METHOD)

## Option 1: Vercel Integration (Recommended - Automatic Setup)

### Step 1: Go to Your Vercel Project
1. Visit: https://vercel.com/dashboard
2. Select your project: `student-attendance-face-recognition-system-antigra`

### Step 2: Add Neon Integration
1. Click **"Storage"** tab (or **"Integrations"** in older UI)
2. Click **"Create Database"** or **"Browse Storage"**
3. Find **"Neon Postgres"** (should be at the top)
4. Click **"Add Integration"** or **"Connect"**

### Step 3: Configure Integration
1. **Authorize** Vercel to connect with Neon
2. **Create new Neon project** or select existing
3. **Project name:** `attendance-system`
4. **Region:** Choose closest to you (e.g., US East)
5. Click **"Create"**

### Step 4: Automatic Environment Variable Setup
Vercel will **automatically**:
- Create the Neon database
- Add `DATABASE_URL` environment variable
- Configure it for all environments

You'll see a success message: "Neon Postgres connected successfully"

### Step 5: Redeploy
1. Go to **Deployments** tab
2. Click **"Redeploy"** on latest deployment
3. Wait 2-3 minutes

### Step 6: Initialize Database
Visit: `https://your-app.vercel.app/init-db`

Expected response:
```json
{"message": "Database initialized successfully! Admin user created (admin/admin123)"}
```

### Step 7: Login
Visit: `https://your-app.vercel.app/login`

Credentials:
- Username: `admin`
- Password: `admin123`

## ✅ Done!

The Vercel integration handles everything automatically - no manual connection string copying needed!

---

## Troubleshooting

**Can't find "Storage" or "Integrations" tab?**
- Try the project Settings → Integrations
- Or visit: https://vercel.com/integrations/neon

**Integration not showing?**
- Search for "Neon" in the integrations marketplace
- Direct link: https://vercel.com/integrations/neon

**Need to check the connection string?**
- Go to Settings → Environment Variables
- You'll see `DATABASE_URL` was added automatically
