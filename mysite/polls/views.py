from django.shortcuts import render
from .forms import Myform
from .models import Info

# def getform(request):
#     form = Myform()
#     return render(request, 'polls/userdata.html',{'form':form})

def showformdata(request):
    if request.method == "POST":
        #Get the posted form
        drive_link = request.POST.get('drive_link')
        data = Info(drive_link=drive_link)
        data.save()
        x = len(drive_link)
        for i in range(x-1,-1,-1):
            if drive_link[i] == '/':
                break
            
        folder_id = drive_link[i+1:]
        print('-----------------'+folder_id+'----------------------------')
        return render(request, 'polls/handleForm.html')
    else:
        form = Myform()

    return render(request, 'polls/userdata.html', {"form" : form})

