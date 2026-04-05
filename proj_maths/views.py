from django.shortcuts import render
from django.core.cache import cache
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
        cache.clear()
        user_name = request.POST.get("name")
        new_bias = request.POST.get("new_bias", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_bias) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            biases_work.write_bias(new_bias, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "bias_request.html", context)
    else:
        add_bias(request)


def show_stats(request):
    stats = biases_work.get_biases_stats()
    return render(request, "stats.html", stats)
