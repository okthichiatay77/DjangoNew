from django.shortcuts import render

# Create your views here.

def home_view(request):

    if request.method == 'POST':
        your_domain = request.POST['your_domain']

    return render(request, 'site/home.html')