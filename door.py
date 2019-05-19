from gpiozero import Button, LED
import time
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# on off open
state = 'off'
set_relay = LED(4)


def set_on():
    set_relay.on()


def set_off():
    set_relay.off()


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    method = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    timef = '%m/%d, %H:%M:%S'

    def __repr__(self):
        return '{} {} at {}'.format(
            self.user, self.method, self.date.strftime(self.timef))


def add(user, method):
    print(user, method)
    global state
    if method == 'open':
        if state == 'on':
            return False
        set_on()
        time.sleep(1)
        set_off()

    elif method in ['on', 'off']:
        if method == state:
            return False
        state = method
        if method == 'on':
            set_on()
        else:
            set_off()

    else:
        return False

    db.session.add(History(user=user, method=method))
    db.session.commit()
    return True


def show(limit=5):
    return db.session.query(History)\
                     .order_by(History.id.desc())\
                     .limit(limit)\
                     .all()
