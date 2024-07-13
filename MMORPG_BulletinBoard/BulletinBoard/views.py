from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import AdFilter, ResponseFilter
from .models import Ad, Response
from .forms import AdForm, ResponseForm
from accounts.models import User


# Create your views here.
class OwnerPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().author == self.request.user:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class AdsList(ListView):
    model = Ad
    ordering = '-dateCreation'
    template_name = 'ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad_detail'
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('forbidden')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ads = Ad.objects.get(pk=self.kwargs.get('pk'))
        context['is_author'] = Response.objects.filter(responseAd=ads).filter(responseUser=self.request.user).exists()
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    raise_exception = True
    template_name = 'ad_create.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        if self.request.method == 'POST':
            ad.author = self.request.user
        ad.save()
        return super().form_valid(form)


class AdUpdate(OwnerPermissionRequiredMixin, UpdateView):
    # Настраиваем проверку прав
    permission_required = ('BulletinBoard.change_ad',)
    form_class = AdForm
    model = Ad
    template_name = 'ad_create.html'


class AdDelete(OwnerPermissionRequiredMixin, DeleteView):
    # Настраиваем проверку прав
    permission_required = ('BulletinBoard.delete_ad',)
    model = Ad
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ad_list')


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Response
    raise_exception = True
    template_name = 'ad_detail.html'

    def get_success_url(self):
        return reverse_lazy('ad_detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        response = form.save(commit=False)
        ad = get_object_or_404(Ad, id=self.kwargs['pk'])
        title = ad.title
        response.responseUser = self.request.user
        response.responseAd_id = self.kwargs.get('pk')
        response.save()
        author = User.objects.get(pk=ad.author_id)

        html_content = render_to_string(
            'response_created_email.html',
            {
                'text': f'{response.responseUser}: {response.text}',
                'link': f'{settings.SITE_URL}/ads/{ad.id}',
                'title': f'{title}'
            }
        )

        msg = EmailMultiAlternatives(
            subject="Отклик на объявление",
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[author.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_detail'] = Ad.objects.get(pk=self.kwargs.get('pk'))
        return context


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('response_list')


@login_required
def response_list(request):
    ads = Ad.objects.filter(author=request.user)
    responses = Response.objects.filter(responseAd__in=ads)
    response_filter = ResponseFilter(request.GET, queryset=responses, request=request.user.id)
    ads_id = request.GET.get('ad_id')
    if ads_id:
        responses = responses.filter(responseAd_id=ads_id)

    return render(request, 'response_list.html', {'filter': response_filter, 'ads': ads, 'responses': responses})


@login_required
def response_accept(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    if request.user != response.responseAd.author:
        messages.error(request, 'Недостаточно прав.')
        return redirect('response_list')

    if response.status != 'PENDING':
        messages.error(request, 'Отклик рассмотрен.')
        return redirect('response_list')

    response.status = 'ACCEPTED'
    response.save()

    html_content = render_to_string(
        'accepted_email.html',
        {
            'link': f'{settings.SITE_URL}/ads/{response.responseAd_id}',
            'title': f'{response.responseAd.title}'
        }
    )

    msg = EmailMultiAlternatives(
        subject="Отклик принят",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[response.responseUser.email],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    return redirect('response_list')


def forbidden(request):
    return render(request, 'forbidden.html')


@login_required()
def subscription(request):
    not_subscriber = User.objects.filter(subscriber=False).filter(id=request.user.id).exists()
    return render(request, 'subscription.html', {'not_subscriber': not_subscriber})


@login_required()
def subscribe(request):
    user = request.user
    user.subscriber = True
    user.save()

    message = 'Вы успешно подписались на рассылку объявлений.'
    return render(request, 'subscribe.html', {'message': message})


@login_required()
def unsubscribe(request):
    user = request.user
    user.subscriber = False
    user.save()

    message = 'Вы успешно отписались от рассылки объявлений.'
    return render(request, 'subscribe.html', {'message': message})
