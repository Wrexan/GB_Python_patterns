## This repo contains:
+ **Web framework** with ORM made from scratch
+ **Simple site** without media for demonstration
### About:
Those are made as a part of educational process. The functionality enough to demonstrate understanding and skills in realising backend features, but not enough for commercial purpose.
### Framework:
+ **How to run:**
   + gunicorn run_server:app
+ **What implemented:**
  + Middleware
  + HTML parser
  + REST architecture work with GET and POST
  + ORM for sqlite3 using Data Mapper pattern
  + Registration using password's hash
  + Login/logout using password or local storage token
### Site:
Emulates educational site with courses (in russian language). You can register/login and participate on educational course
+ **How to run:**
  + Run create_n_fill_db.py once to create database and fill a little
  + Start framework
  + Open in browser http://127.0.0.1:8000
+ **What implemented:**
  + Simple design, menus using JavaScript and HTML
  + Registration
  + Login/logout with local storage token
  + Precreated users:
    + Login `Basil` password `123`
    + Login `Peter` password `123`
