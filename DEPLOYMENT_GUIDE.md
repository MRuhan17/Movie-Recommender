# 🚀 Deployment Guide

Complete guide for deploying the Movie Recommender application using Docker on Render (backend) and Vercel (frontend).

---

## 📋 Prerequisites

Before deploying, ensure you have:

- GitHub account with this repository
- [Render](https://render.com) account
- [Vercel](https://vercel.com) account
- [TMDB API Key](https://www.themoviedb.org/settings/api)

---

## 🔑 Step 1: Get TMDB API Key

1. Go to [TMDB](https://www.themoviedb.org/)
2. Create an account or log in
3. Navigate to Settings → API
4. Request an API key (Developer)
5. Copy your API key for later use

---

## 🐳 Step 2: Deploy Backend on Render

### Option A: Using Render Dashboard

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   ```
   Name: movie-recommender-backend
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Docker
   ```

3. **Set Environment Variables**
   ```
   TMDB_API_KEY=your_tmdb_api_key
   SECRET_KEY=generate_32_character_secret
   DATABASE_URL=sqlite:///./movie_recommender.db
   PORT=8000
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL: `https://your-app.onrender.com`

---

## ▲ Step 3: Deploy Frontend on Vercel

### Option A: Using Vercel Dashboard

1. **Import Project**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository

2. **Configure Project**
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   ```

3. **Set Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   NEXT_PUBLIC_TMDB_API_KEY=your_tmdb_api_key
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-5 minutes)
   - Your app will be live at: `https://your-app.vercel.app`

---

## 🔧 Step 4: Local Development with Docker

### Using Docker Compose

1. **Clone Repository**
   ```bash
   git clone https://github.com/MRuhan17/Movie-Recommender.git
   cd Movie-Recommender
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access Application**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

---

## ✅ Step 5: Verify Deployment

### Backend Health Check
```bash
curl https://your-backend.onrender.com/health
```

### Frontend Check
- Visit your Vercel URL
- Check browser console for errors
- Test API connections

---

## 🔄 Continuous Deployment

Both Render and Vercel auto-deploy on push to main:

1. **Make Changes**
   ```bash
   git add .
   git commit -m "feat: your changes"
   git push origin main
   ```

2. **Automatic Deployment**
   - Render rebuilds backend
   - Vercel rebuilds frontend
   - Changes live in 5-10 minutes

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Build fails on Render
- Check Dockerfile syntax
- Verify requirements.txt dependencies
- Check Render build logs

**Problem**: API returns 500 errors
- Verify environment variables
- Check application logs in Render
- Ensure TMDB API key is valid

### Frontend Issues

**Problem**: Build fails on Vercel
- Check package.json dependencies
- Verify Node.js version compatibility
- Check Vercel build logs

**Problem**: API calls fail
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings on backend
- Inspect browser network tab

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

## 🎉 Success!

Your Movie Recommender app should now be live! Share your deployment:

- Backend: `https://your-backend.onrender.com`
- Frontend: `https://your-app.vercel.app`

Built with ❤️ by Ruhulalemeen Mulla
