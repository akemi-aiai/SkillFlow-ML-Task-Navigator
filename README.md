# SkillFlow ML: Task Navigator & Practice Tests

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-ML%20Learning%20App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Handling-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Progress%20Dashboard-3F4F75?logo=plotly&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Attempt%20Tracking-003B57?logo=sqlite&logoColor=white)
![ML](https://img.shields.io/badge/ML-Task%20Diagnosis-7C5CFF)
![Learning](https://img.shields.io/badge/Learning-Active%20Recall-F59E0B)
![Language](https://img.shields.io/badge/Language-EN%20%7C%20RU-16A34A)

**SkillFlow ML** is a Streamlit-based learning tool that helps students decide how to start a machine learning task, choose the correct ML approach, build a structured pipeline, and practice weak skills through manual active-recall tests.

## Problem

When learning machine learning, students often understand tutorials and longreads but struggle to independently decide:

- whether the task is supervised or unsupervised;
- whether it is classification, regression, clustering, PCA, time series, or NLP;
- which pipeline steps should come first;
- how to reproduce the solution without hints.

As a result, the same coding and ML pipeline mistakes repeat.

## Solution

SkillFlow ML combines:

- **ML Task Navigator** — a rule-based diagnostic assistant that recommends a task type and pipeline;
- **Practice Tests** — manual active-recall questions based on common ML mistakes;
- **Pipeline Checklists** — structured steps for supervised, unsupervised, and time-series projects;
- **Theory Lab** — short theory cards explaining key ML concepts;
- **Progress Dashboard** — saved attempts and learning analytics.


## Features

- Bilingual interface: English / Russian
- Rule-based ML task diagnosis
- Recommended pipelines and starting models
- Manual practice tests with hints, answers, and mini-tasks
- Attempt tracking with SQLite
- Progress dashboard with Plotly charts
- Clean portfolio-ready UI with custom CSS

## Tech Stack

- Python
- Streamlit
- pandas
- Plotly
- SQLite

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Russian Summary

**SkillFlow ML** — это приложение для самостоятельного изучения машинного обучения. Оно помогает понять, с чего начать ML-задачу, выбрать подходящий тип обучения, построить пайплайн и отработать слабые места через ручные тесты.
