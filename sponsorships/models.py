from django.db import models
from games.models import Games
from teams.models import Teams
from sponsors.models import Sponsors

class SponsorshipManagers(models.Manager):
    '''Manager for Sponsorship Model'''

    def create_sponsorship(self, sponsor, team, game, amount, contract_link, start_at, end_at):
        if not sponsor:
            raise ValueError('Sponsor Required')
        if not team:
            raise ValueError('Team Required')
        if not game:
            raise ValueError('Game Required')
        if not amount:
            raise ValueError('Contract Amount Required')
        if not contract_link:
            raise ValueError('Contract Link Required')
        if not start_at:
            raise ValueError('Start Date Required')
        if not end_at:
            raise ValueError('End Date Required')

        sponsorship = self.model(
            sponsor=sponsor, 
            team=team, 
            game=game, 
            amount=amount, 
            contract_link=contract_link, 
            start_at=start_at, 
            end_at=end_at
        )
        self.save(sponsorship)
        return sponsorship
    
    def save(self, sponsorship):
        sponsorship.save(using=self._db)


class Sponsorships(models.Model):
    '''Database model for Sponsorship in the system'''

    sponsor = models.ForeignKey(Sponsors, on_delete=models.CASCADE, null=False)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=False)
    game = models.ForeignKey(Games, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    contract_link = models.CharField(max_length=255, null=False) 
    start_at = models.DateTimeField(null=False)
    modified_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField(null=False)

    objects = SponsorshipManagers()

    def __str__(self) -> str:
        return f"Sponsorship by {self.sponsor} for {self.team} on {self.game}"