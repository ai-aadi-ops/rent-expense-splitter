# Roommate Expense Splitter

A simple Streamlit app to split rent and shared expenses between roommates.

## ✅ Run locally

1. Create/activate a Python virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

## 🚀 Deploying on GitHub (via Streamlit Community Cloud)

1. Create a GitHub repository for this project.
2. Add, commit, and push your code:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

3. Go to https://streamlit.io/cloud and sign in with GitHub.
4. Click **"New app"**, select your repository, branch (usually `main`), and set the entry point to `app.py`.
5. Click **Deploy**.

📝 **Notes**
- Streamlit Cloud automatically installs dependencies from `requirements.txt`.
- Any time you push to the branch configured in Streamlit Cloud, the app redeploys automatically.
