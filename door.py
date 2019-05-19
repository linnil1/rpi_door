# from gpiozero import Button, LED
import time
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# on off open
state = 'off'
# set_relay = LED(4)


def set_on():
    state = 'on'
    set_relay.on()


def set_off():
    state = 'off'
    set_relay.off()


def doorOpen():
    # set_on()
    time.sleep(1)
    # set_off()


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    method = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    timef = '%m/%d, %H:%M:%S'

    def __repr__(self):
        return f'{self.user} {self.method} at {self.date.strftime(self.timef)}'


def add(user, method):
    db.session.add(History(user=user, method=method))
    db.session.commit()


def show(limit=5):
    return db.session.query(History)\
                     .order_by(History.id.desc())\
                     .limit(limit)\
                     .all()
