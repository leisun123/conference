"""Generic workflow engine views"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from apps.activflow.constants import WORKFLOW_APPS, REQUEST_IDENTIFIER
from apps.activflow.helpers import (
    get_model,
    get_model_instance,
    get_form,
    get_formsets,
    get_request_params,
    flow_config,
    get_fk
)

from apps.activflow.mixins import AccessDeniedMixin
from apps.activflow.models import get_workflows_requests, get_task


@login_required
def workflows(request):
    """Lists down registered workflows"""
    return render(request, 'core/index.html', {'workflows': WORKFLOW_APPS})


class WorkflowDetail(LoginRequiredMixin, generic.TemplateView):
    """Generic view to list worflow requests & tasks"""
    template_name = 'core/workflow.html'

    def get_context_data(self, **kwargs):
        """Retrieve context data<"""
        context = super(WorkflowDetail, self).get_context_data(**kwargs)
        app_title = get_request_params('app_name', **kwargs)
        config = flow_config(app_title)
        model = config.FLOW[config.INITIAL]['model']().title
        context['requests'] = get_workflows_requests(app_title)
        context['request_identifier'] = REQUEST_IDENTIFIER
        context['workflow_title'] = config.TITLE
        context['description'] = config.DESCRIPTION
        context['initial'] = model

        return context


class ViewActivity(AccessDeniedMixin, generic.DetailView):
    """Generic view to display activity details"""
    template_name = 'core/detail.html'

    def dispatch(self, request, *args, **kwargs):
        """Overriding dispatch on DetailView"""
        self.model = get_model(**kwargs)
        denied = self.check(request, **kwargs)
        return denied if denied else super(ViewActivity, self).dispatch(
            request, *args, **kwargs)


class RollBackActivity(LoginRequiredMixin, generic.View):
    """Rollbacks workflow task"""
    @transaction.atomic
    def post(self, request, **kwargs):
        """POST request handler for rollback"""
        app_title = get_request_params('app_name', **kwargs)
        identifier = get_request_params('pk', **kwargs)
        get_task(identifier).rollback()

        return HttpResponseRedirect(
            reverse('workflow-detail', args=[app_title]))


class DeleteActivity(LoginRequiredMixin, generic.DeleteView):
    """Deletes activity instance"""
    def dispatch(self, request, *args, **kwargs):
        """Overriding dispatch on DeleteView"""
        self.model = get_model(**kwargs)
        self.success_url = reverse_lazy(
            'workflow-detail', args=[get_request_params(
                'app_name', **kwargs)])

        return super(DeleteActivity, self).dispatch(
            request, *args, **kwargs)


class CreateActivity(AccessDeniedMixin, generic.View):
    """Generic view to initiate activity"""
    def get(self, request, **kwargs):
        """GET request handler for Create operation"""
        form = get_form(**kwargs)
        formsets = [formset(
            prefix=formset.form.__name__) for formset in get_formsets(
                self.__class__.__name__, extra=1, **kwargs)]
        context = {'form': form, 'formsets': formsets}

        denied = self.check(request, **kwargs)
        return denied if denied else render(
            request, 'core/create.html', context)

    @transaction.atomic
    def post(self, request, **kwargs):
        """POST request handler for Create operation"""
        operation = self.__class__.__name__
        instance = None
        form = get_form(**kwargs)(request.POST)
        formsets = get_formsets(operation, **kwargs)
        app_title = get_request_params('app_name', **kwargs)

        (result, context) = FormHandler(
            operation, request, form, formsets).handle(**kwargs)

        if not result:
            return render(request, 'core/create.html', context)
        else:
            instance = context

        if instance.is_initial:
            instance.initiate_request(request.user, app_title)
        else:
            instance.assign_task(
                get_request_params('pk', **kwargs))
            instance.task.initiate()

        return HttpResponseRedirect(
            reverse('update', args=(
                app_title, instance.title, instance.id)))


class UpdateActivity(AccessDeniedMixin, generic.View):
    """Generic view to update activity"""
    def get(self, request, **kwargs):
        """GET request handler for Update operation"""
        instance = get_model_instance(**kwargs)
        form = get_form(**kwargs)
        formsets = get_formsets(self.__class__.__name__, extra=1, **kwargs)
        context = {
            'form': form(instance=instance),
            'formsets': [formset(
                instance=instance,
                prefix=formset.form.__name__
            ) for formset in formsets],
            'object': instance,
            'next': instance.next_activity()
        }

        denied = self.check(request, **kwargs)
        return denied if denied else render(
            request, 'core/update.html', context)

    @transaction.atomic
    def post(self, request, **kwargs):
        """POST request handler for Update operation"""
        operation = self.__class__.__name__
        redirect_to_update = False
        instance = get_model_instance(**kwargs)
        app_title = get_request_params('app_name', **kwargs)
        form = get_form(**kwargs)(request.POST, instance=instance)
        formsets = get_formsets(operation, **kwargs)

        (result, context) = FormHandler(
            operation, request, form, formsets, instance).handle(**kwargs)

        if not result:
            return render(request, 'core/update.html', context)

        if 'save' in request.POST:
            redirect_to_update = True
            instance.update()
        elif 'finish' in request.POST:
            instance.finish()
        else:
            next_activity = request.POST['submit']
            if not instance.validate_rule(next_activity):
                redirect_to_update = True
            else:
                instance.task.submit(
                    app_title, self.request.user, next_activity)

        return HttpResponseRedirect(
            reverse('update', args=(
                app_title, instance.title, instance.id))
        ) if redirect_to_update else HttpResponseRedirect(
            reverse(
                'workflow-detail',
                args=[app_title]
            )
        )


# Handlers


class FormHandler(object):
    """Form and Formsets Manager"""
    def __init__(self, operation, request, form, formsets, instance=None):
        """Initializes FormHandler"""
        self.instance = instance
        self.request = request
        self.operation = operation
        self.form = form
        self.formsets = formsets

    def add(self, formsets, instruction):
        """Includes an additional form in the formset(s)"""
        request = self.request.POST.copy()

        for formset in formsets:
            form_title = formset.form.__name__
            if 'add-' + form_title.replace('Form', '') in instruction:
                total_forms = form_title + '-TOTAL_FORMS'
                request[total_forms] = int(request[total_forms]) + 1

        formsets = [formset(
            request, prefix=formset.form.__name__) for formset in formsets]

        context = {
            'form': self.form,
            'formsets': formsets,
        }

        if self.instance:
            context['object'] = self.instance

        return (False, context)

    def save(self, formsets, **kwargs):
        """Persists validated formset(s)"""
        # form
        instance = self.form.save()
        # formsets
        for formset in formsets:
            if not self.instance:  # create operation
                objects = formset.save(commit=False)
                if objects:
                    fk = get_fk(objects, **kwargs)
                    for obj in objects:
                        setattr(obj, fk, instance)
                        obj.save()
            else:  # update operation
                formset.save()
        return (True, instance)

    def report(self, formsets):
        """Report validation errors"""
        errors = ''

        for formset in formsets:
            for error in formset.errors:
                errors = errors + str(error)

        context = {
            'form': self.form,
            'formsets': [formset(
                self.request.POST,
                prefix=formset.form.__name__
            ) for formset in self.formsets],
            'error_message': errors + str(self.form.errors)
        }

        if self.instance:
            context['object'] = self.instance
            context['next'] = self.instance.next_activity()
        return (False, context)

    def handle(self, **kwargs):
        """Adds, validates and persist formsets"""
        instruction = next(iter(filter(
            lambda key: 'add-' in key, self.request.POST)), None)

        # Handle adding related instance

        if instruction:
            formsets = get_formsets(self.operation, **kwargs)
            return self.add(formsets, instruction)

        # Validate and save form/formsets

        formsets = []

        for formset in self.formsets:
            formsets.append(formset(
                self.request.POST,
                instance=self.instance,  # None for create operation
                prefix=formset.form.__name__
            ))

        if self.form.is_valid() and all(
            formset.is_valid() for formset in formsets
        ):
            return self.save(formsets, **kwargs)
        else:
            return self.report(formsets)
