paperboy
========

Have you ever wanted to send the Calibre recipies to your reading device without the need of having Calibre up and running all the time? And probably you have a little server or Rasperry Pi lying around which doesn't have the horsepower to run a X11 desktop environment?
Then "paperboy" is your solution. It allows you to define jobs with the Calibre recipies of your favorite site, and sends them to your device daily, weekly or monthly on any given time. So you may read what you want when you want.

This application consists of two tools. The paperboy.py server application which sends all defined jobs. And the paperboy-config.py configuration application, to change the settings and delete or create new jobs.

Please be aware that this project is merely in an alpha stage and that there may be lots of hidden bugs, I would appreciate it if you report them. I am also open to suggestions of new features.

Requirements
------------

- Python 2.\*
- Calibre
- sendmail (optional, you can also use a smtp server)

Setup
-----

After you installed all the requirements you may choose how to download paperboy. You can download the newest releases
from this [page](https://github.com/baumartig/paperboy/releases).
Or you can checkout the repositrory via git, which is the most up to date version but may contain more bugs.

```
git clone https://github.com/baumartig/paperboy.git
```

Now that you got paperboy you need to configure it properly. Therefor you need to start `python paperboy-config.py`.

Paperboy
--------

The "paperboy" application is the standalone server application which executes all the jobs defined by the "paperboy-config" application.

Paperboy Config
---------------

The "paperboy-config" application is used to configure the server options and create and edit new jobs.

The main menu has the following options:

- 1 the menu for managing the jobs
- 2 to get into the settings
- 3 to execute all configured jobs (to test the setup)

### Managing Jobs

The jobs menu consists of the options.

- 1 list all current defined jobs, and edit it's properties
- 2 create a new job

#### Edit Jobs

To edit a existing or new job you have the following properties:

- 1 The execution type (daily, weekly or monthly)
- 2 The time when the job will be executed
- 3 Is only visible when the type is weekly or monthly
    - When weekly choose the weekday of the execution (Mo-Su)
    - When monthly choose the day of the month when to execute. If a given day does not exist in the month the job will not be executed.
- d To delete the current job.

#### Create a Job

The creation menu displays a list of all recognized calibre recipies. You can traverse the list with "n" and "p". To simplify the search you are also able to filter the list depending on the language ("l") and the title ("t"). The language of the recipie is displayed in the brackets at the front of the title.
When you found your desired recipe confirm with the creation with the corresponding index. After that you are presented with the standard job editing dialog.

### The Settings Menu

The settings menu consists of the following options:

- 1 to edit the "calibre" recipies folder (default should be "/opt/calibre/resources")
- 2 to change the prefered output format (for example pdf, mobi or epub)
- 3 to change the from adress which is used for the outgoing e-mails
 to change the recipients e-mail adress

If you want to use an smtp server instead of the standard sendmail you enable it by pressing "s" in the settings menu.
This presents you with these aditional options:

- 5 the smtp server adress
- 6 the smtp server port
- 7 the smtp server security
- 8 the smtp server login
- 9 the smtp server password

TODO
----

- [x] Allow job individual execution time.
- [x] Implement daily, weekly or monthly intervals
- [ ] Implement user management
- [ ] Allow multiple e-mail addresses, and allow to chose the e-mail address for a job

LICENSE
-------

The project is open source under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) license.

