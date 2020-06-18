from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def login(request):
    base_url = reverse('login')
    return HttpResponseRedirect(base_url)
	
def profile(request, pk):
    user = User.objects.get(pk=pk)
    contain = {
        'user': user,
    }
    return render(request, 'profile.html', contain)
