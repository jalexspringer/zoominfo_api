from collections import OrderedDict

person_search_dictionary = OrderedDict([
    ('firstName', None),
    ('middleInitial', None),
    ('lastName', None),
    ('personTitle', None),
    ('TitleSeniority', None),
    ('TitleClassification', None),
    ('companyId', None),
    ('IndustryClassification', None),
    ('IndustryKeywords', None),
    ('State', None),
    ('MetroRegion', None),
    ('Country', None),
    ('ZipCode', None),
    ('RadiusMiles', None),
    ('location', None),
    ('locationSearchType', None),
    ('RevenueClassificationMin', None),
    ('RevenueClassificationMax', None),
    ('RevenueClassification', None),
    ('EmployeeSizeClassificationMin', None),
    ('EmployeeSizeClassificationMax', None),
    ('EmployeeSizeClassification', None),
    ('IsPublic', None),
    ('CompanyRanking', None),
    ('school', None),
    ('degree', None),
    ('gender', None),
    ('companyDomainName', None),
    ('titleCertification', None),
    ('companyPastOrPresent', None),
    ('ValidDateMonthDist', None),
    ('ContactRequirements', None),
    ('EmailAddress', None)
])


person_detail_dictionary = OrderedDict([
    ('PersonID', None),
    ('EmailAddress', None),
])


person_match_dictionary = OrderedDict([
    ('outputFieldOptions', None),
    ('personID', None),
    ('fullName', None),
    ('firstName', None),
    ('lastName', None),
    ('emailAddress', None),
    ('companyId', None),
    ('companyName', None),
    ('jobTitle', None),
    ('phone', None),
    ('state', None),
    ('zipcode', None),
    ('country', None)
])


company_search_dictionary = OrderedDict([
    ('companyName', None) ,
    ('companyDesc', None) ,
    ('IndustryClassification', None) ,
    ('IndustryKeywords', None) ,
    ('State', None) ,
    ('MetroRegion', None) ,
    ('Country', None) ,
    ('ZipCode', None) ,
    ('RadiusMiles', None) ,
    ('location', None) ,
    ('RevenueClassificationMin', None) ,
    ('RevenueClassificationMax', None) ,
    ('EmployeeSizeClassificationMin', None) ,
    ('EmployeeSizeClassificationMax', None) ,
    ('IsPublic', None) ,
    ('CompanyRanking', None)
])



company_detail_dictionary = OrderedDict([
    ('CompanyID', None) ,
    ('CompanyDomain', None) ,
])


company_match_dictionary = OrderedDict([
    ('companyID', None),
    ('name', None),
    ('domain', None),
    ('ticker', None),

])
