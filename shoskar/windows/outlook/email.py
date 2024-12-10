import win32com.client as win32

def outlook_email(send_to = '', 
                  subject = 'Requested Data', 
                  attachments = [], 
                  message = "See attached for requested information."
                  ):
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = send_to
    mail.Subject = subject
    mail.GetInspector 

    index = mail.HTMLbody.find('>', mail.HTMLbody.find('<body')) 
    mail.HTMLbody = mail.HTMLbody[:index + 1] + message + "<br><br>" + \
                    mail.HTMLbody[index + 1:].replace("<p class=MsoNormal><o:p>&nbsp;</o:p></p>", "") 

    # To attach a file to the email (optional):
    for attachment in attachments:
        mail.Attachments.Add(attachment)

    mail.Display()