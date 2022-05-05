from flask import Blueprint, request

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
    return {"message": "success"}