# Protein Data Analysis Web App

This is a simple interactive web application built with Flask and pandas to answer protein and protein domain abundance questions.

## 🔍 Description

The application allows users to explore answers to several predefined questions (A1–B2) based on two input data files:

- `9606_abund.txt` — average copy numbers of human proteins per cell
- `9606_gn_dom.txt` — domains associated with each protein

Each question can be answered interactively via a button on a single-page HTML frontend. All calculations are performed server-side in Python and results are shown without reloading the page (via Fetch/AJAX).

---

## 📁 Project Structure
```
Protein-Data-Analysis/
│
├── app.py                          # Entry point for Flask app
├── routes.py                       # API and data logic
├── requirements.txt                # Python dependencies
├── questions_answers.txt           # Answers summary in .txt
├── README.md                       # This file
│
├── data/
│   ├── 9606_abund.txt                              # Input file 1
│   ├── 9606_gn_dom.txt                             # Input file 2
│   ├── protein_analysis.ipynb                      # Jupyter notebook with analysis
│   ├── A2task_mean_std_proteins_abund.csv          # Result table for A2
│   ├── A3task_mean_std_rank.csv                    # Result table for A3
│   └── B2task_avg_abund_protein_domains_ranks.csv  # Result table for B2
│
├── templates/
│   └── index.html                   # HTML frontend
│
└── static/
    ├── css/
    │   └── style.css               # Styles
    └── script/
        └── main_script.js          # JavaScript (Fetch/AJAX logic)
```
---

## ▶️ How to Run

1. **Create a virtual environment:**

```
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**

```
pip install -r requirements.txt
```
3. **Start the application:**
```
python app.py
```