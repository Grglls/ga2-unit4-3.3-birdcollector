from django.shortcuts import render

# Temporary data:
birds = [
  {'name': 'Lolo', 'breed': 'Moa', 'description': 'Big scary bird!', 'age': 5},
  {'name': 'Sachi', 'breed': 'Kiwi', 'description': 'Gentle and loving.', 'age': 2},
  {'name': 'Bob', 'breed': 'Sparrow', 'description': 'Tinee-tiny bird.', 'age': 0},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def birds_index(request):
    return render(request, 'birds/index.html', { 'birds': birds })