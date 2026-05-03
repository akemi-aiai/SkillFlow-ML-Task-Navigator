from __future__ import annotations


def diagnose_task(
    data_type: str,
    has_target: str,
    target_type: str,
    time_order: str,
    needs_groups: str,
    needs_dim_reduction: str,
    class_imbalance: str,
    lang: str = "en",
) -> dict:
    """Rule-based ML task diagnosis.

    This is intentionally transparent: it teaches the learner why a certain
    ML direction is recommended instead of hiding the logic inside a model.
    """

    is_ru = lang == "ru"

    def pack(learning_type, task_type, models, pipeline, warnings, practice):
        return {
            "learning_type": learning_type,
            "task_type": task_type,
            "models": models,
            "pipeline": pipeline,
            "warnings": warnings,
            "practice": practice,
        }

    if data_type in ["Time series", "Временные ряды"] or time_order in ["Yes", "Да"]:
        return pack(
            "Supervised Learning + Time Series" if not is_ru else "Обучение с учителем + временные ряды",
            "Time Series Forecasting" if not is_ru else "Прогнозирование временного ряда",
            ["Baseline: previous value", "Linear/Ridge Regression", "RandomForestRegressor", "Gradient Boosting"],
            [
                "Sort data by datetime" if not is_ru else "Отсортировать данные по времени",
                "Resample to the required frequency" if not is_ru else "Сделать ресемплирование до нужной частоты",
                "Create lag and rolling features without leakage" if not is_ru else "Создать лаги и скользящие признаки без утечки данных",
                "Split data without shuffle" if not is_ru else "Разделить данные без перемешивания",
                "Compare model with time-series baseline" if not is_ru else "Сравнить модель с baseline для временного ряда",
            ],
            [
                "Do not use shuffle=True" if not is_ru else "Не использовать shuffle=True",
                "Rolling mean must use only past values" if not is_ru else "Скользящее среднее должно использовать только прошлые значения",
                "Evaluate on the last time period" if not is_ru else "Оценивать модель на последнем временном отрезке",
            ],
            ["Time Series", "Data Leakage", "RMSE"],
        )

    if data_type in ["Text", "Текст"]:
        if has_target in ["Yes", "Да"]:
            return pack(
                "Supervised Learning + NLP" if not is_ru else "Обучение с учителем + NLP",
                "Text Classification / Text Regression" if not is_ru else "Классификация или регрессия текста",
                ["TF-IDF + Logistic Regression", "Linear SVM", "Naive Bayes", "Transformer baseline"],
                [
                    "Clean and tokenize text" if not is_ru else "Очистить и токенизировать текст",
                    "Create text features: TF-IDF or embeddings" if not is_ru else "Создать текстовые признаки: TF-IDF или эмбеддинги",
                    "Split train/test before fitting vectorizer" if not is_ru else "Разделить train/test до обучения векторизатора",
                    "Train baseline model" if not is_ru else "Обучить baseline-модель",
                    "Evaluate with task-specific metrics" if not is_ru else "Оценить качество подходящими метриками",
                ],
                [
                    "Avoid fitting vectorizer on full data" if not is_ru else "Не обучать векторизатор на всех данных до split",
                    "Check class imbalance" if not is_ru else "Проверить дисбаланс классов",
                ],
                ["NLP", "Data Leakage", "Metrics"],
            )
        return pack(
            "Unsupervised Learning + NLP" if not is_ru else "Обучение без учителя + NLP",
            "Topic discovery / Text clustering" if not is_ru else "Поиск тем или кластеризация текстов",
            ["TF-IDF + K-Means", "Topic Modeling", "Embeddings + clustering"],
            [
                "Clean text" if not is_ru else "Очистить текст",
                "Vectorize text" if not is_ru else "Преобразовать текст в признаки",
                "Reduce dimensions for visualization" if not is_ru else "Снизить размерность для визуализации",
                "Cluster or discover topics" if not is_ru else "Кластеризовать тексты или найти темы",
                "Interpret clusters manually" if not is_ru else "Интерпретировать кластеры вручную",
            ],
            [
                "Clusters are hypotheses, not true labels" if not is_ru else "Кластеры — это гипотезы, а не настоящие классы",
            ],
            ["Clustering", "PCA", "NLP"],
        )

    if has_target in ["Yes", "Да"]:
        if target_type in ["Number", "Число"]:
            return pack(
                "Supervised Learning" if not is_ru else "Обучение с учителем",
                "Regression" if not is_ru else "Регрессия",
                ["Baseline: mean target", "Linear Regression", "Ridge", "RandomForestRegressor", "Gradient Boosting"],
                [
                    "Check target distribution" if not is_ru else "Проверить распределение target",
                    "Split X and y" if not is_ru else "Разделить X и y",
                    "Train/test split" if not is_ru else "Сделать train/test split",
                    "Preprocess features inside a pipeline" if not is_ru else "Обрабатывать признаки внутри пайплайна",
                    "Evaluate with MAE/RMSE/R2" if not is_ru else "Оценить MAE/RMSE/R2",
                ],
                [
                    "Do not calculate RMSE incorrectly" if not is_ru else "Не считать RMSE неправильно",
                    "Check outliers" if not is_ru else "Проверить выбросы",
                ],
                ["Regression", "RMSE", "Data Leakage"],
            )
        return pack(
            "Supervised Learning" if not is_ru else "Обучение с учителем",
            "Classification" if not is_ru else "Классификация",
            ["Baseline: majority class", "Logistic Regression", "Decision Tree", "Random Forest", "Gradient Boosting"],
            [
                "Check target classes" if not is_ru else "Проверить классы target",
                "Check class balance" if not is_ru else "Проверить баланс классов",
                "Split X and y" if not is_ru else "Разделить X и y",
                "Use stratified train/test split if needed" if not is_ru else "Использовать stratified split при необходимости",
                "Evaluate with precision/recall/F1" if not is_ru else "Оценить precision/recall/F1",
            ],
            [
                "Accuracy can be misleading with class imbalance" if not is_ru else "Accuracy может обманывать при дисбалансе классов",
                "Look at confusion matrix" if not is_ru else "Смотреть confusion matrix",
            ] + (["Class imbalance requires special metrics" if not is_ru else "При дисбалансе нужны специальные метрики"] if class_imbalance in ["Yes", "Да"] else []),
            ["Classification", "Metrics", "Train/Test Split"],
        )

    if needs_groups in ["Yes", "Да"]:
        return pack(
            "Unsupervised Learning" if not is_ru else "Обучение без учителя",
            "Clustering" if not is_ru else "Кластеризация",
            ["K-Means", "Hierarchical Clustering", "DBSCAN", "Gaussian Mixture"],
            [
                "Select numeric features" if not is_ru else "Выбрать числовые признаки",
                "Scale features" if not is_ru else "Масштабировать признаки",
                "Try several cluster counts" if not is_ru else "Попробовать разное число кластеров",
                "Evaluate with silhouette score" if not is_ru else "Оценить silhouette score",
                "Interpret clusters using feature profiles" if not is_ru else "Интерпретировать кластеры через профили признаков",
            ],
            [
                "K-Means is sensitive to feature scale" if not is_ru else "K-Means чувствителен к масштабу признаков",
                "Clusters are not automatically true classes" if not is_ru else "Кластеры не равны настоящим классам автоматически",
            ],
            ["Clustering", "Scaling", "PCA"],
        )

    if needs_dim_reduction in ["Yes", "Да"]:
        return pack(
            "Unsupervised Learning" if not is_ru else "Обучение без учителя",
            "Dimensionality Reduction / PCA" if not is_ru else "Снижение размерности / PCA",
            ["PCA", "t-SNE", "UMAP"],
            [
                "Scale numeric features" if not is_ru else "Масштабировать числовые признаки",
                "Fit PCA" if not is_ru else "Обучить PCA",
                "Check explained variance ratio" if not is_ru else "Проверить explained variance ratio",
                "Visualize first components" if not is_ru else "Визуализировать первые компоненты",
                "Interpret carefully" if not is_ru else "Интерпретировать осторожно",
            ],
            [
                "Two PCA components may explain only part of the data" if not is_ru else "Две PCA-компоненты могут объяснять только часть данных",
            ],
            ["PCA", "Scaling", "Interpretation"],
        )

    return pack(
        "Exploratory Data Analysis" if not is_ru else "Исследовательский анализ данных",
        "EDA / Problem framing" if not is_ru else "EDA и формулировка задачи",
        ["Descriptive statistics", "Visualization", "Baseline rules"],
        [
            "Clarify business or learning goal" if not is_ru else "Уточнить цель задачи",
            "Inspect columns and data types" if not is_ru else "Изучить колонки и типы данных",
            "Check missing values and duplicates" if not is_ru else "Проверить пропуски и дубликаты",
            "Decide whether a target can be defined" if not is_ru else "Решить, можно ли определить target",
        ],
        [
            "Do not choose a model before defining the task" if not is_ru else "Не выбирать модель до определения типа задачи",
        ],
        ["EDA", "Task Framing", "Data Preprocessing"],
    )
