"""Views for the CogniTrainer educational project."""

from django.shortcuts import redirect, render

from . import biases_work

MIN_BIAS_TITLE_LENGTH = 3
MIN_BIAS_DESCRIPTION_LENGTH = 15
MIN_BIAS_EXAMPLE_LENGTH = 15
MIN_BIAS_TIP_LENGTH = 10

NO_ANSWER_TEXT = "нет ответа"
NO_PREFERENCE_TEXT = "безразлично"


def index(request):
    """Render the home page."""
    return render(request, "index.html")


def biases_list(request):
    """Render the list of cognitive biases."""
    biases = biases_work.get_biases_for_table()
    return render(request, "bias_list.html", {"biases": biases})


def add_bias(request):
    """Render the form for adding a new bias card."""
    return render(request, "bias_add.html")


def send_bias(request):
    """Validate and save a new bias card."""
    if request.method != "POST":
        return render(request, "bias_add.html")

    user_name = request.session.get("user_name", "")
    title = _sanitize_text(request.POST.get("new_bias", ""))
    description = _sanitize_text(request.POST.get("new_definition", ""))
    example = _sanitize_text(request.POST.get("example", ""))
    tip = _sanitize_text(request.POST.get("tip", ""))

    success, comment = _validate_bias_form(title, description, example, tip)
    context = {
        "user": user_name,
        "success": success,
        "comment": comment,
    }

    if success:
        biases_work.write_bias(title, description, example, tip)

    return render(request, "submit_result.html", context)


def show_stats(request):
    """Render the page with bias statistics."""
    stats = biases_work.get_biases_stats()
    return render(request, "stats.html", stats)


def quiz_view(request):
    """Render the quiz page or quiz results."""
    questions = biases_work.get_quiz_questions()

    if request.method != "POST":
        return render(request, "quiz.html", {"questions": questions})

    user_name = request.session.get("user_name", "")
    results, score = _build_quiz_results(request, questions)

    context = {
        "user_name": user_name,
        "score": score,
        "total": len(questions),
        "results": results,
    }
    return render(request, "quiz_result.html", context)


def risk_game_view(request):
    """Render the risk games page or its results."""
    games = biases_work.get_risk_games()

    if request.method != "POST":
        return render(request, "risk_game.html", {"games": games})

    user_name = request.session.get("user_name", "")
    results, score = _build_risk_game_results(request, games)
    profile = biases_work.analyze_risk_profile(results)

    context = {
        "user_name": user_name,
        "score": score,
        "total": len(games),
        "results": results,
        "profile": profile,
    }
    return render(request, "risk_result.html", context)


def set_user_name(request):
    """Save the user name into the session."""
    if request.method == "POST":
        user_name = _sanitize_text(request.POST.get("global_user_name", ""))
        request.session["user_name"] = user_name

    return redirect(_get_referer_or_home(request))


def clear_user_name(request):
    """Remove the user name from the session."""
    request.session.pop("user_name", None)
    return redirect(_get_referer_or_home(request))


def _sanitize_text(value):
    """Trim text and replace CSV separators."""
    return value.strip().replace(";", ",")


def _validate_bias_form(title, description, example, tip):
    """Validate the bias form and return status with message."""
    if len(title) < MIN_BIAS_TITLE_LENGTH:
        return False, "Название искажения должно содержать минимум 3 символа."

    if len(description) < MIN_BIAS_DESCRIPTION_LENGTH:
        return False, "Объяснение должно содержать минимум 15 символов."

    if len(example) < MIN_BIAS_EXAMPLE_LENGTH:
        return False, "Пример должен содержать минимум 15 символов."

    if len(tip) < MIN_BIAS_TIP_LENGTH:
        return False, "Совет должен содержать минимум 10 символов."

    return True, "Карточка успешно добавлена."


def _build_quiz_results(request, questions):
    """Build detailed quiz results and compute score."""
    results = []
    score = 0

    for question in questions:
        selected_answer = request.POST.get(f"question_{question['id']}", "")
        is_correct = selected_answer == question["correct"]

        if is_correct:
            score += 1

        results.append(
            {
                "question": question["question"],
                "selected": selected_answer,
                "correct": question["correct"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )

    return results, score


def _build_risk_game_results(request, games):
    """Build detailed results for risk games and compute score."""
    results = []
    score = 0

    for game in games:
        selected_answer = request.POST.get(f"game_{game['id']}", "") or NO_ANSWER_TEXT
        is_correct = _is_risk_game_answer_correct(selected_answer, game["recommended"])

        if is_correct:
            score += 1

        results.append(
            {
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
            }
        )

    return results, score


def _is_risk_game_answer_correct(selected_answer, recommended_answer):
    """Check whether the selected risk-game answer is acceptable."""
    if recommended_answer == NO_PREFERENCE_TEXT:
        return selected_answer != NO_ANSWER_TEXT

    return selected_answer == recommended_answer


def _get_referer_or_home(request):
    """Return HTTP_REFERER or fallback to the home page."""
    return request.META.get("HTTP_REFERER", "/")
