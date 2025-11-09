# 🎯 EduPair: Project Pairing Dilemma

> **AI-powered student preference prediction for balanced team formation**

EduPair helps faculty predict whether students prefer working **Solo** or in **Teams** based on personality traits and activities. Built with machine learning and a beautiful glassmorphism UI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **🤖 ML-Powered Predictions**: Logistic Regression model trained on student personality data
- **🎨 Modern Glassmorphism UI**: Beautiful frosted glass effects with gradient backgrounds
- **📊 Real-time Dashboard**: Analytics and visualizations of student preferences
- **⚡ Fast API Backend**: RESTful API built with FastAPI
- **💾 Data Persistence**: Automatic saving of predictions for analysis
- **📈 Model Metrics**: Confusion matrix, accuracy tracking, and distribution charts

## 🎯 Prediction Features

The model uses only **4 key features** for accurate predictions:

1. **📊 Introversion/Extraversion** (1-5 scale)
   - 1 = Highly Introverted
   - 5 = Highly Extraverted

2. **🎲 Risk-Taking Level** (1-5 scale)
   - 1 = Low risk-taker
   - 5 = High risk-taker

3. **🎯 Primary Club/Activity**
   - Coding Club, Sports Club, Music Club, Cultural Club, Drama Club, Entrepreneurship Cell, Literary Club, Robotics Club

4. **⏰ Weekly Hobby Hours**
   - Time spent on hobbies per week

## 🏗️ Project Structure

```
EduPair/
├── the-project-pairing-dilemma-app/
│   ├── backend/
│   │   ├── main.py              # FastAPI backend server
│   │   ├── model.pkl            # Trained ML model
│   │   └── newdata.csv          # Prediction data storage
│   ├── frontend/
│   │   ├── app.py               # Streamlit UI
│   │   └── gradient.png         # Background image
│   └── train.py                 # Model training script
├── model_notebook/
│   └── project.ipynb            # Jupyter notebook for analysis
├── data.csv                     # Original training dataset
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/pauldebanshu19/EduPair.git
cd EduPair
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Train the model** (optional - pre-trained model included)
```bash
python the-project-pairing-dilemma-app/train.py
```

### Running the Application

#### Start the Backend (Terminal 1)
```bash
cd the-project-pairing-dilemma-app/backend
uvicorn main:app --reload
```
Backend will run on: `http://127.0.0.1:8000`

#### Start the Frontend (Terminal 2)
```bash
cd the-project-pairing-dilemma-app/frontend
streamlit run app.py
```
Frontend will open automatically in your browser at: `http://localhost:8501`

## 📊 API Endpoints

### `POST /predict`
Predict student preference

**Request Body:**
```json
{
  "introversion_extraversion": 3,
  "risk_taking": 4,
  "club_top1": "Coding Club",
  "weekly_hobby_hours": 10
}
```

**Response:**
```json
{
  "prediction": "Team",
  "prediction_probability": {
    "Solo": 0.23,
    "Team": 0.77
  }
}
```

### `GET /data-summary`
Get analytics and model performance metrics

**Response:**
```json
{
  "preference_distribution": {"Team": 61, "Solo": 108},
  "introversion_distribution": {...},
  "risk_taking_distribution": {...},
  "accuracy": 0.38,
  "confusion_matrix": [[...], [...]]
}
```

## 🎨 UI Features

- **Glassmorphism Design**: Modern frosted glass effects
- **Gradient Background**: Beautiful red-to-black gradient
- **Interactive Forms**: Smooth animations and hover effects
- **Real-time Predictions**: Instant results with confidence scores
- **Analytics Dashboard**: Visual insights with Plotly charts
- **Responsive Layout**: Works on all screen sizes

## 🧠 Model Details

- **Algorithm**: Logistic Regression with preprocessing pipeline
- **Features**: 4 key personality and activity indicators
- **Target**: Binary classification (Solo vs Team)
- **Preprocessing**: 
  - Numeric features: Median imputation + StandardScaler
  - Categorical features: Most frequent imputation + OneHotEncoder
- **Training**: Stratified train/test split (75/25)

## 📈 Model Performance

The model achieves balanced predictions with:
- Real-time accuracy tracking
- Confusion matrix visualization
- Distribution analysis of predictions
- Feature importance insights

## 🎓 Use Cases

- **Faculty**: Form balanced project teams based on student preferences
- **Students**: Understand their collaboration style
- **Institutions**: Analyze student personality trends
- **Researchers**: Study teamwork preferences in education

## 🛠️ Technology Stack

- **Backend**: FastAPI, scikit-learn, pandas, numpy
- **Frontend**: Streamlit, Plotly, requests
- **ML**: Logistic Regression, preprocessing pipelines
- **Data**: CSV storage, real-time updates

## 📝 Data Format

The model expects CSV data with these columns:
- `introversion_extraversion` (1-5)
- `risk_taking` (1-5)
- `club_top1` (string)
- `weekly_hobby_hours` (integer)
- `teamwork_preference` (1-5, for training only)

**Target Binarization:**
- Solo: teamwork_preference = 1-2
- Team: teamwork_preference = 4-5
- Neutral (3): Excluded from training

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Debanshu Paul**
- GitHub: [@pauldebanshu19](https://github.com/pauldebanshu19)

## 🙏 Acknowledgments

- Built for educational institutions to improve team formation
- Inspired by the need for balanced project teams
- Powered by machine learning and modern web technologies

---

**⭐ Star this repo if you find it helpful!**
