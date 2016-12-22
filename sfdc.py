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


def convert_to_sfdc_fields(results):
    """
    Use the dictionary "field_mapping" to convert ZoomInfo responses to corresponding salesforce.com fields.
    Preparation for salesforce.com update.
    :param results: Dictionary of results from ZoomInfo calls
    :return:
    """
    from field_mapping import field_mapping
    for k, v in results.items():
        for key, value in v["CompanyAddress"].items():
            results[k][key] = value
    new_dict = {}
    for k, v in results.items():
        new_dict[k] = {}
        for key, value in v.items():
            if key in field_mapping:
                new_dict[k][field_mapping[key]] = value
    return new_dict