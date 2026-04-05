from django.shortcuts import render
from . import terms_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        user_name = request.POST.get("name", "").strip()
        title = request.POST.get("new_term", "").strip()
        description = request.POST.get("new_definition", "").strip()
        example = request.POST.get("example", "").strip()
        tip = request.POST.get("tip", "").strip()

        # Убираем символы-разделители CSV
        title = title.replace(";", ",")
        description = description.replace(";", ",")
        example = example.replace(";", ",")
        tip = tip.replace(";", ",")

        context = {"user": user_name}

        if len(title) < 3:
            context["success"] = False
            context["comment"] = "Название искажения должно содержать минимум 3 символа."
        elif len(description) < 15:
            context["success"] = False
            context["comment"] = "Объяснение должно содержать минимум 15 символов."
        elif len(example) < 15:
            context["success"] = False
            context["comment"] = "Пример должен содержать минимум 15 символов."
        elif len(tip) < 10:
            context["success"] = False
            context["comment"] = "Совет должен содержать минимум 10 символов."
        else:
            terms_work.write_term(title, description, example, tip)
            context["success"] = True
            context["comment"] = "Карточка успешно добавлена."

        return render(request, "term_request.html", context)

    return render(request, "term_add.html")


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)


def quiz_view(request):
    questions = terms_work.get_quiz_questions()

    if request.method == "POST":
        user_name = request.POST.get("user_name", "").strip()
        score = 0
        results = []

        for question in questions:
            selected_answer = request.POST.get(f"question_{question['id']}", "")
            is_correct = selected_answer == question["correct"]

            if is_correct:
                score += 1

            results.append({
                "question": question["question"],
                "selected": selected_answer,
                "correct": question["correct"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
            })

        context = {
            "user_name": user_name,
            "score": score,
            "total": len(questions),
            "results": results,
        }
        return render(request, "quiz_result.html", context)

    return render(request, "quiz.html", {"questions": questions})