from django.db import models
from django.contrib.auth.models import User


states = [
    ('alabama', 'Alabama',),
    ('alaska', 'Alaska',),
    ('arizona', 'Arizona',),
    ('arkansas', 'Arkansas',),
    ('california', 'California',),
    ('colorado', 'Colorado',),
    ('connecticut', 'Connecticut',),
    ('delaware', 'Delaware',),
    ('florida', 'Florida',),
    ('georgia', 'Georgia',),
    ('hawaii', 'Hawaii',),
    ('idaho', 'Idaho',),
    ('illinois', 'Illinois',),
    ('indiana', 'Indiana',),
    ('iowa', 'Iowa',),
    ('kansas', 'Kansas',),
    ('kentucky', 'Kentucky',),
    ('louisiana', 'Louisiana',),
    ('maine', 'Maine',),
    ('maryland', 'Maryland',),
    ('massachusetts', 'Massachusetts',),
    ('michigan', 'Michigan',),
    ('minnesota', 'Minnesota',),
    ('mississippi', 'Mississippi',),
    ('missouri', 'Missouri',),
    ('montana', 'Montana',),
    ('nebraska', 'Nebraska',),
    ('nevada', 'Nevada',),
    ('new hampshire', 'New Hampshire',),
    ('new jersey', 'New Jersey',),
    ('new mexico', 'New Mexico',),
    ('new york', 'New York',),
    ('north carolina', 'North Carolina',),
    ('north dakota', 'North Dakota',),
    ('ohio', 'Ohio',),
    ('oklahoma', 'Oklahoma',),
    ('oregon', 'Oregon',),
    ('pennsylvania', 'Pennsylvania',),
    ('rhode island', 'Rhode Island',),
    ('south carolina', 'South Carolina',),
    ('south dakota', 'South Dakota',),
    ('tennessee', 'Tennessee',),
    ('texas', 'Texas',),
    ('utah', 'Utah',),
    ('vermont', 'Vermont',),
    ('virginia', 'Virginia',),
    ('washington', 'Washington',),
    ('west virginia', 'West Virginia',),
    ('wisconsin', 'Wisconsin',),
    ('wyoming', 'Wyoming',),
    ('other', 'Other / Not U.S.'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    location = models.CharField(choices=states, max_length=100, blank=True)

    def __str__(self):
        return self.user.username
