from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class Command(BaseCommand):
    args = '<old_username> <new_username>'
    help = 'Modify the username of an existing user'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Usage is rename_user {0}'.format(self.args))

        try:
            user = User.objects.get(username=args[0])
        except User.DoesNotExist:
            raise LookupError("User %s does not exist. Available users: %s" % (args[0], User.objects.all()))

        #update mongo collections, then sql
        try:
            client = MongoClient()
            db = client.forum
            db.users.update({'username':args[0]}, {'$set': {'username':args[1]}}, multi=True);
            db.contents.update({'author_username':args[0]}, {'$set': {'author_username':args[1]}}, multi=True);
        except:
            print 'Error modifying the username for %s in mongodb' % args[0]
            raise
        else:
            user.username = args[1]
            user.save()
            print "changed username of user: %s to %s" % (args[0], args[1])


