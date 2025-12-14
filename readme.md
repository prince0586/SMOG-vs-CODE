# 🏭 Smog & Code: The Similarity Dashboard

### *Does pollution poison your productivity?*

**Smog & Code** is a data science dashboard that investigates a quirky hypothesis: *Do developers write less code when air quality is bad?* By mashing up two completely unrelated data sources—**GitHub Commit History** and **Historical Air Quality Index (AQI)**—this tool calculates a mathematical "Similarity Score" to see if your digital output syncs with your physical environment.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Normalized+Graph+Preview:+Pollution+vs+Productivity)
*(Replace this link with a screenshot of your actual dashboard once running!)*

---

## 🧪 The Science: How it Works

Most "mash-up" dashboards just plot two lines on different axes, which is often misleading. This project takes a rigorous data science approach to find real correlations:

1.  **Data Mining:**
    * **Productivity:** Fetches public commit history for any GitHub user via the GitHub REST API.
    * **Pollution:** Fetches historical PM2.5 (Particulate Matter) data for the user's city via the Open-Meteo API.
2.  **Normalization (The "Secret Sauce"):**
    * Since "Commits" (e.g., 5-20/day) and "PM2.5" (e.g., 10-150 µg/m³) have vastly different scales, we use **Min-Max Scaling** (`scikit-learn`) to force both datasets onto a shared `0.0` to `1.0` scale.
3.  **Similarity Scoring:**
    * We calculate the **Pearson Correlation Coefficient** to give you a precise "Similarity Score" between -1.0 (Opposites) and 1.0 (Identical).

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (for the interactive dashboard)
* **Visualization:** [Plotly](https://plotly.com/) (for interactive, normalized time-series graphs)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Machine Learning:** [Scikit-learn](https://scikit-learn.org/) (for `MinMaxScaler` normalization)
* **APIs:** GitHub REST API, Open-Meteo Air Quality API

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Clone/Setup
Create a folder for the project and navigate into it:
```bash
mkdir SmogCode
cd SmogCode