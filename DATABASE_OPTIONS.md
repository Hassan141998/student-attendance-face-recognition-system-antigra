# Vercel Postgres Setup (Alternative Option)

If you want to use **Vercel's own database** (simpler):

1. **Install Vercel Postgres:**
   ```bash
   vercel link
   vercel postgres create
   ```

2. **The DATABASE_URL will be set automatically** - no manual configuration needed!

3. **Your app will work immediately**

---

# Current Setup (Neon DB)

If you want to continue with Neon DB, use this connection string in Vercel Environment Variables:

**KEY:** `DATABASE_URL`
**VALUE:** 
```
postgresql://neondb_owner:npg_9daPWGTk7DIx@ep-proud-cloud-ahnnxi3z-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
```

Make sure to **redeploy** after setting the environment variable.

---

# Supabase (Free Alternative)

If Neon doesn't work, try **Supabase** (free tier, very reliable):

1. Go to https://supabase.com and create a project
2. Go to Project Settings → Database
3. Copy the "Connection String" (URI mode)
4. Add it as `DATABASE_URL` in Vercel

The connection string looks like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```
