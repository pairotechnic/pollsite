'''
    Purpose : Tests that ensure the application behaves as intended
    Author : Rohit Pai
    Date : 17th July 2024
'''

# Standard Library Imports
import datetime

# Third Party Imports
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# Local Application Imports
from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
            was_published_recently() returns False for questions whose pub_date is in the future
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        '''
            was_published_recently() returns False for questions whose pub_date is older than 1 day
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        '''
            was_published_recently() returns True for questions whose pub_date is within the last day
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    '''
        Creates a question with the given 'question_text'
        Publish date set to now, offset by the given number of days
        'days' will be negative for questions published in the past, positive for future
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
            If no questions exist, an appropriate message is displayed
        '''
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        '''
            Questions with a pub_date in the past are displayed on the index page
        '''
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_future_question(self):
        '''
            Questions with pub_dates in the future aren't displayed on the index page
        '''
        create_question(question_text="Future question.", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        '''
            Even if both past and future questions exist
            Only past questions are desplayed on index page
        '''
        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        '''
            The questions index page will display multiple past questions
        '''
        question1 = create_question(question_text="Past question 1.", days = -30)
        question2 = create_question(question_text="Past question 2.", days = -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1]
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
            The detail view of a question with pub_date in the future returns a 404 not found
        '''
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
            The detail view of a question published in the past displays the question text
        '''

        past_question = create_question(question_text="Past question.", days=-30)
        url = reverse("polls:details", args=(past_question.id),)
        response=self.client.get(url)
        self.assertContains(response, past_question.question_text)