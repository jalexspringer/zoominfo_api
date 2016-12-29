#!/usr/bin/env python

import logging
import json
import datetime as dt
from pprint import pprint

def sfdc_object_query(sf, query, update_type="account"):
    """
    Runs specified SOQL query, parses output. Prints a list of accounts to be processed.
    :param query: SOQL query, tailored to pull the list of accounts or contacts that should be run through ZoomInfo
    :param sf: simple_salesforce Salesforce object
    :return: Object Ids and either domains (account level), or emails (contact level)
    """
    objects_to_run = sf.query_all(query)
    fields = []
    ids = []
    return_field = "Website"
    if update_type == "contact":
        return_field = "Email"
    elif update_type == "new_contacts":
        return_field = "Website"
    for record in objects_to_run['records']:
        if record[return_field] is not None:
            ids.append(record['Id'])
            fields.append(record[return_field])
    account_string = ""
    for account in fields:
        account_string += account + "\n"
    response = "Processing account list. Updating the following {}:\n{}".format(update_type, account_string)
    print(response)
    return fields, ids


def convert_to_sfdc_fields(results, update_type="account"):
    """
    Use the dictionary "field_mapping" to convert ZoomInfo responses to corresponding salesforce.com fields.
    Preparation for salesforce.com update.
    :param update_type: defaults to account, can be set to "contact" for contact updates
    :param results: Dictionary of results from ZoomInfo calls
    :return:
    """
    # TODO Fix labels for Industry - make list into string
    new_dict = {"Empty dictionary!"}
    if update_type == "account":
        for k, v in results.items():
            try:
                for key, value in v["CompanyDetailRequest"]["CompanyAddress"].items():
                    results[k][key] = value
                results[k].update(v["CompanyDetailRequest"])
                new_dict = field_map(results, update_type)
            except:
                logging.error(json.dumps(results[k]))
                print("ERROR LOGGED")
    elif update_type == "contact":
        for k, v in results.items():
            try:
                pprint(results)
                results[k]["JobTitle"] = v["PersonDetailRequest"]["CurrentEmployment"]["JobTitle"]
                for key, value in v["PersonDetailRequest"]["CurrentEmployment"]["Company"].items():
                    results[k][key] = value
                for key, value in v["PersonDetailRequest"]["CurrentEmployment"]["Company"]["CompanyAddress"].items():
                    results[k][key] = value
                results[k].update(v["PersonDetailRequest"])
                new_dict = field_map(results, update_type)
            except:
                logging.error(json.dumps(results[k]))
                print("ERROR LOGGED")
    elif update_type == "new_contact_search":
        new_dict = {}
        for k,v in results.items():
            try:
                new_dict[k] = {}
                i = 0
                for value in v['PeopleSearchRequest']["PeopleSearchResults"]["PersonRecord"]:
                    new_dict[k][i] = {}
                    new_dict[k][i]["AccountID"] = k
                    new_dict[k][i]["Title"] = value["CurrentEmployment"]["JobTitle"]
                    new_dict[k][i]["Email"] = value["Email"]
                    new_dict[k][i]["LastName"] = value["LastName"]
                    new_dict[k][i]["FirstName"] = value["FirstName"]
                    try:
                        new_dict[k][i]["Phone"] = value["Phone"]
                    except:
                        new_dict[k][i]["Phone"] = None
                    new_dict[k][i]["Zoom_Individual_ID__c"] = value["PersonID"]
                    new_dict[k][i]["LeadSource"] = "ZoomInfo"
                    new_dict[k][i]['ZoomInfo_Appended__c'] = dt.datetime.now().strftime('%Y-%m-%d')
                    i += 1
            except:
                logging.error(json.dumps(results[k]))
                print("ERROR LOGGED")
    return new_dict


def field_map(results, update_type):
    import field_mapping
    new_dict = {}
    if update_type == "account":
        field__to_map = field_mapping.account_field_mapping
    elif update_type == "contact":
        field__to_map = field_mapping.contact_field_mapping
    for k, v in results.items():
        new_dict[k] = {}
        for key, value in v.items():
            if key in field__to_map:
                if isinstance(value, list):
                    value = ", ".join(value)
                new_dict[k][field__to_map[key]] = value
        new_dict[k]['Approved_for_Zoominfo_Append__c'] = False
        new_dict[k]['ZoomInfo_Appended__c'] = dt.datetime.now().strftime('%Y-%m-%d')
    return new_dict

