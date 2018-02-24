from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.encoding import smart_str
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

from apps.accounts.models import Scholar
from apps.thesis.forms import ThesisUploadForm, ThesisReviewForm

from django.views.generic import FormView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.thesis.models import Thesis, Review
from conference import settings



class UploadView(LoginRequiredMixin, FormView):
    
    form_class = ThesisUploadForm
    template_name = 'thesis_review/upload.html'
    success_url = '/'
    #
    # def get(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
            form = ThesisUploadForm(request.POST, request.FILES)
            if form.is_valid():
                return self.form_valid(form, request, **kwargs)
            else:
                return self.form_invalid(form, **kwargs)
            
    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context["errors"] = form.errors
        print(form.errors)
        return self.render_to_response(context)
    
    def form_valid(self, form, request):
    # take some other action here
        form.save(request)
        return HttpResponseRedirect(self.get_success_url())

    
    
class ReviewIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'thesis_review/review_index.html'
    context_object_name = 'thesis'
    
    def get_context_data(self, *args, **kwargs):
        kwargs["status_choices"] = Thesis.STATUS_CHOICES.items()
        kwargs["thesis"] = Thesis.objects.all()
        kwargs["scholars"] = Scholar.objects.all()
        return super(ReviewIndexView, self).get_context_data(**kwargs)
    
class ReviewView(FormMixin, DetailView):
    model = Review
    form_class = ThesisReviewForm
    template_name = 'thesis_review/review.html'

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        try:
            review = Review.objects.get(thesis_id=self.kwargs.get('thesis_id'))
            return review
        except self.model.DoesNotExist:
            raise Http404("No MyModel matches the given query.")

    def get_context_data(self, *args, **kwargs):
        context = super(ReviewView, self).get_context_data(*args, **kwargs)

        # form
        context['form'] = self.get_form()
        context['review'] = self.get_object()
        context['thesis'] = Thesis.objects.get(id=self.object.pk)
        context['conclusion'] = Review.CONCLUSION_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        form = ThesisReviewForm(request.POST)
        
        #print(smart_str(form))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form):
 
        form.save(thesis_id=self.kwargs.get('thesis_id'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
    
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context["errors"] = form.errors

        return self.render_to_response(context)
    
    
        
        
        
        
        
        
        
        
        
        
        
    
    