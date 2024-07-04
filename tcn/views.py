#from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Case, When, IntegerField
from .forms import CustomUserCreationForm
from .manager_forms import OfficeCreationForm, OfficeUpdateForm, AgentUpdateForm
from django.urls import reverse_lazy
#from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Office, CustomUser, Window
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


#class SignUpView(CreateView):
class SignUpView(FormView):
    #form_class = UserCreationForm
    form_class = CustomUserCreationForm
    #success_url = reverse_lazy("tcn:login")
    template_name = "tcn/registration/signup.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated and self.request.user.role == 'manager':
            return reverse_lazy('tcn:listAgents')
        else:
            return reverse_lazy('tcn:login')

#class CreateOfficeView
class CreateOfficeView(FormView):
    #form_class = UserCreationForm
    form_class = OfficeCreationForm
    success_url = reverse_lazy("tcn:home")
    template_name = "tcn/create_office.html"

    # add check authorization check 
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a manager
        if not (request.user.is_authenticated and request.user.role == 'manager'):
            raise PermissionDenied("Only managers can create offices.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # override the manager office
        # when signup manager acces with default office 
        # it must join the new office created 
        user = self.request.user
        if user.is_authenticated and user.role == 'manager':
            if user.office_id and user.office_id != 'guest':
                # Display error in the template
                form.add_error(None, "Manager is already associated with an office.")
                return self.form_invalid(form)
            office_instance = form.save()
            user.office_id = office_instance.ref
            user.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('tcn:listOffices')
    
class ListOffices(ListView):
    model = Office
    template_name = "tcn/list_offices.html"
    def get_queryset(self):
        # authenticated manager 
        manager_user = self.request.user
        # get the office linked to authenticated manager but not guest office 
        offices = Office.objects.filter(users__username=manager_user.username).exclude(ref='guest')
        return offices

class ListAgents(ListView):
    model = CustomUser
    template_name = "tcn/list_agents.html"
    context_object_name = "agent_list"
    def get_queryset(self):
        """Return the last five published questions."""
        manager_user = self.request.user
        
        # Assuming manager_user.role == 'manager', get their associated office_id
        manager_office_id = manager_user.office_id  # Adjust this according to your actual field name

        # Filter agents linked to the manager's office
        #agents = CustomUser.objects.filter(role='agent', office_id=manager_office_id)
        agents = CustomUser.objects.filter(role='agent', office_id=manager_office_id).annotate(
        agent_id=F('pk'),
        number_of_windows=F('office__number_of_windows'),
        num_window=Case(
            When(window__agent_id=F('pk'), then=F('window__number_window')),
            default=0,
            output_field=IntegerField(),
        )
        ).order_by('pk')
        
        return agents
    
def index(request):
    # data context for agent interaface
    agent_user = None
    agent_window = None
    agent_office = None
    # data context for client  interaface
    offices = {}
    # data context for manager  interaface
    windows_office = {}
    # common variables 
    customuser = request.user
    context = {}
    if hasattr(customuser, 'role') and customuser.role == 'manager':
        # we need office_id to track windows
        # fix when manager first sign up it belongs to office guest 
        # we must delete the exclude function on filter
        office_manager = Office.objects.filter(users=customuser).first()
        windows_office = Window.objects.filter(office_id=office_manager.ref)
    elif hasattr(customuser, 'role') and  customuser.role == 'agent':
        # we need agent_id and office_id for service counter 
        agent_office = Office.objects.filter(users=customuser).exclude(ref='guest').first()
        agent_window = Window.objects.filter(agent_id=customuser.id, office_id=agent_office.ref).first()
        agent_user = CustomUser.objects.filter(pk=customuser.id).first()
        pass
    elif hasattr(customuser, 'role') and  customuser.role == 'client':
        offices = Office.objects.all().exclude(ref='guest')
    context = {"agent_user": agent_user,
               "agent_office": agent_office,
               "agent_window": agent_window,
               "offices": offices,
               "windows_office": windows_office}
    return render(request, "tcn/home.html", context)

class ListTrackedOffices(ListView):
    model = Office
    template_name = "tcn/list_offices_tracked.html"
    context_object_name = "list_tracked_offices"

    def get_queryset(self):
        """Return the last five published questions."""
        client_user = self.request.user
        offices = Office.objects.filter(counter_notifications__client=client_user, counter_notifications__is_enabled=True).exclude(ref='guest')
        return offices

## update office module
class UpdateOfficeView(FormView):
    #form_class = UserCreationForm
    form_class = OfficeUpdateForm
    success_url = reverse_lazy("tcn:home")
    template_name = "tcn/update_office.html"

    # check authorization method 
    def dispatch(self, request, *args, **kwargs):
        # Check if the connected user is a manager and if their office matches the 'ref_office' parameter
        office_instance = self.get_office_to_update()
        
        if not (request.user.role == 'manager' and request.user.office_id == office_instance.ref):
            raise PermissionDenied("You are not authorized to update this office.")
        return super().dispatch(request, *args, **kwargs)

    def get_office_to_update(self):
        # access parameters 'ref_office' included in the URL
        ref_office = self.kwargs.get('ref_office')
        return get_object_or_404(Office, ref=ref_office)
    
    def get_initial(self):
        # get the initial object form
        initial = super().get_initial()
        # init the form from database based on ref_office
        office_instance = self.get_office_to_update()
        initial.update({
            'name': office_instance.name,
            'country': office_instance.country,
            'state': office_instance.state,
            'region': office_instance.region,
            'address': office_instance.address,
            'number_of_windows': office_instance.number_of_windows,
            'counter': office_instance.counter,
        })
        return initial

    def form_valid(self, form):
        office_to_update = self.get_office_to_update()
        office_to_update.name = form.cleaned_data['name']
        office_to_update.country = form.cleaned_data['country']
        office_to_update.state = form.cleaned_data['state']
        office_to_update.region = form.cleaned_data['region']
        office_to_update.address = form.cleaned_data['address']
        office_to_update.number_of_windows = form.cleaned_data['number_of_windows']
        office_to_update.counter = form.cleaned_data['counter']
        office_to_update.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tcn:listOffices')

    #update agent ( manager has the ability to do this action )
    # update office module
class UpdateAgentView(FormView):
    #form_class = UserCreationForm
    form_class = AgentUpdateForm
    template_name = "tcn/update_agent.html"

    # check authorization method 
    def dispatch(self, request, *args, **kwargs):
        # Check if the connected user is a manager and if their office matches the 'ref_office' parameter
        agent_instance = self.get_agent_to_update()
        
        if not (request.user.role == 'manager' and request.user.office_id == agent_instance.office_id):
            raise PermissionDenied("You are not authorized to update this Agent.")
        return super().dispatch(request, *args, **kwargs)

    def get_agent_to_update(self):
        # access parameters 'agent_id' included in the URL
        agent_id = self.kwargs.get('agent_id')
        return get_object_or_404(CustomUser, id=agent_id)
    
    def get_initial(self):
        # get the initial object form
        initial = super().get_initial()
        # init the form from database based on agent_id
        agent_instance = self.get_agent_to_update()
        initial.update({
            'username': agent_instance.username,
            'first_name': agent_instance.first_name,
            'last_name': agent_instance.last_name,
            'email': agent_instance.email,
            'national_id': agent_instance.national_id,
        })
        return initial

    def form_valid(self, form):
        agent_to_update = self.get_agent_to_update()
        agent_to_update.username = form.cleaned_data['username']
        agent_to_update.first_name = form.cleaned_data['first_name']
        agent_to_update.last_name = form.cleaned_data['last_name']
        agent_to_update.email = form.cleaned_data['email']
        agent_to_update.national_id = form.cleaned_data['national_id']
        agent_to_update.save()
        return super().form_valid(form) 
    
    def get_form_kwargs(self):
        # Override this method to pass the instance to the form
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_agent_to_update()
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('tcn:listAgents')