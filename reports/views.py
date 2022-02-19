
from pyexpat import model

from matplotlib.pyplot import cla
from profiles.models import Profile
from django.shortcuts import render, get_object_or_404
from reports.models import Report
from reports.forms import ReportForm
from django.http import HttpResponse, JsonResponse
from reports.utils import get_report_image, is_ajax

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
# Create your views here.


class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if is_ajax(request.META):
        #name = request.POST.get('name')
        #remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img = get_report_image(image)
        print(request.user)
        author = Profile.objects.filter(user=request.user)
        print(author)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()
        return JsonResponse({'msg': 'send'})
    return JsonResponse({})
