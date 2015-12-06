from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from event.forms import NewEventForm


def NewEvent(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            #event = Event()
            print "Ok"
            return HttpResponseRedirect('new_event')
        else:
            return render_to_response('new_event.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' '''
        form = NewEventForm()
        context = {'form':form}
        return  render_to_response('new_event.html',context, context_instance=RequestContext(request))
