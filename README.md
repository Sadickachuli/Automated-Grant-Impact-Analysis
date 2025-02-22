# Grant Report Analysis App

This project consists of a FastAPI backend for analyzing grant reports and a React frontend (with Vite and TypeScript) for the user interface.

![grantAI](https://github.com/user-attachments/assets/764c9988-086d-47da-9047-13955c2a7203)

## 🚀 Features
- Upload a PDF grant report for analysis
- Extract key themes and impact areas using spaCy
- Perform sentiment analysis using a Transformer model
- View results in an interactive UI

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python)
- **spaCy** (for NLP)
- **Transformers** (for sentiment analysis)
- **PyMuPDF** (for PDF processing)
- **Uvicorn** (for running the API)

### Frontend
- **React** (with Vite)
- **TypeScript**
- **Styled Components**
- **Axios** (for API calls)

## 💻 Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```
## 📌 Backend Setup
###2️⃣ Install Python & Virtual Environment
Ensure you have Python 3.8+ installed. Then run:
```sh
python -m venv venv
# Activate virtual environment:
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```
###3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
###4️⃣ Run the Backend
```sh
uvicorn main:app --reload
```
Access the backend at: http://127.0.0.1:8000

##🌍 Frontend Setup
###5️⃣ Install Node.js & Dependencies
Ensure Node.js 16+ is installed.
Then, run:
```sh
cd grant-analysis-ui  # Navigate to the frontend directory
npm install  # Install dependencies
```
###6️⃣ Start the Frontend
```sh
npm run dev
```
The frontend will start at:
http://localhost:5173
![22 02 2025_16 09 50_REC](https://github.com/user-attachments/assets/ba5830fb-c854-4d22-8aea-6f0c0cf4db5a)
👤 Author
[Sadick Mustapha]

GitHub: [ github.com/Sadickachuli](https://github.com/Sadickachuli)

connect with me to work together
