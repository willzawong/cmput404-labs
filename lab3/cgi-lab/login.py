#!/usr/bin/env python3
import cgi
import cgitb
cgitb.enable()
from templates import login_page, secret_page, after_login_incorrect
import secret
import os
from http.cookies import SimpleCookie

# create login form
s = cgi.FieldStorage()
user = s.getfirst("username")
password = s.getfirst("password")

# set cookie if correct info
form_ok = user == secret.username and password == secret.password
cookie = SimpleCookie(os.environ["HTTP_COOKIE"])
cookie_user = None
cookie_pass = None
if cookie.get("username"):
    cookie_user = cookie.get("username").value
if cookie.get("password"):
    cookie_pass = cookie.get("password").value

cookie_ok = cookie_user == secret.username and cookie_pass == secret.password

# if cookie exists and is good, set pass+user
if cookie_ok:
    user = cookie_user
    password = cookie_pass

# print to html
print("Content-Type: text/html")
if form_ok:
    print(f"Set-Cookie: username={user}")
    print(f"Set-Cookie: password={password}")

print("")

# load login page and print info
if not user and not password:
    print(login_page())
elif user == secret.username and password == secret.password:
    print(secret_page(user,password))
else:
    print(after_login_incorrect())