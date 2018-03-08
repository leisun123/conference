from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView

from apps.accounts.models import Scholar

from apps.main.models import GenericTagContent, SideBar
from django.shortcuts import render_to_response
from conference import settings

class IndexView(TemplateView):
    
    template_name = "main/index.html"
    
class GenericTabContentView(DetailView):

    template_name = 'main/generic_tab_content.html'
    model = GenericTagContent
    pk_url_kwarg = 'content_id'
    context_object_name = "GenericTagContent"


    def get_context_data(self, **kwargs):
        content_id = int(self.kwargs[self.pk_url_kwarg])
        user = self.request.user

        content = GenericTagContent.objects.filter(id=content_id).first()
        
        kwargs['content'] = content
        return super(GenericTabContentView, self).get_context_data(**kwargs)
    
class ScholarListView(ListView):
    
    template_name = 'main/scholar_list.html'
    context_object_name = 'scholar_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM
    
    def get_queryset(self):
        scholar_list = Scholar.objects.order_by('username')
        return scholar_list
    
    def get_context_data(self, **kwargs):
        return super(ScholarListView, self).get_context_data(**kwargs)
    
    
class ReviewIndexView(TemplateView):
    
    template_name = "Judgment/index.html"


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


