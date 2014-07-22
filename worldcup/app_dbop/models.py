from django.db import models

class Guess(models.Model):
    user   = models.CharField(max_length=128)
    mvp    = models.IntegerField(default=0)
    match  = models.CharField(max_length=128)
    result = models.IntegerField(default=0)
    score  = models.IntegerField(default=0)
    total  = models.IntegerField(default=0)
    primarykey= models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return '%s %s %s' % (self.user, self.match, self.result)

class Score(models.Model):
    user   = models.CharField(max_length=128,primary_key=True)
    score  = models.IntegerField(default=0)
    def __str__(self):
        return '%s %s' % (self.user, self.score)

class Auth(models.Model):
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=16)




class vote_display(models.Model):
    user = models.CharField(max_length=128,primary_key=True)
    vote = models.CharField(max_length=128)

    def __str__(self):
        return '%s %s' % (self.user, self.vote)


class vote_rank(models.Model):
    player   = models.CharField(max_length=128)
    score    = models.IntegerField(default=0)
    name     = models.CharField(max_length=64)
    url      = models.CharField(max_length=256)
    del_flag = models.IntegerField(default=0)
    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.player, self.score, self.name, self.url, self.del_flag)

class vote_admin(models.Model):
    anynomous = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % (self.anynomous)



