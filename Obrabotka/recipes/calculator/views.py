from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def omlet(request):
    ingredient_number = int(request.GET.get("servings", 1))
    context = {
        'omlet': {
            'яйца, шт': 2 * ingredient_number,
            'молоко, л': 0.1 * ingredient_number,
            'соль, ч.л.': 0.5 * ingredient_number,
        }
    }
    return render(request, 'calculator/index.html', context)


def pasta(request):
    ingredient_number = int(request.GET.get("servings", 1))
    context = {
        'pasta': {
            'макароны, г': 0.3 * ingredient_number,
            'сыр, г': 0.05 * ingredient_number,
        }
    }
    return render(request, 'calculator/index1.html', context)


def buter(request):
    ingredient_number = int(request.GET.get("servings", 1))
    context = {
        'buter': {
            'хлеб, ломтик': 1 * ingredient_number,
            'колбаса, ломтик': 1 * ingredient_number,
            'сыр, ломтик': 1 * ingredient_number,
            'помидор, ломтик': 1 * ingredient_number,
        },
    }
    return render(request, 'calculator/index2.html', context)