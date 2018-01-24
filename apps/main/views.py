from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from apps.main.models import GenericTagContent, SideBar


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
    
    
from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('share_layout/404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('share_layout/500.html', {})
    response.status_code = 500
    return response