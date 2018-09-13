from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from MinApp.Minimizer import *
# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        minimizedURL = "media\\" + filename

        try:
            theMinimizer = Minimizer(minimizedURL,20,20,5)
            theMinimizer.minimizeAndSave(minimizedURL)
        except ValueError:
            errorMessage = "Image minmizing failed. Image may be too small."
            return render(request, 'MinApp/index.html', {
                    'error_message' : errorMessage
                })

        return render(request, 'MinApp/index.html', {
            'uploaded_file_url': minimizedURL
        })
    return render(request, 'MinApp/index.html')

def results(request):
	context = {}
	return render(request, 'MinApp/results.html',context)