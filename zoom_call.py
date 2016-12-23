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

    def __init__(self, partner_code=None, api_key=None, output_format="JSON"):
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
            elif partner_code != None or api_key != None:
                raise ValueError("Please enter partner_code and api_key parameters to connect to ZoomInfo.")
            else:
                raise ValueError("{} is not a valid format. Please use JSON or XML (default is JSON and required if "
                                 "using the partner sfdc_update package.".format(output_format))
        except ValueError as e:
            print(e.args)

    def company_search(self, search_params, search="detail"):
        """
        :param search: which company endpoint to hit.
        :param search_params: Company domain to be searched.
        :return: API response - JSON formatted by default.
        """
        # TODO Add XML formatting option
        # TODO Add additional endpoint methods
        # TODO Create search options (email, name, etc.) Use dictionary to define this.
        url = self.construct_url(search_params, search, search_type="company")
        r = requests.get(url)
        return r.json()

    def person_search(self, search_params, search="detail"):
        """
        :param search: which person endpoint to hit.
        :param search_params: Person email to be searched.
        :return: API response - JSON formatted by default.
        """
        # TODO Add XML formatting option
        # TODO Add additional endpoint methods
        # TODO Create search options (email, name, etc.) Use dictionary to define this.
        if search == "detail":
            url = self.construct_url(search_params, search, search_type="person")
        elif search == "search":
            url = self.construct_url(search_params, search, search_type="people")
        r = requests.get(url)
        return r.json()

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
        url = "http://partnerapi.zoominfo.com/partnerapi/usage/query?&pc={0}&key={1}" \
              "&outputType={2}&queryTypeOptions=people_search_query,person_detail,person_match," \
              "company_search_query,company_detail,company_match". \
            format(self.partner_code, hashed_key, self.output_format)
        try:
            r = requests.get(url)
            return r.json()
        except:
            logging.error("Failed to get usage information. Check partner code and api key.")

    def create_hash(self, search_params):
        """
        Helper function for url construction.
        Use MD5 encoding and ZoomInfo formatting guidelines to generate the encrypted key.
        See formatting rules here: http://www.zoominfo.com/business/zoominfo-new-api-documentation#2.2
        :param search_params: Each search parameter.
        :return: hashed_key
        """
        now = dt.datetime.now()
        date_string = "{}{}{}".format(now.day, now.month, now.year)
        params_list = search_params.split(",")
        params_string = ""
        for p in params_list:
            params_string += p[:2]
        full_key = str.encode(params_string + self.api_key + date_string)
        key = hl.md5()
        key.update(full_key)
        hashed_key = key.hexdigest()
        return hashed_key

    def construct_url(self, search_params, search, search_type="company"):
        """
        :param search: type of search - match, detail, or search
        :param search_params: Each search parameter.
        :param search_type: see http://www.zoominfo.com/business/zoominfo-new-api-documentation#1.2 for query types.
        :return:
        """
        hashed_key = self.create_hash(search_params)
        if search_type == "company":
            return "http://partnerapi.zoominfo.com/partnerapi/company/{4}?CompanyDomain={0}&pc={1}&key={2}" \
                   "&outputType={3}&outputFieldOptions=companyRevenueNumeric,companyTopLevelIndustry".format(
                    search_params, self.partner_code, hashed_key, self.output_format, search)
        elif search_type == "person":
            return "http://partnerapi.zoominfo.com/partnerapi/person/{4}?name={0}&pc={1}&key={2}&outputType={3}".format(
                search_params, self.partner_code, hashed_key, self.output_format, search)
        elif search_type == "people":
            return "http://partnerapi.zoominfo.com/partnerapi/person/{4}?name={0}&pc={1}&key={2}&outputType={3}".format(
                search_params, self.partner_code, hashed_key, self.output_format, search)
            # TODO Add conditionals for each ZoomInfo endpoint
            # TODO Modify to include the option to use cid instead of domain
