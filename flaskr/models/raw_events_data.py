from ..database import db


class RawEventsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String())
    positionX = db.Column(db.Integer())
    positionY = db.Column(db.Integer())
    timestamp = db.Column(db.Float())
    button = db.Column(db.String())
    windowName = db.Column(db.String())
    userId = db.Column(db.Integer())

    def __init__(self, event, positionX, positionY, timestamp, windowName, userId, button):
        self.event = event
        self.button = button
        self.positionX = positionX
        self.positionY = positionY
        self.timestamp = timestamp
        self.windowName = windowName
        self.userId = userId

    def __repr__(self):
        return f""
