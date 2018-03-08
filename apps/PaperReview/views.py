from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from apps.PaperReview.forms import AuthorForm, PaperForm, MyFormSetHelper, \
    AuthorFormset, KeywordsForm, KeywordsFormset, AssignmentForm, InlineReviewFormset, ReviewForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views import generic
from apps.PaperReview.models import Paper, Assignment, Review, Keywords,  Author
from apps.accounts.models import Scholar
from guardian.decorators import permission_required_or_403, permission_required
from guardian.mixins import PermissionRequiredMixin
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm
from apps.PaperReview.forms import mylinehelper
from apps.crispy_forms.layout import Layout
from apps.mail.mail import send_mail
from conference import settings


class PaperListView(LoginRequiredMixin, generic.ListView):
    
    template_name = 'upload/list.html'
    context_object_name = 'paper_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        paper_list = Paper.objects.order_by('create_time')
        return paper_list

    def get_context_data(self, **kwargs):
        return super(PaperListView, self).get_context_data(**kwargs)


class PaperCreateView(LoginRequiredMixin, generic.CreateView):

    model = Paper
    template_name = 'upload/create.html'
    form_class = PaperForm
    
    
    def dispatch(self, request, *args, **kwargs):
        return super(PaperCreateView, self).dispatch(request)


    def get_context_data(self, **kwargs):
        context = super(PaperCreateView, self).get_context_data(**kwargs)
        context['paper_form'] = PaperForm
        context['keywords_formset'] = KeywordsFormset(prefix='keywords_form')
        context['authors_formset'] = AuthorFormset(prefix='authors_form')
        context['myinlinehelper'] = mylinehelper
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        paper_form = PaperForm(request.POST, request.FILES)
        keywords_formset = KeywordsFormset(request.POST, prefix='keywords_form')
        authors_formset = AuthorFormset(request.POST, prefix='authors_form')
        if paper_form.is_valid() and keywords_formset.is_valid() and authors_formset.is_valid():
            return self.form_valid(request, [paper_form, keywords_formset, authors_formset])
        else:
            return self.form_invalid([paper_form, keywords_formset, authors_formset])
    
    def form_valid(self, request, forms):
        self.object = None
    
        paper, keywords, authors = [form.cleaned_data for form in forms]
        paper['uploader'] = Scholar.objects.get(username=request.user)
        paper_object = Paper.objects.create(**paper)

        paper_object.keywords_set.set(
            [Keywords.objects.create(**keyword) for keyword in keywords]
        )

        paper_object.author_set.set(
            [Author.objects.create(**author) for author in  authors]
        )

        #TODO:celery to assign
        import random
        editors = Group.objects.get(name="editor").user_set.all()
        editor = random.choice(editors)
        
        assignment = Assignment.objects.create(editor=editor, paper=paper_object)
        
        assign_perm('view_paper', request.user, paper_object)
        assign_perm('view_paper', editor, paper_object)
        assign_perm('view_assignment', editor, assignment)
        assign_perm('create_assignment', editor, assignment)
        
        #TODO:mail to editor
        send_mail("123", "123", settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com',], html='core/base.html')
        
        return HttpResponseRedirect(
                reverse('display_paper', kwargs={'pk':paper_object.id})
            )

    def form_invalid(self, *forms):
        return self.render_to_response(
            self.get_context_data()
            )

class PaperUpdateView(LoginRequiredMixin, generic.UpdateView):

        model = Paper
        template_name = 'upload/create.html'
        form_class = PaperForm
       
        def dispatch(self, request, *args, **kwargs):
            return super(PaperUpdateView, self).dispatch(request)

        
        def get_context_data(self, **kwargs):
        
            context = super(PaperUpdateView, self).get_context_data(**kwargs)
            
            
            InlineKeywordsFormset = inlineformset_factory(Paper, Keywords, fields=('keyword',), extra=0, can_delete=False)
            InlineAuthorFormset = inlineformset_factory(Paper, Author, fields=('name', 'organization', 'email', 'index'), extra=0, can_delete=False)
            
            context['paper_form'] = PaperForm(instance=self.get_object())
            context['keywords_formset'] = InlineKeywordsFormset(prefix='keywords_form', instance=self.get_object())
            context['authors_formset'] = InlineAuthorFormset(prefix='authors_form', instance=self.get_object())
            context['myinlinehelper'] = mylinehelper
            return context

       
        def post(self, request, *args, **kwargs):
            paper_form = PaperForm(request.POST, request.FILES)
            keywords_formset = KeywordsFormset(request.POST, prefix='keywords_form')
            authors_formset = AuthorFormset(request.POST, prefix='authors_form')
            if paper_form.is_valid() and keywords_formset.is_valid() and authors_formset.is_valid():
                return self.form_valid(request, [paper_form, keywords_formset, authors_formset])
            else:
                return self.form_invalid([paper_form, keywords_formset, authors_formset])

        def form_valid(self, request, forms):
            self.object = self.get_object()
            paper, keywords, authors = [form.cleaned_data for form in forms]
            
            lastest_version = self.get_object().version
            paper['uplodaer'] = request.user
            paper['version'] = lastest_version + 1
            paper['serial_number'] = self.get_object().serial_number
            
            new_paper_obj = Paper.objects.create(**paper)
         
            new_paper_obj.keywords_set.set(
                [Keywords.objects.create(**keyword) for keyword in keywords]
            )
            
            new_paper_obj.author_set.set(
                [Author.objects.create(**author) for author in  authors]
            )
            
            lastest_assignment_object = self.get_object().assignment

            if lastest_assignment_object.status == '3':
                lastest_review_set = [Review.objects.create(reviewer=review.reviewer) for review in lastest_assignment_object.review_set().all()]
                lastest_assignment_object = Assignment.objects.create(editor=lastest_assignment_object.editor, paper=new_paper_obj)
                lastest_assignment_object.review_set.set(lastest_review_set)
                #TODO: send mail to old reviewers except editor
                send_mail("123", "123", settings.DEFAULT_FROM_EMAIL, recipient_list=['genius_wz@aliyun.com',], html='core/base.html')
            
            assign_perm('view_paper', request.user, self.get_object())
            assign_perm('view_paper', lastest_assignment_object.editor, self.get_object())
            assign_perm('view_assignment', lastest_assignment_object.editor, lastest_assignment_object)
            assign_perm('create_assignment', lastest_assignment_object.editor, lastest_assignment_object)
            
            
            return HttpResponseRedirect(
                reverse('display_paper', kwargs=
                {"pk":new_paper_obj.id}
                ))

        def form_invalid(self, *forms):

            return self.render_to_response(
                self.get_context_data()
                )

class PaperDisplayView(LoginRequiredMixin, generic.DetailView):
    
    template_name = 'upload/display.html'
    model = Paper
    


class AssignmentListView(LoginRequiredMixin, generic.ListView):
    
    template_name = 'assign/list.html'
    context_object_name = 'assignment_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        assignment_list = Assignment.objects.order_by('id')
        return assignment_list

    def get_context_data(self, **kwargs):
        return super(AssignmentListView, self).get_context_data(**kwargs)


class AssignmentCreateView(LoginRequiredMixin, generic.UpdateView):
    
    model = Assignment
    template_name = 'assign/create.html'
    form_class = AssignmentForm
    
    def dispatch(self, request, *args, **kwargs):
        return super(AssignmentCreateView, self).dispatch(request)
        
    def get_context_data(self, **kwargs):
        context = super(AssignmentCreateView, self).get_context_data(**kwargs)
        context['assignment_form'] = AssignmentForm
        context['inline_review_formset'] = InlineReviewFormset(prefix='inline_review_form')
        context['myinlinehelper'] = mylinehelper
        context['paper_object'] = self.get_object().paper
        return context
    
    def post(self, request, *args, **kwargs):

        assignment_form = AssignmentForm(request.POST)
        inline_review_formset = InlineReviewFormset(request.POST, prefix='inline_review_form')
        
        if assignment_form.is_valid() and inline_review_formset.is_valid():
            return self.form_valid(request, [assignment_form, inline_review_formset])
        else:
            return self.form_invalid([assignment_form, inline_review_formset])
        
    def form_valid(self, request, forms):
        self.object = self.get_object()
        assignment, reviews = [form.cleaned_data for form in forms]
        
        if assignment['status']:
            self.object.status = assignment['status']
            if assignment['status'] == "3":
                 assign_perm('update_review', self.object.paper.uploader, self.object.paper)
            
            #TODO: send email with three templates according to difffent status
            if assignment['status'] == "2":
                pass
            
            if assignment['status'] == "1":
                pass
            
            
        if assignment['proposal_to_author']:
            self.object.proposal_to_author = assignment['proposal_to_author']
        self.object.save()
        
        
        
        for review in reviews:
            review_object = Review.objects.create(reviewer=review['reviewer'], assignment=self.object)
            assign_perm('view_paper', review['reviewer'], self.object().paper)
            assign_perm('view_review', review['reviewer'], review_object)
            assign_perm('create_review', review['reviewer'], review_object)
        
        return HttpResponseRedirect(
            reverse('displayassignment'), kwargs=
                {"pk": self.get_object().id})
    
    def form_invalid(self, *forms):
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data()
            )

class AssignmentDisplayView(LoginRequiredMixin, generic.DeleteView):
    
    template_name = 'assign/display.html'
    model = Assignment


class ReviewCreateView(LoginRequiredMixin, generic.UpdateView):

        model = Review
        template_name = 'review/create.html'
        form_class = ReviewForm
       
        def dispatch(self, request, *args, **kwargs):
            return super(ReviewCreateView, self).dispatch(request)
        
        def get_success_url(self):
            return HttpResponseRedirect(
                reverse('displayreview', kwargs={"pk":self.get_object().id}))

        
class ReviewDisplayView(LoginRequiredMixin, generic.DetailView):
    
    template_name = 'review/display.html'
    model = Review


class StatusView(LoginRequiredMixin, generic.TemplateView):
    
    template_name = 'Judgment/status.html'























