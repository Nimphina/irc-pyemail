import imaplib
import os
import sys
import pprint

#imaplib.Debug = 4

def open_connection(verbose=False):

    hostname = "imap.gmail.com"
    port = 993
    username = "nimsphina"
    password = "outside12"

    connection = imaplib.IMAP4_SSL(hostname, port)

    # Login to our account
    if verbose: print 'Logging in as', username
    connection.login(username, password)
    return connection

def get_email_sender(conn, email_num):
    
    try:
            conn.select('INBOX', readonly=True) #open Inbox folder for reading

            typ, msg_data = conn.fetch(str(email_num), '(BODY.PEEK[HEADER])') #Fetch email titles

            for response_part in msg_data:

                if isinstance(response_part, tuple):
                    counter = 0
                    return_string = "Null"
                    email_title = response_part[1].split()
                    
                    for item in email_title:
                        #print item
                        if item == "From:":
                            return_string = ""
                            while email_title[counter +1] != "To:":
                                return_string = return_string + email_title[counter +1] + " "
                                counter +=1
                            #return return_string
                        counter += 1
                    return return_string

    except: #If error, logout
        return "error"

def get_email_subject(conn, email_num):
    
    try:
        conn.select('INBOX', readonly=True) #open Inbox folder for reading
        
        typ, msg_data = conn.fetch(str(email_num), '(BODY.PEEK[HEADER])') #Fetch email titles
        
        for response_part in msg_data:
            #print response_part[1]
            if isinstance(response_part, tuple):
                counter = 0
                return_string = "Null"
                email_title = response_part[1].split()
                
                for item in email_title:
                    
                    if item == "Subject:":
                        return_string = ""
                        while email_title[counter +1] != "Content-type:":
                            return_string = return_string + email_title[counter +1] + " "
                            counter +=1
                        #return return_string
                    counter += 1
                return return_string

    except: #If error, logout
        print "Unexpected error:", sys.exc_info()[0]
        return "error"
        

def get_link(): #This function needs to delete read mail
    pass

def read_emails(conn, option, email_no):
    
    #Declare needed variables
    email_subject       = "NULL"
    email_link          = "NULL"
    email_post_sub      = "NULL"
    return_array        = []

    typ, msg_data = conn.select('INBOX', readonly=True)

    no_of_emails = int(msg_data[0])

    for x in range(no_of_emails):
        x+=1
        email_post_sub = get_email_sender(conn, x)
        print email_post_sub
        if "\"Minecraft Forum\" <noreply@curse.com>" in email_post_sub:
            email_subject = get_email_subject(conn, x)
            return_array.append("{0}- {1}".format(email_subject, email_link))

    if email_subject == "error":
        print "An error occured while trying to get the email_subject"
        return "NULL"

    else:
        return return_array

#main function
if __name__ == '__main__':
    c = open_connection(verbose=True)

    try:
       
       post_array = read_emails(c, "last", 0)
       for item in post_array:
            print item     
                        
    finally:
        c.logout()