from django.shortcuts import render, redirect, reverse
from filme.models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHome

# Create your views here.
# def homepage(request):
#     return render(request, 'homepage.html')

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHome

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

# def homefilmes(request):
#     context = {}
#     context['lista_filmes'] = Filme.objects.all()
#     return render(request, 'homefilmes.html', context)

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme

    def get(self, request, *args, **kwargs):
        #descobrir qual o filme acessado
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        context['filmes_relacionados'] = Filme.objects.filter(categoria = self.get_object().categoria)
        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            objedt_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return objedt_list
        else:
            return None


class PaginaPerfil(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['first_name', 'last_name', 'email']
    template_name = 'editarperfil.html'

    def get_success_url(self):
        return reverse('filme:homefilmes')


class Criarconta(FormView):
    form_class = CriarContaForm
    template_name = 'criarconta.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')
