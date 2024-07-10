from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ad, Response
from .forms import AdForm, ResponseForm


# Create your views here.
class OwnerPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().author == self.request.user:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class AdsList(ListView):
    model = Ad
    ordering = 'dateCreation'
    template_name = 'ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad_detail'
    queryset = Ad.objects.all()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
    success_url = reverse_lazy('ad_detail')

    def form_valid(self, form):
        response = form.save(commit=False)
        response.responseUser = self.request.user
        response.responseAd_id = self.kwargs.get('pk')
        response.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_detail.id'] = Ad.objects.get(pk=self.kwargs['pk'])
        return context


