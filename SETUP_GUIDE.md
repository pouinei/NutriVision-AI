# Food Recognition & Calorie Counter - Setup Guide

## 📋 Prerequisites
- Python 3.8 or higher
- Gemini API Key (from Google AI Studio)

## 🚀 Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key (keep it secure!)

## 🔧 Step 2: Setup Environment

### Windows (PowerShell):
```powershell
# Navigate to project directory
cd "d:\gemini-project\gemini-pro-vision-project-food\End-To-End-Gemini-Project"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Windows (Command Prompt):
```cmd
cd d:\gemini-project\gemini-pro-vision-project-food\End-To-End-Gemini-Project
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 📝 Step 3: Configure .env File

1. Open `.env` file in the project directory
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. Save the file

⚠️ **Important**: Never share your `.env` file or API key publicly!

## ▶️ Step 4: Run the Application

Choose the app you want to run:

### Food Recognition & Calorie Counter (Recommended):
```bash
streamlit run food_recognition.py
```

### Other Apps:
```bash
# Q&A Chatbot
streamlit run app.py

# Image Analysis (General)
streamlit run vision.py

# Q&A Chatbot (Alternative)
streamlit run qachat.py
```

Your app will open in browser at `http://localhost:8501`

## 📦 Project Structure

```
End-To-End-Gemini-Project/
├── app.py                    # Q&A Chatbot with Gemini Pro
├── vision.py                 # Image analysis with Gemini Pro Vision
├── qachat.py                 # Alternative Q&A implementation
├── food_recognition.py       # 🆕 Food recognition & calorie counter
├── requirements.txt          # Python dependencies
├── .env                       # Environment variables (API keys)
└── README.md                 # Project information
```

## 🔑 Environment Variables

The `.env` file contains:
- `GOOGLE_API_KEY`: Your Gemini API key for authentication

Load it with:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

## ✅ Testing the Setup

1. After running the app, upload a food photo
2. Click "Analyze Food & Get Calories"
3. You should see calorie and nutrition information

## 🆘 Troubleshooting

### Issue: "API key not found"
- Make sure `.env` file exists in the project directory
- Check that `GOOGLE_API_KEY` is correctly set
- Verify the API key is valid (no typos, spaces)

### Issue: "ModuleNotFoundError"
- Verify virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version`

### Issue: "No module named 'streamlit'"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: App won't load
- Check if port 8501 is available
- Try: `streamlit run food_recognition.py --logger.level=debug`

## 📚 API Documentation

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

## 🎯 Features

✅ Upload food photos
✅ Identify food items
✅ Get calorie estimates
✅ Nutritional breakdown
✅ Download analysis results
✅ Health tips

## 💡 Tips for Best Results

1. **Clear Photos**: Use well-lit, clear images
2. **Portion Size**: Ensure the full portion is visible
3. **Single Angle**: For mixed dishes, take photos from above
4. **Real Food**: Works best with actual food photos
5. **Close-up**: Frame the food to fill most of the image

## 🚫 Limitations

- Calorie estimates are approximate
- Depends on portion size visibility
- Works best with common food items
- For precise nutritional info, consult a nutritionist

## 📞 Need Help?

- Check the Gemini API documentation
- Review Streamlit documentation
- Verify your API key is active
- Check internet connection

---

**Happy analyzing! 🍎**
