from django.db import models

#options
STATUS_CHOICES = (
    ('A','Admin'),
    ('M', 'Member'),
    ('O', 'Observer'),
)

GENDER_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('N', 'Not stated'),
)


# User data that group uses for contacts and assigning to tasks
class Userprofile(models.Model):
    real_name  = models.CharField(max_length=30)
    skype_id   = models.CharField(max_length=30)
    ning_id    = models.CharField(max_length=30)
    twitter_id = models.CharField(max_length=30)
    email      = models.EmailField()
    status     = models.CharField(max_length=30)
    location   = models.CharField(max_length=30)
    country    = models.CharField(max_length=30)
    timezone   = models.CharField(max_length=30)
    membersince = models.DateField('member since')
    languagelist = models.TextField()

# Ning inputs
class Ninguserprofile(models.Model):
    contributorid = models.CharField(max_length=30)
    ningaddress = models.URLField()
    statedname = models.CharField(max_length=30)
    email = models.CharField(max_length=300)
    stated_gender = models.CharField(max_length=30)
    stated_location = models.CharField(max_length=300)
    stated_country = models.CharField(max_length=30)
    stated_zipcode = models.CharField(max_length=30)
    age = models.IntegerField()
    stated_birthdate = models.DateField()
    date_joined = models.DateField()
    receiving_broadcasts = models.BooleanField()
    receiving_emails = models.BooleanField()
    last_visit = models.DateField()
    stated_organisation = models.CharField(max_length=30)
    stated_website = models.CharField(max_length=300)
    stated_email = models.CharField(max_length=300)
    stated_skypeid = models.CharField(max_length=30)
    stated_twitterid = models.CharField(max_length=30)
    stated_bio = models.TextField()
    stated_ushahidi_experience = models.TextField()
    stated_ushahidi_tasks = models.TextField()
    stated_desired_team = models.CharField(max_length=30)
    stated_skills = models.TextField()
    stated_languages = models.TextField()
    stated_location_and_timezone = models.TextField()

class Ninggroup(models.Model):
    ning_id = models.CharField(max_length=30)

class Ningevent(models.Model):
    ning_id = models.CharField(max_length=30)

# Skype inputs
class Skypeuserprofile(models.Model):
    skype_id         = models.CharField(max_length=30)
    stated_fullname  = models.CharField(max_length=30)
    about            = models.TextField()
    stated_homepage  = models.CharField(max_length=300)
    stated_homephone = models.CharField(max_length=30)
    language         = models.CharField(max_length=90)
    numberofbuddies  = models.IntegerField()
    lastonline       = models.DateTimeField("last online")
    stated_country   = models.CharField(max_length=60)
    stated_province  = models.CharField(max_length=30)
    stated_city      = models.CharField(max_length=30)
    stated_timezone  = models.CharField(max_length=30)

class Skypegroup(models.Model):
    skype_id = models.CharField(max_length=30)

class Skypechatlog(models.Model):
    skype_id = models.CharField(max_length=30)

class Skypechatentry(models.Model):
    skype_id = models.CharField(max_length=30)

class Skypeurl(models.Model):
    skype_id = models.CharField(max_length=30)

class Skypememberlist(models.Model):
    skype_id = models.CharField(max_length=30)

# Googlegroup inputs
class Googleuserprofile(models.Model):
    google_id        = models.CharField(max_length=30)
    stated_fullname  = models.CharField(max_length=30)
    about            = models.TextField()
 
