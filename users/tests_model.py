from django.test import TestCase
from datetime import datetime, timezone
from .models import User, Profile, Job, ReviewRating, Comment

# Test Cases for all Models.
class ModelsTestCase(TestCase):
    user = None
    job = None
    def setUp(self) -> None:
        self.user = User.objects.create_user(
                username="spiderman",
                email="spider@web.com",
                password="GreatPower",
                first_name="Peter",
                last_name="Parker"
        )
              
    def tearDown(self) -> None:
        return super().tearDown()
    
    # Complete Create test cases for User Model
    def test_create_user(self):
        self.assertEqual('Peter', self.user.first_name)
        self.assertEqual('Parker', self.user.last_name)
        self.assertEqual('spiderman', self.user.username)
        self.assertEqual('spider@web.com', self.user.email)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        
    # Create test cases for Profile Model
    def test_create_profile(self):
        Profile.objects.update(
            role="creator",
            time_zone="US/Pacific",
            native_auth=True,
            rating=0,
            number_of_ratings=0,
            user_id=self.user.pk
        )
        profile = Profile.objects.get(user_id=self.user.pk)
        self.assertEqual('creator', profile.role)
        self.assertEqual('US/Pacific', profile.time_zone)
        self.assertEqual(True, profile.native_auth)
        self.assertEqual(0, profile.rating)
        self.assertEqual(0, profile.number_of_ratings)
    
    # Create test cases for Job Model    
    def test_create_job(self):
        self.job = Job.objects.create(
                name="Test Job",
                price="123",
                limit_price="150",
                created_date=datetime.now(timezone.utc).isoformat(),
                end_date=datetime.now(timezone.utc).isoformat(),
                description="Job Created for Testing the App",
                url2audio="www.google.com",
                user_id = self.user.pk
        )
        self.assertEqual("Test Job", self.job.name)
        self.assertEqual(123, int(self.job.price))
        self.assertEqual(150, int(self.job.limit_price))
        self.assertEqual("Job Created for Testing the App", self.job.description)
        self.assertEqual("www.google.com", self.job.url2audio)
        self.assertEqual(self.user.pk, self.job.user.pk)
        self.Test_create_comment()
    
    # Create test cases for ReviewRating Model
    def test_create_review(self):
        review = ReviewRating.objects.create(
            job_id=1,
            creator_id=self.user.pk,
            worker_id=self.user.pk,
            subject="Test Review",
            review="This is a test review for the job",
            rating=5
        )
        self.assertEqual(1, review.job_id)
        self.assertEqual(self.user.pk, review.creator_id)
        self.assertEqual(self.user.pk, review.worker_id)
        self.assertEqual("Test Review", review.subject)
        self.assertEqual("This is a test review for the job", review.review)
        self.assertEqual(5, review.rating)
    
    # Create test cases for Comment Model
    def Test_create_comment(self):
        comment = Comment.objects.create(
            name="Test Comment",
            content="This is a test comment for the job",
            job_id=self.job.pk
        )
        self.assertEqual("Test Comment", comment.name)
        self.assertEqual("This is a test comment for the job", comment.content)
        self.assertEqual(self.job.pk, comment.job.pk)  
    
    
        
        