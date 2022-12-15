from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser
from datetime import datetime
import uuid

# Create your models here.


class Resident(AbstractBaseUser):
    address = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    isManager = models.BooleanField(default=False, null=True)
    resident_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    USERNAME_FIELD = 'address'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['address']
    
    def __str__(self) -> str:
        return self.address


class newUser(AbstractUser):
    name = models.CharField(unique=True, max_length=100, null=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_manager = models.BooleanField(default=False, null=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['name']


class Messege(models.Model):
    messege_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    messege_content = models.TextField(max_length=300, null=True, blank=False)
    creater = models.ForeignKey(newUser, on_delete=models.SET_NULL, null=True, related_name="messeges")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class InfoMessege(models.Model):
    info_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    info_messege_content = models.TextField(null=True, blank=False)
    creater = models.ForeignKey(newUser, on_delete=models.SET_NULL, null=True, related_name="inforation_messeges")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Poll(models.Model):
    poll_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    detail = models.TextField(max_length=400, null=True, blank=True)
    creater = models.ForeignKey(newUser, on_delete=models.SET_NULL, null=True, related_name="polls")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    isActive = models.BooleanField(default=True)

    def voter_list(self):
        votes = self.vote_set.all()
        votes = votes.filter(poll=self)
        voters = []
        for vote in votes:
            voters.append(vote.voter)
        return voters


    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qualification = user_votes.filter(poll=self)

        if qualification.exists():
            return False
        return True

    class Meta:
        ordering = ['start_date']

    @property
    def event_status(self):
        status = None

        present = datetime.now().date()
        deadline = self.end_date
        startline = self.start_date

        boolPaststartline = (startline > present)
        boolPastDeadline = (present > deadline)

        if (boolPastDeadline):
            status = 'Finished'
        elif (boolPaststartline):
            status = 'Not yet'
        else:
            status = 'Ongoing'

        return status
    
    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self) -> str:
        return self.title

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=25)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self) -> str:
        return f"{self.poll.title[:25]} - {self.choice[:25]}"

class Vote(models.Model):
    vote_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    voter = models.ForeignKey(newUser, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True)
