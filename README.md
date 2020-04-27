o2-webdav-sync
==============

Script to sync your o2 calendar (https://client.o2.fr) with a webdav calendar (like framagenda.org).

# How to use it ?

Create a `.env` file with the needed env variables :

```
export O2_USER=toto@coucou.fr
export O2_PASS=xxxxxxxxxxx
export WEBDAV_URL=framagenda.org/remote.php/dav/calendars/xxxuserxxx/yyycalendaryyy/
export WEBDAV_CAL=menage
export WEBDAV_USER=toto
export WEBDAV_PASS=xxxxxxxxx
```

run the script (`run.sh` is creating the venv for you)

```
./run.sh
```
