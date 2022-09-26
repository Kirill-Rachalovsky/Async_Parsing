from bson.objectid import ObjectId


def object_id_to_string(value) -> str:
    if isinstance(value, ObjectId):
        return str(value)
    return value
