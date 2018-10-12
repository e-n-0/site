from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from gcc.models import Answer, Applicant, Edition, Event, EventChoice, SubscriberEmail, Trainer, Forms
from users.models import ProloginUser

from gcc.forms import EmailForm, build_dynamic_form, ApplicationValidationForm

# Photos


class PhotosIndexView(TemplateView):
    template_name = "gcc/photos_index.html"


class PhotosEditionView(TemplateView):
    template_name = "gcc/photos_edition.html"


class PhotosEventView(TemplateView):
    template_name = "gcc/photos_event.html"


# Posters


class PostersView(TemplateView):
    template_name = "gcc/posters.html"


# Team


class TeamIndexView(TemplateView):
    template_name = "gcc/team_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editions"] = Edition.objects.order_by('-year')
        context["trainers"] = Trainer.objects.order_by('user__last_name', 'user__first_name')
        return context


class TeamEditionView(TemplateView):
    template_name = "gcc/team_edition.html"

    def get_context_data(self, year):
        context = {
            'edition': get_object_or_404(Edition, year=year)
        }
        return context


# About


class AboutView(TemplateView):
    template_name = "gcc/about.html"


# Homepage


class IndexView(FormView):
    template_name = "gcc/index.html"
    form_class = EmailForm
    success_url = reverse_lazy("gcc:news_confirm_subscribe")

    def form_valid(self, form):
        instance, created = SubscriberEmail.objects.get_or_create(
            email=form.cleaned_data['email'])
        return super().form_valid(form)


# Newsletter


class NewsletterUnsubscribeView(FormView):
    success_url = reverse_lazy("gcc:news_confirm_unsub")
    template_name = "gcc/news_unsubscribe.html"
    form_class = EmailForm

    def form_valid(self, form):
        try:
            account = SubscriberEmail.objects.get(
                    email=form.cleaned_data['email'])
            account.delete()
            return super().form_valid(form)
        except SubscriberEmail.DoesNotExist:
            return HttpResponseRedirect(
                    reverse_lazy("gcc:news_unsubscribe_failed"))


class NewsletterConfirmSubscribeView(TemplateView):
    template_name = "gcc/news_confirm_subscribe.html"


class NewsletterConfirmUnsubView(TemplateView):
    template_name = "gcc/news_confirm_unsub.html"


# Application


#TODO: Check if the user is logged in
class ApplicationForm(FormView):
    template_name = 'gcc/application_form.html'

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        self.user = get_object_or_404(ProloginUser, pk=self.kwargs['user_id'])
        return build_dynamic_form(Forms.application, self.user)

    def get_success_url(self):
        return reverse_lazy(
            'gcc:application_validation',
            kwargs = {'user_id': self.user.pk})

    def form_valid(self, form):
        form.save()
        return super(ApplicationForm, self).form_valid(form)


#TODO: Check if the user is logged in
#TODO: Check if there is an event with opened application
#TODO: Check that the user has filled ApplicationForm and isn't registered yet
class ApplicationValidation(FormView):
    success_url = reverse_lazy("gcc:index")
    template_name = 'gcc/application_validation.html'
    form_class = ApplicationValidationForm

    def get_context_data(self, **kwargs):
        kwargs['events'] = Event.objects.filter(
            signup_start__lt = date.today(),
            signup_end__gt = date.today()
        )
        return super(ApplicationValidation, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.user = get_object_or_404(ProloginUser, pk=self.kwargs['user_id'])
        form.save(self.user)
        return super(ApplicationValidation, self).form_valid(form)


#TODO: Check permissions to access this page
class ApplicationIndexView(TemplateView):
    template_name = "gcc/application_index.html"

    def get_context_data(self, **kwargs):
        """
        Extract the list of users who have an application this year and list
        their applications in the same object.
        """
        #TODO: permissions to moderate each event ?
        current_edition = Edition.objects.latest('year')
        applicants = Applicant.objects.filter(edition=current_edition)

        # Get the set of users applying for this year
        applicants_list = {
            app: {
                'user': app.user,
                'answers': Answer.objects.filter(applicant=app),
                'applications': EventChoice.objects.filter(applicant=app)
            }
            for app in applicants
        }

        return {'applicants': applicants_list}
