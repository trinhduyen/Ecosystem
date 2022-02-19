from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def my_profile_view(request):
    pass
