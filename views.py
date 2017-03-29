from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from Codify import datamanagement
from multiprocessing import Process, Queue
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.formsets import formset_factory, ManagementForm
from django.core.exceptions import ValidationError
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import Deserializer
import ast, json, time
from Codify.forms import UploadFileForm

###index.html
def index(request):
    return render(request,'Codify/index.html')

@csrf_exempt
def jobcall(request):
    if request.method == 'POST':
        environment = str(json.loads(request.body)['environment'])
        batch = json.loads(request.body)['batch']
        client_Name = json.loads(request.body)['client_Name']
        feed_Name = json.loads(request.body)['feed_Name']
        date = json.loads(request.body)['date']
        email = json.loads(request.body)['Email']
        startDate = date['startDate'][:10]
        endDate = date['endDate'][:10]
        startDate = time.strftime("%Y%m%d",time.strptime(startDate,"%Y-%m-%d"))
        endDate = time.strftime("%Y%m%d",time.strptime(endDate,"%Y-%m-%d"))
        dateOption = json.loads(request.body)['DateOption']
        try:
           mediaYear = str(json.loads(request.body)['mediaYear'])
        except KeyError:
           mediaYear = '1901'
        try:
           dateSlicer = str(json.loads(request.body)['mediaQuarter'])
        except KeyError:
           try:
                dateSlicer = str(json.loads(request.body)['mediaMonth'])
           except KeyError:
                dateSlicer = 'Custom' 
        print startDate
        print endDate
        print dateOption
        print dateSlicer
        print mediaYear
        queue = Queue()
        p = Process(target=datamanagement.jobcall(environment,batch,client_Name,feed_Name,startDate,endDate,email,dateOption,dateSlicer,mediaYear))
        p.start()
        p.join()
        return HttpResponse('Success')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            datamanagement.classAct(request.FILES['streamFile'],request.FILES['mapFile'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})
   