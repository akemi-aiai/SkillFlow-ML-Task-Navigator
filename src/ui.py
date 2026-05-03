from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        .hero {
            padding: 2rem 2rem;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.14), rgba(14, 165, 233, 0.12));
            border: 1px solid rgba(120, 120, 120, 0.18);
            margin-bottom: 1.2rem;
        }
        .hero h1 {
            font-size: 2.45rem;
            margin-bottom: 0.4rem;
            line-height: 1.12;
        }
        .hero p {
            font-size: 1.05rem;
            opacity: 0.86;
            max-width: 850px;
        }
        .card {
            padding: 1.1rem 1.2rem;
            border-radius: 22px;
            border: 1px solid rgba(120, 120, 120, 0.18);
            background: rgba(255, 255, 255, 0.035);
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.05);
            height: 100%;
        }
        .card h3 {
            margin-top: 0;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        .badge {
            display: inline-block;
            padding: 0.22rem 0.58rem;
            border-radius: 999px;
            border: 1px solid rgba(120, 120, 120, 0.22);
            font-size: 0.78rem;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            background: rgba(124, 58, 237, 0.10);
        }
        .step-box {
            padding: 0.9rem 1rem;
            border-radius: 16px;
            background: rgba(14, 165, 233, 0.08);
            border-left: 4px solid rgba(14, 165, 233, 0.65);
            margin: 0.45rem 0;
        }
        .warning-box {
            padding: 0.9rem 1rem;
            border-radius: 16px;
            background: rgba(245, 158, 11, 0.10);
            border-left: 4px solid rgba(245, 158, 11, 0.7);
            margin: 0.45rem 0;
        }
        .success-box {
            padding: 0.9rem 1rem;
            border-radius: 16px;
            background: rgba(34, 197, 94, 0.10);
            border-left: 4px solid rgba(34, 197, 94, 0.7);
            margin: 0.45rem 0;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(120, 120, 120, 0.16);
            border-radius: 18px;
            padding: 0.8rem 1rem;
            background: rgba(255, 255, 255, 0.035);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{text}</p>
            <span class="badge">ML</span>
            <span class="badge">Streamlit</span>
            <span class="badge">Practice Tests</span>
            <span class="badge">Learning Analytics</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def list_box(items: list[str], kind: str = "step") -> None:
    css_class = "step-box" if kind == "step" else "warning-box"
    for item in items:
        st.markdown(f'<div class="{css_class}">{item}</div>', unsafe_allow_html=True)
