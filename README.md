paperboy
========

Server for compiling and sending the calibre news to a device via e-mail.

This application consists of two tools. The paperboy.py server application which sends all defined jobs. And the paperboy-config.py configuration application, to change the settings and delete or create new jobs.

Please be aware that this project is merely in an alpha stage so be aware that there may be lots of bugs hidden, i would appreciate if you report them. I am also open to suggestions of new features.

Requirements
------------

- Python 2.\*
- calibre
- sendmail (optional, you can also use a smtp server)

Setup
-----

After you installed all the requirements you may choose how to download paperboy. You can download the newest releases
from this [page](https://github.com/baumartig/paperboy/releases).
Or you can checkout the repositrory via git, which is the most up to date version but may contain more bugs.

``
git clone https://github.com/baumartig/paperboy.git
``

Now that you got paperboy you need to configure it properly. Therefor you need to start `python paperboy-config.py` and
proceed like this:

- Press 2 to get into the settings

In the settings menu:

- Press 1 to edit the "calibre" recipies folder (default should be "/opt/calibre/resources")
- Press 2 to change the prefered output format (for example pdf, mobi or epub)
- Press 3 to change the from adress which is used for the outgoing e-mails
- Press 4 to change the recipients e-mail adress

If you want to use an smtp server instead of the standard sendmail you enable it by pressing "s" in the settings menu.
This presents you with these aditional options:

- 5 the smtp server adress
- 6 the smtp server port
- 7 the smtp server security
- 8 the smtp server login
- 9 the smtp server password

Job handling
------------




## TODO

- [x] Allow job individual execution time.
- [x] Implement daily, weekly or monthly intervals
- [ ] Implement User management
- [ ] Allow multiple e-mail adresses, and allow to chose the e-mail adress for a job


The project is open source under the [Apache 2.0](https://github.com/FriendCode/codebox/blob/master/LICENSE) license.
