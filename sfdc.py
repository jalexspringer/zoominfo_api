#!/usr/bin/env python


def sfdc_object_query(sf, query, type="account"):
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
    if type == "contact":
        return_field = "Email"
    for record in objects_to_run['records']:
        fields.append(record[return_field])
        ids.append(record['Id'])
    account_string = ""
    for account in fields:
        account_string += account + "\n"
    response = "Processing account list. Updating the following {}:\n{}".format(type, account_string)
    print(response)
    return fields, ids


def convert_to_sfdc_fields(results, type="account"):
    """
    Use the dictionary "field_mapping" to convert ZoomInfo responses to corresponding salesforce.com fields.
    Preparation for salesforce.com update.
    :param results: Dictionary of results from ZoomInfo calls
    :return:
    """
    # TODO Fix labels for Industry - make list into string
    from field_mapping import field_mapping
    for k, v in results.items():
        for key, value in v["CompanyAddress"].items():
            results[k][key] = value
    new_dict = {}
    for k, v in results.items():
        new_dict[k] = {}
        for key, value in v.items():
            if key in field_mapping:
                if isinstance(value, list):
                    value = ", ".join(value)
                new_dict[k][field_mapping[key]] = value
        new_dict[k]['Approved_for_Zoominfo_Append__c'] = False
        if type == "account":
            new_dict[k]['Account_Appended__c'] = True
        elif type == "contact_append":
            new_dict[k]['Contacts_Appended__c'] = True

    return new_dict


def convert_revenue(money):
    if money.endswith("Million"):
        money = float(money[1:].split(" ")[0]) * 1000000
    elif money.endswith("Billion"):
        money = float(money[1:].split(" ")[0]) * 1000000000
    else:
        money = 0
    return int(money)