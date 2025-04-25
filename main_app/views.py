import uuid
import os
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Bird, Toy, Photo
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def birds_index(request):
    birds = Bird.objects.filter(user=request.user)
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


def add_photo(request, bird_id):
    # 'photo-file' will be the name of the input field in the form,
    #   return None if it doesn't exist:
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # Create a unique 'key' for S3, needs file extension too:
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # Wrap in a try/except block to handle errors:
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # Build the full URL for the photo:
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # Add the photo to the database (use bird_id from the URL):
            # Note: using bird_id from the URL, not the bird object saves a DB query:
            Photo.objects.create(url=url, bird_id=bird_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', bird_id=bird_id)


class BirdCreate(CreateView):
    model = Bird
    fields = ['name', 'species', 'description', 'age']

    # Override the inherited method called when a valid form is submitted:
    def form_valid(self, form):
        # Assign the logged in user (self.request.user) to the bird (form.instance):
        form.instance.user = self.request.user
        # Pass control back to the superclass CreateView's form_valid() method to do its job:
        return super().form_valid(form)


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


def unassoc_toy(request, bird_id, toy_id):
    Bird.objects.get(id=bird_id).toys.remove(toy_id)
    return redirect('detail', bird_id=bird_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # Create a UserCreationForm instance using the data from the request:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the form to the database:
            user = form.save()
            # Log the user in:
            login(request, user)
            return redirect('index')
        else:
            # If the form is not valid, set the error message:
            error_message = 'Invalid sign up - try again'
    # If the request method is GET, or the sign up fails, render signup.html with an empty form:
    form = UserCreationForm()
    context = { 'form': form, 'error': error_message }
    return render(request, 'registration/signup.html', context)