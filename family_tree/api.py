from flask.views import MethodView
from flask import request, abort, render_template
import uuid
# import json
from jsonschema import Draft7Validator
from jsonschema.exceptions import best_match
import datetime

# from app.decorators import app_required
from family_tree.models import Person
from family_tree.schema import schema
from family_tree.templates import person_obj, persons_obj, persons_obj_list

from helper.helper import make_response


class PersonAPI(MethodView):

    # decorators = [app_required]

    def __init__(self):
        self.PERSONS_PER_PAGE = 10
        if request.method not in ['GET', 'DELETE'] and not request.json:
            print(request.method, request.json)
            abort(400)

    def get(self, person_id):
        print(person_id)
        if person_id:
            person = Person.find_by_id(person_id)
            if person:
                relation_type = ""
                if "siblings" in request.url:
                    relation_type, persons = "siblings", person.siblings
                elif "grandparents" in request.url:
                    relation_type, persons = "grandparents", person.grandparents
                elif "parents" in request.url:
                    relation_type, persons = "parents", person.parents
                elif "children" in request.url:
                    relation_type, persons = "children", person.children
                elif "cousins" in request.url:
                    relation_type, persons = "cousins", person.cousins
                if relation_type:
                    response = {
                        "result": "ok",
                        "links": [
                            {
                                "href": "/persons/%s/%s" % (person_id, relation_type),
                                "rel": "self"
                            }
                        ],
                        "data": persons_obj_list(persons, noparents=True, nochildren=True),
                    }
                else:
                    response = {
                        "result": "ok",
                        "data": [person_obj(person)]
                    }
                return make_response(response=response, code=200)
            else:
                response = {}
                return make_response(response=response, code=404)
        else:
            person_href = "/persons/?page=%s"
            persons = Person.get_all_live()
            if "firstname" in request.args:
                firstname = request.args.get('firstname')
                persons = persons.filter_by(firstname=firstname)
                person_href += "&firstname=" + firstname
            if "state" in request.args:
                state = request.args.get('state')
                persons = persons.filter_by(state=state)
                person_href += "&state=" + state

            # pagination
            page = int(request.args.get('page', 1))
            persons = persons.paginate(page=page, per_page=self.PERSONS_PER_PAGE)
            response = {
                "result": "ok",
                "links": [
                    {
                        "href": person_href % page,
                        "rel": "self"
                    }
                ],
                "data": persons_obj(persons)
            }
            if persons.has_prev:
                response["links"].append(
                    {
                        "href": person_href % persons.prev_num,
                        "rel": "previous"
                    }
                )
            if persons.has_next:
                response["links"].append(
                    {
                        "href": person_href % persons.next_num,
                        "rel": "next"
                    }
                )
            return make_response(response=response, code=200)

    def post(self):
        person_json = request.json
        error = best_match(Draft7Validator(schema).iter_errors(person_json))
        if error:
            response = {'error': error.message}
            return make_response(response=response, code=400)
        try:
            birthdate = datetime.datetime.strptime(
                person_json.get('birthdate'), "%Y-%m-%d"
            )
        except:
            response = {'error': "INVALID_BIRTHDATE"}
            return make_response(response=response, code=400)
        if person_json.get("children"):
            children = Person.query.filter(Person.person_id.in_(person_json.get("children"))).all()
            person_json['children'] = children
        if person_json.get("parents"):
            parents = Person.query.filter(Person.person_id.in_(person_json.get("parents"))).all()
            person_json['parents'] = parents

        person = Person(
            person_id=str(uuid.uuid4()),
            firstname=person_json.get('firstname'),
            lastname=person_json.get('lastname'),
            birthdate=birthdate,
            email=person_json.get('email'),
            street_address=person_json.get('street_address'),
            city=person_json.get('city'),
            state=person_json.get('state'),
            zip=person_json.get('zip'),
            phone=person_json.get('phone'),
            children=person_json.get('children', []),
            parents=person_json.get('parents', [])
        )
        person.save_to_db()
        response = {
            "result": "ok",
            "data": [person_obj(person)]
        }
        return make_response(response=response, code=201)

    def put(self, person_id):
        person = Person.find_by_id(person_id)
        print(person)
        if not person:
            response = {}
            return make_response(response=response, code=404)
        # print(person_id)
        person_json = request.json
        error = best_match(Draft7Validator(schema).iter_errors(person_json))
        if error:
            response = {'error': error.message}
            return make_response(response=response, code=400)
        # print(person_id)
        if person_json.get('birthdate'):
            try:
                birthdate = datetime.datetime.strptime(
                    person_json.get('birthdate'), "%Y-%m-%d"
                )
                person_json['birthdate'] = birthdate
            except:
                response = {'error': "INVALID_BIRTHDATE"}
                return make_response(response=response, code=400)
        # print(person_id)
        if person_json.get("children"):
            children = Person.query.filter(Person.person_id.in_(person_json.get("children"))).all()
            person_json['children'] = children
        if person_json.get("parents"):
            parents = Person.query.filter(Person.person_id.in_(person_json.get("parents"))).all()
            person_json['parents'] = parents
        print(person_id)
        person.patch(person_json)
        print(person_id)
        person.save_to_db()
        print(person_id)
        response = {
            "result": "ok",
            "data": [person_obj(person)]
        }
        print(response)
        return make_response(response=response, code=200)

    def delete(self, person_id):
        person = Person.find_by_id(person_id)
        if not person:
            response = {}
            return make_response(response=response, code=404)
        person.live = False
        person.save_to_db()
        response = {'result': 'ok'}
        return make_response(response=response, code=204)
