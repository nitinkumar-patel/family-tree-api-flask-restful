import uuid
import pytest
import datetime

from family_tree.models import Person, Relation


# created person obj based on the family tree api template (person)
def create_person_obj(first_name='test', last_name='user', email=''):
    return Person(
        person_id=str(uuid.uuid4()),
        firstname=first_name,
        lastname=last_name,
        email=str(uuid.uuid4()) if not email else email,
        birthdate=datetime.datetime.strptime("2019-12-31", "%Y-%m-%d"),
        street_address="123 Main St.",
        city="City_name",
        state="IL",
        zip="12345",
        phone="123-123-1234"
    )


@pytest.fixture
def create_person(session):
    def _create_person(first_name="Test", last_name="User", email=''):
        p = create_person_obj(first_name, last_name, email)
        session.add(p)
        session.commit()
        return p

    return _create_person


def test_create_person(session):
    new_user = create_person_obj(first_name="test", last_name="user", email=str(uuid.uuid4()))

    session.add(new_user)
    session.commit()
    assert new_user.id is not None


def test_create_relation(session):
    parent = create_person_obj(first_name="parent", last_name="user")
    child = create_person_obj(first_name="child", last_name="user", email="child@user.com")
    parent.children.append(child)

    session.add(parent)
    session.add(child)
    session.commit()

    assert parent in child.parents


def test_delete_relation_relationship_when_deleting_person(session):
    """Checking DELETE ON CASCADE functionality"""
    parent = create_person_obj(first_name="parent", last_name="user", email="parent@user.com")
    child = create_person_obj(first_name="child", last_name="user", email="child@user.com")
    parent.children.append(child)

    session.add(parent)
    session.add(child)
    session.commit()
    assert parent in child.parents

    session.delete(parent)
    assert len(Relation.query.all()) == 0


def test_family_tree(session, create_person):
    child1 = create_person()
    child1_child1 = create_person()
    child1_child2 = create_person()
    child1.children.extend([child1_child1, child1_child2])

    child3 = create_person()
    child3_child1 = create_person()
    child3_child2 = create_person()
    child3_child3 = create_person()
    child3.children.extend([child3_child1, child3_child2, child3_child3])

    head_of_family = create_person()
    child2 = create_person()
    head_of_family.children.extend([child1, child2, child3])
    expected_grandchildren_list = [child1_child1, child1_child2, child3_child1, child3_child2, child3_child3]

    assert set(head_of_family.grandchildren) == set(expected_grandchildren_list)
    assert set(child2.grandchildren) == set([])

    expected_cousins = [child3_child1, child3_child2, child3_child3]
    assert set(child1_child1.cousins) == set(expected_cousins)



