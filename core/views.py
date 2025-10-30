from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_financiera_view(request):
    return render(request, 'dashboard/dashboard_financiera.html')