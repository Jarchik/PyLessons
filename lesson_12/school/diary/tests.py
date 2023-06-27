from django.urls import reverse
import pytest
from pytest_django.asserts import assertQuerysetEqual
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .models import WeekDay, Note


def create_and_authenticate_user(client: Client):
    User.objects.create_user(username='fred', password='A4F33fsdfFDSF', email='test@test.com')

    assert get_user(client).is_authenticated is False
    client.login(username='fred', password='A4F33fsdfFDSF')
    assert get_user(client).is_authenticated is True


@pytest.mark.django_db
@pytest.mark.urls('diary.urls')
def test_index_redirects(client):
    response = client.get('/')
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.urls('diary.urls')
def test_index_redirects_to_my_week(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.url == reverse('my_week')


@pytest.mark.django_db
def test_my_week_login_required(client):
    assert get_user(client).is_authenticated is False
    response = client.get('/week/')

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_week_has_three_days(client):
    create_and_authenticate_user(client)

    response_clean_database = client.get('/week/')
    weeks_days = WeekDay.objects.all()
    assertQuerysetEqual(response_clean_database.context["days"], weeks_days)
    for day in ['Mon', 'Tue', 'Wed']:
        WeekDay.objects.create(day=day)
    weeks_days_updated = WeekDay.objects.all()
    response_fulfilled_database = client.get('/week/')
    assertQuerysetEqual(response_fulfilled_database.context["days"], weeks_days_updated, ordered=False)
    assert len(response_fulfilled_database.context["days"]) == 3


@pytest.mark.django_db
def test_my_week_login_required(client):
    assert get_user(client).is_authenticated is False
    response = client.get('/day/1/')

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_day_returns_notes(client):
    create_and_authenticate_user(client)

    # Prefill DB
    monday = WeekDay.objects.create(day='Mon')
    tuesday = WeekDay.objects.create(day='Tue')

    Note.objects.create(week_day=monday, title='Title Monday 1', msg='message monday 1')

    Note.objects.create(week_day=tuesday, title='Title Tuesday 1', msg='message tuesday 1')
    Note.objects.create(week_day=tuesday, title='Title Tuesday 2', msg='message tuesday 2')
    Note.objects.create(week_day=tuesday, title='Title Tuesday 3', msg='message tuesday 3')

    # Check Monday's notes
    response_qs_monday = client.get('/day/1/')
    assertQuerysetEqual(response_qs_monday.context["week_day"].note_set.all(), monday.note_set.all(), ordered=False)
    assert len(response_qs_monday.context["week_day"].note_set.all()) == 1

    # Check Tuesday's notes
    response_qs_tuesday = client.get('/day/2/')
    assertQuerysetEqual(response_qs_tuesday.context["week_day"].note_set.all(), tuesday.note_set.all(), ordered=False)
    assert len(response_qs_tuesday.context["week_day"].note_set.all()) == 3


@pytest.mark.django_db
def test_my_week_login_required(client):
    assert get_user(client).is_authenticated is False
    response = client.get('/note/1/')

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_note_returns_certain_note(client):
    create_and_authenticate_user(client)

    # Prefill DB
    tuesday = WeekDay.objects.create(day='Tue')
    note1 = Note.objects.create(week_day=tuesday, title='Title Tuesday 1', msg='message tuesday 1')
    note2 = Note.objects.create(week_day=tuesday, title='Title Tuesday 2', msg='message tuesday 2')

    # Check Tuesday's notes
    response_qs_tuesday = client.get('/note/1/')
    assert response_qs_tuesday.context["note"] == note1

    response_qs_tuesday = client.get('/note/2/')
    assert response_qs_tuesday.context["note"] == note2


@pytest.mark.django_db
def test_login_only_existing_user(client):
    assert get_user(client).is_authenticated is False
    client.login(username='fred', password='fake_password')
    assert get_user(client).is_authenticated is False


@pytest.mark.django_db
def test_user_registration__ok(client):
    response = client.post(reverse('register'),
                           data={'username': 'alice',
                                 'email': 'alice@example.com',
                                 'password1': 'A4F33fsdfFasdF',
                                 'password2': 'A4F33fsdfFasdF'})

    assert response.status_code == 302
    assert response.url == '/login'
    users = User.objects.all()
    assert users.count() == 1


@pytest.mark.django_db
def test_user_registration__password_mismatch(client):
    response = client.post(reverse('register'),
                           data={'username': 'alice',
                                 'email': 'alice@example.com',
                                 'password1': 'A4F33fsdfFasdF',
                                 'password2': 'dsfdsf'})

    assert response.status_code == 200

    users = User.objects.all()
    assert users.count() == 0
