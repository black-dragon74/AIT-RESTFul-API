"""
    Code is poetry
"""
from flask_restful import (
    Resource,
    reqparse,
)
import requests
from utils.functions import *
from utils.constants import *
from bs4 import BeautifulSoup


# Default home route, also serves as a 404 route
class Home(Resource):
    def get(self):
        return {
            "msg": "Welcome to AIT ERP REST API",
            "error": "No/Invalid route requested. Please refer to the documentation."
        }


# Get student's attendance
class Attendance(Resource):
    def get(self):
        # Init the request parses
        parser = reqparse.RequestParser()
        parser.add_argument('sessionid', help="SessionID is missing", required=True)

        # Get the args
        args = parser.parse_args()

        sessionID = args["sessionid"]

        if not sessionID:
            return throwError("Session id not found!")

        # Else, we move forward and get the required data
        with requests.session() as attendanceSession:

            erp_cookies = {
                "ASP.NET_SessionId": sessionID
            }

            headers = {
                "User-Agent": API_USER_AGENT,
                "Connection": "keep-alive",
                "DNT": "1",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cache-Control": "no-cache",
                "Sec-Fetch-Dest": "empty",
                "X-Requested-With": "XMLHttpRequest",
                "X-MicrosoftAjax": "Delta=true",
                "Accept": "*/*",
                "Origin": "https://erp.aitpune.edu.in",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Referer": "https://erp.aitpune.edu.in/Secured/StudentSection/StudentProfileComplete.aspx",
                "Accept-Language": "en-US,en;q=0.9"
            }

            aitget = attendanceSession.get(DASH_URL, headers=headers, cookies=erp_cookies).content

            if not aitget:
                return throwError("Unable to fetch details from the server")

            aitsoup = BeautifulSoup(aitget, 'html.parser')

            # Create the payload
            formdata = {
                "__EVENTTARGET": "ctl00$ContentPlaceHolderBody$lnkRefreshAttendance",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": getValueFromInput(aitsoup, ID_FOR_VIEWSTATE),
                "__VIEWSTATEGENERATOR": "9BC554CB",
                "__EVENTVALIDATION": getValueFromInput(aitsoup, ID_FOR_EVALIDATION),
                "ctl00$ContentPlaceHolderBody$txtFromDateAttendance": getValueFromInput(aitsoup, ID_FOR_ATTEN_FROM),
                "ctl00$ContentPlaceHolderBody$txtToDateAttendance": getValueFromInput(aitsoup, ID_FOR_ATTEN_TO),
                "ctl00$ContentPlaceHolderBody$hdClassID": getValueFromInput(aitsoup, ID_FOR_CLASS_ID),
                "ctl00$ContentPlaceHolderBody$hdStudentEntrollID": getValueFromInput(aitsoup, ID_FOR_ENROLL_ID),
                "__ASYNCPOST": "true"
            }

            # Post and get the attendance
            attendancePost = attendanceSession.post(DASH_URL, headers=headers, cookies=erp_cookies, data=formdata).content

            if not attendancePost:
                return throwError("Unable to get attendance from the server")

            attendanceSoup = BeautifulSoup(attendancePost, 'html.parser')

            attendance = parseHTMLTable(attendanceSoup, ID_FOR_ATTEN_TABLE)

            attendanceSession.close()

            # Now is the time to create a dict to return
            masterDict = {
                "percent": "0",
                "attendance": []
            }

            for row in attendance:
                subjectDict = dict()
                index = 0

                for item in row:
                    key = str(ATTEN_TABLE_STRUCT[index])
                    subjectDict[key] = item
                    index += 1

                masterDict["attendance"].append(subjectDict)

            masterDict["percent"] = attendanceSoup.find('span', selectid(ID_FOR_TOTAL_ATTEN_PERCENT)).text
            return masterDict
