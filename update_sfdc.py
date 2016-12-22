#!/usr/bin/env python

import json
import logging
import datetime as dt

from simple_salesforce import Salesforce
from pprint import pprint

from zoom_call import ZoomInfo
from sfdc import *
from sec import *


def get_zoom_accounts(sf, zoom):
    """
    Calls down the total of marked accounts. Queries Zoom to build results lists.
    """
    # Begin run of account queries
    # TODO Add not in already appended to SOQL query.
    query = "SELECT Id, Name, Website FROM Account WHERE Approved_for_Zoominfo_Append__c = True AND " \
            "ZoomInfo_Appended__c = NULL "
    domains, ids = sfdc_object_query(sf, query)
    logging.info("Accounts to be run: %s", str(len(domains)))

    results = {}
    """
    for idx, account in enumerate(domains):
        results[ids[idx]] = zoom.company_search(account)
    pprint(results)
    """
    # Testing JSON strings grabbed from ZoomInfo Testing Tool
    with open("sample_data/ticketmaster") as f:
        results["0010L00001k4A86QAE"] = json.loads(f.read())["CompanyDetailRequest"]
    with open("sample_data/dicks") as f:
        results["0010L00001k4A8GQAU"] = json.loads(f.read())["CompanyDetailRequest"]
    return convert_to_sfdc_fields(results)


def get_zoom_contacts(sf, zoom):
    """
    Calls down the total of marked contacts. Queries Zoom to build results lists.
    """
    query = "SELECT Id, Email, Name FROM Contact WHERE Approved_for_Zoominfo_Append__c = True AND " \
            "ZoomInfo_Appended__c = NULL "
    emails, ids = sfdc_object_query(sf, query, type="contact")
    logging.info("Contacts to be run: %s", str(len(emails)))

    results = {}
    """
    for idx, email in enumerate(emails):
        results[ids[idx]] = zoom.person_search(email)
    pprint(results)
    """
    # Testing JSON strings grabbed from ZoomInfo Testing Tool
    with open("sample_data/alex") as f:
        results["0030L00001lmodWQAQ"] = json.loads(f.read())["PersonDetailRequest"]
    with open("sample_data/elon") as f:
        results["0030L00001lmpYCQAY"] = json.loads(f.read())["PersonDetailRequest"]
    return convert_to_sfdc_fields(results, update_type="contact")


def update_sfdc(sf, objects_to_update, object_type):
    """Update sfdc accounts with acquired ZoomInfo"""
    response = "ERROR IN UPDATE_SFDC"
    for k, v in objects_to_update.items():
        try:
            if object_type == "account":
                sf.Account.update(k, v)
            elif object_type == "contact":
                sf.Contact.update(k, v)
            response = "{} update complete - all successful.".format(object_type)
        except:
            logging.error("Unable to update %s", k)
            response = "{} update complete with errors. Check logs.".format(object_type)
    print(response)


def get_sfdc_fields(sf):
    pprint(sf.Contact.get("0030L00001lmodWQAQ"))


if __name__ == "__main__":
    log_file = "logs/update-{}".format(dt.datetime.utcnow().strftime())
    logging.basicConfig(filename='ZoomInfoCalls.log', format='%(asctime)s %(message)s', level=logging.INFO)
    # Initialize SF and zoom instances
    SF = Salesforce(username=SFUN, password=SFPWD, security_token=SFTKN, client_id="Sales_Bot")
    zoom = ZoomInfo(ZPC, ZKEY)
    # TODO - distribute usage information
    pprint("Usage for account: {}".format(ZPC))
    pprint(zoom.usage_report)

    logging.info('Started')
    accounts_to_update = get_zoom_accounts(SF, zoom)
    contacts_to_update = get_zoom_contacts(SF, zoom)
    logging.info('Finished getting info from ZoomInfo')
    pprint(accounts_to_update)
    pprint(contacts_to_update)
    logging.info("Starting sfdc update")
    update_sfdc(SF, accounts_to_update, object_type="account")
    update_sfdc(SF, contacts_to_update, object_type="contact")
    logging.info("Success")
