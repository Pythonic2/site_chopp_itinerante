from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request,'index.html')

@csrf_exempt
def simple_test(request):
    if request.method == "POST":
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'xx'})
