#!/usr/bin/python

import urllib2
import smtplib
import sys
import argparse
import time
import datetime
import httplib
import urllib

def printD(string, indent):
    strindent = ""
    for x in range(0, indent):
        strindent = strindent + " "
    print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + strindent + " " + string)

parser = argparse.ArgumentParser(
    description='Monitor a web page for a string (or not a string).',
    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80, width=80))
parser.add_argument('-u', '--smtpuser', help='The SMTP username', default='')
parser.add_argument('-p', '--smtppass', help='The SMTP password', default='')
parser.add_argument('-l', '--smtpsubject', help='The SMTP subject line', default='A web page change has been detected!')
parser.add_argument('-o', '--interval', help='The interval in minutes between checks (default 60)', default=60, type=int)
parser.add_argument('-r', '--reverse', help='Tells page-check to alerg when the string does not exist', default='', action='store_true')
parser.add_argument('-i', '--insensitive', help='Make the comparison case insensitive', default='', action='store_true')
parser.add_argument('-n', '--noexit', help='Do not exit once the change is detected', default='', action='store_true')
parser.add_argument('-y', '--pushoverapi', help='The pushover.net API key', default='')
parser.add_argument('-z', '--pushoveruser', help='The pushover.net user key', default='')
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument('-s', '--smtpserver', help='The SMTP server:port', required=True)
requiredArguments.add_argument('-f', '--smtpfrom', help='The FROM email address', required=True)
requiredArguments.add_argument('-t', '--smtpto', help='The TO email address', required=True)
requiredArguments.add_argument('-w', '--url', help='The URL to monitor', required=True)
requiredArguments.add_argument('-m', '--string', help='The string to watch for', required=True)
args = parser.parse_args()

pageHeaders = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept-Language': 'en-US,en;q=0.8,pt;q=0.6',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

while True:
    if not args.reverse:
        printD("Checking for '" + args.string + "' on " + args.url, 0)
    else:
        printD("Checking for absence of '" + args.string + "' on " + args.url, 0)
    needle = args.string
    req = urllib2.Request(args.url, headers=pageHeaders)
    success = False
    try:
        haystack = urllib2.urlopen(req).read()
        success = True
    except:
        printD("Error connecting to site.", 0)
    if success:
        if args.insensitive:
            needle = needle.lower()
            haystack = haystack.lower()

        if (not args.reverse and needle in haystack) or (args.reverse and needle not in haystack):
            if not args.reverse:
                printD("String found", 2)
            else:
                printD("String not found", 2)
            message = "Subject: " + args.smtpsubject + "\n\n"
            message = message + args.url
            server = smtplib.SMTP(args.smtpserver)
            server.starttls()
            if args.smtpuser != '' and args.smtppass != '':
                server.login(args.smtpuser, args.smtppass)
            server.sendmail(args.smtpfrom, args.smtpto, message)
            server.quit()
            if args.pushoverapi != '' and args.pushoveruser != '':
                printD("Sending Pushover message",2)
                conn = httplib.HTTPSConnection("api.pushover.net:443")
                conn.request("POST", "/1/messages.json",
                    urllib.urlencode({
                        "token": args.pushoverapi,
                        "user": args.pushoveruser,
                        "message": message,
                        "sound": "falling",
                    }), { "Content-type": "application/x-www-form-urlencoded" })
                conn.getresponse()
            if not args.noexit:
                sys.exit(0)
        else:
            if not args.reverse:
                printD("String not found", 2)
            else:
                printD("String found", 2)
        

    printD("Waiting " + str(args.interval) + " minutes for next check.", 0)
    time.sleep(args.interval * 60)
