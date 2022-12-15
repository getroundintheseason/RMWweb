from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import django.views.generic.base 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Messege, Resident, InfoMessege, Poll, Choice, Vote, newUser
from .forms import CreateNewUserForm, PollForm, ChoiceFormA, ChoiceFormD, PollForm, VoteForm
from datetime import datetime

# Create your views here.
class main(LoginView):
    template_name = 'managementAPP/main.html'
    fields = '__all__'
    reverse_lazy('main')

class ResidentLoginView(LoginView):
    template_name: str = 'managementAPP/login.html'
    field = '__all__'
    model = newUser
    redirect_authenticated_user: bool = True

    def get_success_url(self) -> str:
        return reverse_lazy('infomesseges')

class RegisterView(FormView):
    template_name: str = 'managementAPP/register.html'
    model = newUser
    form_class = CreateNewUserForm
    field = '__all__'
    redirect_authenticated_user = True
    success_url = reverse_lazy("main")
    
    def form_valid(self, form):
        user = form.save()
        user.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterView, self).get(*args, **kwargs)

#Messege
class MessegeList(LoginRequiredMixin, ListView):
    model = Messege
    context_object_name = 'messeges'

    def get_context_data(self, **kwargs):
        messege = super().get_context_data(**kwargs)
        messege['count'] = messege['messeges'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            messege['messeges'] = messege['messeges'].filter(messege_content__icontains=search_input)
        
        messege['search_input'] = search_input
        return messege

class MessegeDetail(LoginRequiredMixin, DetailView):
    model = Messege
    context_object_name: str = 'messege'
    template_name: str = 'managementAPP/messeges.html'

class MessegeCreate(LoginRequiredMixin, CreateView):
    model = Messege
    fields = ['messege_content']
    success_url = reverse_lazy('messeges')
    
    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super(MessegeCreate, self).form_valid(form)

class MessegeUpdate(LoginRequiredMixin, UpdateView):
    model = Messege
    fields = ['messege_content']
    success_url = reverse_lazy('messeges')

    def form_valid(self, form):
        success_url = self.get_success_url()
        if(self.request.user == self.object.creater):
            self.object = form.save()
            return super().form_valid(form)
        return HttpResponseRedirect(success_url)

class MessegeDelete(LoginRequiredMixin, DeleteView):
    model = Messege
    fields = '__all__'
    success_url = reverse_lazy('messeges')

    def form_valid(self, form):
        success_url = self.get_success_url()
        if(self.request.user == self.object.creater):
            self.object.delete()
        return HttpResponseRedirect(success_url)

#InfoMessege
class InfoMessegeList(LoginRequiredMixin, ListView):
    model = InfoMessege
    context_object_name = 'infomesseges'

    def get_context_data(self, **kwargs):
        infomessege = super().get_context_data(**kwargs)
        infomessege['count'] = infomessege['infomesseges'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            infomessege['infomesseges'] = infomessege['infomesseges'].filter(info_messege_content__icontains=search_input)
        
        infomessege['search_input'] = search_input
        return infomessege

class InfoMessegeDetail(LoginRequiredMixin, DetailView):
    model = InfoMessege
    context_object_name: str = 'infomessege'
    template_name: str = 'managementAPP/infomesseges.html'

class InfoMessegeCreate(LoginRequiredMixin, CreateView):
    model = InfoMessege
    fields = ['info_messege_content']
    success_url = reverse_lazy('infomesseges')
    
    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super(InfoMessegeCreate, self).form_valid(form)

class InfonMessegeUpdate(LoginRequiredMixin, UpdateView):
    model = InfoMessege
    fields = ['info_messege_content']
    success_url = reverse_lazy('infomesseges')

    def form_valid(self, form):
        success_url = self.get_success_url()
        if(self.request.user.is_manager):
            self.object = form.save()
            return super().form_valid(form)
        return HttpResponseRedirect(success_url)

class InfoMessegeDelete(LoginRequiredMixin, DeleteView):
    model = InfoMessege
    fields = '__all__'
    success_url = reverse_lazy('infomesseges')

    def form_valid(self, form):
        success_url = self.get_success_url()
        if(self.request.user.is_manager):
            self.object.delete()
        return HttpResponseRedirect(success_url)


#Poll
class PollList(LoginRequiredMixin, ListView):
    model = Poll
    context_object_name = 'polls'

    def get_context_data(self, **kwargs):
        poll = super().get_context_data(**kwargs)
        poll['count'] = poll['polls'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            poll['polls'] = poll['polls'].filter(title__icontains=search_input)
        
        poll['search_input'] = search_input
        return poll

class PollDetail(LoginRequiredMixin, DetailView):
    model = Poll
    context_object_name: str = 'poll'
    template_name: str = 'managementAPP/polls.html'

class PollCreate(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    success_url = reverse_lazy('polls')
    
    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super(PollCreate, self).form_valid(form)

@login_required()
def CreatePoll(request):
    if request.method == 'POST':
        poll_form = PollForm(data=request.POST)
        poll_form.instance.creater = request.user

        choice_formA = ChoiceFormA(data=request.POST)
        choice_formD = ChoiceFormD(data=request.POST)

        poll_form['start_date']
        if poll_form.is_valid() and choice_formA.is_valid() and choice_formD.is_valid():

            datetime.strptime(poll_form['start_date'].value(), "%Y-%M-%d")
            #start_date = datetime.strptime(poll_form['start_date'].value(), "%Y-%M-%d").date()
            #end_date = datetime.strptime(poll_form['end_date'].value(), "%Y-%M-%d").date()
            start_date = poll_form.cleaned_data.get('start_date')
            end_date = poll_form.cleaned_data.get('end_date')
            
            now = datetime.now().date()
            print("start_date : {}\n end_date : {}\n now : {}".format(start_date, end_date, now))
            if start_date > end_date:       
                error_messege = "start_date is older than end_date"
                return render(request,'managementAPP/poll_form.html', {'poll_form': poll_form, 'choice_formA': choice_formA, 'choice_formD': choice_formD, 'error_messege': error_messege})

            if now > end_date:
                error_messege = "now is older than ending date"
                return render(request,'managementAPP/poll_form.html', {'poll_form': poll_form, 'choice_formA': choice_formA, 'choice_formD': choice_formD, 'error_messege': error_messege})

            poll = poll_form.save()
            choiceA = choice_formA.save(commit=False)
            choiceD = choice_formD.save(commit=False)

            # Set Choice
            choiceA.poll = poll
            choiceA.choice = 'Agree'
            choiceA.save()
            choice_formA.save_m2m()

            choiceD.poll = poll
            choiceD.choice = 'Disagree'
            choiceD.save()
            choice_formD.save_m2m()

            return redirect('polls')
        else:
        # Handle errors
            error_messege = "Form error occur, please try again later!!"
            return render(request,'managementAPP/poll_form.html', {'poll_form': poll_form, 'choice_formA': choice_formA, 'choice_formD': choice_formD, 'error_messege': error_messege})
    else:  
        # GET
        poll_form = PollForm()
        choice_formA = ChoiceFormA()
        choice_formD = ChoiceFormD()

    return render(request,'managementAPP/poll_form.html', {'poll_form': poll_form, 'choice_formA': choice_formA, 'choice_formD': choice_formD})


#Choice
class ChoiceList(LoginRequiredMixin, ListView):
    pass

class ChoiceDetail(LoginRequiredMixin, DetailView):
    pass

class ChoiceCreate(LoginRequiredMixin, CreateView):
    pass


#Vote
class VoteList(LoginRequiredMixin, ListView):
    pass

class VoteDetail(LoginRequiredMixin, DetailView):
    pass

class VoteCreate(LoginRequiredMixin, CreateView):
    pass

@login_required()
def CreateVote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    choice_mk = poll.choice_set.all()

    choice_id = request.POST.get('choice')

    if not poll.user_can_vote(request.user):
        print("You already voted this poll!")
        return redirect("polls")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(voter=request.user, poll=poll, choice=choice)
        vote.save()
        return redirect('poll', pk = pk)
    else:
        print("No choice selected!")
        return render(request, 'managementAPP/vote_form.html', {'poll': poll})

    return render(request, 'polls/poll_result.html', {'poll': poll})
