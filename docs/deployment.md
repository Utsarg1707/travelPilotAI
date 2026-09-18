# TravelPilot AI — Free Cloud Deployment Guide

This guide details step-by-step instructions for deploying **TravelPilot AI** publicly on 100% free-tier cloud infrastructure:
- **Frontend**: Vercel (Free Hobby Tier)
- **Backend**: Render (Free Web Service - Docker)
- **Database**: Supabase (Free PostgreSQL Database)
- **LLM**: Groq API (Free Tier)
- **Weather API**: Open-Meteo (Free REST API)

---

## 🏗️ Architecture Overview

```text
               GitHub Repository
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
   Vercel Free                 Render Free
 (React Frontend)            (FastAPI Backend)
                                    │
                       ┌────────────┼────────────┐
                       ▼            ▼            ▼
                   LangGraph   MCP Servers     Groq
                                    │
                            Open-Meteo Weather
                                    │
                             Supabase Postgres
```

---

## 📌 Step 1: Create Supabase Free PostgreSQL Database

1. Sign up / Log in to [Supabase](https://supabase.com).
2. Click **New Project** and name it `travelpilot-db`.
3. Set a strong database password (save this password!).
4. Choose a region close to your target audience.
5. Once provisioned, navigate to **Project Settings -> Database -> Connection String**.
6. Select **URI** mode and copy the PostgreSQL connection string:
   ```text
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

---

## 📌 Step 2: Push Your Code to GitHub

1. Create a public repository named `travelPilotAI` on [GitHub](https://github.com).
2. Initialize and push your code:
   ```bash
   git add .
   git commit -m "feat: Prepare application for free cloud deployment"
   git remote add origin https://github.com/YOUR_USERNAME/travelPilotAI.git
   git branch -M main
   git push -u origin main
   ```

---

## 📌 Step 3: Deploy Backend to Render (Free Web Service)

1. Sign up / Log in to [Render](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository `travelPilotAI`.
4. Render will detect `render.yaml` or Docker environment automatically:
   - **Name**: `travelpilot-backend`
   - **Runtime**: `Docker`
   - **Plan**: `Free`
   - **Health Check Path**: `/api/v1/health`
5. Configure Environment Variables under **Environment**:
   - `APP_MODE` = `demo`
   - `ENVIRONMENT` = `production`
   - `LOG_LEVEL` = `INFO`
   - `GROQ_API_KEY` = `gsk_your_groq_api_key_here`
   - `GROQ_MODEL` = `llama-3.3-70b-versatile`
   - `DATABASE_URL` = `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`
   - `CORS_ORIGINS` = `["https://your-app.vercel.app"]` *(Update once Vercel URL is generated)*
6. Click **Deploy Web Service**.
7. Once deployed, note down your Render Backend URL (e.g. `https://travelpilot-backend.onrender.com`).

---

## 📌 Step 4: Deploy Frontend to Vercel (Free Hobby Tier)

1. Sign up / Log in to [Vercel](https://vercel.com).
2. Click **Add New...** -> **Project**.
3. Import your `travelPilotAI` GitHub repository.
4. Configure Project Settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add:
   - `VITE_API_BASE_URL` = `https://travelpilot-backend.onrender.com`
6. Click **Deploy**.
7. Once deployed, copy your public Vercel URL (e.g. `https://travelpilot-ai.vercel.app`).

---

## 📌 Step 5: Update CORS on Render

1. Go back to your **Render Dashboard** -> `travelpilot-backend` -> **Environment**.
2. Update `CORS_ORIGINS` to match your Vercel URL:
   ```json
   ["https://travelpilot-ai.vercel.app"]
   ```
3. Save changes (Render will perform a quick zero-downtime redeploy).

---

## 🧪 Step 6: Verify Deployment

1. **Backend Health Check**:
   Open `https://travelpilot-backend.onrender.com/api/v1/health` in your browser. Expect:
   ```json
   {"status":"ok","app":"TravelPilot AI","mode":"demo"}
   ```
2. **Frontend UI Test**:
   Open `https://travelpilot-ai.vercel.app`.
   - Submit a travel request (e.g., *Bangalore to Goa, 5 days, budget ₹1,50,000*).
   - Test Human-in-the-Loop review modal (`Approve` / `Edit` / `Reject`).
   - Check the **Day-by-Day Itinerary**, **Flights**, **Hotels**, **Weather**, and **Budget** tabs!

---

## ⚠️ Free Tier Limitations & Operational Notes

- **Render Cold Starts**: Render free instances spin down after 15 minutes of inactivity. Initial request may take 30-50 seconds to wake up the container.
- **Supabase Inactivity**: Free Supabase databases pause after 1 week of inactivity (can be unpaused with 1 click).
- **Simulated Flight & Hotel Data**: Booking availability for flights and hotels is simulated in demo mode for compliance.
