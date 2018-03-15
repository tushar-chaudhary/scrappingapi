import requests
from lxml import etree
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import re
re.compile('<title>(.*)</title>')
from urllib.parse import urlencode
from urllib.request import Request, urlopen




######################################    NCDRC    ##############################################################
####################################### CASE HISTORY##############################################################
#URL:http://cms.nic.in/ncdrcusersWeb/courtroommodule.do?method=loadCaseHistory

def ncdrccasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
        ("method", "caseHistory"),
        ("searchCaseNo", caseno),
        ("stateid", 0),
        ("distid", 0),
        ("prop1", "on"),
        ("prop2", "on"),
        ("prop4", "on"),
        ("prop6", "on"),
        ("prop8", "on"),
        ("prop10", "on"),
        ("prop12", "on"),
        ("prop13", "on"),
        ("prop14", "on"),
        ("prop15", "on"),
        ("prop16", "on"),
        ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    # additional hearing info
    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ',
                                          details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})



def statecommisiondelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 0),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def centraldelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 3),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def eastdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 5),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def newdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
        ("method", "caseHistory"),
        ("searchCaseNo", caseno),
        ("stateid", 8),
        ("distid", 12),
        ("prop1", "on"),
        ("prop2", "on"),
        ("prop4", "on"),
        ("prop6", "on"),
        ("prop8", "on"),
        ("prop10", "on"),
        ("prop12", "on"),
        ("prop13", "on"),
        ("prop14", "on"),
        ("prop15", "on"),
        ("prop16", "on"),
        ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def northcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 9),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def northeastcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 10),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def northwestcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 7),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})



def southdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 6),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def south2casehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
        ("method", "caseHistory"),
        ("searchCaseNo", caseno),
        ("stateid", 8),
        ("distid", 16),
        ("prop1", "on"),
        ("prop2", "on"),
        ("prop4", "on"),
        ("prop6", "on"),
        ("prop8", "on"),
        ("prop10", "on"),
        ("prop12", "on"),
        ("prop13", "on"),
        ("prop14", "on"),
        ("prop15", "on"),
        ("prop16", "on"),
        ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})


def southwestcasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 15),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"": ret_this})


def westdelhicasehistory(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    url = "http://cms.nic.in/ncdrcusersWeb/courtroommodule.do"
    params = [
     ("method",	"caseHistory"),
     ("searchCaseNo",	caseno),
     ("stateid", 8),
     ("distid", 4),
     ("prop1", "on"),
     ("prop2", "on"),
     ("prop4", "on"),
     ("prop6", "on"),
     ("prop8", "on"),
     ("prop10", "on"),
     ("prop12", "on"),
     ("prop13", "on"),
     ("prop14", "on"),
     ("prop15", "on"),
     ("prop16", "on"),
     ("prop18", "on"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[6]
        complainant.append(re.sub(r'[^\x00-\x7F]+', '', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[8]
        respondent.append(re.sub(r'[^\x00-\x7F]+', '', respondent1.strip()))
    except:
        pass

    # filling date
    fillingdate = []
    try:
        fillingdate1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[1]
        fillingdate.append(re.sub(r'[^\x00-\x7F]+', '', fillingdate1.strip()))
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        dateOfnextHearing1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[4]
        dateOfnextHearing.append(re.sub(r'[^\x00-\x7F]+', '', dateOfnextHearing1.strip()))
    except:
        pass

    # Case Stage
    casestage = []
    try:
        casestage1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[2]
        casestage.append(re.sub(r'[^\x00-\x7F]+', '', casestage1.strip()))
    except:
        pass

    # CaseNo
    casenoo = []
    try:
        casenoo1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[0]
        casenoo.append(re.sub(r'[^\x00-\x7F]+', '', casenoo1.strip()))
    except:
        pass

    # CaseCategory
    casecategory = []
    try:
        casecategory1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[3]
        casecategory.append(re.sub(r'[^\x00-\x7F]+', '', casecategory1.strip()))
    except:
        pass

    # ResultOfCase
    resultofcase = []
    try:
        result1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[5]
        resultofcase.append(re.sub(r'[^\x00-\x7F]+', '', result1.strip()))
    except:
        pass

    # Advocate Name
    advocatename = []
    try:
        advocatename1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[7]
        advocatename.append(re.sub(r'[^\x00-\x7F]+', '', advocatename1.strip()))
    except:
        pass

    # Advocate Name2
    advocatename2 = []
    try:
        advocatename3 = tree.xpath('//*[@class="maintextborderdata"]/text()')[9]
        advocatename2.append(re.sub(r'[^\x00-\x7F]+', '', advocatename3.strip()))
    except:
        pass

    # Remarks in Filing
    remarks = []
    try:
        remarks1 = tree.xpath('//*[@class="maintextborderdata"]/text()')[10]
        remarks.append(re.sub(r'[^\x00-\x7F]+', '', remarks1.strip()))
    except:
        pass

    additionaldetails1 = tree.xpath('//tr[@id="cond3"]//td[@class="maintextborderdata"]//text()')
    additionaldetails = []
    index = []
    info = []
    details = []
    hearinginfo = []
    dates = []
    dateofhearingadd = []
    dateofnexthearingadd = []
    try:

        for i in range(0, len(additionaldetails1)):
            if additionaldetails1[i].strip() != "":
                additionaldetails.append(additionaldetails1[i].strip())
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                index.append(i)
        index.append(len(additionaldetails))

        for i in range(0, len(index) - 1):
            for j in range(index[i] + 1, index[i + 1]):
                info.append(additionaldetails[j])
            details.append(' '.join(info))
            info = []
        for i in range(0, len(details)):
            if details[i] != "":
                hearinginfo.append(re.sub(r'[^\x00-\x7F]+', ' ', details[i].replace('\n', '').replace('\r', '').replace('&nbsp', '')))
        # DATES INFO
        for i in range(0, len(additionaldetails)):
            if re.match('(\d{2})[/](\d{2})[/](\d{4})$', additionaldetails[i]):
                dates.append(additionaldetails[i])

        for i in range(0, len(dates)):
            if i % 2 == 0:
                dateofhearingadd.append(dates[i])
            else:
                dateofnexthearingadd.append(dates[i])


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Filing Date'] = fillingdate
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Case No'] = casenoo
        ret_this['Case Category'] = casecategory
        ret_this['Advocate Name'] = advocatename
        ret_this['Advocate Name.'] = advocatename2
        ret_this['Remarks in Filing'] = remarks
        ret_this['Result Of The Case'] = resultofcase
        ret_this['Additional Hearing Info'] = {}
        ret_this['Additional Hearing Info']['Date Of Hearing'] = dateofhearingadd
        ret_this['Additional Hearing Info']['Date Of Next Hearing'] = dateofnexthearingadd
        ret_this['Additional Hearing Info']['Case Proceedings Entered'] = hearinginfo
    except:
        pass

    return ({"Case History": ret_this})

####################################### CASE HISTORY##############################################################


########################################CASE STATUS################################################################

#URL:http://cms.nic.in/ncdrcusersWeb/login.do?method=caseStatus
#case:CC/123/2017
def ncdrccasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "0/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"0"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    #complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except: pass

    #respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except: pass

    #date of hearing
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass


    #Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass


    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except: pass

    #Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except: pass


    #orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings', 'orderflag':	'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except: pass


    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except: pass

    return ({"Case Status": ret_this})


def delhistatecommisioncasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districteastdelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/5/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"5"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtsouthdelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/6/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"6"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtwestdelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/4/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"4"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtcentraldelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/3/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"3"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtnewdelhicasestaus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/12/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"12"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtnortheastdelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/10/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"10"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtnorthwestdelhicasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/7/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"7"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtsouth2casestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/16/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"16"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtsouthwestcasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/15/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"15"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})


def districtnorthcasestatus(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/9/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"9"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # complaint
    complainant = []
    try:
        complainant1 = tree.xpath('//*[@class="rpttxthval"]/text()')[0]
        complainant.append(re.sub(r'[^\x00-\x7F]+', ' ', complainant1.strip()))
    except:
        pass

    # respondent
    respondent = []
    try:
        respondent1 = tree.xpath('//*[@class="rpttxthval"]/text()')[1]
        respondent.append(re.sub(r'[^\x00-\x7F]+', ' ', respondent1.strip()))
    except:
        pass

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # dateOfnextHearing
    dateOfnextHearing = []
    try:
        hearing = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(1, len(hearing), 2):
            if hearing[i] != " ":
                date = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                hearing1 = date.strip()
                if hearing1 != "":
                    dateOfnextHearing.append(hearing1)

    except:
        pass

    # Case Stage
    casestage = []
    try:
        case = tree.xpath('//*[@class="rpttxthval"]/text()')
        for i in range(2, len(case)):
            if case[i] != " ":
                case1 = tree.xpath('//*[@class="rpttxthval"]/text()')[i]
                case2 = case1.strip()
                if case2 != "":
                    casestage.append(case2)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # Proceedings
    proceedings = []
    try:
        for i in range(0, len(datereversed1)):
            url2 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetProceedings"
            payload = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings'}
            r2 = requests.post(url=url2, params=payload)
            a = BeautifulSoup(r2.text, "lxml").text
            proceedings.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ')))


    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['complainant'] = complainant
        ret_this['respondent'] = respondent
        ret_this['Date Of Hearing'] = dateOfHearing
        ret_this['Date Of Next Hearing'] = dateOfnextHearing
        ret_this['Case Stage'] = casestage
        ret_this['Court Proceedings'] = proceedings
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Status": ret_this})

###############################################CASE STATUS############################################################

###############################################CASE JUDGMENT##########################################################


#URL:http://cms.nic.in/ncdrcusersWeb/search.do?method=loadSearchPub
def ncdrcjudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "0/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"0"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    #date of hearing used to pass the value to the judgment url(usually for last date of hearing)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin': caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def delhistatecommisionjudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districteastdelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/5/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"5"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin': caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtsouthdelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/6/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"6"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtwestdelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/4/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"4"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})



def districtcentraldelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/3/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"3"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    #lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    #Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass


    return ({"Case Judgment": ret_this})



def districtnortheastdelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/10/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"10"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ',a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtnorthwestdelhijudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/7/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"7"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtsouth2judgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/16/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"16"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtsouthwestjudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/15/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"15"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


def districtnorthjudgment(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/9/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"8"),
     ("distCode",	"9"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass
    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)
    except:
        pass
    # lastdate for judgments
    lastdate=[]
    try:
        lastdate = datereversed1[len(datereversed1) - 1]
    except:
        pass
    # Judgements
    judgment = []
    try:
        url2 = "http://cms.nic.in/ncdrcusersWeb/GetJudgement.do"
        payload = {'method': 'GetJudgement', 'dtofhearing': lastdate, 'caseidin':caseidin}
        r2 = requests.post(url=url2, params=payload)
        a = BeautifulSoup(r2.text, "lxml").text
        judgment.append(re.sub(r'[^\x00-\x7F]+', ' ', a.replace('\n', ' ').replace('\r', ' ').replace('&nbsp', ' ')))
    except:
        pass
    ret_this = {}
    try:
        ret_this['Final Judgment'] = judgment
    except:
        pass

    return ({"Case Judgment": ret_this})


################################################Case Judgment#######################################################

##################################################Case Order#######################################################

def ncdrcorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "0/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
     ("method",	"ViewProceedingCS"),
     ("fano",	caseno),
     ("case_id_in", ""),
     ("dtOfHearing", ""),
     ("courtId",	""),
     ("cid",	caseidin),
     ("stateCode",	"0"),
     ("distCode",	"0"),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    #Date Of hearing
    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    #datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except: pass

    #orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings', 'orderflag':	'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ',a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except: pass


    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except: pass

    return ({"Case Order": ret_this})


def statecommisionorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/0/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "0"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def eastdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/5/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "5"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def southdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/6/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "6"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def westdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/4/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "4"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def centraldelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/3/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "3"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def newdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/12/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "12"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))

    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def northeastdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/10/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "10"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def northwestdelhiorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/7/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "7"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})


def south2order(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/16/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "16"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})



def southwestorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/15/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "15"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})



def northorder(casetype, caseno, caseyear):
    caseno = str(casetype) + '/' + str(caseno) + '/' + str(caseyear)
    caseidin = "8/9/{}".format(caseno)
    url = "http://cms.nic.in/ncdrcusersWeb/ViewProceedingCS.jsp"
    params = [
        ("method", "ViewProceedingCS"),
        ("fano", caseno),
        ("case_id_in", ""),
        ("dtOfHearing", ""),
        ("courtId", ""),
        ("cid", caseidin),
        ("stateCode", "8"),
        ("distCode", "9"),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    dateOfHearing = []
    try:
        hearing2 = tree.xpath('//*[@class="rptnumhval"]/text()')
        for i in range(0, len(hearing2), 2):
            if hearing2[i] != " ":
                date1 = tree.xpath('//*[@class="rptnumhval"]/text()')[i]
                ofhearing = date1.strip()
                if ofhearing != "":
                    dateOfHearing.append(ofhearing)
    except:
        pass

    # datereverse
    datereversed1 = []
    try:
        for i in range(0, len(dateOfHearing)):
            datereversed = datetime.strptime(dateOfHearing[i], '%d/%m/%Y').strftime('%Y-%m-%d')
            datereversed1.append(datereversed)

    except:
        pass

    # orders
    orders = []
    try:
        for i in range(0, len(datereversed1)):
            url3 = "http://cms.nic.in/ncdrcusersWeb/servlet/confonet.courtroom.GetDailyOrder"
            payload1 = {'case_id_in': caseidin, 'dtofhearing': datereversed1[i], 'method': 'GetProceedings',
                        'orderflag': 'D'}
            r3 = requests.post(url=url3, params=payload1)
            a1 = BeautifulSoup(r3.text, "lxml").text
            orders.append(re.sub(r'[^\x00-\x7F]+', ' ', a1.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('&nbsp', ' ').replace('Daily Order', '')))


    except:
        pass

    ret_this = {}
    try:
        ret_this['Orders'] = orders
    except:
        pass

    return ({"Case Order": ret_this})



######################################################Case Order####################################################



###############################################  CGATNEW     #########################################################


def cgatnewcasestatus(casetype, caseno, caseyear):
    if casetype == "Cr.CP":
        number="7"
    elif casetype == "C.P.":
        number="4"
    elif casetype == "M.A.":
        number="3"
    elif casetype == "O.A.":
        number="1"
    elif casetype == "P.T.":
        number="5"
    elif casetype == "R.A.":
        number="6"
    else: number="2"

    url = "http://cgatnew.gov.in/catweb/Delhi/services/case_detail_report.php"
    params = [
     ("frmAction",	"add"),
     ("case_number",	""),
     ("filing_no", "11072000000"),
     ("filing_no", "11072000000"),
     ("app_type", "cno"),
     ("case_type",	number),
     ("case_no",	caseno),
     ("case_year",	caseyear),
     ("pet_name",	""),
     ("res_name", ""),
    ]
    r = requests.post(url=url, params = params)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(r.text), parser)

    # Applicant Name
    applicantname=[]
    try:
        applicantname1 = tree.xpath('//*[@class="textbox"]/@value')[2]
        applicantname.append(re.sub(r'[^\x00-\x7F]+', ' ',applicantname1.replace(' ', '+')))

    except:
        pass

    # Respondent Name
    respondentname = []
    try:
        respondentname1 = tree.xpath('//*[@class="textbox"]/@value')[3]
        respondentname.append(re.sub(r'[^\x00-\x7F]+', ' ',respondentname1.replace(' ', '+')))
    except:
        pass

    # filling Number
    fillingnumber = []
    try:
        hiddenvalues = tree.xpath('//*[@type="hidden"]/@value')
        for i in range(len(hiddenvalues)-2, len(hiddenvalues)):
            fillingnumber.append(re.sub(r'[^\x00-\x7F]+', ' ',hiddenvalues[i]))
    except:
        pass

    #submitting the above values as parameter to other page
    dairynumber = []
    locationnamelocationcode = []
    casenumber = []
    dateoffiling = []
    casestatus = []
    referencecasenumber = []
    subject = []
    listingdate1=[]
    bench=[]
    court=[]
    proccedingdate=[]
    dateofdisposal=[]
    court1=[]
    bench1=[]
    lastactionincourt=[]
    applicant=[]
    applicantadvocate=[]
    respondent =[]
    respondentadvocate=[]
    try:
        url2 = "http://cgatnew.gov.in/catweb/Delhi/services/case_detail_report_action2.php"
        params2 = [
            ("frmAction", "add"),
            ("case_number", ""),
            ("filing_no", fillingnumber[0]),
            ("filing_no", fillingnumber[1]),
            ("app_type", "cno"),
            ("case_type", number),
            ("case_no", caseno),
            ("case_year", caseyear),
            ("pet_name", applicantname),
            ("res_name", respondentname),
        ]
        r1 = requests.post(url=url2, params=params2)
        parser1 = etree.HTMLParser()
        tree1 = etree.parse(StringIO(r1.text), parser1)
        ##################################CASE DETAIL################################################################
        try:
            #DAIRY NUMBER
            details1=tree1.xpath('//table[1]/tr[3]/td[2]/font/text()')
            dairynumber.append(details1[0].strip())

            #LOCATION NAME / LOCATION CODE
            details2 =tree1.xpath('//table[1]/tr[4]/td[2]/font/text()')
            locationnamelocationcode.append(details2[0].strip())

            #CASE NUMBER
            details3 =tree1.xpath('//table[1]/tr[5]/td[2]/font/text()')
            casenumber.append(details3[0].strip())

            #DATE OF FILING.
            details4 =tree1.xpath('//table[1]/tr[6]/td[2]/font/text()')
            dateoffiling.append(details4[0].strip())

            #CASE STATUS
            details5 = tree1.xpath('//table[1]/tr[7]/td[2]/font/text()')
            casestatus.append(details5[0].strip())

            #REFERENCE CASE NUMBER
            details6 = tree1.xpath('//table[1]/tr[8]/td[2]/font/text()')
            referencecasenumber.append( details6[0].strip())

            #SUBJECT
            details7 = tree1.xpath('//table[1]/tr[9]/td[2]/font/text()')
            subject.append(details7[0].strip())
        except:
            pass

        try:
            ##################################################CASE LISTING DETAILS##########################################
            # LISTING DATE
            listingdate1 = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[1]/td[2]/font/text()')

            # BENCH
            bench = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[2]/td[2]/font/text()')

            # COURT
            court = tree1.xpath('//table[2]/tr[2]/td[1]/table/tr[3]/td[2]/font/text()')
        except:
            pass


        try:
            ###############################################CASE PROCEEDINGS DETAILS#####################################
            # PROCEEDING DATE
            proccedingdate = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[1]/td[2]/font/text()')

            # DATE OF DISPOSAL
            dateofdisposal = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[2]/td[2]/font/text()')

            # COURT
            court1 = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[3]/td[2]/font/text()')

            # BENCH
            bench1 = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[4]/td[2]/font/text()')

            # LAST ACTION IN COUURT
            lastactionincourt = tree1.xpath('//table[2]/tr[2]/td[2]/table/tr[5]/td[2]/font/text()')

        except:
            pass

        try:
            ##############################################APPLICANT AND APPLICANT ADVOCATES#############################
            #APPLICANT
            applicant = tree1.xpath('//table[3]/tr[2]/td[2]/font/text()')

            # APPLICANT ADVOCATE
            applicantadvocate = tree1.xpath('//table[3]/td[2]/font/text()')

        except:
            pass

        try:
            #############################################RESPONDENT AND RESPONDENT ADVOCATES############################
            #RESPONDENT NAME
            respondent = tree1.xpath('//table[3]/tr[4]/td[2]/font/text()')

            #RESPONDENT ADVOCATE
            respondentadvocate = tree1.xpath('//table[3]/td[4]/font/text()')
        except:
            pass

    except:
        pass

    ret_this = {}
    try:
        ret_this['Case Details'] = {}
        ret_this['CASE LISTING DETAILS'] = {}
        ret_this['CASE PROCEEDING DETAILS'] = {}
        ret_this['APPLICANT AND APPLICANT ADVOCATES'] = {}
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']={}
        ret_this['Case Details']['Dairy Number'] = dairynumber
        ret_this['Case Details']['LOCATION NAME / LOCATION CODE'] = locationnamelocationcode
        ret_this['Case Details']['CASE NUMBER'] = casenumber
        ret_this['Case Details']['DATE OF FILING.'] = dateoffiling
        ret_this['Case Details']['CASE STATUS'] = casestatus
        ret_this['Case Details']['REFERENCE CASE NUMBER'] = referencecasenumber
        ret_this['Case Details']['SUBJECT'] = subject
        ret_this['CASE LISTING DETAILS']['LISTING DATES'] = listingdate1
        ret_this['CASE LISTING DETAILS']['BENCH'] = bench
        ret_this['CASE LISTING DETAILS']['COURT'] = court
        ret_this['CASE PROCEEDING DETAILS']['PROCEEDING DATE']= proccedingdate
        ret_this['CASE PROCEEDING DETAILS']['NEXT LISTING DATE / DATE OF DISPOSAL'] = dateofdisposal
        ret_this['CASE PROCEEDING DETAILS']['COURT'] = court1
        ret_this['CASE PROCEEDING DETAILS']['BENCH'] = bench1
        ret_this['CASE PROCEEDING DETAILS']['LAST ACTION IN COURT'] = lastactionincourt
        ret_this['APPLICANT AND APPLICANT ADVOCATES']['APPLICANT'] = applicant
        ret_this['APPLICANT AND APPLICANT ADVOCATES']['APPLICANT ADVOCATE'] = applicantadvocate
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']['RESPONDENT NAME'] = respondent
        ret_this['RESPONDENT AND RESPONDENT ADVOCATES']['RESPONDENT ADVOCATE'] = respondentadvocate

    except: pass

    return ({"Case Status": ret_this})


def cgatneworders(casetype, caseno, caseyear):
    if casetype == "Cr.CP":
        number = "7"
    elif casetype == "C.P.":
        number = "4"
    elif casetype == "M.A.":
        number = "3"
    elif casetype == "O.A.":
        number = "1"
    elif casetype == "P.T.":
        number = "5"
    elif casetype == "R.A.":
        number = "6"
    else:
        number = "2"
    url = "http://cgatnew.gov.in/catweb/Delhi/services/upload_order_detail.php"
    params = [
        ("search_type", "1"),
        ("judge_detail", "0"),
        ("from_date", ""),
        ("to_date", ""),
        ("from_date1", ""),
        ("to_date1", ""),
        ("case_type", number),
        ("case_no", caseno),
        ("case_year", caseyear),
        ("txtState", ""),
        ("filing_no", ""),
    ]
    r = requests.post(url=url, params=params)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(r.text), parser)

    ###########################################Party Detail#############################################
    # ApplicantVSRespondent
    applicantvsrespondent = []
    try:
        applicantvsrespondent1 = tree.xpath('//table[6]/tr[2]/td/font/text()')
        applicantvsrespondent.append(applicantvsrespondent1[0].strip())
    except:
        pass

    # SerialNumber
    srno = []
    srno1 = tree.xpath('//*[@class="hoverTable"]/tr/td/text()')
    for i in range(0, len(srno1)):
        if srno1[i].strip().isdigit() == True:
            srno.append(srno1[i].strip())

    # CaseNumber
    caseno = []
    for i in range(4, len(srno) + 4):
        caseno1 = tree.xpath("//table[6]/tr[{}]/td[2]/text()".format(i))
        caseno.append(caseno1[0].strip())

    # Part Detail
    partydetail = []
    join = []
    for i in range(4, len(srno) + 4):
        partydetail1 = tree.xpath("//table[6]/tr[{}]/td[3]/text()".format(i))
        join.append(''.join(partydetail1))
        partydetail.append(join[0].strip())
        join = []

    # Member Name
    membername = []
    join1 = []
    for i in range(4, len(srno) + 4):
        membername1 = tree.xpath("//table[6]/tr[{}]/td[4]/text()".format(i))
        join1.append(''.join(membername1))
        membername.append(join1[0].strip())
        join1 = []

    # Date Of Order
    dateoforder = []
    join2 = []
    for i in range(4, len(srno) + 4):
        dateoforder1 = tree.xpath("//table[6]/tr[{}]/td[5]/text()".format(i))
        join2.append(''.join(dateoforder1))
        dateoforder.append(join2[0].strip())
        join2 = []

    # Remarks
    remarks = []
    join3 = []
    for i in range(4, len(srno) + 4):
        remarks1 = tree.xpath("//table[6]/tr[{}]/td[6]/text()".format(i))
        join3.append(''.join(remarks1))
        remarks.append(join3[0].strip())
        join3 = []

    # Orders
    join4 = []
    orders_link = []
    for i in range(4, len(srno) + 4):
        orders1 = tree.xpath("//table[6]/tr[{}]/td[7]/a/@href".format(i))
        join4.append(''.join(orders1))
        orders_link.append("http://cgatnew.gov.in/catweb/Delhi/services/" + join4[0])
        join4 = []

    ret_this = {}
    try:
        ret_this['ApplicantVSRespondent'] = applicantvsrespondent
        ret_this['Sr No'] = srno
        ret_this['PARTY DETAIL'] = partydetail
        ret_this[' Member Name'] = membername
        ret_this['Date of Order'] = dateoforder
        ret_this['Remarks'] = remarks
        ret_this['Orders File'] = orders_link
    except:
        pass

    return ({"Case Order": ret_this})


def cgatnewjudgments(bench, casetype, caseno, caseyear):

    #value for casetype
    casetypecode = {}
    casetypecode['OA Orignal Appl.'] = 1
    casetypecode['TA Transfer Appl.'] = 2
    casetypecode['MA Misc. Appl.'] = 3
    casetypecode['CP Contempt Appl.'] = 4
    casetypecode['PT Transfer Petition'] = 5
    casetypecode['RA Review appl.'] = 6
    casetypecode['EA Execution petition'] = 7

    #value for bench
    benchcode = {}
    benchcode['Principal Bench, New Delhi'] = 1
    benchcode['Ahmedabad Bench'] = 2
    benchcode['Allahabad Bench'] = 3
    benchcode['Bangalore Bench'] = 4
    benchcode['Bombay Bench'] = 5
    benchcode['Calcutta Bench'] = 6
    benchcode['Chandigarh Bench'] = 7
    benchcode['Chennai Bench'] = 8
    benchcode['Cuttack Bench'] = 9
    benchcode['Ernakulam Bench'] = 10
    benchcode['Guwahati Bench'] = 11
    benchcode['Hyderabad Bench'] = 12
    benchcode['Jabalpur Bench'] = 13
    benchcode['Jaipur Bench'] = 14
    benchcode['Jodhpur Bench'] = 15
    benchcode['Lucknow Bench'] = 16


    url = "http://judis.nic.in/CAT/list_new.asp"
    params = [
     ("action",	"validate_login"),
     ("Bench_Code",	benchcode[bench]),
     ("CaseType", casetypecode[casetype]),
     ("CaseNo", caseno),
     ("CaseYr",	caseyear),
    ]
    r = Request(url, urlencode(params).encode())
    htmltext = urlopen(r).read().decode()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(htmltext), parser)

    #Bench
    benchtext = []
    benchtext1 = tree.xpath('//table[2]/tr/td[1]/text()')
    benchtext.append(re.sub(r'[^\x00-\x7F]+', ' ', benchtext1[0].replace('Bench :', '').strip()))

    #CaseNo. Info
    caseinfo = []
    caseinfo1 = tree.xpath('//table[2]/tr/td[2]/text()')
    caseinfo.append(re.sub(r'[^\x00-\x7F]+', ' ', caseinfo1[0].strip()))

    #Dated
    dated = []
    dated1 = tree.xpath('//table[2]/tr/td[4]/text()')
    dated.append(re.sub(r'[^\x00-\x7F]+', ' ', dated1[0].strip()))

    #Click Here Link
    link = []
    link1 = tree.xpath('//table[2]/tr/td[5]/a/@href')
    link.append("http://judis.nic.in/CAT/" + link1[0])

    ret_this = {}
    try:
        ret_this['Bench'] = bench
        ret_this['Dated'] = dated
        ret_this['Case Info'] = caseinfo
        ret_this['Click Here'] = link
    except:
        pass

    return ({"Case Judgment": ret_this})