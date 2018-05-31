# page-check
Watches a web page and sends an email when a string is detected (or not).

## Usage
```
# wget https://raw.githubusercontent.com/Fmstrat/page-check/master/page-check.py
# ./page-check.py --help
usage: page-check.py [-h] [-u SMTPUSER] [-p SMTPPASS] [-l SMTPSUBJECT]
                     [-o INTERVAL] [-r] [-i] [-n] -s SMTPSERVER -f SMTPFROM -t
                     SMTPTO -w URL -m STRING

Monitor a web page for a string (or not a string).

optional arguments:
  -h, --help                                 show this help message and exit
  -u SMTPUSER, --smtpuser SMTPUSER           The SMTP username
  -p SMTPPASS, --smtppass SMTPPASS           The SMTP password
  -l SMTPSUBJECT, --smtpsubject SMTPSUBJECT  The SMTP subject line
  -o INTERVAL, --interval INTERVAL           The interval in minutes between
                                             checks (default 60)
  -r, --reverse                              Tells page-check to alerg when the
                                             string does not exist
  -i, --insensitive                          Make the comparison case
                                             insensitive
  -n, --noexit                               Do not exit once the change is
                                             detected

required arguments:
  -s SMTPSERVER, --smtpserver SMTPSERVER     The SMTP server:port
  -f SMTPFROM, --smtpfrom SMTPFROM           The FROM email address
  -t SMTPTO, --smtpto SMTPTO                 The TO email address
  -w URL, --url URL                          The URL to monitor
  -m STRING, --string STRING                 The string to watch for
```

## Docker
The following example is for docker-compose.
```
  page-check:
    image: nowsci/page-check
    container_name: page-check
    volumes:
      - /etc/localtime:/etc/localtime:ro
    environment:
      - OPTIONS=--smtpserver mail:25 --smtpfrom user@domain.tld --smtpto user@domain.tld --url https://domain.tld --string "Monitor Me"
    restart: "no"
```
