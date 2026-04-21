from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Alumni,Deplome,Reseau,Histoire,Retour,News ,Event ,Prof,Equipe ,Prerequi ,Formati ,Objec
from django.views.generic.edit import CreateView , UpdateView ,DeleteView , FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Mixin for common functionality
class PaginatedListMixin(ListView):
    """Mixin to add pagination to list views"""
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatis'] = Formati.objects.filter(publish=True)[:10]
        return context



class HOMEView(TemplateView):
    template_name = 'Acceuil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.objects.filter(publish=True)[:10]
        context['formatis'] = Formati.objects.filter(publish=True)
        context['contact_form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Vérification du champ honeypot
            honeypot = form.cleaned_data.get('honeypot')
            if honeypot:  # Si le champ honeypot est rempli, c'est un bot
                return HttpResponse("Erreur: spam détecté.")

            # Envoi de l'email
            try:
                send_mail(
                    subject=f'Contact de {name}',
                    message=f'Nom: {name}\\nEmail: {email}\\nMessage: {message}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['khadijaelmrabt2025@gmail.com'],
                    fail_silently=False,
                )
                return self.render_to_response({
                    'message_sent': True,
                    'contact_form': ContactForm(),  # Réinitialiser le formulaire après envoi
                    'news_list': News.objects.all(),
                    'formatis': Formati.objects.all(),
                })
            except Exception as e:
                return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")
        else:
            # Si le formulaire n'est pas valide, renvoyer les erreurs
            return self.render_to_response({
                'contact_form': form,
                'form_errors': form.errors,
                'news_list': News.objects.all(),
                'formatis': Formati.objects.all(),
            })


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    Model = News
    context_object_name = 'news'

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields =  '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user =True
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()
        if user  :
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self, *args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage,self).get(*args,**kwargs)


class NewsList(PaginatedListMixin):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        try:
            queryset = News.objects.filter(publish=True).select_related('user').order_by('-date')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(title__icontains=search_input) | Q(content__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in NewsList.get_queryset: {e}")
            return News.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
   
class NewssList(PaginatedListMixin):
    model = News
    template_name = 'NewsList.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        try:
            queryset = News.objects.filter(publish=True).select_related('user').order_by('-date')
            theme_filter = self.request.GET.get('theme', '').strip()
            if theme_filter:
                queryset = queryset.filter(theme__icontains=theme_filter)
            return queryset
        except Exception as e:
            logger.error(f"Error in NewssList.get_queryset: {e}")
            return News.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = sorted(set([theme.strip().lower() for theme in News.objects.filter(publish=True).values_list('theme', flat=True).distinct() if theme]))
        context['selected_theme'] = self.request.GET.get('theme', '')
        return context
    
class NewsDetail(DetailView):
    model = News    
    template_name = 'news.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.objects.filter(publish=True).select_related('user')
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['formatis'] = Formati.objects.filter(publish=True)[:5]
            return context
        except Exception as e:
            logger.error(f"Error in NewsDetail.get_context_data: {e}")
            return super().get_context_data(**kwargs)
    
class NewsCreate(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title','image','theme','lieu','date','content','publish']
    template_name = 'news_form.html'  
    success_url = reverse_lazy('news_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in NewsCreate.form_valid: {e}")
            form.add_error(None, f"Error creating news: {str(e)}")
            return self.form_invalid(form)

class NewsUpdate(LoginRequiredMixin, UpdateView):
    model = News
    fields = ['title','image','theme','lieu','date','content','publish']
    template_name = 'news_form.html' 
    success_url = reverse_lazy('news_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in NewsUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating news: {str(e)}")
            return self.form_invalid(form)

class Newsdelete(LoginRequiredMixin, DeleteView):
    model = News
    context_object_name = 'news'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('news_list')
    login_url = 'login'

class EventList(PaginatedListMixin):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        try:
            queryset = Event.objects.filter(publish=True).select_related('user').order_by('-event_start_date')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(title__icontains=search_input) | Q(content__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in EventList.get_queryset: {e}")
            return Event.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
   

            
    
class EventDetail(DetailView):
    model = Event    
    template_name = 'event.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(publish=True).select_related('user')
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['formatis'] = Formati.objects.filter(publish=True)[:5]
            return context
        except Exception as e:
            logger.error(f"Error in EventDetail.get_context_data: {e}")
            return super().get_context_data(**kwargs)

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title','image','theme','content','lieu','event_start_date','event_finish_date','publish']
    template_name = 'event_form.html'  
    success_url = reverse_lazy('event_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in EventCreate.form_valid: {e}")
            form.add_error(None, f"Error creating event: {str(e)}")
            return self.form_invalid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title','image','theme','content','lieu','event_start_date','event_finish_date','publish']
    template_name = 'event_form.html' 
    success_url = reverse_lazy('event_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in EventUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating event: {str(e)}")
            return self.form_invalid(form)

class Eventdelete(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = 'event'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('event_list')
    login_url = 'login'

class EquipeList(PaginatedListMixin):
    model = Equipe
    template_name = 'equipe_list.html'
    context_object_name = 'equipe'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Equipe.objects.filter(publish=True).select_related('user').order_by('name')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(position__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in EquipeList.get_queryset: {e}")
            return Equipe.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    


class EquipeDetail(DetailView):
    model = Equipe   
    template_name = 'equipe.html'
    context_object_name = 'equipe'
    
    def get_queryset(self):
        return Equipe.objects.filter(publish=True).select_related('user')

class EquipeCreate(LoginRequiredMixin, CreateView):
    model = Equipe
    fields = ['name','position','content','image','publish']
    template_name = 'equipe_form.html'  
    success_url = reverse_lazy('equipe_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in EquipeCreate.form_valid: {e}")
            form.add_error(None, f"Error creating team member: {str(e)}")
            return self.form_invalid(form)

class EquipeUpdate(LoginRequiredMixin, UpdateView):
    model = Equipe
    fields = ['name','position','content','image','publish']
    template_name = 'equipe_form.html' 
    success_url = reverse_lazy('equipe_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in EquipeUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating team member: {str(e)}")
            return self.form_invalid(form)

class Equipedelete(LoginRequiredMixin, DeleteView):
    model = Equipe
    context_object_name = 'equipe'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('equipe_list')
    login_url = 'login'

class FormationList(PaginatedListMixin):
    model = Formati
    template_name = 'formation_list.html'
    context_object_name = 'formatis'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Formati.objects.filter(publish=True).prefetch_related('prof', 'prerequi', 'obj').order_by('name')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(description__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in FormationList.get_queryset: {e}")
            return Formati.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context



class FormationDetail(DetailView):
    model = Formati
    template_name = 'formation.html'
    context_object_name = 'formati'
    
    def get_queryset(self):
        return Formati.objects.filter(publish=True).prefetch_related('prof', 'prerequi', 'obj')
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['profs'] = self.object.prof.all()
            context['prerequisites'] = self.object.prerequi.all()
            context['objec'] = self.object.obj.all()
            return context
        except Exception as e:
            logger.error(f"Error in FormationDetail.get_context_data: {e}")
            return super().get_context_data(**kwargs)


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formati
        fields = ['name','description','presentation','formation_type','im','ima','imag','obj','prof','prerequi','conditions_access','programme']
        widgets = {
            'obj': forms.CheckboxSelectMultiple(),  # Affiche des cases à cocher
            'prof': forms.CheckboxSelectMultiple(),
            'prerequi': forms.CheckboxSelectMultiple(),
        }

class FormationCreate(LoginRequiredMixin, CreateView):
    model = Formati
    form_class = FormationForm
    template_name = 'formation_form.html'
    success_url = reverse_lazy('formation_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in FormationCreate.form_valid: {e}")
            form.add_error(None, f"Error creating formation: {str(e)}")
            return self.form_invalid(form)
    
class FormationUpdate(LoginRequiredMixin, UpdateView):
    model = Formati
    form_class = FormationForm
    template_name = 'formation_form.html'
    success_url = reverse_lazy('formation_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in FormationUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating formation: {str(e)}")
            return self.form_invalid(form)

class Formationdelete(LoginRequiredMixin, DeleteView):
    model = Formati
    context_object_name = 'formati'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('formation_list')
    login_url = 'login'

class ProfList(PaginatedListMixin):
    model = Prof
    template_name = 'prof_list.html'
    context_object_name = 'profs'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Prof.objects.filter(publish=True).select_related('user') if hasattr(Prof, 'publish') else Prof.objects.all().select_related('user')
            queryset = queryset.order_by('name')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(position__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in ProfList.get_queryset: {e}")
            return Prof.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
   
class ProfsList(PaginatedListMixin):
    model = Prof
    template_name = 'ProfsList.html'
    context_object_name = 'profs'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Prof.objects.all().select_related('user').order_by('name')
            return queryset
        except Exception as e:
            logger.error(f"Error in ProfsList.get_queryset: {e}")
            return Prof.objects.none()

class ProfDetail(DetailView):
    model = Prof
    template_name = 'prof.html'
    context_object_name = 'prof'
    
    def get_queryset(self):
        return Prof.objects.all().select_related('user')

class ProfCreate(LoginRequiredMixin, CreateView):
    model = Prof
    fields = ['name','position','image']
    template_name = 'prof_form.html'  
    success_url = reverse_lazy('prof_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ProfCreate.form_valid: {e}")
            form.add_error(None, f"Error creating professor: {str(e)}")
            return self.form_invalid(form)

class ProfUpdate(LoginRequiredMixin, UpdateView):
    model = Prof
    fields = ['name','position','image']
    template_name = 'prof_form.html' 
    success_url = reverse_lazy('prof_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ProfUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating professor: {str(e)}")
            return self.form_invalid(form)

class Profdelete(LoginRequiredMixin, DeleteView):
    model = Prof
    context_object_name = 'prof'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('prof_list')
    login_url = 'login'

class ObjectifList(PaginatedListMixin):
    model = Objec
    template_name = 'objectif_list.html'
    context_object_name = 'objecs'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Objec.objects.all().select_related('user').order_by('title')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in ObjectifList.get_queryset: {e}")
            return Objec.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    
class ObjectifsList(PaginatedListMixin):
    model = Objec
    template_name = 'ObjectifList.html'
    context_object_name = 'objecs'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            return Objec.objects.all().select_related('user').order_by('title')
        except Exception as e:
            logger.error(f"Error in ObjectifsList.get_queryset: {e}")
            return Objec.objects.none()

class ObjectifDetail(DetailView):
    model = Objec
    template_name = 'objectif.html'
    context_object_name = 'objec'
    
    def get_queryset(self):
        return Objec.objects.all().select_related('user')

class ObjectifCreate(LoginRequiredMixin, CreateView):
    model = Objec
    fields = ['title','description']
    template_name = 'objectif_form.html'  
    success_url = reverse_lazy('objectif_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ObjectifCreate.form_valid: {e}")
            form.add_error(None, f"Error creating objective: {str(e)}")
            return self.form_invalid(form)
    
class ObjectifUpdate(LoginRequiredMixin, UpdateView):
    model = Objec
    fields = ['title','description']
    template_name = 'objectif_form.html' 
    success_url = reverse_lazy('objectif_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ObjectifUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating objective: {str(e)}")
            return self.form_invalid(form)

class Objectifdelete(LoginRequiredMixin, DeleteView):
    model = Objec
    context_object_name = 'objec'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('objectif_list')
    login_url = 'login'

class PrerequisiteList(PaginatedListMixin):
    model = Prerequi
    template_name = 'prerequisite_list.html'
    context_object_name = 'prerequisites'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Prerequi.objects.all().select_related('user').order_by('description')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(description__icontains=search_input)
            return queryset
        except Exception as e:
            logger.error(f"Error in PrerequisiteList.get_queryset: {e}")
            return Prerequi.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

class PrerequisiteDetail(DetailView):
    model = Prerequi
    template_name = 'prerequisite.html'
    context_object_name = 'prerequisite'
    
    def get_queryset(self):
        return Prerequi.objects.all().select_related('user')

class PrerequisiteCreate(LoginRequiredMixin, CreateView):
    model = Prerequi
    fields = ['description']
    template_name = 'prerequisite_form.html'  
    success_url = reverse_lazy('prerequisite_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in PrerequisiteCreate.form_valid: {e}")
            form.add_error(None, f"Error creating prerequisite: {str(e)}")
            return self.form_invalid(form)

class PrerequisiteUpdate(LoginRequiredMixin, UpdateView):
    model = Prerequi
    fields = ['description']
    template_name = 'prerequisite_form.html' 
    success_url = reverse_lazy('prerequisite_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in PrerequisiteUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating prerequisite: {str(e)}")
            return self.form_invalid(form)

class Prerequisitedelete(LoginRequiredMixin, DeleteView):
    model = Prerequi
    context_object_name = 'prerequisite'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('prerequisite_list')
    login_url = 'login'    

class RetourList(PaginatedListMixin):
    model = Retour
    template_name = 'retour_list.html'
    context_object_name = 'retours'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Retour.objects.all().select_related('user').order_by('-id')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(comment__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in RetourList.get_queryset: {e}")
            return Retour.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

class RetourDetail(DetailView):
    model = Retour
    template_name = 'retour.html'
    context_object_name = 'retour'
    
    def get_queryset(self):
        return Retour.objects.all().select_related('user')

class RetourCreate(LoginRequiredMixin, CreateView):
    model = Retour
    fields = ['name','comment']
    template_name = 'retour_form.html'  
    success_url = reverse_lazy('retour_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in RetourCreate.form_valid: {e}")
            form.add_error(None, f"Error creating feedback: {str(e)}")
            return self.form_invalid(form)

class RetourUpdate(LoginRequiredMixin, UpdateView):
    model = Retour
    fields = ['name','comment']
    template_name = 'retour_form.html' 
    success_url = reverse_lazy('retour_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in RetourUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating feedback: {str(e)}")
            return self.form_invalid(form)

class Retourdelete(LoginRequiredMixin, DeleteView):
    model = Retour
    context_object_name = 'retour'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('retour_list')
    login_url = 'login'   

class HistoireList(PaginatedListMixin):
    model = Histoire
    template_name = 'histoire_list.html'
    context_object_name = 'histoires'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Histoire.objects.all().select_related('user').order_by('-id')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(title__icontains=search_input) | Q(content__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in HistoireList.get_queryset: {e}")
            return Histoire.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    
class HistoireDetail(DetailView):
    model = Histoire
    template_name = 'histoire.html'
    context_object_name = 'histoire'
    
    def get_queryset(self):
        return Histoire.objects.all().select_related('user')

class HistoireCreate(LoginRequiredMixin, CreateView):
    model = Histoire
    fields = ['title','content']
    template_name = 'histoire_form.html'  
    success_url = reverse_lazy('histoire_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in HistoireCreate.form_valid: {e}")
            form.add_error(None, f"Error creating story: {str(e)}")
            return self.form_invalid(form)
    
class HistoireUpdate(LoginRequiredMixin, UpdateView):
    model = Histoire
    fields = ['title','content']
    template_name = 'histoire_form.html' 
    success_url = reverse_lazy('histoire_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in HistoireUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating story: {str(e)}")
            return self.form_invalid(form)

class Histoiredelete(LoginRequiredMixin, DeleteView):
    model = Histoire
    context_object_name = 'histoire'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('histoire_list')
    login_url = 'login'

class ReseauList(PaginatedListMixin):
    model = Reseau
    template_name = 'reseau_list.html'
    context_object_name = 'reseaus'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Reseau.objects.all().select_related('user').order_by('name')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(poste__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in ReseauList.get_queryset: {e}")
            return Reseau.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context

class ReseauDetail(DetailView):
    model = Reseau
    template_name = 'reseau.html'
    context_object_name = 'reseau'
    
    def get_queryset(self):
        return Reseau.objects.all().select_related('user')

class ReseauCreate(LoginRequiredMixin, CreateView):
    model = Reseau
    fields = ['name','poste']
    template_name = 'reseau_form.html'  
    success_url = reverse_lazy('reseau_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ReseauCreate.form_valid: {e}")
            form.add_error(None, f"Error creating network member: {str(e)}")
            return self.form_invalid(form)

class ReseauUpdate(LoginRequiredMixin, UpdateView):
    model = Reseau
    fields = ['name','poste']
    template_name = 'reseau_form.html' 
    success_url = reverse_lazy('reseau_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in ReseauUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating network member: {str(e)}")
            return self.form_invalid(form)

class Reseaudelete(LoginRequiredMixin, DeleteView):
    model = Reseau
    context_object_name = 'reseau'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('reseau_list')
    login_url = 'login'

class DeplomeList(PaginatedListMixin):
    model = Deplome
    template_name = 'deplome_list.html'
    context_object_name = 'deplomes'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            queryset = Deplome.objects.all().select_related('user').order_by('-promo', 'name')
            search_input = self.request.GET.get('search_area', '').strip()
            if search_input:
                queryset = queryset.filter(Q(name__icontains=search_input) | Q(poste__icontains=search_input))
            return queryset
        except Exception as e:
            logger.error(f"Error in DeplomeList.get_queryset: {e}")
            return Deplome.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_input'] = self.request.GET.get('search_area', '')
        return context
    
class DeplomeDetail(DetailView):
    model = Deplome
    template_name = 'deplome.html'
    context_object_name = 'deplome'
    
    def get_queryset(self):
        return Deplome.objects.all().select_related('user')

class DeplomeCreate(LoginRequiredMixin, CreateView):
    model = Deplome
    fields = ['name','poste','promo','image']
    template_name = 'deplome_form.html'  
    success_url = reverse_lazy('deplome_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in DeplomeCreate.form_valid: {e}")
            form.add_error(None, f"Error creating graduate: {str(e)}")
            return self.form_invalid(form)
    
class DeplomeUpdate(LoginRequiredMixin, UpdateView):
    model = Deplome
    fields = ['name','poste','promo','image']
    template_name = 'deplome_form.html' 
    success_url = reverse_lazy('deplome_list')
    login_url = 'login'
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in DeplomeUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating graduate: {str(e)}")
            return self.form_invalid(form)

class Deplomedelete(LoginRequiredMixin, DeleteView):
    model = Deplome
    context_object_name = 'deplome'
    template_name = 'confirm_delete.html' 
    success_url = reverse_lazy('deplome_list')
    login_url = 'login'

class AlumniDetail(TemplateView):
    template_name = 'alumni.html'
    context_object_name = 'alumni'
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            alumni = get_object_or_404(Alumni)
            context['alumni'] = alumni
            context['retours'] = alumni.retour.all()[:10]
            context['histoires'] = alumni.histoire.all()[:10]
            context['reseaus'] = alumni.reseau.all()[:10]
            context['deplomes'] = alumni.deplome.all()[:10]
            return context
        except Exception as e:
            logger.error(f"Error in AlumniDetail.get_context_data: {e}")
            return super().get_context_data(**kwargs)

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['NbL', 'echange', 'insertion', 'retour', 'histoire', 'reseau', 'deplome']
        widgets = {
            'retour': forms.CheckboxSelectMultiple(),
            'histoire': forms.CheckboxSelectMultiple(),
            'reseau': forms.CheckboxSelectMultiple(),
            'deplome': forms.CheckboxSelectMultiple(),
        }

class AlumniUpdate(LoginRequiredMixin, UpdateView):
    model = Alumni
    form_class = AlumniForm
    template_name = 'alumni_form.html'
    success_url = reverse_lazy('alumni_detail')
    login_url = 'login'

    def get_object(self, queryset=None):
        try:
            alumni, created = Alumni.objects.get_or_create(id=1)
            return alumni
        except Exception as e:
            logger.error(f"Error in AlumniUpdate.get_object: {e}")
            return None
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error in AlumniUpdate.form_valid: {e}")
            form.add_error(None, f"Error updating alumni: {str(e)}")
            return self.form_invalid(form)

class Alumnidelete(LoginRequiredMixin, DeleteView):
    model = Alumni
    context_object_name = 'alumni'
    template_name = 'alumni_delete.html' 
    success_url = reverse_lazy('alumni_list')
    login_url = 'login'       

def faculte(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'faculte.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in faculte view: {e}")
        return render(request, 'faculte.html', {})

def mot_president(request):
    try:
        return render(request, 'mot_president.html')
    except Exception as e:
        logger.error(f"Error in mot_president view: {e}")
        return render(request, '404.html', {}, status=404)
  
def avis(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'avis.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in avis view: {e}")
        return render(request, 'avis.html', {})

def bda(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'bda.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in bda view: {e}")
        return render(request, 'bda.html', {})
  
def bde(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'bde.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in bde view: {e}")
        return render(request, 'bde.html', {})

def club(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'clubs.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in club view: {e}")
        return render(request, 'clubs.html', {})
 
def ecole(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'ecole.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in ecole view: {e}")
        return render(request, 'ecole.html', {})
        
def eservice(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'eservice.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in eservice view: {e}")
        return render(request, 'eservice.html', {})
        
def partein(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'partenaire_in.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in partein view: {e}")
        return render(request, 'partenaire_in.html', {})
        
def partelocaux(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'partenaire_lo.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in partelocaux view: {e}")
        return render(request, 'partenaire_lo.html', {})
        
def recrutement(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'recrutement.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in recrutement view: {e}")
        return render(request, 'recrutement.html', {})
        
def reglements(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'reglement.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in reglements view: {e}")
        return render(request, 'reglement.html', {})
        
def stage(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'stage.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in stage view: {e}")
        return render(request, 'stage.html', {})
        
def viesportive(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'viesportive.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in viesportive view: {e}")
        return render(request, 'viesportive.html', {})
        
def equipement(request):
    try:
        formatis = Formati.objects.filter(publish=True)[:10]
        return render(request, 'equipements.html', {'formatis': formatis})
    except Exception as e:
        logger.error(f"Error in equipement view: {e}")
        return render(request, 'equipements.html', {})


  
 

