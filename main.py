import base64
import calendar
import datetime
import os
import sys
import mysql.connector as sql
import webview
from PIL import Image
import qrcode

print("Loading...")


class Api:


#connect to server
    def Connect(self):
        global db, sqls
        print("Connecting...")
        try:
            sqls = sql.connect(host="localhost", user="root", passwd="2005", database="covid")
            db = sqls.cursor()

            xaxis = []
            ycases = []
            ydeaths = []
            yrecovered = []
            db.execute("select count(*) from Reports where status='-' and historystatus ='+'")
            recovered = db.fetchone()[0]
            db.execute(
                "select count(*) from Reports where status='+'")
            cases = db.fetchone()[0]
            db.execute("select count(*) from Reports where status='d'")
            deaths = db.fetchone()[0]
            db.execute("select count(*) from Reports where vaccinated=1")
            vaccinated = db.fetchone()[0]
            cur = datetime.datetime.now()
            for i in range(1, calendar.monthrange(cur.year, cur.month)[1]):
                if i < 10:
                    j = '0' + str(i)

                else:
                    j = str(i)
                db.execute("select count(*) from Reports where status='+' and statusdate = '{}'".format(
                    str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                ycases.append(list(db.fetchone())[0])
                db.execute(
                    "select count(*) from Reports where status='-' and historystatus ='+' and statusdate = '{}'".format(
                        str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                yrecovered.append(list(db.fetchone())[0])
                db.execute("select count(*) from Reports where status='d' and statusdate = '{}'".format(
                    str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                ydeaths.append(list(db.fetchone())[0])
                xaxis.append(i)

            data = {
                'type': 'dashboard', 'cur': 'connect', 'xaxis': xaxis, 'ycases': ycases, 'yrecovered': yrecovered,
                'ydeaths': ydeaths,
                'recovered': recovered, 'cases': cases, 'deaths': deaths, 'vaccinated': vaccinated}
            return data
        except Exception as e:
            e = str(e)
            print(e)
#Reload when database is updated
    def Rel(self):
        try:
            xaxis = []
            ycases = []
            ydeaths = []
            yrecovered = []
            db.execute("select count(*) from Reports where status='-' and historystatus ='+'")
            recovered = db.fetchone()[0]
            db.execute(
                "select count(*) from Reports where status='+'")
            cases = db.fetchone()[0]
            db.execute("select count(*) from Reports where status='d'")
            deaths = db.fetchone()[0]
            db.execute("select count(*) from Reports where vaccinated=1")
            vaccinated = db.fetchone()[0]
            cur = datetime.datetime.now()
            for i in range(1, calendar.monthrange(cur.year, cur.month)[1]):
                if i < 10:
                    j = '0' + str(i)

                else:
                    j = str(i)
                db.execute("select count(*) from Reports where status='+' and statusdate = '{}'".format(
                    str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                ycases.append(list(db.fetchone())[0])
                db.execute(
                    "select count(*) from Reports where status='-' and historystatus ='+' and statusdate = '{}'".format(
                        str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                yrecovered.append(list(db.fetchone())[0])
                db.execute("select count(*) from Reports where status='d' and statusdate = '{}'".format(
                    str(cur.year) + "/" + cur.strftime("%m") + "/" + j))
                ydeaths.append(list(db.fetchone())[0])
                xaxis.append(i)

            data = {
                'type': 'dashboard', 'cur': 'rel', 'xaxis': xaxis, 'ycases': ycases, 'yrecovered': yrecovered,
                'ydeaths': ydeaths,
                'recovered': recovered, 'cases': cases, 'deaths': deaths, 'vaccinated': vaccinated}
            return data
        except Exception as e:
            print(e)

#Display all user Reports
    def DisplayReports(self):
        try:
            print("Collecting")
            global db, sqls
            db.execute(
                "select emirates_id,name,Age,Status,Vaccinated from Users U , Reports R where U.emirates_id = R.em_id")
            row = db.fetchall()
            html = ''
            for rec in row:
                status = ''
                vaccinated = ''
                colortype = ''
                if rec[3] == '-':
                    status = 'Negative'
                    colortype = 'negative'
                elif rec[3] == '+':
                    status = 'Positive'
                    colortype = 'positive'
                elif rec[3] == 'd':
                    status = 'Deceased'
                    colortype= 'deaths'

                else:
                    status = 'Out Dated'
                    colortype = 'null'

                if rec[4]:
                    vaccinated = 'Yes'

                else:
                    vaccinated = 'No'

                html = html + '''<li id="{}" class="table-row {}" onclick="ShowDetails(this.id)">
                  <div class="col col-1" data-label="Emirates Id">{}</div>
                  <div class="col col-2" data-label="Name">{}</div>
                  <div class="col col-3" data-label="Age">{}</div>
                  <div class="col col-4" data-label="Status">{}</div>
                  <div class="col col-5" data-label="Vaccinated">{}</div>
                </li>'''.format(rec[0], colortype, rec[0], rec[1], rec[2], status, vaccinated)
            data = {
                'html': html, 'type': 'reports', 'cur': None}
            return data

        except Exception as e:
            print(e)

#Display the user report
    def DisplayDetails(self, emid):
        try:
          #user table
            print(emid)
            db.execute("select * from Users where emirates_id = '{}'".format(emid))
            user_table =db.fetchone()
            name = user_table[1]
            #report table
            db.execute("select * from Reports where em_id = '{}'".format(emid))
            reports_obj=db.fetchone()
            reports_data=list(reports_obj)

            #making it understandable by the reader
            status = ''
            emirateid = emid
            colortype = ''
            if reports_data[1] == '-':
                status = 'Negative'
                colortype = 'negative'
            elif reports_data[1] == '+':
                status = 'Positive'
                colortype = 'positive'
            elif reports_data[1] == 'd':
                status = 'Deceased'
                colortype = 'deaths'
            else:
                status = 'Out Dated'
                colortype = 'null'

            #Generate qr code if required or display from table
            if reports_data[7] is None:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(
                    "Name:{}\nEmirates_ID:{}\nAge:{}\nResult:{}\nResult Date:{}".format(name, emid, user_table[2], status, reports_data[2]))
                qr.make(fit=True)
                if reports_data[1] == '-':
                    img = qr.make_image(fill_color=(74, 185, 178), back_color="white")
                elif reports_data[1] == '+':
                    img = qr.make_image(fill_color=(231, 67, 102), back_color="white")

                else:
                    img = qr.make_image(fill_color=(101, 110, 128), back_color="white")

                img.save("temp.png")

                with open("temp.png", "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read())
                    db.execute(
                        'update Reports set qr_code = "{}" where em_id="{}"'.format(b64_string.decode('utf-8'), emid))
                    sqls.commit()

                qrs = b64_string.decode('utf-8')
                os.remove("temp.png")
            else:
                qrs = reports_data[7]

            #Some more user data convertion
            gender=""

            if user_table[3]=='M':
                gender="Male"
            elif user_table[3]=='F':
                gender="Female"
            else:
                gender=user_table[3]

            #setting up html for the below section
            html_below=""
            #latest pcr result
            if reports_data[1] is not None:
                html_below= html_below + '''<div class="reports"><div class="{}" style="display: inline-block;margin-top:10px;width:15px;height:15px;border-radius: 30px;">&nbsp;</div>
            <p style="display: inline-block;padding-left: 5px;">{}</p>
            <p style="color:5e5e5e;padding-left: 25px;">Date: {}</p></div>
                </div>'''.format(colortype, status, str(reports_data[2]))

            #list of last pcr history
            if reports_data[3] is not None:
                history_status=''
                history_color_type=''
                if reports_data[3] == '-':
                    history_status = 'Negative'
                    history_color_type = 'negative'
                elif reports_data[3] == '+':
                    history_status = 'Positive'
                    history_color_type = 'positive'

                elif reports_data[3] == 'd':
                    history_status = 'Deceased'
                    history_color_type= 'deaths'

                html_below=html_below+'''<div class="reports"><div class="{}" style="display: inline-block;margin-top:10px;width:15px;height:15px;border-radius: 30px;">&nbsp;</div>
        <p style="display: inline-block;padding-left: 5px;">{}</p>
        <p style="color:5e5e5e;padding-left: 25px;">Date: {}</p></div>
            </div>'''.format(history_color_type,history_status,str(reports_data[4]))

            #list of other pcr history
            last_history_reports=[]
            last_history_date=[]
            if reports_data[8] is not None:
                last_history_reports=reports_data[8].split(',')
                last_history_date=reports_data[9].split(',')
            for vs in range(len(last_history_reports)):
                if vs!=0:
                    if last_history_reports[vs] is not None:
                        last_history_status=""
                        last_history_color_type=''
                        if last_history_reports[vs] == '-':
                            last_history_status= 'Negative'
                            last_history_color_type= 'negative'
                        elif last_history_reports[vs] == '+':
                            last_history_status= 'Positive'
                            last_history_color_type = 'positive'
                        elif last_history_reports[vs] == 'd':
                            last_history_status = 'Deceased'
                            last_history_color_type= 'deaths'

                        html_below=html_below+'''<div class="reports"><div class="{}" style="display: inline-block;margin-top:10px;width:15px;height:15px;border-radius: 30px;">&nbsp;</div>
            <p style="display: inline-block;padding-left: 5px;">{}</p>
            <p style="color:5e5e5e;padding-left: 25px;">Date: {}</p></div>
                </div>'''.format(last_history_color_type,last_history_status,str(last_history_date[vs]))

            #vaccination details
            reports_vaccinated="No"
            if reports_data[5]:
              reports_vaccinated ="Yes"

            html_below='''<div class="reports">
    <p style="display: inline-block;padding-left: 25px;">Vaccinated: {}</p>
    <p style="color:5e5e5e;padding-left: 25px;">Vaccination: {}</p></div>
        </div>'''.format(reports_vaccinated,reports_data[6])+html_below

        #counting the days since the result date
            since_pcr=''
            if reports_data[2] is not None:
                since_pcr= (datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")-datetime.datetime.strptime(str(reports_data[2]), "%Y-%m-%d")).days
            
            actions='''  <button class="btnz" id="usebtn" onclick="showupuser()" type="button">UPDATE USER DETAILS</button>
        <button class="btnz" id="delbtn" onclick="showdel()" type="button">DELETE USER</button>      <div id="userupdate">
      
        <input id="updid" class="searcher" type="text" value="{}" placeholder="Enter Emirates ID"><br><br>

        <input id="updname" class="searcher" type="text" value="{}"  placeholder="Enter Name"><br><br>

        <input id="updage" class="searcher" type="number" value="{}"  placeholder="Enter Age"><br><br>

        <input id="updgender" class="searcher" type="text" value="{}"  placeholder="Gender"><br><br>
        <button class="btnz" onclick="UpdateUser(this.id)" id='{}' type="button">UPDATE USER DETAILS</button><br>
        <p id="errorumessage"></p><br>
        
        <button class="btnz" onclick="hideupduser()" type="button">CANCEL</button>
      </div>
      <div id="userdelete">
      <h5>Are You Sure To Delete All User Details?
        <button class="btnz" id ="{}" onclick="DeleteUser(this.id)" type="button">Yes</button>
        
        <button class="btnz" onclick="hidedel()" type="button">CANCEL</button>
      </div>'''.format(emid,name,user_table[2],gender,emid,emid)
            if status!= "Deceased":
                actions='''<div id="actions">
                <center>
                {}
        <button class="btnz" id="resbtn" onclick="showupres()" type="button">UPDATE RESULT</button>
        <button class="btnz" id="vacbtn" onclick="showupvac()" type="button">UPDATE VACCINATION</button>
      
        <div id="resultupdate">
        <button onclick="togres()" class="filter-result">Result &nbsp;<i class="fi-rr-angle-small-down"></i></button>
              <div id="result" class="filter-content">
                  <a href="#" onclick="Setresult(this.id)" id="0">Negative</a>
                  <a href="#" onclick="Setresult(this.id)" id="1">Positive</a>
                  <a href="#" onclick="Setresult(this.id)" id="2">Deceased</a>
              </div><br><br>
      <input id="resdate" class="dates" type="date"><br><br>
        <button class="btnz" id ="{}" onclick="UpdateResult(this.id)" type="button">UPDATE RESULT</button>
        
        <button class="btnz" onclick="hideres()" type="button">CANCEL</button>
      </div>
        <div id="vaccinatonupdate">
        <button onclick="togvac()" class="filter-result">Vaccinated &nbsp;<i class="fi-rr-angle-small-down"></i></button>
              <div id="vaccupdate" class="filter-content">
                  <a href="#" onclick="Setvac(this.id)" id="vac">Yes</a>
                  <a href="#" onclick="Setvac(this.id)" id="notvac">No</a>
              </div><br><br>
        <input id="vacdate" class="searcher" placeholder="Vaccination" type="text"><br><br>
        <button class="btnz" id ="{}" onclick="UpdateVac(this.id)" type="button">UPDATE VACCINATION</button>
        
        <button class="btnz" onclick="hidevac()" type="button">CANCEL</button>
      </div>

      </center>
      </div>'''.format(actions,emid,emid)

            html ='''
          <div class="Details-header {}">
          <h2>{}</h2>
          <p>Emirates ID: {}</p>
          <p>Age: {}</p>
          <p>Gender: {}</p>
        </div>
        <div class="Details-body">    <br><br>
        {}
          <h4>{}</h4>
          <h2>Since {} Day/s</h2>
          <img style="border-radius:15px;" width="200px" src="data:image/png;base64,{}">{}
          </div>'''.format(colortype, name, emid,user_table[2],gender, actions,status, since_pcr, qrs,html_below)
            data = {
                'html': html, 'type': 'details-content', 'cur': None}

            return data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)

#filtering
    def filters(self, emid, Name, Age, Status, Vaccinated):
        print("filtering")
        query = ""
        #generating query
        if emid is not None and (Name is not None or Age is not None or Status is not None or Vaccinated is not None):
          #if emid is specified and there r more than 1 queries
            query+= " R.em_id like '" + str(emid) + "%' and "

        elif emid is not None and (Name is None or Age is None or Status is None or Vaccinated is None):
          #if only one query
            query+= " R.em_id like '" + str(emid) + "%'"

        if Name is not None and (Age is not None or Status is not None or Vaccinated is not None):
          #if emid,name and more is specified
            query += " U.name like '" + str(Name) + "%' and "

        elif Name is not None and (Age is None or Status is None or Vaccinated is None):
          #if only name and emid is specified
            query += " U.name like '" + str(Name) + "%'"

        if Age is not None and (Status is not None or Vaccinated is not None):
          #if emid,name,age and more is specified
            query += " U.age=" + str(Age) + " and "


        elif Age is not None and (Status is None or Vaccinated is None):
            #if age is last filer specified
            query += " U.age=" + str(Age)

        if Status is not None and Vaccinated is not None:
          #if status and more  is specified
            query += " R.status='" + str(Status) + "' and "


        elif Status is not None and Vaccinated is None:
          #if status is the last filer specified
            query += " R.status='" + str(Status) + "' "

        if Vaccinated is not None:
          #if vaccinated is specified
            query += " R.vaccinated=" + str(Vaccinated)

        #check if no filter
        if query != '':
            db.execute(
                "select emirates_id,name,Age,Status,Vaccinated from Users U , Reports R where  U.emirates_id = R.em_id and " + query)

        else:
            db.execute(
                "select emirates_id,name,Age,Status,Vaccinated from Users U , Reports R where  U.emirates_id = R.em_id ")
        #refreshing reports on filter
        d = db.fetchall()
        h = ''
        for i in d:
            s = ''
            v = ''
            t = ''
            if i[3] == '-':
                s = 'Negative'
                t = 'negative'
            elif i[3] == '+':
                s = 'Positive'
                t = 'positive'
            elif i[3] == 'd':
                s = 'Deceased'
                t = 'deaths'

            else:
                s = 'Out Dated'
                t = 'null'

            if i[4]:
                v = 'Yes'

            else:
                v = 'No'

            h = h + '''<li id="{}" class="table-row {}" onclick="ShowDetails(this.id)">
              <div class="col col-1" data-label="Emirates Id">{}</div>
              <div class="col col-2" data-label="Name">{}</div>
              <div class="col col-3" data-label="Age">{}</div>
              <div class="col col-4" data-label="Status">{}</div>
              <div class="col col-5" data-label="Vaccinated">{}</div>
            </li>'''.format(i[0], t, i[0], i[1], i[2], s, v)
        data = {
            'html': h, 'type': 'reports', 'cur': None}
        return data

#updating pcr result
    def UpdateData(self, status, date, emid):
        try:
            result = ''
            #getting current pcr status
            db.execute("select status,statusdate,HistoryStatus,HistoryDate,liststatus,listdate from Reports where em_id='{}'".format(emid))
            data = list(db.fetchone())
            HistoryStatus = data[0]
            HistoryDate = data[1]
            #moving current to previous
            previoushistorystatus=''
            previoushistorydate=''
            if data[2] is not None and data[3] is not None:
                previoushistorystatus = data[2]
                previoushistorydate = datetime.datetime.strftime(data[3],"%Y-%m-%d")
            #getting history of pcr
            if data[4] is not None and data[5] is not  None:
                last_history_status = data[4].split(',')
                last_history_date = data[5].split(',')
            else:
                last_history_status=[]
                last_history_date=[]

            #adding previous to history
            last_history_date.append(previoushistorydate)
            last_history_status.append(previoushistorystatus)
            string_history_status=','.join(last_history_status)
            string_history_date=','.join(last_history_date)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            #converting js var to table
            if str(status) == '0':
                result = '-'
            elif str(status) == '1':
                result = '+'
            elif str(status) == '2':
                result = 'd'

            #generating qrcode
            db.execute("select name,age from Users where emirates_id='{}'".format(emid))
            ll = list(db.fetchone())
            qr.add_data("Name:{}\nEmirates_ID:{}\nAge:{}\nResult:{}\nResult Date:{}".format(ll[0], emid, ll[1], result, date))
            qr.make(fit=True)
            if result == '-':

                img = qr.make_image(fill_color=(74, 185, 178), back_color="white")
            elif result == '+':
                img = qr.make_image(fill_color=(231, 67, 102), back_color="white")
            elif result == 'd':
                img = qr.make_image(fill_color=(235, 140, 52), back_color="white")

            else:
                img = qr.make_image(fill_color=(101, 110, 128), back_color="white")

            img.save("temp.png")

            with open("temp.png", "rb") as img_file:
                b64_string = base64.b64encode(img_file.read())
                db.execute('update Reports set qr_code = "{}" where em_id="{}"'.format(b64_string.decode('utf-8'), emid))
                sqls.commit()

            os.remove("temp.png")

            #if there is a previous status and date then update all records
            if HistoryStatus is not None and HistoryDate is not None:
                db.execute(
                    "update Reports set status='{}', statusdate='{}',HistoryStatus='{}',HistoryDate='{}',liststatus='{}',listdate='{}' where em_id='{}'".format(
                        result, date, HistoryStatus, HistoryDate,','.join(last_history_status),','.join(last_history_date), emid))
            else:
                db.execute("update Reports set status='{}', statusdate='{}' where em_id='{}'".format(result, date, emid))
            sqls.commit()

            print("Updated")
            return {'type': 'reload', 'cur': None, 'emi': emid}

        except Exception as e:
            print(e)

#updating Vaccination result
    def UpdateVacData(self, status, date, emid):
        try:
            if status == "vac":
                status="1"

            elif status =="notvac":
                status="0"
            db.execute("update Reports set Vaccinated='{}', Vaccination='{}' where em_id='{}'".format(status, date, emid))
            sqls.commit()

            print("Updated")
            return {'type': 'reload', 'cur': None, 'emi': emid}

        except Exception as e:
            print(e)

#add a new user
    def AddUser(self, e, na, a, g):
        try:
            print("Adding...")
            db.execute("select name from Users where emirates_id = '{}'".format(e))
            if len(list(db.fetchall())) ==0:
                db.execute("insert into Users(emirates_id,name,age,gender) values('{}','{}',{},'{}')".format(e, na, a, g))
                db.execute("insert into Reports(em_id,status) values('{}','n')".format(e))
                sqls.commit()
                return {'type': 'reload', 'cur': None,}
            else:
                print("Already there")
                return {"type":"ea","error":"Emirates ID Already in use"}

        except Exception as e:
            print(e)
            return {"type":"ea","error":"Emirates ID Already in use"}


#updating User Data
    def UpdateUserData(self,e, emid, name, age,gender):
        try: 
            print("Updating...")
            db.execute("select name from Users where emirates_id = '{}'".format(emid))
            if len(list(db.fetchall())) ==0:

                db.execute("update Users set emirates_id='{}',name='{}', age='{}', gender='{}' where emirates_id='{}'".format(emid,name, age, gender.upper(), e))
                db.execute("update Reports set em_id='{}' where em_id='{}'".format(emid,e))
                sqls.commit()

                print("Updated")
                return {'type': 'reload', 'cur': None, 'emi': emid}
            else:
                print("Already there")
                return {"type":"eu","error":"Emirates ID Already in use"}

        except Exception as e:
            print(e)
            return {"type":"eu","error":"Emirates ID Already in use"}



#Deleting User Data
    def DeleteUser(self, emid):
        try:
            db.execute("delete from Users where emirates_id='{}'".format(emid))
            sqls.commit()
            db.execute("delete from Reports where em_id='{}'".format(emid))
            sqls.commit()

            print("Updated")
            return {'type': 'reload', 'cur': 'delete', 'emi': emid}

        except Exception as e:
            print(e)



if __name__ == '__main__':
    api = Api()
    ht = ''
    with open('index.html', 'r') as f:
        ht = str(f.read())
    window = webview.create_window('Computer Project', html=ht, js_api=api)
    webview.start(debug=True)
