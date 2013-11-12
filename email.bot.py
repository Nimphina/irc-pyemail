import gmail, os, sys, time
#Gmail - https://github.com/charlierguo/gmail	

def gm_connect():

	username 		= "nimsphina@gmail.com" #Send me some emails sure
	password		= ""

	try:
		print "Logging into {0}".format(username)
		gmail_connection = gmail.login(username, password)
		return gmail_connection
	except:
		print "Error", sys.exc_info()[0:5]
		gmail_connection.logout()

def get_email(g_conn):

	email_subject 		= "NULL"
	email_link			= "NULL"
	final_array			= []

	unread_emails = g_conn.inbox().mail(unread=True, sender="noreply@curse.com") #Get all unread mail from target address
	
	counter = 0

	print "Fetching new emails, may take a while if there is a lot of them"

	for email in unread_emails: #Read through list of mail
		unread_emails[counter].fetch() #Fetch email content

		email_subject = unread_emails[counter].subject #Get subject

		email_body = unread_emails[counter].body #Fetch emailbody and assign a variable
		email_array = email_body.split() #Split body into array

		for item in email_array: 
			if "http://www.minecraftforum.net/topic/" in item:
				email_link = item

		email.read() #For when the bot is deployed

		counter += 1
		final_array.append("{0} - {1}".format(email_subject, email_link))

	return final_array 

try:
	
	g_conn = gm_connect()

	list_of_topics = get_email(g_conn)

	for item in list_of_topics:
		
		print item

finally:
	g_conn.logout()