FROM python:2-onbuild
MAINTAINER Mopsalarm

CMD python ./main.py --host=$HOST --user=$USER --password=$PASSWORD --receiver=$RECEIVER

EXPOSE 5000

