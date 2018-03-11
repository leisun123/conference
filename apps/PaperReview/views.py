from django.contrib.auth.models import Group, Permission
from django.forms import inlineformset_factory
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from apps.PaperReview.forms import AuthorForm, PaperForm, MyFormSetHelper, \
    AuthorFormset, KeywordsForm, KeywordsFormset, AssignmentForm,  ReviewForm, AssignReviewFormset

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views import generic
from apps.PaperReview.models import Paper, Assignment, Review, Keywords, Author
from apps.accounts.models import Scholar
#from apps.PaperReview.wrappers import permission_required_or_403
from guardian.mixins import PermissionRequiredMixin
from guardian.core import ObjectPermissionChecker
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required_or_403
from apps.PaperReview.forms import mylinehelper
from apps.crispy_forms.layout import Layout
from apps.mail.mail import send_mail
from conference import settings
from guardian.models import UserObjectPermission
from apps.PaperReview.mixins import AccessDeniedMixin
from apps.PaperReview.signals import paper_save_signal, paper_update_signal, assignment_save_signal, \
    assignment_save_callback


class PaperListView(AccessDeniedMixin, generic.ListView):
    template_name = 'upload/list.html'
    context_object_name = 'paper_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM
    model = Paper
    
    def dispatch(self, request, *args, **kwargs):
        denind = self.check(request, **kwargs)
        return denind if denind else \
            super(PaperListView, self).dispatch(request)
    
    
    def get_queryset(self, *args, **kwargs):
        content_type = Permission.objects.get(codename='view_paper').content_type

        return \
            [Paper.objects.get(id=obj.object_pk) for obj in UserObjectPermission.objects \
                .filter(user=self.request.user, content_type=content_type).all()]
    
    def get_context_data(self, **kwargs):
        return super(PaperListView, self).get_context_data(**kwargs)


class PaperCreateView(AccessDeniedMixin, generic.CreateView):
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
            [Author.objects.create(**author) for author in authors]
        )
        
        paper_save_signal.send(sender=self.__class__, request=request, paper_object=paper_object)
        return HttpResponseRedirect(
            reverse('display_paper', kwargs={'pk': paper_object.id})
        )
    
    def form_invalid(self, *forms):
        self.object = None
        return self.render_to_response(
            self.get_context_data()
        )


class PaperUpdateView(AccessDeniedMixin, generic.UpdateView):
    model = Paper
    template_name = 'upload/create.html'
    form_class = PaperForm
    
    @method_decorator(permission_required_or_403('PaperReview.update_paper', (Paper, 'id', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(PaperUpdateView, self).dispatch(request)
    
    def get_context_data(self, **kwargs):
        
        context = super(PaperUpdateView, self).get_context_data(**kwargs)
        
        InlineKeywordsFormset = inlineformset_factory(Paper, Keywords, fields=('keyword',), extra=0, can_delete=False)
        InlineAuthorFormset = inlineformset_factory(Paper, Author, fields=('name', 'organization', 'email', 'index'),
                                                    extra=0, can_delete=False)
        
        context['paper_form'] = PaperForm(instance=self.get_object())
        context['keywords_formset'] = InlineKeywordsFormset(prefix='keywords_form', instance=self.get_object())
        context['authors_formset'] = InlineAuthorFormset(prefix='authors_form', instance=self.get_object())
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
        self.object = self.get_object()
        paper, keywords, authors = [form.cleaned_data for form in forms]
        
        lastest_version = self.get_object().version
        paper['uploader'] = request.user
        paper['version'] = lastest_version + 1
        paper['serial_number'] = self.get_object().serial_number
        
        new_paper_obj = Paper.objects.create(**paper)
        
        new_paper_obj.keywords_set.set(
            [Keywords.objects.create(**keyword) for keyword in keywords]
        )
        
        new_paper_obj.author_set.set(
            [Author.objects.create(**author) for author in authors]
        )
        
        paper_update_signal.send(sender=self.__class__, request=request, new_paper_object=new_paper_obj, old_paper_object=self.get_object())
        return HttpResponseRedirect(
            reverse('display_paper', kwargs=
            {"pk": new_paper_obj.id}
                    ))
    
    def form_invalid(self, *forms):
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data()
        )


class PaperDisplayView(AccessDeniedMixin, generic.DetailView):
    template_name = 'upload/display.html'
    model = Paper


class AssignmentListView(AccessDeniedMixin, generic.ListView):
    template_name = 'assign/list.html'
    context_object_name = 'assignment_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM
    

    def dispatch(self, request, *args, **kwargs):
        denind = self.check(request, **kwargs)
        return denind if denind else \
            super(AssignmentListView, self).dispatch(request)
    
 
    def get_queryset(self):
        assignment_list = Assignment.objects.order_by('id')
        return assignment_list
    
    def get_context_data(self, **kwargs):
        return super(AssignmentListView, self).get_context_data(**kwargs)

class AssignmentCreateView(AccessDeniedMixin, generic.UpdateView):
    model = Assignment
    template_name = 'assign/create.html'
    form_class = AssignmentForm
    
    @method_decorator(permission_required_or_403('PaperReview.create_assignment', (Assignment, 'id', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(AssignmentCreateView, self).dispatch(request)
    
    def get_context_data(self, **kwargs):
        context = super(AssignmentCreateView, self).get_context_data(**kwargs)
        context['assignment_form'] = AssignmentForm
        context['assignreview_formset'] = AssignReviewFormset(prefix='assignreview_formset')
        context['myinlinehelper'] = mylinehelper
        return context
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        
        assignment_form = AssignmentForm(request.POST)
        assignreview_formset = AssignReviewFormset(request.POST, prefix='assignreview_formset')
        
        if assignment_form.is_valid() and assignreview_formset.is_valid():
            
            return self.form_valid(request, [assignment_form, assignreview_formset])
        else:
            return self.form_invalid()
    
    def form_valid(self, request, forms):
        self.object = self.get_object()
        assignment, reviewers = [form.cleaned_data for form in forms]
        
        # if assignment['status']:
        #     self.object.status = assignment['status']
        #     if assignment['status'] == "3":
        #         assign_perm('update_paper', self.object.paper.uploader, self.object.paper)
        #
        #     # TODO: send email with three templates according to difffent status
        #     if assignment['status'] == "2":
        #         pass
        #
        #     if assignment['status'] == "1":
        #         pass
        #
        # if assignment['proposal_to_author']:
        #     self.object.proposal_to_author = assignment['proposal_to_author']
        # self.object.save()
        #
        #
        # for review in reviews:
        #     if "reviewer" in review.keys():
        #         review_object = Review.objects.create(reviewer=review['reviewer'], assignment=self.object)
        #         assign_perm('view_paper', review['reviewer'], self.object().paper)
        #         assign_perm('view_review', review['reviewer'], review_object)
        #         assign_perm('create_review', review['reviewer'], review_object)
        
        return HttpResponseRedirect(
            reverse('display_assignment', kwargs=
            {"pk": self.get_object().id}
                    ))
    
    def form_invalid(self):
        print(11121111)
        self.object = self.get_object()
        return self.render_to_response(
            self.get_context_data()
        )


class AssignmentDisplayView(AccessDeniedMixin, generic.DeleteView):
    template_name = 'assign/display.html'
    model = Assignment


class ReviewListView(AccessDeniedMixin, generic.ListView):
    template_name = 'review/list.html'
    context_object_name = 'review_list'
    page_kwarg = 'page'
    paginate_by = settings.PAGE_NUM


    def dispatch(self, request, *args, **kwargs):
        denind = self.check(request, **kwargs)
        return denind if denind else \
            super(ReviewListView, self).dispatch(request)

    def get_queryset(self, *args, **kwargs):
        queryset = Review.objects.filter(reviewer=self.request.user).order_by('create_time')
        return queryset


class ReviewCreateView(AccessDeniedMixin, generic.UpdateView):
    model = Review
    template_name = 'review/create.html'
    form_class = ReviewForm
    
    @method_decorator(permission_required_or_403('PaperReview.create_review', (Review, 'id', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewCreateView, self).dispatch(request)
    
    def get_success_url(self):
        return HttpResponseRedirect(
            reverse('displayreview', kwargs={"pk": self.get_object().id}))


class ReviewDisplayView(AccessDeniedMixin, generic.DetailView):
    template_name = 'review/display.html'
    model = Review
    
    @method_decorator(permission_required_or_403('review.view_review'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReviewDisplayView, self).dispatch(request)

























