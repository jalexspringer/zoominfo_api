import json
import requests
from simple_salesforce import Salesforce
from pprint import pprint

from zoomCall import *
from sec import *


def get_zoom_accounts(SF):
    """
    Calls down the total of marked accounts and contacts. Queries Zoom to build results lists.
    """

    # Begin run of account queries
    domains, ids = sfdc_account_check(SF)
    account_string = ""
    for account in domains:
        account_string += account + "\n"
    response = "Processing account list. Updating the following accounts:\n{}".format(account_string)
    print(response)

    results = {}
    for idx, account in enumerate(domains):
        query = construct_query(account, ZKEY, ZPC, type="Account")
        print(query)
        # r = requests.get(query)
        # results[ids[idx]] = r.json()
    with open("ticketmaster") as f:
        results["0010L00001k4A86QAE"] = json.loads(f.read())["CompanyDetailRequest"]
    with open("dicks") as f:
        results["0010L00001k4A8GQAU"] = json.loads(f.read())["CompanyDetailRequest"]
    response = "Zoom Account Requests Made."
    print(response)
    results = get_sfdc_ready(results)
    pprint(results)
    return results


def update_sfdc_accounts(results):
    """Update sfdc accounts with acquired ZoomInfo"""

    response = "Accounts successfully updated."
    print(response)


def get_sfdc_fields():
    pprint(SF.Account.get("0010L00001k4A8GQAU"))


    # Begin run of contact queries
    """
    contacts_to_run = sf.query_all("SELECT Id, Name, Email FROM Contact WHERE Approved_for_Zoominfo_Append__c = True")
    contacts, ids = slice_for_zoom(contacts_to_run)
    for idx, contact in enumerate(domains):
        query = construct_contact_query(contact, ZKEY)
        r = requests.get(query)
        results[ids[idx]] = r.json()

    """

if __name__ == "__main__":
    SF = Salesforce(username=SFUN, password=SFPWD, security_token=SFTKN, client_id="Sales_Bot")
    r = requests.get(usage_report_query(ZKEY))
    pprint(r.json())
