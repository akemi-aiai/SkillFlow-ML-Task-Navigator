# SkillFlow ML: Task Navigator & Practice Tests

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
