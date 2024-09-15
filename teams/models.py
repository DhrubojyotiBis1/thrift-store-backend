from django.db import models
from django.contrib.auth import get_user_model

from games.models import Games

class TeamManagers(models.Manager):
    '''Manager for Teams Model'''

    def create_team(self, name: str, created_by=None):
        if not created_by:
            raise ValueError('Team Creater Required')
        team = self.model(name=name, created_by=created_by)
        self.save(team=team)
        return team
    
    def save(self, team):
        team.save(using=self._db)


class Teams(models.Model):
    '''Database model for Teams in the system'''

    name = models.CharField(max_length=255, null=False, default='')
    members = models.ManyToManyField('gamers.Gamers', related_name='team_members')
    games = models.ManyToManyField(Games)
    created_by = models.ForeignKey('gamers.Gamers', on_delete=models.CASCADE, related_name='creater')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    objects = TeamManagers()

    def __str__(self) -> str:
        teamsVisuals = f"""Name: {self.name} \n TeamId: {self.id} \n Created_By: {self.created_by.pk} \n 
                        Members: {self.members} \n Created_Date: {self.created_at} \n"""
        
        return teamsVisuals