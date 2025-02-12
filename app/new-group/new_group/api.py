from flask import Blueprint, current_app, jsonify
from .utils import set_group_id

blueprint = Blueprint(
    'new_group',
    __name__,
    url_prefix='/new-group',
    template_folder='templates',
    static_folder='static'
)

@blueprint.route('/<string:group_id>')
def set_new_group_id(group_id):
    """Set new group id callback function

    Arguments:
        group_id(str): Group id

    Returns:
        json: Result message
    """
    try:
        set_group_id(group_id)
        return jsonify({
            'result': 'OK',
            'message': 'Success.'
        })
    except Exception as ex:
        current_app.logger.error(ex)
        return jsonify({
            'result': 'NG',
            'message': str(ex)
        })