"""
Add module's permissions to the global permissions.
Contains permissions for sagemaker ML Studio
"""

from dataall.db.permissions import (
    ENVIRONMENT_ALL,
    ENVIRONMENT_INVITED,
    RESOURCES_ALL_WITH_DESC,
    RESOURCES_ALL,
    ENVIRONMENT_INVITATION_REQUEST,
    TENANT_ALL,
    TENANT_ALL_WITH_DESC
)


CREATE_SGMSTUDIO_NOTEBOOK = 'CREATE_SGMSTUDIO_NOTEBOOK'
LIST_ENVIRONMENT_SGMSTUDIO_NOTEBOOKS = 'LIST_ENVIRONMENT_SGMSTUDIO_NOTEBOOKS'

MANAGE_SGMSTUDIO_NOTEBOOKS = 'MANAGE_SGMSTUDIO_NOTEBOOKS'

GET_SGMSTUDIO_NOTEBOOK = 'GET_SGMSTUDIO_NOTEBOOK'
UPDATE_SGMSTUDIO_NOTEBOOK = 'UPDATE_SGMSTUDIO_NOTEBOOK'
DELETE_SGMSTUDIO_NOTEBOOK = 'DELETE_SGMSTUDIO_NOTEBOOK'
SGMSTUDIO_NOTEBOOK_URL = 'SGMSTUDIO_NOTEBOOK_URL'

SGMSTUDIO_NOTEBOOK_ALL = [
    GET_SGMSTUDIO_NOTEBOOK,
    UPDATE_SGMSTUDIO_NOTEBOOK,
    DELETE_SGMSTUDIO_NOTEBOOK,
    SGMSTUDIO_NOTEBOOK_URL,
]

ENVIRONMENT_ALL.append(CREATE_SGMSTUDIO_NOTEBOOK)
ENVIRONMENT_ALL.append(LIST_ENVIRONMENT_SGMSTUDIO_NOTEBOOKS)
ENVIRONMENT_INVITED.append(CREATE_SGMSTUDIO_NOTEBOOK)
ENVIRONMENT_INVITED.append(LIST_ENVIRONMENT_SGMSTUDIO_NOTEBOOKS)
ENVIRONMENT_INVITATION_REQUEST.append(CREATE_SGMSTUDIO_NOTEBOOK)

TENANT_ALL.append(MANAGE_SGMSTUDIO_NOTEBOOKS)
TENANT_ALL_WITH_DESC[MANAGE_SGMSTUDIO_NOTEBOOKS] = 'Manage ML studio notebooks'

RESOURCES_ALL.append(SGMSTUDIO_NOTEBOOK_ALL)
RESOURCES_ALL_WITH_DESC[CREATE_SGMSTUDIO_NOTEBOOK] = 'Create ML Studio profiles on this environment'

