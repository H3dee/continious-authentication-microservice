from flask import Blueprint, request
from os import mkdir, path

from ..util import sql_query_to_csv, settings, start_features_extracting
from ..ML_API import API
from ..models import RawEventsData
from ..database import db

continious_auth = Blueprint("continious_auth", __name__, url_prefix="/api/continious-auth/")


@continious_auth.route("chunk", methods=["POST"])
def chunk():
    if request.is_json:
        body = request.get_json()
        chunk_records = []

        if body["mode"] == "training":
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

            return {"message": "success"}
        else:
            chunk_records = [
                {
                    "event": raw_data_chunk["event"],
                    "positionX": raw_data_chunk["positionX"],
                    "positionY": raw_data_chunk["positionY"],
                    "timestamp": raw_data_chunk["timestamp"],
                    "windowName": raw_data_chunk["windowName"],
                    "userId": raw_data_chunk["userId"],
                    "id": i + 1,
                    "button": raw_data_chunk["button"]
                } for i, raw_data_chunk in enumerate(body["chunks"])
            ]

            user_id = chunk_records[0]["userId"]
            user_directory = '/user' + str(user_id)
            full_directory_path = settings.TEST_DATA_FOLDER + user_directory

            if not path.exists(full_directory_path):
                mkdir(full_directory_path)

            target_file_path = full_directory_path + '/raw_events_data.csv'
            headers = ["event", "positionX", "positionY", "timestamp", "windowName", "userId", "id", "button"]

            sql_query_to_csv(target_file_path, chunk_records, headers)
            start_features_extracting(user_directory)

            path_to_target_file = full_directory_path + '/features_with_classes.csv'
            features = open(path_to_target_file, 'r')

            validation_result = API.validate_user(features, user_id)

        return {"result":  validation_result}
    else:
        return {"status": "400", "message": "The request payload is not in JSON format"}


@continious_auth.route("complete", methods=["POST"])
def complete():
    if request.is_json:
        body = request.get_json()
        user_id = body["userId"]

        raw_events_data = RawEventsData.query.filter_by(userId=user_id).order_by("timestamp").all()
        data_not_found = len(raw_events_data) == 0

        if data_not_found:
            return {"message": "Collected data were not found"}

        directory_path = settings.TRAINING_RAW_DATA_BASE_FOLDER + "/user" + str(user_id)

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
    else:
        return {"status": "400", "message": "The request payload is not in JSON format"}


@continious_auth.route("train", methods=["get"])
def train():
    start_features_extracting()

    path_to_target_file = settings.TRAINING_FEATURE_FILENAME
    features = open(path_to_target_file, 'r')

    API.train_all(features)

    return {"message": "success"}
