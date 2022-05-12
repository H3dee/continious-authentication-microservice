from flask import Blueprint, request
from os import mkdir, path

from ..util import sql_query_to_csv, settings
from ..models import RawEventsData
from ..database import db

continious_auth = Blueprint("continious_auth", __name__, url_prefix="/api/continious-auth/")


@continious_auth.route("chunk", methods=["POST"])
def chunk():
    if request.is_json:
        body = request.get_json()
        chunk_records = []

        for raw_data_chunk in body["chunks"]:
            record = RawEventsData(
                event=raw_data_chunk["event"],
                positionX=raw_data_chunk["positionX"],
                positionY=raw_data_chunk["positionY"],
                timestamp=raw_data_chunk["timestamp"],
                windowName=raw_data_chunk["windowName"],
                button=raw_data_chunk["button"],
                userId=raw_data_chunk["userId"]
            )

            chunk_records.append(record)

        db.session.add_all(chunk_records)
        db.session.commit()

        return {"message": "chunk successfully added"}
    else:
        return {"status": "400", "message": "The request payload is not in JSON format"}


@continious_auth.route("complete", methods=["GET"])
def complete():
    raw_events_data = RawEventsData.query.all()

    directory_path = settings.TRAINING_RAW_DATA_BASE_FOLDER + "/user1"

    if not path.exists(directory_path):
        mkdir(directory_path)

    target_file_path = directory_path + '/raw_events_data.csv'
    headers = ["event", "positionX", "positionY", "timestamp", "windowName", "userId", "id", "button"]

    mapped_data = [
        {
            "event": data_chunk.event,
            "positionX": data_chunk.positionX,
            "positionY": data_chunk.positionY,
            "timestamp": data_chunk.timestamp,
            "windowName": data_chunk.windowName,
            "userId": data_chunk.userId,
            "id": data_chunk.id,
            "button": data_chunk.button
        } for data_chunk in raw_events_data
    ]

    sql_query_to_csv(target_file_path, mapped_data, headers)

    return {"message": "success"}
