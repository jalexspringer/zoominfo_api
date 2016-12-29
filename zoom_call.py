#!/usr/bin/env python

"""A python wrapper for the ZoomInfo Partner API"""

import datetime as dt
import hashlib as hl
import logging

import requests


class ZoomInfo(object):
    """
    Returns search result of companies or contacts based on input criteria.
    Available search inputs and returned output is restricted by access rights for public accounts.

    See: http://www.zoominfo.com/business/zoominfo-new-api-documentation
    """

    def __init__(self, partner_code=None, api_key=None, output_format="JSON",
                 sortBy=None, sortOrder=None, rpp=None, page=None):
        """
        Create ZoomInfo object with security keys.
        :type output_format: String
        :param partner_code: ZoomInfo Partner Code
        :param api_key: ZoomInfo API Key
        :param output_format: Defaults to JSON - alternate option is XML. Raise error if anything else.
        """
        try:
            if output_format in ["JSON", "XML"] and partner_code != None and api_key != None:
                self.output_format = output_format
                self.partner_code = partner_code
                self.api_key = api_key
                self.sortBy = sortBy
                self.sortOrder = sortOrder
                self.rpp = rpp
                self.page = page
                self.picky = False
                for value in ["rpp", "page", "sortBy", "sortOrder"]:
                    if value is not None:
                        self.picky = True
            elif partner_code is not None or api_key is not None:
                raise ValueError(
                    "Please enter partner_code and api_key parameters to connect to ZoomInfo.")
            else:
                raise ValueError("{} is not a valid format. Please use JSON or XML (default is JSON and required if "
                                 "using the partner sfdc_update package.".format(output_format))
        except ValueError as e:
            print(e.args)


    @property
    def usage_report(self):
        """
        Calls the full usage report for the organization.
        :return: JSON formatted
        """
        now = dt.datetime.now()
        date_string = "{}{}{}".format(now.day, now.month, now.year)
        full_key = str.encode(self.api_key + date_string)
        key = hl.md5()
        key.update(full_key)
        hashed_key = key.hexdigest()
        url = f"http://partnerapi.zoominfo.com/partnerapi/usage/query?&pc={self.partner_code}&key={hashed_key}" \
              f"&outputType={self.output_format}&queryTypeOptions=people_search_query,person_detail,person_match," \
              "company_search_query,company_detail,company_match"
        try:
            r = requests.get(url)
            return r.json()
        except:
            logging.error(
                "Failed to get usage information. Check partner code and api key.")


    def query(self, entity, query_type, payload, outputFieldOptions=None):
        url = f"http://partnerapi.zoominfo.com/partnerapi/{entity}/{query_type}"
        payload["key"] = self.create_hash(payload)
        if self.picky:
            payload["sortBy"] = self.sortBy
            payload["sortOrder"] = self.sortOrder
            payload["rpp"] = self.rpp
            payload["page"] = self.page
        if outputFieldOptions is not None:
            payload["outputFieldOptions"] = ",".join(outputFieldOptions)
        payload["pc"] = self.partner_code
        payload["outputType"] = self.output_format
        #r = requests.get(url, params = payload)
        r = requests.get("http://partnerapi.zoominfo.com/partnerapi/person/search?pc=SF_ImpactRadius&key=9a2510146a4824cfca5c52f1d7da8614&titleSeniority=C_EXECUTIVES,VP_EXECUTIVES,DIRECTOR,MANAGER&titleClassification=786434,2555906,3932162,3932163,3276802&companyName=radio%20shack&industryClassification=5386,5898,5642,4106,1290&companyPastOrPresent=Current&contactRequirements=4&outputType=JSON&RPP=5")
        return r.json()


    def create_hash(self, payload):
        """
        Helper function for url construction.
        Use MD5 encoding and ZoomInfo formatting guidelines to generate the encrypted key.
        See formatting rules here: http://www.zoominfo.com/business/zoominfo-new-api-documentation#2.2
        :param search_params: Each search parameter.
        :return: hashed_key
        """
        now = dt.datetime.now()
        date_string = "{}{}{}".format(now.day, now.month, now.year)
        params_string = ""
        for k,v  in payload.items():
            if v is not None:
                params_string += v[:2]
        full_key = str.encode(params_string + self.api_key + date_string)
        key = hl.md5()
        key.update(full_key)
        hashed_key = key.hexdigest()
        return hashed_key
