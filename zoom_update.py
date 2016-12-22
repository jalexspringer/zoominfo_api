#!/usr/bin/env python

import json

from simple_salesforce import Salesforce
from pprint import pprint

from zoom_call import ZoomInfo
from sfdc import *
from sec import *


def get_zoom_accounts(SF):
    """
    Calls down the total of marked accounts. Queries Zoom to build results lists.
    """
    # Begin run of account queries
    # TODO Add not in already appended to SOQL query.
    query = "SELECT Id, Name, Website FROM Account WHERE Approved_for_Zoominfo_Append__c = True"
    domains, ids = sfdc_object_query(SF, query)

    results = {}
    """
    Remove after testing complete.
    for idx, account in enumerate(domains):
        results[ids[idx]] = zoom.company_search(account)
    """
    # Testing JSON strings grabbed from ZoomInfo Testing Tool
    with open("ticketmaster") as f:
        results["0010L00001k4A86QAE"] = json.loads(f.read())["CompanyDetailRequest"]
    with open("dicks") as f:
        results["0010L00001k4A8GQAU"] = json.loads(f.read())["CompanyDetailRequest"]

    response = "Zoom Requests Made."
    print(response)
    return convert_to_sfdc_fields(results)


def get_zoom_contacts(SF):
    """
    Calls down the total of marked contacts. Queries Zoom to build results lists.
    """
    query = "SELECT Id, Email FROM Contact WHERE Approved_for_Zoominfo_Append__c = True"


def update_sfdc_accounts(results):
    """Update sfdc accounts with acquired ZoomInfo"""

    response = "Accounts successfully updated."
    print(response)


def get_sfdc_fields():
    pprint(SF.Account.get("0010L00001k4A8GQAU"))


if __name__ == "__main__":
    SF = Salesforce(username=SFUN, password=SFPWD, security_token=SFTKN, client_id="Sales_Bot")
    zoom = ZoomInfo(ZPC, ZKEY)
    pprint("Usage for account: {}".format(ZPC))
    pprint(zoom.usage_report)
    accounts_to_update = get_zoom_accounts(SF)
    pprint(accounts_to_update)
    # contacts_to_update = get_zoom_contacts(SF)