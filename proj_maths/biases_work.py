from math import ceil


def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]

    count = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        title, description, example, tip, source = line.split(";")
        terms.append([count, title, description, example, tip, source])
        count += 1

    return terms


def write_term(title, description, example, tip):
    new_line = f"{title};{description};{example};{tip};user"

    with open("./data/terms.csv", "r", encoding="utf-8") as file:
        existing_lines = [line.strip("\n") for line in file.readlines()]

    header = existing_lines[0]
    old_terms = existing_lines[1:]
    updated_terms = old_terms + [new_line]
    updated_terms.sort()

    with open("./data/terms.csv", "w", encoding="utf-8") as file:
        file.write("\n".join([header] + updated_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    description_lengths = []
    example_lengths = []

    with open("./data/terms.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        title, description, example, tip, source = line.split(";")
        description_lengths.append(len(description.split()))
        example_lengths.append(len(example.split()))

        if source == "user":
            user_terms += 1
        elif source == "db":
            db_terms += 1

    total = db_terms + user_terms

    if total == 0:
        return {
            "terms_all": 0,
            "terms_own": 0,
            "terms_added": 0,
            "words_avg": 0,
            "words_max": 0,
            "words_min": 0,
            "example_avg": 0,
        }

    return {
        "terms_all": total,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": round(sum(description_lengths) / len(description_lengths), 1),
        "words_max": max(description_lengths),
        "words_min": min(description_lengths),
        "example_avg": round(sum(example_lengths) / len(example_lengths), 1),
    }


def get_quiz_questions():
    return [
        {
            "id": 1,
            "question": "Человек читает только те новости, которые подтверждают его прежнее мнение. Какое искажение здесь проявляется?",
            "options": [
                "Ошибка подтверждения",
                "Регрессия к среднему",
                "Ошибка выжившего",
                "Эффект ореола",
            ],
            "correct": "Ошибка подтверждения",
            "explanation": "Ошибка подтверждения — это склонность замечать и ценить только подтверждающую информацию.",
        },
        {
            "id": 2,
            "question": "После того как товар сначала показали за 20 000 рублей, цена 12 000 кажется очень выгодной. Какое искажение проявляется?",
            "options": [
                "Эвристика доступности",
                "Эффект якоря",
                "Избыточная уверенность",
                "Иллюзия понимания",
            ],
            "correct": "Эффект якоря",
            "explanation": "Первая увиденная цена становится якорем и влияет на дальнейшую оценку.",
        },
        {
            "id": 3,
            "question": "Человек делает вывод о профессии по одной яркой истории, игнорируя общую статистику. Что это показывает?",
            "options": [
                "Игнорирование базовой частоты",
                "Регрессия к среднему",
                "Подмена трудного вопроса лёгким",
                "Ошибка выжившего",
            ],
            "correct": "Игнорирование базовой частоты",
            "explanation": "Базовая частота — это общая статистика по явлению. Её игнорирование ведёт к плохим выводам.",
        },
        {
            "id": 4,
            "question": "Человек изучает только истории успешных стартапов и решает, что почти все стартапы становятся прибыльными. Какое искажение здесь видно?",
            "options": [
                "Ошибка выжившего",
                "Эффект якоря",
                "Эффект ореола",
                "Ошибка подтверждения",
            ],
            "correct": "Ошибка выжившего",
            "explanation": "Видимы только успешные примеры, а неудачные остаются вне поля зрения.",
        },
        {
            "id": 5,
            "question": "После серии очень плохих результатов ученик показывает чуть лучший результат, даже без нового метода подготовки. Какой принцип это объясняет?",
            "options": [
                "Эвристика доступности",
                "Регрессия к среднему",
                "Эффект якоря",
                "Избыточная уверенность",
            ],
            "correct": "Регрессия к среднему",
            "explanation": "Сильные отклонения часто сменяются более обычными значениями просто из-за статистики.",
        },
    ]