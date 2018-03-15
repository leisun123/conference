from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from apps.PaperReview.models import Assignment, Author, Paper
from apps.accounts.models import Scholar

from apps.main.models import GenericTagContent, SideBar
from django.shortcuts import render_to_response
from conference import settings

class IndexView(TemplateView):
    
    template_name = "main/index.html"
    
class GenericTabContentView(DetailView):

    template_name = 'main/generic_tab_content.html'
    model = GenericTagContent
    
class ScholarListView(ListView):
    
    template_name = 'main/scholar_list.html'
    context_object_name = 'assignment_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM
    
    def get_queryset(self):
        
        return \
            Assignment.objects.filter(status='2').order_by('paper__create_time')
            
    
    def get_context_data(self, **kwargs):
        return super(ScholarListView, self).get_context_data(**kwargs)
    

def handler403(request):
    response = render_to_response('share_layout/403.html', {})
    response.status_code = 403
    return response

def handler404(request):
    response = render_to_response('share_layout/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('share_layout/500.html', {})
    response.status_code = 500
    return response


def display_data(request, data, **kwargs):
    return render_to_response('posted-data.html', dict(data=data, **kwargs))







