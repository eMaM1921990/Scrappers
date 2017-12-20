from django.conf import settings

__author__ = 'eMaM'

from simple_salesforce import Salesforce
from datetime import datetime
import pytz
import re
from time import sleep


E164_RE = re.compile('^\+\d{11}$')
# Lead object reference: https://developer.salesforce.com/docs/atlas.en-us.sfFieldRef.meta/sfFieldRef/salesforce_field_reference_Lead.htm
# SOQL reference: https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm

sf = Salesforce(
    username=settings.USERNAME,
    password=settings.PASS,
    security_token=settings.TOKEN,
    # sandbox=True
)


def get_lead_object(last_name, phone, campaign_source, lead_source, website, company, tags, is_international):
    return {
        'Status': 'New',  # static
        'LastName': last_name,  # put whole name string into last name
        'Phone': phone,  # phone number formatted to E.164 number formatting. +[countrycode][areacode][number]
        'Campaign_Source__c': campaign_source,  # City and State (and country if applicable)
        'LeadSource': lead_source,  # website name and medium. For example: HomeAway Website,
        'Website': website,  # Advertising website
        'Rating': '1. New',  # Static
        'Company': company,  # website name
        'Tag_Cloud__c': tags,  # random tags, i used source, method, property type.
        'International_Phone__c': is_international
    }


def create_lead(last_name, phone, campaign_source, lead_source, website, company, tags, is_international):
    lead_obj = get_lead_object(last_name, phone, campaign_source, lead_source, website, company, tags, is_international)
    sf.Lead.create(lead_obj)


# Pulls all phone numbers. Phone numbers are not all the same format, so numbers will need to be standardized or converted before comparison
def query_all_leads():
    tables = ['Lead', 'Contact', 'Account']
    entries = []
    for each in tables:
        entries.extend(sf.query_all("select Id, Phone from {}".format(each)))
    return entries


# You can use this to create a single lead to salesforce
def check_and_create_lead(last_name, phone, campaign_source, lead_source, website, company, tags, is_international):
    # if phone_exists(phone):
    #     raise Exception("Phone already exists: {}".format(phone))
    create_lead(
        last_name=last_name,
        phone=phone,
        campaign_source=campaign_source,
        lead_source=lead_source,
        website=website,
        company=company,
        tags=tags,
        is_international=is_international
    )


check_and_create_lead(
    last_name='(Fake do not process) Joe & Mathers Fava',
    phone='16268645227',
    campaign_source='Panama City, FL',
    lead_source='Flipkey Website',
    website='https://www.flipkey.com/properties/8801586/',
    company='Flipkey',
    tags='flipkey, scrape, house',
    is_international=True
)
