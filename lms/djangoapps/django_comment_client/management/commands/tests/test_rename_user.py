from django.core.management.base import BaseCommand, CommandError
import unittest
from django.contrib.auth.models import User
from pymongo import MongoClient
from student.tests.factories import UserFactory
import datetime
from django.test import TestCase

from .. import rename_user


class TestRenameUser(TestCase):
    NEW_USERNAME = "targetName"


    @classmethod
    def setUpClass(cls):
        client = MongoClient()
        #chooses to temporarily write to the forum database
        cls.db = client.forum
        #maintain arrays of mongo data so that we can delete them when the tests are done
        cls.mongo_user_ids = []
        cls.mongo_comment_ids = []
        cls.sql_users = []
        cls.rename_cmd = rename_user.Command()
        cls.seed_sql_users()
        cls.seed_mongo_comments()
        cls.seed_mongo_users()


    @classmethod
    def seed_sql_users(cls):
        cls.sql_users.append(UserFactory.create())
        cls.sql_users.append(UserFactory.create())
        cls.sql_users.append(UserFactory.create())

    @classmethod
    def seed_mongo_comments(cls):
        comment_1 = {
	                "_type" : "CommentThread",
	                "abuse_flaggers" : [ ],
	                "anonymous" : False,
	                "anonymous_to_peers" : False,
	                "at_position_list" : [ ],
	                "author_id" : "1",
	                "author_username" : cls.sql_users[0].username,
	                "body" : "Architecto suscipit dolores. Velit enim quasi doloribus suscipit maxime laboriosam. Voluptatibus totam dolor dolorem dolorum placeat. Provident necessitatibus fugiat quia aut numquam repudiandae. Cum excepturi doloremque mollitia itaque eum praesentium.\n\nEx tempore maiores eum ea sed alias sint. Maiores veritatis commodi dolores aut et dolorem mollitia. Qui neque sed ea placeat.\n\nSit voluptas dicta et ut. Voluptas velit beatae veniam magni dolores. Est sed impedit numquam dolorum perspiciatis veniam. Temporibus inventore distinctio ratione labore nobis alias dolores. Est velit nihil dolorem qui nesciunt asperiores veritatis.",
	                "closed" : False,
	                "comment_count" : 9,
	                "commentable_id" : "video_1",
	                "course_id" : "MITx/6.002x/2012_Fall",
                    "created_at" : datetime.datetime.strptime('22092013', "%d%m%Y"),
                    "historical_abuse_flaggers" : [ ],
                    "last_activity_at" :  datetime.datetime.strptime('22092013', "%d%m%Y"),
                    "tags_array" : [
                        "c#",
                        "2012",
                        "java-sucks"
                    ],
                    "thread_type" : "discussion",
                    "title" : "Dolore et molestias quia maxime eaque quos voluptatem et.",
                    "updated_at" :  datetime.datetime.strptime('22092013', "%d%m%Y"),
                    "visible" : True,
                    "votes" : {
                        "count" : 7,
                        "down" : [
                            "1",
                            "3",
                            "4",
                            "5",
                            "7"
                        ],
                        "down_count" : 5,
                        "point" : -3,
                        "up" : [
                            "2",
                            "6"
                        ],
                        "up_count" : 2
	                }

                }

        comment_2 = {
                        "_type" : "Comment",
                        "abuse_flaggers" : [ ],
                        "anonymous" : False,
                        "anonymous_to_peers" : False,
                        "at_position_list" : [ ],
                        "author_id" : "2",
                        "author_username" : cls.sql_users[1].username,
                        "body" : "Tempora quis molestias unde. Dolore facilis tenetur repellendus quia labore doloribus molestiae.",
                        "comment_thread_id" : "523e7ed87b36b70200000001",
                        "course_id" : "MITx/6.002x/2012_Fall",
                        "created_at" : datetime.datetime.strptime('22092013', "%d%m%Y"),
                        "endorsed" : False,
                        "historical_abuse_flaggers" : [ ],
                        "parent_ids" : [ ],
                        "sk" : "523e7ed87b36b70200000005",
                        "updated_at" : datetime.datetime.strptime('22092013', "%d%m%Y"),
                        "visible" : True,
                        "votes" : {
                            "count" : 7,
                            "down" : [
                                "3",
                                "5",
                                "6",
                                "7"
                            ],
                            "down_count" : 4,
                            "point" : -1,
                            "up" : [
                                "1",
                                "2",
                                "4"
                            ],
                            "up_count" : 3
                        }
                    }

        comment_3 = {
                        "visible" : True,
                        "abuse_flaggers" : [ ],
                        "historical_abuse_flaggers" : [ ],
                        "parent_ids" : [
                            "523e7ed87b36b70200000005"
                        ],
                        "votes" : {
                            "up" : [ ],
                            "down" : [ ],
                            "up_count" : 0,
                            "down_count" : 0,
                            "count" : 0,
                            "point" : 0
                        },
                        "at_position_list" : [ ],
                        "body" : "Quia est laborum. Non fugiat laborum omnis vero. Ipsum nihil sint neque. Voluptatum nemo repellendus voluptates sequi aliquid earum.",
                        "_type" : "Comment",
                        "endorsed" : False,
                        "anonymous" : False,
                        "anonymous_to_peers" : False,
                        "parent_id" : "523e7ed87b36b70200000005",
                        "author_id" : "3",
                        "comment_thread_id" : "523e7ed87b36b70200000001",
                        "course_id" : "MITx/6.002x/2012_Fall",
                        "author_username" : cls.sql_users[2].username,
                        "sk" : "523e7ed87b36b70200000005-523e7ed97b36b70200000006",
                        "updated_at" : datetime.datetime.strptime('22092013', "%d%m%Y"),
                        "created_at" : datetime.datetime.strptime('22092013', "%d%m%Y")
                    }
        cls.mongo_comment_ids.append(cls.db.contents.insert(comment_1))
        cls.mongo_comment_ids.append(cls.db.contents.insert(comment_2))
        cls.mongo_comment_ids.append(cls.db.contents.insert(comment_3))


    @classmethod
    def seed_mongo_users(cls):
        user_1 = {
                    "default_sort_key" : "date",
                    "notification_ids" : [ ],
                    "external_id" : "test_user_1",
                    "username" : cls.sql_users[0].username
                }
        user_2 = {
                    "default_sort_key" : "date",
                    "email" : "robot2@robots.com",
                    "external_id" : "test_user_2",
                    "notification_ids" : [ ],
                    "read_states" : [
                        {
                            "_id" : "5410bb0d9fbe726175000002",
                            "course_id" : "Carnegie/Training/CLASlite",
                            "last_read_times" : {
                                "5410bb0a9fbe727505000001" : datetime.datetime.strptime('10092014', "%d%m%Y"),
                                "541b0ef870da966ba5000001" : datetime.datetime.strptime('10092014', "%d%m%Y")
                            }
                        }
                    ],
                    "username" : cls.sql_users[1].username
                }

        user_3 = {
                    "default_sort_key" : "date",
                    "notification_ids" : [ ],
                    "external_id" : "test_user_3",
                    "username" : cls.sql_users[2].username,
                    "email" : "robot3@robots.com"
                }

        cls.mongo_user_ids.append(cls.db.users.insert(user_1))
        cls.mongo_user_ids.append(cls.db.users.insert(user_2))
        cls.mongo_user_ids.append(cls.db.users.insert(user_3))



    def test_mongo_seed(self):
        self.assertTrue(len(self.mongo_user_ids) == 3, 'Test mongo users were not properly seeded, rendering tests invalid.')
        self.assertTrue(len(self.mongo_comment_ids) == 3, 'Test mongo comments were not properly seeded, rendering the tests invalid.')

    def test_incorrect_num_args(self):
        zero_args = []
        one_arg = ['arg']
        three_args = ['arg', 'arg', 'arg']
        self.assertRaises(CommandError, self.rename_cmd.handle, *zero_args)
        self.assertRaises(CommandError, self.rename_cmd.handle, *one_arg)
        self.assertRaises(CommandError, self.rename_cmd.handle, *three_args)

    def test_user_does_not_exist(self):
        args = ['---@---.com', '---2@---2.com']
        self.assertRaises(LookupError, self.rename_cmd.handle, *args)


    def test_change_username_basic(self):
        #ensure that the starting sql username is different from the target username
        self.assertTrue(self.sql_users[0].username != TestRenameUser.NEW_USERNAME)

        #ensure that the starting mongo username matches the starting sql username
        mongo_user = self.db.users.find_one({'username':self.sql_users[0].username})
        self.assertTrue(mongo_user['username'] == self.sql_users[0].username)
        mongo_comment = self.db.contents.find_one({'author_username':self.sql_users[0].username})
        self.assertTrue(mongo_comment['author_username'] == self.sql_users[0].username)

        #perform the rename
        args = [self.sql_users[0].username, TestRenameUser.NEW_USERNAME]
        self.rename_cmd.handle(*args)

        #check that the sql username now matches the target username
        self.sql_users[0] = User.objects.get(id=self.sql_users[0].id)
        self.assertEqual(self.sql_users[0].username, TestRenameUser.NEW_USERNAME)

        #check that the mongo username now matches the target username
        mongo_user = self.db.users.find_one({'_id':mongo_user['_id']})
        self.assertEqual(mongo_user['username'], TestRenameUser.NEW_USERNAME)

        mongo_comment = self.db.contents.find_one({'_id':mongo_comment['_id']})
        self.assertEqual(mongo_comment['author_username'], TestRenameUser.NEW_USERNAME)



    def test_change_username_advanced(self):
        #ensure that the starting  usernames are different from the target username

        self.assertTrue(self.sql_users[0].username != TestRenameUser.NEW_USERNAME)
        self.assertTrue(self.sql_users[1].username != TestRenameUser.NEW_USERNAME)
        self.assertTrue(self.sql_users[2].username != TestRenameUser.NEW_USERNAME)

        mongo_user1 = self.db.users.find_one({'username':self.sql_users[0].username})
        mongo_user2 = self.db.users.find_one({'username':self.sql_users[1].username})
        mongo_user3 = self.db.users.find_one({'username':self.sql_users[2].username})

        mongo_comment1 = self.db.contents.find_one({'author_username':self.sql_users[0].username})
        mongo_comment2 = self.db.contents.find_one({'author_username':self.sql_users[1].username})
        mongo_comment3 = self.db.contents.find_one({'author_username':self.sql_users[2].username})

        #ensure that the starting mongo usernames match the starting sql usernames
        self.assertTrue(mongo_user1['username'] == self.sql_users[0].username)
        self.assertTrue(mongo_comment1['author_username'] == self.sql_users[0].username)

        self.assertTrue(mongo_user2['username'] == self.sql_users[1].username)
        self.assertTrue(mongo_comment2['author_username'] == self.sql_users[1].username)

        self.assertTrue(mongo_user3['username'] == self.sql_users[2].username)
        self.assertTrue(mongo_comment3['author_username'] == self.sql_users[2].username)



        #perform the rename only for the second user
        args = [self.sql_users[1].username, TestRenameUser.NEW_USERNAME]
        self.rename_cmd.handle(*args)


        #requery sql and mongo users
        self.sql_users[0] = User.objects.get(id=self.sql_users[0].id)
        self.sql_users[1] = User.objects.get(id=self.sql_users[1].id)
        self.sql_users[2] = User.objects.get(id=self.sql_users[2].id)

        mongo_user1 = self.db.users.find_one({'_id':mongo_user1['_id']})
        mongo_user2 = self.db.users.find_one({'_id':mongo_user2['_id']})
        mongo_user3 = self.db.users.find_one({'_id':mongo_user3['_id']})

        mongo_comment1 = self.db.contents.find_one({'_id':mongo_comment1['_id']})
        mongo_comment2 = self.db.contents.find_one({'_id':mongo_comment2['_id']})
        mongo_comment3 = self.db.contents.find_one({'_id':mongo_comment3['_id']})

        #check that the rename was successful for only the second user
        self.assertNotEqual(self.sql_users[0].username, TestRenameUser.NEW_USERNAME)
        self.assertNotEqual(mongo_user1['username'], TestRenameUser.NEW_USERNAME)
        self.assertNotEqual(mongo_comment1['author_username'], TestRenameUser.NEW_USERNAME)

        self.assertEqual(self.sql_users[1].username, TestRenameUser.NEW_USERNAME)
        self.assertEqual(mongo_user2['username'], TestRenameUser.NEW_USERNAME)
        self.assertEqual(mongo_comment2['author_username'], TestRenameUser.NEW_USERNAME)

        self.assertNotEqual(self.sql_users[2].username, TestRenameUser.NEW_USERNAME)
        self.assertNotEqual(mongo_user3['username'], TestRenameUser.NEW_USERNAME)
        self.assertNotEqual(mongo_comment3['author_username'], TestRenameUser.NEW_USERNAME)




    @classmethod
    def tearDownClass(cls):
        #remove test mongo users
        for test_user_id in cls.mongo_user_ids:
            cls.db.users.remove({"_id":test_user_id})
        #remove test mongo comments
        for test_comment_id in cls.mongo_comment_ids:
            cls.db.contents.remove({"_id":test_comment_id})
        #sql users are flushed before each test because this class inherits from django.test.TestCase







