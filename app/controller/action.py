from drape.response import json_response
from drape.util import toInt, tile_list_data

from app.model.action import ActionModel


def index(request):
    # uid
    params = request.params()
    uid = toInt(params.get('userinfo_id'), 0)

    # action model
    action_model = ActionModel()
    return json_response(action_model.getList(
        {
            'from_object_id': uid,
            'from_object_type': 'user'
        },
        toInt(params.get('from_id', -1))
    ))
