# GPT Coder

This project is a lightweight Flask web app for coding or summarizing text data using OpenAI's GPT models (like GPT-4o). You can upload a CSV file, choose a column, write a prompt, and get GPT responses back — all in one interface.

- 🔐 Data is processed in-memory only (no server-side storage)
- 🧪 Built for prototyping or lightweight research use
- 🚀 Deployable to Vercel or run locally with Python

## 🖥 Why Run Locally?

The hosted version at [gptcoder-livid.vercel.app](https://gptcoder-livid.vercel.app) limits CSV files to **3000 rows** to manage serverless memory usage on Vercel.

If you need to process larger files (e.g. 5,000+ rows), running the app locally is recommended.

## 🚀 Run Locally (Mac/Linux/Windows)

### 1. Clone the repository
```bash
git clone https://github.com/blasimon/gptcoder.git
cd gptcoder
```

### 2. Create a virtual environment and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Flask app
```bash
export FLASK_APP=api/index.py
flask run
```
Open your browser and go to the address displayed in the terminal. 

---

## 🔧 How to Increase the Row Limit Locally

1. Open the `index.py` file inside the `api/` folder.
2. Find this line:

```python
if len(df) > 3000:
    return "Too many rows. Please upload a file with 3000 rows or fewer.", 400
```

3.	Change it to something like:
```python
if len(df) > 100000:
    return "Too many rows. Please upload a file with 100,000 rows or fewer.", 400
```

4.	Save and restart the Flask app:
```python
flask run
```	
---

## 🌐 Deploy on Vercel (Serverless)

Vercel is a great choice for deploying this app because it’s fast, secure, and free for small-scale or personal use. It supports serverless Python functions, handles HTTPS by default, and integrates directly with GitHub for easy auto-deploys. If you’re just testing or using the app for light research, Vercel gives you a no-cost way to get your GPT Coder online without needing to manage servers or cloud infrastructure.

### 1. Make sure your repo contains:
```bash
gptcoder/
├── api/
│   └── index.py         # Flask app
├── templates/
│   └── form.html        # UI
├── requirements.txt     # Python deps
├── vercel.json          # Vercel routing config
```

### 2. Push the repo to YOUR Github
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/gptcoder.git
git push -u origin main
```

### 3. Connect to Vercel
- Visit [https://vercel.com/import/git](https://vercel.com/import/git)
- Link your GitHub repository
- Leave the **Build Command** and **Output Directory** fields blank in the UI
- Make sure your repo includes `vercel.json` in the root

Vercel will:
- Install Python dependencies via `requirements.txt`
- Route all incoming requests to your Flask app at `api/index.py`

Your deployed app will be available. 
