"""
    Code is poetry

    Created by Nick aka black.dragon74
"""
from bs4 import BeautifulSoup


# Funtion to select an id
def selectid(elem_id):
    return {'id': elem_id}


# Used to extract value attribute from the HTML DOM
def getValueFromInput(dom_elem, elem_id):
    retVal = None
    try:
        retVal = dom_elem.find('input', selectid(elem_id))["value"]
    except AttributeError:
        retVal = None
    finally:
        return retVal


# Returns a simple error msg in JSON
def throwError(msg):
    return {'error': msg}


# Function to parse a HTML table and get the values
def parseHTMLTable(dom_elem, table_id, hasThead=True, hasTbody=False, hasTFoot=True):
    table = dom_elem.find('table', selectid(table_id))
    mTableRows = table.find('tbody').find_all('tr') if hasTbody else table.find_all('tr')

    retVal = []

    for row in mTableRows:
        mTableData = row.findAll('td')
        data = [d.text.strip() for d in mTableData]
        retVal.append(data)

    # Now if has thead but not tbody remove first indice
    if hasThead and not hasTbody:
        retVal.pop(0)

    # Now id has tfooot but not tbody remove the last indice
    if hasTFoot and not hasTbody:
        retVal.pop(len(retVal)-1)

    return retVal
