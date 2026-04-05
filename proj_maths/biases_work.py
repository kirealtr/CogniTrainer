"""Business logic and data helpers for the Think Slow project."""

from pathlib import Path

DATA_FILE_PATH = Path("./data/biases.csv")

NO_ANSWER_TEXT = "нет ответа"
NO_PREFERENCE_TEXT = "безразлично"


def get_biases_for_table():
    """Return all bias cards formatted for table output."""
    biases = []

    for count, parts in enumerate(_iter_bias_rows(), start=1):
        title, description, example, tip, source = parts
        biases.append([count, title, description, example, tip, source])

    return biases


def write_bias(title, description, example, tip):
    """Append a new user bias card to the CSV file."""
    new_line = f"{title};{description};{example};{tip};user"

    with DATA_FILE_PATH.open("r", encoding="utf-8") as file:
        existing_lines = [line.strip("\n") for line in file.readlines()]

    header = existing_lines[0]
    old_biases = existing_lines[1:]
    updated_biases = old_biases + [new_line]
    updated_biases.sort()

    with DATA_FILE_PATH.open("w", encoding="utf-8") as file:
        file.write("\n".join([header] + updated_biases))


def get_biases_stats():
    """Return summary statistics for all bias cards."""
    db_biases = 0
    user_biases = 0
    description_lengths = []
    example_lengths = []

    for parts in _iter_bias_rows():
        _, description, example, _, source = parts
        description_lengths.append(len(description.split()))
        example_lengths.append(len(example.split()))

        if source == "user":
            user_biases += 1
        elif source == "db":
            db_biases += 1

    total = db_biases + user_biases

    if total == 0:
        return {
            "biases_all": 0,
            "biases_own": 0,
            "biases_added": 0,
            "words_avg": 0,
            "words_max": 0,
            "words_min": 0,
            "example_avg": 0,
        }

    return {
        "biases_all": total,
        "biases_own": db_biases,
        "biases_added": user_biases,
        "words_avg": round(sum(description_lengths) / len(description_lengths), 1),
        "words_max": max(description_lengths),
        "words_min": min(description_lengths),
        "example_avg": round(sum(example_lengths) / len(example_lengths), 1),
    }


def get_quiz_questions():
    """Return quiz questions about cognitive biases."""
    return [
        {
            "id": 1,
            "question": (
                "Человек читает только те новости, которые подтверждают "
                "его прежнее мнение. Какое искажение здесь проявляется?"
            ),
            "options": [
                "Ошибка подтверждения",
                "Регрессия к среднему",
                "Ошибка выжившего",
                "Эффект ореола",
            ],
            "correct": "Ошибка подтверждения",
            "explanation": (
                "Ошибка подтверждения — это склонность замечать и ценить "
                "только подтверждающую информацию."
            ),
        },
        {
            "id": 2,
            "question": (
                "После того как товар сначала показали за 20 000 рублей, "
                "цена 12 000 кажется очень выгодной. Какое искажение "
                "проявляется?"
            ),
            "options": [
                "Эвристика доступности",
                "Эффект якоря",
                "Избыточная уверенность",
                "Иллюзия понимания",
            ],
            "correct": "Эффект якоря",
            "explanation": (
                "Первая увиденная цена становится якорем и влияет "
                "на дальнейшую оценку."
            ),
        },
        {
            "id": 3,
            "question": (
                "Человек делает вывод о профессии по одной яркой истории, "
                "игнорируя общую статистику. Что это показывает?"
            ),
            "options": [
                "Игнорирование базовой частоты",
                "Регрессия к среднему",
                "Подмена трудного вопроса лёгким",
                "Ошибка выжившего",
            ],
            "correct": "Игнорирование базовой частоты",
            "explanation": (
                "Базовая частота — это общая статистика по явлению. "
                "Её игнорирование ведёт к плохим выводам."
            ),
        },
        {
            "id": 4,
            "question": (
                "Человек изучает только истории успешных стартапов и решает, "
                "что почти все стартапы становятся прибыльными. "
                "Какое искажение здесь видно?"
            ),
            "options": [
                "Ошибка выжившего",
                "Эффект якоря",
                "Эффект ореола",
                "Ошибка подтверждения",
            ],
            "correct": "Ошибка выжившего",
            "explanation": (
                "Видимы только успешные примеры, а неудачные остаются "
                "вне поля зрения."
            ),
        },
        {
            "id": 5,
            "question": (
                "После серии очень плохих результатов ученик показывает "
                "чуть лучший результат, даже без нового метода подготовки. "
                "Какой принцип это объясняет?"
            ),
            "options": [
                "Эвристика доступности",
                "Регрессия к среднему",
                "Эффект якоря",
                "Избыточная уверенность",
            ],
            "correct": "Регрессия к среднему",
            "explanation": (
                "Сильные отклонения часто сменяются более обычными "
                "значениями просто из-за статистики."
            ),
        },
    ]


def get_risk_games():
    """Return risk-game scenarios for the prospect theory section."""
    return [
        {
            "id": 1,
            "kind": "choice",
            "group": "fourfold_high_gain",
            "title": "Вероятный выигрыш",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "95% выиграть 10 000 руб.",
            "right_text": "100% выиграть 9 000 руб.",
            "left_ev": 9500,
            "right_ev": 9000,
            "recommended": "А",
            "time_limit": 10,
            "explanation": (
                "Математическое ожидание у варианта А выше: 9 500 руб. "
                "против 9 000 руб. Но многие выбирают более надёжный "
                "вариант Б."
            ),
            "lesson": "Высоковероятные выигрыши: интуиция часто избегает риска.",
        },
        {
            "id": 2,
            "kind": "choice",
            "group": "fourfold_high_loss",
            "title": "Вероятная потеря",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "95% потерять 10 000 руб.",
            "right_text": "100% потерять 9 000 руб.",
            "left_ev": -9500,
            "right_ev": -9000,
            "recommended": "Б",
            "time_limit": 10,
            "explanation": (
                "Математически вариант Б лучше: гарантированный убыток "
                "9 000 меньше ожидаемого убытка 9 500 у варианта А. "
                "Но люди часто предпочитают рискнуть, чтобы избежать "
                "гарантированной потери."
            ),
            "lesson": "Высоковероятные потери: интуиция часто ищет риск.",
        },
        {
            "id": 3,
            "kind": "choice",
            "group": "fourfold_low_gain",
            "title": "Маловероятный выигрыш",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "5% выиграть 10 000 руб.",
            "right_text": "100% выиграть 400 руб.",
            "left_ev": 500,
            "right_ev": 400,
            "recommended": "А",
            "time_limit": 10,
            "explanation": (
                "Ожидаемое значение у варианта А выше: 500 руб. "
                "против 400 руб. Здесь и интуиция, и математика часто "
                "совпадают в пользу шанса на большой приз."
            ),
            "lesson": "Маловероятные выигрыши: люди часто переоценивают шанс крупного приза.",
        },
        {
            "id": 4,
            "kind": "choice",
            "group": "fourfold_low_loss",
            "title": "Маловероятная потеря",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "5% потерять 10 000 руб.",
            "right_text": "100% потерять 400 руб.",
            "left_ev": -500,
            "right_ev": -400,
            "recommended": "Б",
            "time_limit": 10,
            "explanation": (
                "Математически вариант Б лучше: потерять 400 гарантированно "
                "лучше, чем ожидаемо потерять 500. Но многие готовы "
                "переплатить, чтобы убрать даже маленький шанс крупной потери."
            ),
            "lesson": "Маловероятные потери: люди часто переплачивают за полное устранение риска.",
        },
        {
            "id": 5,
            "kind": "choice",
            "group": "gain_tradeoff",
            "title": "Почти наверняка или точно?",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "90% выиграть 10 000 руб.",
            "right_text": "100% выиграть 9 500 руб.",
            "left_ev": 9000,
            "right_ev": 9500,
            "recommended": "Б",
            "time_limit": 10,
            "explanation": "Вариант Б лучше как интуитивно, так и математически.",
            "lesson": "Нечастый случай, когда интуиция обычно даёт правильный совет.",
        },
        {
            "id": 6,
            "kind": "choice",
            "group": "loss_tradeoff",
            "title": "Почти наверняка или точно? Потери",
            "subtitle": "Что выберешь?",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "95% потерять 10 000 руб.",
            "right_text": "100% потерять 9 500 руб.",
            "left_ev": -9500,
            "right_ev": -9500,
            "recommended": NO_PREFERENCE_TEXT,
            "time_limit": 10,
            "explanation": "По ожиданию варианты равны. Разница только в форме риска.",
            "lesson": "При потерях люди часто тянутся к риску даже при равной математике.",
        },
        {
            "id": 7,
            "kind": "choice",
            "group": "classic_1",
            "title": "Решение 1",
            "subtitle": "Выберите между:",
            "left_label": "А",
            "right_label": "Б",
            "left_text": "верная прибыль 240 долларов",
            "right_text": (
                "25%-ный шанс выиграть 1000 долларов и 75%-ный шанс "
                "не выиграть ничего"
            ),
            "left_ev": 240,
            "right_ev": 250,
            "recommended": "Б",
            "time_limit": 20,
            "explanation": (
                "Математическое ожидание у Б выше: 250 против 240. "
                "Но большинство людей предпочитает надёжную прибыль А."
            ),
            "lesson": "Надёжный выигрыш психологически переоценивается.",
        },
        {
            "id": 8,
            "kind": "choice",
            "group": "classic_2",
            "title": "Решение 2",
            "subtitle": "Выберите между:",
            "left_label": "В",
            "right_label": "Г",
            "left_text": "верная потеря 750 долларов",
            "right_text": (
                "75%-ный шанс потерять 1000 долларов и 25%-ный шанс "
                "не потерять ничего"
            ),
            "left_ev": -750,
            "right_ev": -750,
            "recommended": NO_PREFERENCE_TEXT,
            "time_limit": 20,
            "explanation": (
                "С точки зрения ожидания варианты одинаковы: −750 и −750. "
                "Но многие выбирают Г, надеясь избежать потери."
            ),
            "lesson": "При потерях даже равные варианты переживаются неравно.",
        },
        {
            "id": 9,
            "kind": "choice",
            "group": "classic_3",
            "title": "Решение 3",
            "subtitle": "Выберите между:",
            "left_label": "АГ",
            "right_label": "БВ",
            "left_text": (
                "25%-ный шанс выиграть 240 долларов и 75%-ный шанс "
                "потерять 760 долларов"
            ),
            "right_text": (
                "25%-ный шанс выиграть 250 долларов и 75%-ный шанс "
                "потерять 750 долларов"
            ),
            "left_ev": -510,
            "right_ev": -500,
            "recommended": "БВ",
            "time_limit": 30,
            "explanation": (
                "Очевидно, что вариант БВ лучше: выигрыши больше, "
                "потери меньше, а шансы равны. При этом АГ эквивалентен "
                "сочетанию выборов А и Г из игр Решений 1 и 2."
            ),
            "lesson": (
                "Игры лучше рассматривать в более широких рамках: "
                "так прибыль на дистанции обычно выше."
            ),
        },
    ]


def analyze_risk_profile(results):
    """Analyze user decisions in risk games."""
    skipped = 0
    mathematically_better = 0
    certainty_pref = 0
    risk_seeking_losses = 0
    contradiction_flag = False
    picked = {}

    for item in results:
        selected = item["selected"]
        group = item["group"]

        if selected == NO_ANSWER_TEXT:
            skipped += 1

        if item["is_correct"]:
            mathematically_better += 1

        if group in {"fourfold_high_gain", "classic_1"} and selected in {"А", "Б"}:
            certainty_pref += 1

        if group in {"fourfold_high_loss", "classic_2"} and selected in {"А", "Г"}:
            risk_seeking_losses += 1

        picked[group] = selected

    contradiction_flag = (
        picked.get("classic_1") == "А"
        and picked.get("classic_2") == "Г"
        and picked.get("classic_3") == "БВ"
    )

    return {
        "skipped": skipped,
        "mathematically_better": mathematically_better,
        "certainty_pref": certainty_pref,
        "risk_seeking_losses": risk_seeking_losses,
        "contradiction_flag": contradiction_flag,
        "summary": _build_risk_summary(mathematically_better),
    }


def _iter_bias_rows():
    """Yield parsed rows from the CSV file without the header."""
    with DATA_FILE_PATH.open("r", encoding="utf-8") as file:
        for line in file.readlines()[1:]:
            stripped_line = line.strip()
            if stripped_line:
                yield stripped_line.split(";")


def _build_risk_summary(mathematically_better):
    """Return a short summary for the risk profile."""
    if mathematically_better >= 7:
        return (
            "Ты часто ориентируешься на математическое ожидание, "
            "даже когда интуиция толкает к более комфортному выбору."
        )

    if mathematically_better >= 4:
        return (
            "У тебя смешанный стиль: часть решений опирается на математику, "
            "часть — на интуицию и форму подачи."
        )

    return (
        "Ты часто следуешь интуитивной реакции на риск и определённость, "
        "даже когда математика предлагает иной выбор."
    )
