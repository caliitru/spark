# 🚀 STREAMLIT DEPLOYMENT GUIDE

## 📦 What You Need

1. **streamlit_app.py** - Your Streamlit frontend
2. **main.py** (backend) - Your FastAPI backend  
3. **generator.py** - Generation logic
4. **models.py** - Pydantic models
5. **prompt.py** - Prompt builders
6. **requirement.txt** - Dependencies

---

## 🎯 How It Works

```
Streamlit Frontend (Port 8501) 
        ↓
    HTTP POST
        ↓
FastAPI Backend (Port 8000)
        ↓
    OpenAI API
        ↓
Generated Content
        ↓
Display in Streamlit
```

---

## ⚡ Quick Start (Local Testing)

### Step 1: Update requirement.txt
```txt
streamlit
fastapi
uvicorn[standard]
python-dotenv
openai
requests
Pillow
```

### Step 2: Set Up Environment
Create `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
```

### Step 3: Start Backend (Terminal 1)
```bash
uvicorn main:app --reload --port 8000
```

### Step 4: Start Streamlit (Terminal 2)
```bash
streamlit run streamlit_app.py
```

### Step 5: Open Browser
Streamlit will automatically open: `http://localhost:8501`

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Frontend Only)

**For this setup, you need to deploy backend separately!**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add secrets in Streamlit Cloud:
   ```
   BACKEND_URL = "https://your-backend-url.com"
   ```
5. Deploy!

**Note**: You'll need to deploy your FastAPI backend somewhere else (Railway, Render, etc.)

---

### Option 2: Full Stack on Railway

**Deploy both together:**

1. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT & streamlit run streamlit_app.py --server.port 8501",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
worker: streamlit run streamlit_app.py --server.port 8501
```

---

### Option 3: Separate Deployments (Recommended)

**Backend (Railway/Render):**
```bash
# Deploy FastAPI backend
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Frontend (Streamlit Cloud):**
- Update `BACKEND_URL` in `streamlit_app.py` to your backend URL
- Deploy to Streamlit Cloud

---

## 🔧 Configuration

### Update Backend URL

In `streamlit_app.py`, line 13:
```python
BACKEND_URL = "http://localhost:8000"  # Local

# OR for production:
BACKEND_URL = "https://your-backend.railway.app"  # Railway
BACKEND_URL = "https://your-backend.onrender.com"  # Render
```

### Add CORS to Backend

Make sure your `main.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 File Structure

```
your-project/
├── streamlit_app.py       # Streamlit frontend
├── main.py               # FastAPI backend
├── generator.py          # Generation logic
├── models.py            # Pydantic models
├── prompt.py            # Prompt builders
├── requirement.txt      # Dependencies
├── .env                 # Environment variables (local only)
└── README.md           # Documentation
```

---

## 🧪 Testing Locally

1. **Start backend:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Start Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Test the flow:**
   - Fill in campaign form
   - Click "Generate Campaign"
   - Should see loading spinner
   - Results appear in "View Results" tab
   - Check sidebar for campaign summary

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Make sure FastAPI is running on port 8000
- Check `BACKEND_URL` in streamlit_app.py
- Verify CORS is enabled in main.py

### "Images not displaying"
- Images are saved locally by backend
- For Streamlit to display them, backend needs static file serving
- Add to `main.py`:
  ```python
  from fastapi.staticfiles import StaticFiles
  app.mount("/images", StaticFiles(directory="."), name="images")
  ```
- Update image URLs in Streamlit to use backend URL

### "Module not found"
- Install all dependencies: `pip install -r requirement.txt`
- Make sure you're in the right directory

### Streamlit won't start
- Check if port 8501 is available
- Try: `streamlit run streamlit_app.py --server.port 8502`

---

## 🎨 Features in Streamlit App

### Input Page
✅ Platform selector (LinkedIn, Instagram, Twitter)
✅ Two-column form layout
✅ Campaign basics (company, event, title, message, CTA)
✅ Content settings (audience, product, style, mood, colors)
✅ Generation options (toggles for captions/images, sliders for count)
✅ Form validation
✅ API request debugging (expandable payload viewer)
✅ Loading state with spinner
✅ Error handling with friendly messages

### Output Page
✅ Campaign summary sidebar
✅ Tabbed interface (Captions | Images)
✅ Caption display with copy functionality
✅ Image display (when backend serves them properly)
✅ Raw API response viewer
✅ "Generate New Campaign" button

---

## 🚀 Production Checklist

- [ ] Set OPENAI_API_KEY in environment
- [ ] Update BACKEND_URL to production URL
- [ ] Enable CORS in FastAPI
- [ ] Add static file serving for images
- [ ] Test on production environment
- [ ] Add authentication (optional)
- [ ] Set up monitoring/logging
- [ ] Configure rate limiting

---

## 💡 Next Steps

1. **Test locally** to make sure everything works
2. **Deploy backend** to Railway/Render
3. **Update BACKEND_URL** in streamlit_app.py
4. **Deploy frontend** to Streamlit Cloud
5. **Test production** deployment

---

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Cloud](https://share.streamlit.io)
- [Railway](https://railway.app)
- [Render](https://render.com)

---

## ✨ You're Ready!

Run these two commands and you're live:

```bash
# Terminal 1
uvicorn main:app --reload --port 8000

# Terminal 2  
streamlit run streamlit_app.py
```

Then open http://localhost:8501 and start generating! 🎉