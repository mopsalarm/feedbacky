FROM gliderlabs/python-runtime:3.4
MAINTAINER Mopsalarm

EXPOSE 5000
CMD /env/bin/python /app/main.py --host=$HOST --user=$USER --password=$PASSWORD --receiver=$RECEIVER
