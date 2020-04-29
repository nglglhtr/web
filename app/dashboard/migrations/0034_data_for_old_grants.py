# Generated by Django 2.1.7 on 2019-04-29 21:15

from django.db import migrations
from grants.models import Grant, Subscription
from dashboard.models import Activity
from datetime import datetime, timedelta
from pytz import UTC

def record_grant_activity_helper(activity_type, grant, profile, date):
    """Registers a new activity concerning a grant

    Args:
        activity_type (str): The type of activity, as defined in dashboard.models.Activity.
        grant (grants.models.Grant): The grant in question.
        profile (dashboard.models.Profile): The current user's profile.

    """
    try:
        grant_logo = grant.logo.url
    except:
        grant_logo = None
    metadata = {
        'id': grant.id,
        'value_in_token': '{0:.2f}'.format(grant.amount_received),
        'token_name': grant.token_symbol,
        'title': grant.title,
        'grant_logo': grant_logo,
        'grant_url': grant.url,
        'category': 'grant',
    }
    kwargs = {
        'profile': profile,
        'grant': grant,
        'activity_type': activity_type,
        'metadata': metadata,
        'created_on': date,
    }
    if not activity_exists(activity_type, grant, 'grant', profile, date):
        Activity.objects.create(**kwargs)

def record_subscription_activity_helper(activity_type, subscription, profile, date):
    """Registers a new activity concerning a grant subscription

    Args:
        activity_type (str): The type of activity, as defined in dashboard.models.Activity.
        subscription (grants.models.Subscription): The subscription in question.
        profile (dashboard.models.Profile): The current user's profile.

    """
    try:
        grant_logo = subscription.grant.logo.url
    except:
        grant_logo = None
    metadata = {
        'id': subscription.id,
        'value_in_token': str(subscription.amount_per_period),
        'value_in_usdt_now': str(subscription.amount_per_period_usdt),
        'token_name': subscription.token_symbol,
        'title': subscription.grant.title,
        'grant_logo': grant_logo,
        'grant_url': subscription.grant.reference_url,
        'category': 'grant',
    }
    kwargs = {
        'profile': profile,
        'subscription': subscription,
        'activity_type': activity_type,
        'metadata': metadata,
        'created_on': date,
    }
    if not activity_exists(activity_type, subscription, 'subscription', profile, date):
        Activity.objects.create(**kwargs)

def close_enough(date1, date2):
    bigger = max(date1, date2)
    smaller = min(date1, date2)
    delta = bigger - smaller
    threshold = timedelta(1) # one day
    return delta < threshold

def activity_exists(activity_type, object, object_type, profile, date):
    if object_type == 'grant':
        candidates = Activity.objects.filter(grant = object)
    else:
        candidates = Activity.objects.filter(subscription__grant = object.grant)
    for activity in candidates:
        if activity.activity_type == activity_type:
            if activity_type == 'new_grant' or activity_type == 'killed_grant':
                return True # there can't be two activities of this type for one grant
            elif activity.profile == profile and close_enough(activity.created_on, date):
                return True
    return False

def generate_grant_activities(deployment):
    for grant in Grant.objects.all():
        if grant.created_on < deployment:
            profile = grant.admin_profile
            date = grant.created_on
            record_grant_activity_helper('new_grant', grant, profile, date)
            if not(close_enough(grant.modified_on, grant.created_on)) and grant.modified_on < deployment:
                date = grant.modified_on
                if grant.active:
                    record_grant_activity_helper('update_grant', grant, profile, date)
                else:
                    record_grant_activity_helper('killed_grant', grant, profile, date)

def generate_subscription_activities(deployment):
    for subscription in Subscription.objects.all():
        if subscription.created_on < deployment:
            profile = subscription.contributor_profile
            date = subscription.created_on
            if subscription.num_tx_approved == 1:
                record_subscription_activity_helper('new_grant_contribution', subscription, profile, date)
            else:
                record_subscription_activity_helper('new_grant_subscription', subscription, profile, date)
            if not subscription.active and subscription.modified_on < deployment:
                date = subscription.modified_on
                record_subscription_activity_helper('killed_grant_contribution', subscription, profile, date)

def generate_activities(apps, schema_editor):
    deployment = datetime(2019, 4, 24, 11, 53, 00, tzinfo=UTC)
    generate_grant_activities(deployment)
    generate_subscription_activities(deployment)

class Migration(migrations.Migration):


    dependencies = [
        ('dashboard', '0033_bounty_bounty_categories'),
        ('grants', '0024_auto_20190612_1645'),
    ]

    operations = [
        # migrations.RunPython(generate_activities),
    ]