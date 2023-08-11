"""
SHARE OBJECT
"""
from dataall.core.permissions.permissions import ENVIRONMENT_INVITED, ENVIRONMENT_INVITATION_REQUEST, ENVIRONMENT_ALL, RESOURCES_ALL, \
    RESOURCES_ALL_WITH_DESC

ADD_ITEM = 'ADD_ITEM'
REMOVE_ITEM = 'REMOVE_ITEM'
SUBMIT_SHARE_OBJECT = 'SUBMIT_SHARE_OBJECT'
APPROVE_SHARE_OBJECT = 'APPROVE_SHARE_OBJECT'
REJECT_SHARE_OBJECT = 'REJECT_SHARE_OBJECT'
DELETE_SHARE_OBJECT = 'DELETE_SHARE_OBJECT'
GET_SHARE_OBJECT = 'GET_SHARE_OBJECT'
LIST_SHARED_ITEMS = 'LIST_SHARED_ITEMS'
SHARE_OBJECT_REQUESTER = [
    ADD_ITEM,
    REMOVE_ITEM,
    SUBMIT_SHARE_OBJECT,
    GET_SHARE_OBJECT,
    LIST_SHARED_ITEMS,
    DELETE_SHARE_OBJECT,
]
SHARE_OBJECT_APPROVER = [
    ADD_ITEM,
    REMOVE_ITEM,
    APPROVE_SHARE_OBJECT,
    REJECT_SHARE_OBJECT,
    DELETE_SHARE_OBJECT,
    GET_SHARE_OBJECT,
    LIST_SHARED_ITEMS,
]
SHARE_OBJECT_ALL = [
    ADD_ITEM,
    REMOVE_ITEM,
    SUBMIT_SHARE_OBJECT,
    APPROVE_SHARE_OBJECT,
    REJECT_SHARE_OBJECT,
    DELETE_SHARE_OBJECT,
    GET_SHARE_OBJECT,
    LIST_SHARED_ITEMS,
]

CREATE_SHARE_OBJECT = 'CREATE_SHARE_OBJECT'
LIST_ENVIRONMENT_SHARED_WITH_OBJECTS = 'LIST_ENVIRONMENT_SHARED_WITH_OBJECTS'

ENVIRONMENT_INVITED.append(CREATE_SHARE_OBJECT)
ENVIRONMENT_INVITED.append(LIST_ENVIRONMENT_SHARED_WITH_OBJECTS)
ENVIRONMENT_INVITATION_REQUEST.append(CREATE_SHARE_OBJECT)
ENVIRONMENT_INVITATION_REQUEST.append(LIST_ENVIRONMENT_SHARED_WITH_OBJECTS)
ENVIRONMENT_ALL.append(CREATE_SHARE_OBJECT)
ENVIRONMENT_ALL.append(LIST_ENVIRONMENT_SHARED_WITH_OBJECTS)

RESOURCES_ALL.extend(SHARE_OBJECT_ALL)
for perm in SHARE_OBJECT_ALL:
    RESOURCES_ALL_WITH_DESC[perm] = perm

RESOURCES_ALL_WITH_DESC[CREATE_SHARE_OBJECT] = 'Request datasets access for this environment'
RESOURCES_ALL_WITH_DESC[LIST_ENVIRONMENT_SHARED_WITH_OBJECTS] = "List datasets shared with this environments"