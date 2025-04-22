from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Bird, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def birds_index(request):
    birds = Bird.objects.all()
    return render(request, 'birds/index.html', { 'birds': birds })


def birds_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    # Get the id's of the toys that are already associated with the bird:
    id_list = bird.toys.all().values_list('id')
    # Get the toys that are not associated with the bird:
    toys_bird_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    return render(request, 'birds/detail.html', {
        'bird': bird,
        'feeding_form': feeding_form,
        'toys': toys_bird_doesnt_have
    })


def add_feeding(request, bird_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bird_id = bird_id
        new_feeding.save()
    return redirect('detail', bird_id=bird_id)


class BirdCreate(CreateView):
    model = Bird
    fields = ['name', 'species', 'description', 'age']


class BirdUpdate(UpdateView):
    model = Bird
    fields = ['species', 'description', 'age']


class BirdDelete(DeleteView):
    model = Bird
    success_url = '/birds'


class ToyIndex(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'


def assoc_toy(request, bird_id, toy_id):
    Bird.objects.get(id=bird_id).toys.add(toy_id)
    return redirect('detail', bird_id=bird_id)