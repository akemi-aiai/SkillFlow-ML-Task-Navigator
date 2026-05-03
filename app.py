from __future__ import annotations

import random

import pandas as pd
import plotly.express as px
import streamlit as st

from src.i18n import t
from src.practice_data import PRACTICE_TESTS, get_difficulties, get_topics
from src.rules import diagnose_task
from src.storage import clear_attempts, load_attempts, save_attempt
from src.ui import card, hero, inject_css, list_box

st.set_page_config(
    page_title="SkillFlow ML",
    layout="wide",
)

inject_css()

if "lang" not in st.session_state:
    st.session_state.lang = "ru"

with st.sidebar:
    st.title("SkillFlow ML")
    st.caption(t("app_tagline", st.session_state.lang))

    lang_choice = st.radio(
        "Language / Язык",
        options=["ru", "en"],
        format_func=lambda x: "Русский" if x == "ru" else "English",
        horizontal=True,
        key="language_radio",
    )
    st.session_state.lang = lang_choice
    lang = st.session_state.lang

    st.divider()
    nav = st.radio(
        "Navigation",
        options=["home", "navigator", "practice", "checklists", "theory", "dashboard"],
        format_func=lambda key: t(key, lang),
    )

    st.divider()
    st.markdown(f"**{t('how_it_works', lang)}**")
    st.caption(t("loop", lang))

    if st.button("Clear attempts" if lang == "en" else "Очистить попытки"):
        clear_attempts()
        st.success("Attempts cleared." if lang == "en" else "Попытки удалены.")
        st.rerun()


def render_home() -> None:
    hero(t("hero_title", lang), t("hero_text", lang))

    c1, c2, c3 = st.columns(3)
    with c1:
        card(t("problem_title", lang), t("problem_text", lang))
    with c2:
        card(t("solution_title", lang), t("solution_text", lang))
    with c3:
        card(t("goal_title", lang), t("goal_text", lang))

    st.subheader(t("how_it_works", lang))
    st.markdown(f"### `{t('loop', lang)}`")

    f1, f2, f3 = st.columns(3)
    with f1:
        card(t("feature_1", lang), t("feature_1_text", lang))
    with f2:
        card(t("feature_2", lang), t("feature_2_text", lang))
    with f3:
        card(t("feature_3", lang), t("feature_3_text", lang))


def render_navigator() -> None:
    st.title(t("navigator", lang))
    st.write(
        "Answer a few questions and get a recommended ML path."
        if lang == "en"
        else "Ответь на несколько вопросов и получи рекомендуемый путь решения ML-задачи."
    )

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            data_type = st.selectbox(
                t("choose_data_type", lang),
                ["Tabular", "Text", "Time series", "Images / Other"]
                if lang == "en"
                else ["Табличные данные", "Текст", "Временные ряды", "Изображения / другое"],
            )
            has_target = st.radio(
                t("has_target", lang),
                ["Yes", "No", "Not sure"] if lang == "en" else ["Да", "Нет", "Не уверена"],
                horizontal=True,
            )
            target_type = st.radio(
                t("target_type", lang),
                ["Number", "Category", "Not applicable"]
                if lang == "en"
                else ["Число", "Категория", "Не применимо"],
                horizontal=True,
            )
            class_imbalance = st.radio(
                t("imbalance", lang),
                ["Yes", "No", "Not sure"] if lang == "en" else ["Да", "Нет", "Не уверена"],
                horizontal=True,
            )

        with col2:
            time_order = st.radio(
                t("time_order", lang),
                ["Yes", "No", "Not sure"] if lang == "en" else ["Да", "Нет", "Не уверена"],
                horizontal=True,
            )
            needs_groups = st.radio(
                t("groups", lang),
                ["Yes", "No", "Not sure"] if lang == "en" else ["Да", "Нет", "Не уверена"],
                horizontal=True,
            )
            needs_dim_reduction = st.radio(
                t("dim_reduce", lang),
                ["Yes", "No", "Not sure"] if lang == "en" else ["Да", "Нет", "Не уверена"],
                horizontal=True,
            )
            goal_text = st.text_area(
                t("goal", lang),
                placeholder=(
                    "Example: predict taxi demand for the next hour"
                    if lang == "en"
                    else "Например: спрогнозировать количество заказов такси на следующий час"
                ),
            )

    if st.button(t("run_diagnosis", lang), type="primary"):
        result = diagnose_task(
            data_type=data_type,
            has_target=has_target,
            target_type=target_type,
            time_order=time_order,
            needs_groups=needs_groups,
            needs_dim_reduction=needs_dim_reduction,
            class_imbalance=class_imbalance,
            lang=lang,
        )
        st.session_state["diagnosis"] = result
        st.session_state["goal_text"] = goal_text

    if "diagnosis" in st.session_state:
        result = st.session_state["diagnosis"]

        st.subheader(t("recommendation", lang))
        m1, m2 = st.columns(2)
        m1.metric(t("learning_type", lang), result["learning_type"])
        m2.metric(t("task_type", lang), result["task_type"])

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                t("pipeline", lang),
                t("recommended_models", lang),
                t("watch_out", lang),
                t("practice_to_do", lang),
            ]
        )
        with tab1:
            list_box(result["pipeline"], kind="step")
        with tab2:
            for model in result["models"]:
                st.markdown(f"<span class='badge'>{model}</span>", unsafe_allow_html=True)
        with tab3:
            list_box(result["warnings"], kind="warning")
        with tab4:
            for topic in result["practice"]:
                st.markdown(f"<span class='badge'>{topic}</span>", unsafe_allow_html=True)
            st.info(
                "Open Practice Tests and filter by these topics."
                if lang == "en"
                else "Открой раздел «Ручные тесты» и отфильтруй задания по этим темам."
            )


def localize_test(test: dict, field: str) -> str:
    return test[f"{field}_{lang}"]


def render_practice() -> None:
    st.title(t("practice", lang))
    st.write(
        "Manual active-recall tests: answer first, then reveal the solution."
        if lang == "en"
        else "Ручные тесты по активному вспоминанию: сначала ответь сама, потом открой правильное решение."
    )

    c1, c2 = st.columns(2)
    with c1:
        topic = st.selectbox(t("select_topic", lang), ["All"] + get_topics())
    with c2:
        difficulty = st.selectbox(t("select_difficulty", lang), get_difficulties())

    filtered = PRACTICE_TESTS
    if topic != "All":
        filtered = [x for x in filtered if x["topic"] == topic]
    if difficulty != "All":
        filtered = [x for x in filtered if x["difficulty"] == difficulty]

    if not filtered:
        st.warning("No tests found." if lang == "en" else "Тесты не найдены.")
        return

    if st.button("Random test" if lang == "en" else "Случайный тест"):
        st.session_state["selected_test_id"] = random.choice(filtered)["id"]

    default_id = st.session_state.get("selected_test_id", filtered[0]["id"])
    ids = [x["id"] for x in filtered]
    if default_id not in ids:
        default_id = ids[0]

    selected_id = st.selectbox(
        t("select_test", lang),
        ids,
        index=ids.index(default_id),
        format_func=lambda test_id: f"#{test_id} — {next(x['topic'] for x in PRACTICE_TESTS if x['id'] == test_id)}",
    )
    st.session_state["selected_test_id"] = selected_id
    test = next(x for x in PRACTICE_TESTS if x["id"] == selected_id)

    st.markdown(f"<span class='badge'>{test['learning_type']}</span><span class='badge'>{test['topic']}</span><span class='badge'>{test['difficulty']}</span>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("❓ " + t("question", lang))
        st.write(localize_test(test, "question"))

        answer_key = f"answer_{selected_id}"
        user_answer = st.text_area(t("your_answer", lang), key=answer_key, height=140)

        with st.expander("💡 " + t("hint", lang)):
            st.write(localize_test(test, "hint"))

        if st.button(t("show_solution", lang)):
            st.session_state[f"show_solution_{selected_id}"] = True

        if st.session_state.get(f"show_solution_{selected_id}", False):
            st.markdown(t("correct_answer", lang))
            st.success(localize_test(test, "answer"))
            st.markdown(t("mini_task", lang))
            st.info(localize_test(test, "mini_task"))

        s1, s2, s3 = st.columns([1, 1, 2])
        with s1:
            self_score = st.slider(t("self_score", lang), min_value=1, max_value=5, value=3)
        with s2:
            status_options = ["Need Practice", "Practiced", "Mastered"]
            status = st.selectbox(t("status", lang), status_options)
        with s3:
            st.write("")
            st.write("")
            if st.button(t("save_attempt", lang), type="primary"):
                save_attempt(
                    test_id=test["id"],
                    topic=test["topic"],
                    status=status,
                    self_score=self_score,
                    answer_text=user_answer,
                )
                st.success(t("saved", lang))


def render_checklists() -> None:
    st.title(t("checklists", lang))
    st.write(t("checklist_intro", lang))

    supervised_ru = [
        "Поняла, что есть target и это задача с учителем",
        "Разделила признаки X и целевую переменную y",
        "Проверила пропуски, дубликаты и типы данных",
        "Сделала train/test split до масштабирования и кодирования",
        "Проверила дисбаланс классов или распределение target",
        "Выбрала подходящие метрики",
        "Сравнила модель с baseline",
        "Проверила, нет ли data leakage",
    ]
    supervised_en = [
        "Confirmed that the task has a target variable",
        "Separated features X and target y",
        "Checked missing values, duplicates, and data types",
        "Split train/test before scaling and encoding",
        "Checked class balance or target distribution",
        "Selected appropriate metrics",
        "Compared model with a baseline",
        "Checked data leakage risks",
    ]

    unsup_ru = [
        "Поняла, что target нет",
        "Определила цель: кластеры, PCA, сегментация или визуализация",
        "Выбрала числовые признаки",
        "Масштабировала признаки",
        "Попробовала несколько параметров модели",
        "Посчитала silhouette score или explained variance",
        "Интерпретировала результат осторожно",
    ]
    unsup_en = [
        "Confirmed that there is no target variable",
        "Defined the goal: clusters, PCA, segmentation, or visualization",
        "Selected numeric features",
        "Scaled features",
        "Tried several model parameters",
        "Calculated silhouette score or explained variance",
        "Interpreted results carefully",
    ]

    ts_ru = [
        "Отсортировала данные по времени",
        "Сделала ресемплирование",
        "Создала лаги через shift",
        "Создала rolling mean только по прошлым значениям",
        "Разделила данные без shuffle",
        "Сравнила модель с baseline: предыдущий час/день/неделя",
        "Посчитала RMSE корректно",
    ]
    ts_en = [
        "Sorted data by datetime",
        "Resampled data",
        "Created lag features with shift",
        "Created rolling mean using only past values",
        "Split data without shuffle",
        "Compared with baseline: previous hour/day/week",
        "Calculated RMSE correctly",
    ]

    tab1, tab2, tab3 = st.tabs([t("supervised", lang), t("unsupervised", lang), t("time_series", lang)])
    with tab1:
        for item in supervised_ru if lang == "ru" else supervised_en:
            st.checkbox(item)
    with tab2:
        for item in unsup_ru if lang == "ru" else unsup_en:
            st.checkbox(item)
    with tab3:
        for item in ts_ru if lang == "ru" else ts_en:
            st.checkbox(item)


def render_theory() -> None:
    st.title(t("theory", lang))
    st.write(t("theory_intro", lang))

    cards_ru = [
        ("Обучение с учителем", "Есть target. Модель учится по парам: признаки → правильный ответ. Примеры: классификация и регрессия."),
        ("Обучение без учителя", "Target нет. Модель ищет структуру в данных: кластеры, скрытые группы, главные компоненты."),
        ("Классификация", "Нужно предсказать категорию: уйдёт клиент или нет, спам или не спам, класс объекта."),
        ("Регрессия", "Нужно предсказать число: цену, спрос, температуру, количество заказов."),
        ("Кластеризация", "Нужно найти группы похожих объектов. Важно масштабирование и осторожная интерпретация."),
        ("Data Leakage", "Утечка данных возникает, когда модель получает информацию, которая в реальности была бы недоступна на момент предсказания."),
        ("Active Recall", "Активное вспоминание — это когда ты сначала пытаешься ответить по памяти, а только потом смотришь правильное решение."),
    ]
    cards_en = [
        ("Supervised Learning", "There is a target variable. The model learns from feature-answer pairs. Examples: classification and regression."),
        ("Unsupervised Learning", "There is no target variable. The model looks for structure: clusters, hidden groups, or principal components."),
        ("Classification", "The goal is to predict a category: churn/no churn, spam/not spam, object class."),
        ("Regression", "The goal is to predict a number: price, demand, temperature, number of orders."),
        ("Clustering", "The goal is to find groups of similar objects. Scaling and careful interpretation are important."),
        ("Data Leakage", "Data leakage happens when the model uses information that would not be available at prediction time."),
        ("Active Recall", "Active recall means trying to answer by memory before looking at the correct solution."),
    ]

    selected_cards = cards_ru if lang == "ru" else cards_en
    for i in range(0, len(selected_cards), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(selected_cards):
                title, text = selected_cards[i + j]
                with col:
                    card(title, text)


def render_dashboard() -> None:
    st.title(t("dashboard", lang))
    df = load_attempts()

    if df.empty:
        st.info(t("no_attempts", lang))
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("total_attempts", lang), len(df))
    c2.metric(t("mastered", lang), int((df["status"] == "Mastered").sum()))
    c3.metric(t("need_practice", lang), int((df["status"] == "Need Practice").sum()))
    c4.metric(t("average_score", lang), round(df["self_score"].mean(), 2))

    col1, col2 = st.columns(2)
    with col1:
        topic_counts = df["topic"].value_counts().reset_index()
        topic_counts.columns = ["topic", "count"]
        fig = px.bar(topic_counts, x="topic", y="count", title=t("attempts_by_topic", lang))
        st.plotly_chart(fig, width="stretch")
    with col2:
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        fig = px.pie(status_counts, names="status", values="count", title=t("status_distribution", lang))
        st.plotly_chart(fig, width="stretch")

    st.subheader(t("recent_attempts", lang))
    st.dataframe(df.head(10), width="stretch")


if nav == "home":
    render_home()
elif nav == "navigator":
    render_navigator()
elif nav == "practice":
    render_practice()
elif nav == "checklists":
    render_checklists()
elif nav == "theory":
    render_theory()
elif nav == "dashboard":
    render_dashboard()
