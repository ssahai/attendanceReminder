import requests
import getpass
import datetime
from bs4 import BeautifulSoup

# Main function
def main():
    success = False
    while (not success):
        username, password = get_credentials()
        payload     = { 'TR_Username': username,
                      'TR_Password': password}
        authURL     = "https://kendra.cse.iitk.ac.in/kendra/pages/AuthenticateUser.php"
        reportURL   = "https://kendra.cse.iitk.ac.in/kendra/pages/StudentAttendanceReport1.php?Select=&val=i&FMonth=" 
        d           = datetime.date.today()
        s           = requests.Session()
        
        s.post(authURL, data=payload, verify=False)
        r = s.get(reportURL+str(d.month)+'&FYear='+str(d.year))
        success   = login_success(r.text)
        if (success) :
            print "[SUCCESS] Successfully logged in."
        else: 
            print "[ERROR] Incorrect username/password. Please try again.\n"
            continue
        ts = get_attendance_time(r.text, d.day-1)
        if (ts == '-'):
            print "Attendance not marked"
        elif (ts =="Sat" or ts == "Sun"):
            print "Its a holiday : "+ts
        else: 
            print "Attendance marked at " + ts

# Method to get login credentials from user
def get_credentials():
    user = raw_input("Username: ")
    pwd = getpass.getpass()
    return (user, pwd)

# To check if login is successful
def login_success(r):
    soup = BeautifulSoup(r)
    res  = soup.find_all('p')
    if (len(res)==0):
        return True
    else:
        return False

# To extract the attendance record for the day
def get_attendance_time(tab, day):
    soup = BeautifulSoup(tab)
    return soup.find_all('table')[0].findAll('tr')[2].findAll('td')[day].text

if __name__ == "__main__":
    main()
