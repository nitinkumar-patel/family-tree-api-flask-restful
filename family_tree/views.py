from flask import Blueprint

from family_tree.api import PersonAPI

family_tree_app = Blueprint('family_tree_app', __name__)


person_view = PersonAPI.as_view('person_api')

family_tree_app.add_url_rule('/persons/', defaults={'person_id': None}, view_func=person_view, methods=['GET', ])
family_tree_app.add_url_rule('/persons/', view_func=person_view, methods=['POST', ])
family_tree_app.add_url_rule('/persons/<string:person_id>', view_func=person_view, methods=['GET', 'PUT', 'DELETE', ])
family_tree_app.add_url_rule('/persons/<string:person_id>/siblings', view_func=person_view, methods=['GET', ])
family_tree_app.add_url_rule('/persons/<string:person_id>/parents', view_func=person_view, methods=['GET', ])
family_tree_app.add_url_rule('/persons/<string:person_id>/children', view_func=person_view, methods=['GET', ])
family_tree_app.add_url_rule('/persons/<string:person_id>/grandparents', view_func=person_view, methods=['GET', ])
family_tree_app.add_url_rule('/persons/<string:person_id>/cousins', view_func=person_view, methods=['GET', ])
