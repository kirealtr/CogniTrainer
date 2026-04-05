from django.shortcuts import render, redirect
from . import biases_work


def index(request):
    return render(request, "index.html")


def biases_list(request):
    biases = biases_work.get_biases_for_table()
    return render(request, "bias_list.html", context={"biases": biases})


def add_bias(request):
    return render(request, "bias_add.html")


def send_bias(request):
    if request.method == "POST":
        user_name = request.session.get("user_name", "")
        title = request.POST.get("new_bias", "").strip()
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
            biases_work.write_bias(title, description, example, tip)
            context["success"] = True
            context["comment"] = "Карточка успешно добавлена."

        return render(request, "bias_request.html", context)

    return render(request, "bias_add.html")


def show_stats(request):
    stats = biases_work.get_biases_stats()
    return render(request, "stats.html", stats)


def quiz_view(request):
    questions = biases_work.get_quiz_questions()

    if request.method == "POST":
        user_name = request.session.get("user_name", "")
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

def risk_game_view(request):
    games = biases_work.get_risk_games()

    if request.method == "POST":
        user_name = request.session.get("user_name", "")
        score = 0
        results = []

        for game in games:
            selected_answer = request.POST.get(f"game_{game['id']}", "")

            if not selected_answer:
                selected_answer = "нет ответа"

            if game["recommended"] == "безразлично":
                is_correct = selected_answer != "нет ответа"
            else:
                is_correct = selected_answer == game["recommended"]

            if is_correct:
                score += 1

            results.append({
                "group": game["group"],
                "title": game["title"],
                "subtitle": game["subtitle"],
                "left_label": game["left_label"],
                "right_label": game["right_label"],
                "left_text": game["left_text"],
                "right_text": game["right_text"],
                "selected": selected_answer,
                "recommended": game["recommended"],
                "is_correct": is_correct,
                "explanation": game["explanation"],
                "lesson": game["lesson"],
                "left_ev": game["left_ev"],
                "right_ev": game["right_ev"],
            })

        profile = biases_work.analyze_risk_profile(results)

        context = {
            "user_name": user_name,
            "score": score,
            "total": len(games),
            "results": results,
            "profile": profile,
        }
        return render(request, "risk_result.html", context)

    return render(request, "risk_game.html", {"games": games})

def set_user_name(request):
    if request.method == "POST":
        user_name = request.POST.get("global_user_name", "").strip()
        user_name = user_name.replace(";", ",")
        request.session["user_name"] = user_name
    return redirect(request.META.get("HTTP_REFERER", "/"))


def clear_user_name(request):
    request.session.pop("user_name", None)
    return redirect(request.META.get("HTTP_REFERER", "/"))