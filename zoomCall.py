import hashlib as hl
import datetime as dt
from field_mapping import field_mapping


def create_hash(search_params, key):
    now = dt.datetime.now()
    date_string = "{}{}{}".format(now.day, now.month, now.year)
    params_list = search_params.split(",")
    params_string = ""
    for p in params_list:
        params_string += p[:2]
    full_key = str.encode(params_string + key + date_string)
    key = hl.md5()
    key.update(full_key)
    hashed_key = key.hexdigest()
    return hashed_key


def construct_query(search_params, key, partner_code, type):
    hashed_key = create_hash(search_params, key)
    if type == "Account":
        return "http://partnerapi.zoominfo.com/partnerapi/company/detail?CompanyDomain={0}&pc={1}&key={2}&outputType=JSON".format(search_params, partner_code, hashed_key)
    elif type == "Contact":
        return "http://partnerapi.zoominfo.com/partnerapi/company/match?name={0}&pc={1}&key={2}&outputType=JSON".format(search_params, partner_code, hashed_key)


def usage_report_query(key):
    now = dt.datetime.now()
    date_string = "{}{}{}".format(now.day, now.month, now.year)
    full_key = str.encode(key + date_string)
    key = hl.md5()
    key.update(full_key)
    hashed_key = key.hexdigest()
    partner_code = "ImpactRadius.client"
    return "http://partnerapi.zoominfo.com/partnerapi/usage/query?&pc={0}&key={1}&outputType=JSON&queryTypeOptions=people_search_query,person_detail,person_match,company_search_query,company_detail,company_match".format(partner_code, hashed_key)

def sfdc_account_check(sf):
    accounts_to_run = sf.query_all("SELECT Id, Name, Website FROM Account WHERE Approved_for_Zoominfo_Append__c = True")
    domains = []
    ids = []
    for record in accounts_to_run['records']:
        domains.append(record['Website'])
        ids.append(record['Id'])
    return domains, ids


def sfdc_contact_check(sf):
    accounts_to_run = sf.query_all("SELECT Id, Email FROM Contact WHERE Approved_for_Zoominfo_Append__c = True")
    emails = []
    ids = []
    for record in accounts_to_run['records']:
        emails.append(record['Email'])
        ids.append(record['Id'])
    return emails, ids


def get_sfdc_ready(results):
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