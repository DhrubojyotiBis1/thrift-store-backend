from django.db import models

class GameManagers(models.Manager):
    '''Manager for Teams Model'''

    def create_game(self, name: str):
        game = self.model(name=name)
        self.save(game=game)
        return game
    
    def save(self, game):
        game.save(using=self._db)

class Genres(models.Model):
    '''Database model for Genre in the system'''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Games(models.Model):
    '''Database model for Game in the system'''

    name = models.CharField(max_length=255, null=False, default='')
    genre = models.ManyToManyField(Genres)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = GameManagers()

    def __str__(self) -> str:
        genre_names = ', '.join([genre.name for genre in self.genre.all()]) 
        return f"Name: {self.name} \n GameId: {self.id} \n Genres: {genre_names}"
        
        