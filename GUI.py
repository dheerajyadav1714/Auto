import tkinter as tk
from tkinter import *
import requests
from requests.auth import HTTPBasicAuth
import os
from PIL import Image,ImageTk

var=os.system('set HTTP_PROXY=http://A200164805:Welcome@1234@10.24.19.83:8080')
print(var)
os.system('set HTTPS_PROXY=http://A200164805:Welcome@1234@10.24.19.83:8080')

window1 = tk.Tk()
logo = PhotoImage(file = "logo2.PNG")
window1.iconphoto(True,logo)

window1.title('SAP Password Self-Service')
window1.geometry("1200x1000")
#window1['background']='#856ff8'


# SOAP request URL
urlS4P670 = "http://tps0203-s4project.demosystems.t-systems.net/sap/bc/srt/rfc/sap/zsec_pr_ws3/670/zsec_pr_ws3/zsec_pr_ws3"
urlS4P710 = "http://tps0203-s4project.demosystems.t-systems.net/sap/bc/srt/rfc/sap/zsec_pr_ws6/710/zsec_pr_ws6/zsec_pr_ws6"
my_string_var1=StringVar()
my_string_var2=StringVar()
returnOutput=StringVar()
def SAOPFun(urlSOAP):
    user_name=username.get()
    user_name=user_name.upper()
    payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:sap-com:document:sap:rfc:functions">
   <soapenv:Header/>
   <soapenv:Body>
      <urn:ZSEC_PASSWORD_RESET>
         <USER_ID>"""+user_name+"""</USER_ID>
      </urn:ZSEC_PASSWORD_RESET>
    </soapenv:Body>
    </soapenv:Envelope>"""
    headers = {
    'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    res = requests.request("POST", urlSOAP, headers=headers, data=payload, auth=HTTPBasicAuth('TSI_SEC_AUTO', '@Welcome12345'))
    #except requests.ConnectionError as e:
        #returnOutput=("Request to SAP failed with return code"+str(e))
    response=str(res.text)
    #print(response)
    usrNotFound="User "+user_name+" does not exist"
    acknowledge=response[response.index('<ACKNOWLEDGE>')+len('<ACKNOWLEDGE>'):response.index('</ACKNOWLEDGE>')]
    
    if res.status_code==200:
        if response.find(usrNotFound) == -1:
            emailID=response[response.index('<EMAIL_ID>')+len('<EMAIL_ID>'):response.index('</EMAIL_ID>')]
            password=response[response.index('<PASSWORD>')+len('<EMAIL_ID>'):response.index('</PASSWORD>')]
            returnOutput=(acknowledge+" mail sent to "+emailID)
        else:
            returnOutput="User not found"

    else:
        returnOutput="bad requested"

    return returnOutput

def loopSystem():
    my_string_var1.set("")
    my_string_var2.set("")
    if username.get()=="":
        my_string_var1.set("No username entered")
        return
    if var1.get():
        my_string_var1.set("S4P670: "+SAOPFun(urlS4P670))
    if var2.get():
        my_string_var2.set("S4P710: "+SAOPFun(urlS4P710))
        #my_string_var.set("Selected System not implimented")

    if var1.get()==0 and var2.get()==0:
        my_string_var1.set("No system selected")


tk.Label(window1, text='Enter Username', width=25, font=("Arial", 15, "bold")).pack(pady=5)
username = tk.Entry(window1, width=45)
username.pack(pady=5)

tk.Label(window1, text='Select System', width=25, font=("Arial", 15, "bold")).pack(pady=5)

var1 = tk.IntVar()
tk.Checkbutton(window1, text='S4P670', variable=var1).pack(pady=5)
var2 = tk.IntVar()
tk.Checkbutton(window1, text='S4P710', variable=var2).pack(pady=5)

button = tk.Button(window1, text='Submit', width=25, font=(10), bg='#87CEEB', command=loopSystem)
button.pack(pady=5)
close = tk.Button(window1, text='Close', width=25,font=(10), bg='#87CEEB', command=window1.destroy)
close.pack(pady=5)
#print(username.get())
tk.Label(window1, text="Result", font=("Arial", 15, "bold"), pady=5).pack(pady=5)

tk.Label(window1, textvariable=my_string_var1, font=("Arial", 10)).pack()
tk.Label(window1, textvariable=my_string_var2, font=("Arial", 10)).pack()


window1.mainloop()



#str1=username.get()
#tk.Label(window1, text=str1).pack()
