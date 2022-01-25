# page-check
Watches a web page and sends an email when a string is detected (or not).

***Please see the `python` branch for the original python version.***

## Usage
Page Check will stop checking a page once an alert has fired.
```yml
  page-check:
    image: nowsci/page-check:latest
    container_name: page-check
    volumes:
      - /etc/localtime:/etc/localtime:ro
    environment:
      # CHECKS is an array of page checks
      #    "url"     - The URL to check
      #    "string"  - The string to check for
      #    "reverse" - To check if the string exists or does not
      CHECKS: '[
                    {
                        "url": "https://www.mysite.com",
                        "string": "Alert when this string exists",
                        "reverse": false
                    },
                    {
                        "url": "https://www.anothersite.com",
                        "string": "Alert when this string does not exist",
                        "reverse": true
                    }
                ]'
      INTERVALMIN: 60                   # Interval in minutes between checks
      # Either Pushover or SMTP alerts can be used
      PUSHOVERAPI: '<redacted>'         # Optional Pushover API key
      PUSHOVERUSER: '<redacted>'        # Optional Pushover API user
      SMTPSERVER: '<server>:<port>'     # Optional SMTP server and port
      SMTPFROM: '<user>@<domain>.<ext>' # Optional email address an email will come from
      SMTPTO: '<user>@<domain>.<ext>'   # Optional email address that will recieve the email
    restart: "always"
```
