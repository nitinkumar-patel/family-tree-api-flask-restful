def person_obj(person, noparents=False, nochildren=False, nospouse=False):
    return_person_obj = {
        "person_id":        person.person_id,
        "firstname":        person.firstname,
        "lastname":         person.lastname,
        "birthdate":        str(person.birthdate.isoformat()[:10]),
        "email":            person.email,
        "street_address":   person.street_address,
        "city":             person.city,
        "state":            person.state,
        "zip":              person.zip,
        "phone":            person.phone,
        "links": [
            {
                "rel":  "self",
                "href": "/persons/" + person.person_id
            }
        ]
    }

    if not noparents:
        return_person_obj["parents"] = [{'id': parent.person_id,
                                         'fullname': ' '.join((parent.firstname, parent.lastname))}
                                        for parent in person.parents]
    if not nochildren:
        return_person_obj["children"] = [{'id': child.person_id,
                                          'fullname': ' '.join((child.firstname, child.lastname))}
                                         for child in person.children]
    return return_person_obj


def persons_obj(persons, noparents=False, nochildren=False):
    return_persons_obj = []
    for person in persons.items:
        return_persons_obj.append(person_obj(person, noparents, nochildren))
    return return_persons_obj


def persons_obj_list(persons, noparents=False, nochildren=False):
    return_persons_obj = []
    for person in persons:
        return_persons_obj.append(person_obj(person, noparents, nochildren))
    return return_persons_obj

