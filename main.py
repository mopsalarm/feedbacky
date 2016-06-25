import argparse
import base64
import traceback
import zlib

import flask
from flask import request, jsonify
from mailer import Mailer, Message


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="smtp.gmail.com", help="Host of the smtp server")
    parser.add_argument("--user", required=True, help="Username to use to login into the smtp server")
    parser.add_argument("--password", required=True, help="Password for the smtp server")
    parser.add_argument("--receiver", required=True, help="Address of the receiver of feedback mails")

    return parser.parse_args()


def make_app(args):
    app = flask.Flask(__name__)

    @app.route("/post", methods=["POST"])
    def post():
        version = request.form["version"]
        username = request.form.get("name", "")
        feedback = request.form.get("feedback", "")

        if "logcat64" in request.form:
            logcat = base64.b64decode(request.form.get("logcat64"))
            logcat = zlib.decompress(logcat, 32+15).decode("utf8")
        else:
            logcat = request.form.get("logcat", "")

        send_feedback_mail(version, username, feedback, logcat)
        return jsonify(success=True)

    def send_feedback_mail(version, username, feedback, logcat):
        # noinspection PyBroadException
        try:
            msg = Message(From=args.user, To=args.receiver, charset="utf8")
            msg.Subject = u"Feedback {} ({})".format(version, username)
            msg.Body = u"User: {0} http://pr0gramm.com/user/{0}\nFeedback: {1}\n\nLogcat: {2}\n".format(username, feedback, logcat)

            mailer = Mailer(args.host, port=587, use_tls=True, usr=args.user, pwd=args.password)
            mailer.send(msg)

        except:
            traceback.print_exc()

    return app


def main():
    args = parse_arguments()

    app = make_app(args)
    app.run(host="0.0.0.0", debug=False)


if __name__ == '__main__':
    main()
