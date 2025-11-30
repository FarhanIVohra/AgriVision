# AgriVision Backend Deployment Guide

This guide provides step-by-step instructions for deploying the AgriVision backend to Render.

## 🚀 Quick Deploy to Render

### Prerequisites
- [Render Account](https://render.com) (Free tier available)
- [Supabase Account](https://supabase.com) for database
- OpenWeatherMap API Key (Free tier available)
- Geoapify API Key (Free tier available)

### Step 1: Prepare Your Repository
Ensure your repository contains these files in the `backend/` directory:
- `requirements.txt` ✅ (Updated with all dependencies)
- `Procfile` ✅ (Created for deployment)
- `render.yaml` ✅ (Created for Render configuration)
- `.env.example` ✅ (Created with required environment variables)
- `app/main.py` (Main FastAPI application)
- `app/routers/` (All API routers)
- `app/services/` (All service modules)

### Step 2: Set Up Supabase Database
1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the initial schema:

```sql
-- Create users table
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    region TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create yield_predictions table
CREATE TABLE yield_predictions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    crop TEXT NOT NULL,
    year INTEGER NOT NULL,
    season TEXT NOT NULL,
    area DOUBLE PRECISION NOT NULL,
    predicted_yield DOUBLE PRECISION NOT NULL,
    input_parameters JSONB,
    model_version TEXT,
    confidence_score DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_yield_predictions_user_id ON yield_predictions(user_id);
CREATE INDEX idx_yield_predictions_created_at ON yield_predictions(created_at);
```

3. Note down your Supabase credentials:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon Key**: From Project Settings → API
   - **Service Role Key**: From Project Settings → API (keep secret!)

### Step 3: Get API Keys
1. **OpenWeatherMap**: Sign up at [openweathermap.org](https://openweathermap.org/api) and get your API key
2. **Geoapify**: Sign up at [geoapify.com](https://geoapify.com) and get your API key

### Step 4: Deploy to Render
1. **Connect Repository**:
   - Go to [render.com](https://render.com) and click "New +"
   - Select "Web Service"
   - Connect your GitHub/GitLab repository
   - Set the **Root Directory** to `backend`

2. **Configure Build & Deploy**:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-jwt-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   SUPABASE_ANON_KEY=your-anon-key
   OPENWEATHERMAP_API_KEY=your-openweather-key
   GEOAPIFY_API_KEY=your-geoapify-key
   CORS_ORIGINS=https://your-frontend-domain.com
   ```

4. **Deploy**: Click "Create Web Service" and wait for deployment to complete.

### Step 5: Verify Deployment
1. Check your Render service logs for any errors
2. Visit `https://your-service-name.onrender.com/api/health` to verify the API is running
3. Test authentication endpoints with a tool like Postman

## 📋 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | JWT signing key | ✅ | `your-super-secret-key` |
| `ALGORITHM` | JWT algorithm | ✅ | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration | ✅ | `30` |
| `SUPABASE_URL` | Supabase project URL | ✅ | `https://xxx.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | ✅ | `eyJ...` |
| `SUPABASE_ANON_KEY` | Supabase anon key | ✅ | `eyJ...` |
| `OPENWEATHERMAP_API_KEY` | Weather API key | ✅ | `abc123...` |
| `GEOAPIFY_API_KEY` | Geocoding API key | ✅ | `def456...` |
| `CORS_ORIGINS` | Frontend URL for CORS | ✅ | `https://yourapp.com` |
| `GOOGLE_TRANSLATE_API_KEY` | Translation API key | ❌ | `ghi789...` |

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Database Connection**: Verify Supabase credentials and table schema
3. **API Keys**: Check that all required API keys are set
4. **CORS Issues**: Update `CORS_ORIGINS` with your frontend URL
5. **Model Loading**: Ensure ML models are in the correct path

### Build Failures:
- Check Render logs for specific error messages
- Verify Python version compatibility (Python 3.8+)
- Ensure all dependencies have compatible versions

### Runtime Errors:
- Check environment variables are set correctly
- Verify database connectivity
- Test API endpoints individually

## 🔧 Local Development

To run locally for testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file)
cp .env.example .env
# Edit .env with your actual values

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 API Endpoints

Once deployed, your API will be available at:
- **Base URL**: `https://your-service.onrender.com`
- **API Docs**: `https://your-service.onrender.com/api/docs`
- **Health Check**: `https://your-service.onrender.com/api/health`

## 🚀 Next Steps

1. **Frontend Deployment**: Deploy your React frontend to Vercel/Netlify
2. **Domain Setup**: Configure custom domain if needed
3. **Monitoring**: Set up Render monitoring and alerts
4. **Scaling**: Upgrade to paid plans as needed

---

**Need Help?** Check the [AgriVision Documentation](./README.md) or create an issue in the repository.
