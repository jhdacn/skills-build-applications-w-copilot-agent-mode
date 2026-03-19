from django.core.management.base import BaseCommand
from django.conf import settings
 
import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Collections
        users = db['users']
        teams = db['teams']
        activities = db['activities']
        leaderboard = db['leaderboard']
        workouts = db['workouts']

        # Clear collections
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Ensure unique index on email
        users.create_index([('email', 1)], unique=True)

        # Sample teams
        marvel = {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Thor', 'Black Widow']}
        dc = {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman', 'Flash']}
        teams.insert_many([marvel, dc])

        # Sample users
        user_data = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Thor', 'email': 'thor@marvel.com', 'team': 'Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Marvel'},
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonder@dc.com', 'team': 'DC'},
            {'name': 'Flash', 'email': 'flash@dc.com', 'team': 'DC'},
        ]
        users.insert_many(user_data)

        # Sample activities
        activities.insert_many([
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Superman', 'activity': 'Flying', 'duration': 60},
        ])

        # Sample leaderboard
        leaderboard.insert_many([
            {'team': 'Marvel', 'points': 100},
            {'team': 'DC', 'points': 90},
        ])

        # Sample workouts
        workouts.insert_many([
            {'user': 'Thor', 'workout': 'Hammer lifts', 'reps': 50},
            {'user': 'Batman', 'workout': 'Pushups', 'reps': 100},
        ])

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
