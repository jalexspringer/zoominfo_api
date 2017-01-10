#!/usr/bin/env python

import json
import logging
import datetime as dt

from simple_salesforce import Salesforce
from pprint import pprint
import requests

from zoom_call import ZoomInfo
from sfdc import *
from sec import *
from query_dictionaries import *


def zoom_account_query(sf, zoom):
    """
    Calls down the total of marked accounts. Queries Zoom to build results lists.
    """
    # Begin run of account queries
    query = "SELECT Id, Name, Website FROM Account WHERE Approved_for_Zoominfo_Append__c = True AND " \
            "ZoomInfo_Appended__c = NULL "
    domains, ids = sfdc_object_query(sf, query)
    logging.info("Accounts to be run: %s", str(len(domains)))

    results = {}
    for idx, account in enumerate(domains):
        dictionary = company_detail_dictionary.copy()
        dictionary["CompanyDomain"] = account.lstrip("www.")
        print(dictionary)
    #    results[ids[idx]] = zoom.query("company", "detail", dictionary)

    # Testing JSON strings grabbed from ZoomInfo Testing Tool
    #with open("sample_data/dicks") as f:
    #    results["0010L00001k4A8GQAU"] = json.loads(f.read())["CompanyDetailRequest"]
    results["0010L00001k4A8G"] = requests.get("http://partnerapi.zoominfo.com/partnerapi/company/detail?pc=SF_ImpactRadius&key=2db3224f0501af7cbef579db9e034628&companyDomain=dickssportinggoods.com&outputType=JSON&outputFieldOptions=companyRevenueNumeric").json()
    #pprint(results)
    return convert_to_sfdc_fields(results)


def zoom_contact_query(sf, zoom):
    """
    Calls down the total of marked contacts. Queries Zoom to build results lists.
    """
    query = "SELECT Id, Email, Name FROM Contact WHERE Approved_for_Zoominfo_Append__c = True AND " \
            "ZoomInfo_Appended__c = NULL "
    emails, ids = sfdc_object_query(sf, query, update_type="contact")
    logging.info("Contacts to be run: %s", str(len(emails)))

    results = {}

    for idx, email in enumerate(emails):
        dictionary = person_detail_dictionary.copy()
        dictionary["EmailAddress"] = email
        #results[ids[idx]] = zoom.query("person", "detail", dictionary, outputFieldOptions="companyRevenueNumeric")

    # Testing JSON strings grabbed from ZoomInfo Testing Tool
    #with open("sample_data/alex") as f:
    #    results["0030L00001mDbO5QAK"] = json.loads(f.read())["PersonDetailRequest"]
    results["0030L00001mDbO5QAK"] = requests.get(
        "http://partnerapi.zoominfo.com/partnerapi/person/detail?pc=SF_ImpactRadius&key=8520c081687991687b580c4617763e3e&emailAddress=aspringer@impactradius.com&outputType=JSON").json()
    return convert_to_sfdc_fields(results, update_type="contact")


def get_new_zoom_contacts(sf, zoom):
    person_search_dictionary_ir = OrderedDict([
        ('personTitle', None),
        ('TitleSeniority', "C_EXECUTIVES,VP_EXECUTIVES,DIRECTOR,MANAGER"),
        ('titleClassification', "786434,2555906,3932162,3932163,3276802"),
        ('companyId', None),
        ('IndustryClassification', "5386,5898,5642,4106,1290"),
        ('RevenueClassificationMin', "5000"),
        ('RevenueClassificationMax', "5000000"),
        ('companyDomainName', None),
        ('ValidDateMonthDist', None),
        ('ContactRequirements', "4"),
        ('companyPastOrPresent', "Current")
    ])

    query = "SELECT Name, Website, Id FROM Account WHERE Zoom_Contacts_Request__c = True AND Contacts_Appended__c = Null"
    accounts, ids = sfdc_object_query(sf, query, update_type="new_contacts")
    logging.info("Accounts to search for new contacts: %s", str(len(accounts)))

    results = {}
    for idx, account in enumerate(accounts):
        # dead_list = f"SELECT Name, Email FROM Contact WHERE Account = '{account}'"
        dictionary = person_search_dictionary_ir.copy()
        dictionary["companyDomainName"] = account
        results[ids[idx]] = zoom.query("person", "search", dictionary)
    return convert_to_sfdc_fields(results, update_type="new_contact_search")


def update_sfdc(sf, objects_to_update, object_type):
    """Update sfdc accounts with acquired ZoomInfo"""
    response = "ERROR IN UPDATE_SFDC"
    for k, v in objects_to_update.items():
        try:
            if object_type == "account":
                sf.Account.update(k, v)
            elif object_type == "contact":
                sf.Contact.update(k, v)
            elif object_type == "add_new_contacts":
                sf.Contact.create(v)
            response = "{} update complete - all successful.".format(object_type)
        except:
            logging.error("Unable to update %s", k)
            response = "{} update complete with errors. Check logs.".format(object_type)
    print(response)


def get_sfdc_fields(sf):
    pprint(sf.Account.get("001E000000TLdsp"))


if __name__ == "__main__":
    now = dt.datetime.utcnow().strftime("%Y%m%_%X")
    log_file = f"logs/{now}"
    logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', level=logging.INFO)
    # Initialize SF and zoom instances
    SF = Salesforce(username=SFUN, password=SFPWD, security_token=SFTKN, client_id="Sales_Bot")
    zoom = ZoomInfo(ZPC, ZKEY)
    #pprint("Usage for account: {}".format(ZPC))
    #pprint(zoom.usage_report)
    logging.info('Started')
    accounts_to_update = zoom_account_query(SF, zoom)
    contacts_to_update = zoom_contact_query(SF, zoom)
    contacts_to_add = get_new_zoom_contacts(SF, zoom)
    logging.info('Finished getting info from ZoomInfo')
    pprint(accounts_to_update)
    pprint(contacts_to_update)
    pprint(contacts_to_add)
    logging.info("Starting sfdc update")
    update_sfdc(SF, accounts_to_update, object_type="account")
    update_sfdc(SF, contacts_to_update, object_type="contact")
    for account, contacts in contacts_to_add.items():
        temp = {account: {"Zoom_Contacts_Request__c": False, "Contacts_Appended__c": dt.datetime.now().strftime('%Y-%m-%d')}}
        update_sfdc(SF, temp, object_type="account")
        update_sfdc(SF, contacts, object_type="add_new_contacts")
    logging.info("Success")
