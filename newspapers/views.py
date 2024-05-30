from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from .models import Redactor, Newspaper, Topic
from .models import ActivateToken
from .forms import (
    RedactorCreationForm,
    RedactorLicenseUpdateForm,
    NewspaperForm,
    ProfileForm,
    RegisterForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    TopicSearchForm,
)
from .services import AccountsEmailNotification

User = get_user_model()


class CreateProfileView(LoginRequiredMixin, FormView):
    template_name = "registration/create_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("movies:movie_list")

    def get_initial(self):
        initial = super().get_initial()

        profile_picture = self.request.session.get("profile_picture")
        if profile_picture:
            initial["avatar"] = profile_picture

        return initial

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()

        self.request.session.pop("profile_picture", None)
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("newspapers:login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect("movies:movie_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        user_token = ActivateToken.objects.create(user=user)

        activate_url = (
            f"{self.request.scheme}://{self.request.get_host()}"
            f"""{reverse("newspapers:activate",
                                     args=[
                                         user.username,
                                         user_token.token
                                     ])}"""
        )

        email_service = AccountsEmailNotification()
        email_service.send_activation_email(
            user.email, user.get_full_name(), activate_url
        )

        messages.info(
            self.request,
            "Registration completed."
            " Please check your email to activate your account.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request: HttpRequest, username: str, token: str):
        user = get_object_or_404(User, username=username)
        token = get_object_or_404(ActivateToken, token=token, user=user)

        if user.is_active:
            messages.error(request, "Redactor is already activated")
            return redirect("movies:movie_list")

        if token.verify_token():
            user.is_active = True
            token.delete()
            user.save()

            messages.success(request, "Activation complete")
            return redirect("movies:movie_list")

        messages.error(request, "Token expired")
        return redirect("movies:movie_list")


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You already logged in")
        return redirect("movies:movie_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True
            user.save()

            messages.info(request, "Registration completed")
            AccountsEmailNotification.send_activation_email(
                user.email, user.get_full_name(), "http://127.0.0.1:8000"
            )
            return redirect("registration:login")
        else:
            return render(request, "registration/register.html", {"form": form})

    return render(request, "registration/register.html", {"form": RegisterForm()})


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspapers/topic_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = TopicSearchForm(
            initial={
                "title": title,
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        for topic in queryset:
            topic.is_creator = topic.newspapers.filter(
                redactor=self.request.user
            ).exists()
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspapers:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("newspapers:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("newspapers:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 5
    context_object_name = "newspapers_list"
    queryset = Newspaper.objects.select_related("topic")
    template_name = "newspapers/newspapers_list.html"
    # num_redactors = Redactor.objects.count()
    # num_newspapers = Newspaper.objects.count()
    # num_topics = Topic.objects.count()
    #
    # extra_context = {
    #     'num_redactors': num_redactors,
    #     'num_newspapers': num_newspapers,
    #     'num_topics': num_topics
    # }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = NewspaperSearchForm(
            initial={
                "title": title,
            }
        )
        return context

    def get_queryset(self):
        self.queryset = Newspaper.objects.all()
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(title__icontains=form.cleaned_data["title"])
        return self.queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    context_object_name = "newspapers"
    template_name = "newspapers/newspapers_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_creator"] = self.object.redactor.filter(
            id=self.request.user.id
        ).exists()
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspapers:newspapers-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("newspapers:newspapers-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("newspapers:newspapers-list")
    template_name = "newspapers/newspapers_confirm_delete.html"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    context_object_name = "redactor_list"
    template_name = "newspapers/redactor_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = RedactorSearchForm(
            initial={
                "username": username,
            }
        )
        return context

    def get_queryset(self):
        self.queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorLicenseUpdateForm
    success_url = reverse_lazy("newspapers:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("")


def toggle_theme(request):
    if request.method == "POST":
        white = request.session.get("white", 1)
        request.session["white"] = 1 if white == 0 else 0
    return redirect("newspapers:newspapers-list")


@login_required
def toggle_assign_to_newspaper(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if Newspaper.objects.get(id=pk) in redactor.newspaper.all():
        redactor.newspaper.remove(pk)
    else:
        redactor.newspaper.add(pk)
    return HttpResponseRedirect(reverse_lazy("newspaper:newspaper-detail", args=[pk]))


def create_newspaper(request):
    if request.method == "POST":
        form = NewspaperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = NewspaperForm()
    return render(request, "newspapers/newspaper_form.html", {"form": form})
