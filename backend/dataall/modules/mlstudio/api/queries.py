"""The module defines GraphQL queries for the SageMaker ML Studio"""
from dataall.api import gql
from dataall.modules.mlstudio.api.resolvers import (
    get_sagemaker_studio_user,
    # get_user_applications,
    list_sagemaker_studio_users,
    get_sagemaker_studio_user_presigned_url,
)

getSagemakerStudioUser = gql.QueryField(
    name='getSagemakerStudioUser',
    args=[
        gql.Argument(
            name='sagemakerStudioUserUri', type=gql.NonNullableType(gql.String)
        )
    ],
    type=gql.Ref('SagemakerStudioUser'),
    resolver=get_sagemaker_studio_user,
)

# TODO: is this used????
# getSagemakerStudioUserApps = gql.QueryField(
#     name='getSagemakerStudioUserApps',
#     args=[
#         gql.Argument(
#             name='sagemakerStudioUserUri', type=gql.NonNullableType(gql.String)
#         )
#     ],
#     type=gql.ArrayType(gql.Ref('SagemakerStudioUserApps')),
#     resolver=get_user_applications,
# )

listSagemakerStudioUsers = gql.QueryField(
    name='listSagemakerStudioUsers',
    args=[gql.Argument('filter', gql.Ref('SagemakerStudioUserFilter'))],
    type=gql.Ref('SagemakerStudioUserSearchResult'),
    resolver=list_sagemaker_studio_users,
)

getSagemakerStudioUserPresignedUrl = gql.QueryField(
    name='getSagemakerStudioUserPresignedUrl',
    args=[
        gql.Argument(
            name='sagemakerStudioUserUri', type=gql.NonNullableType(gql.String)
        )
    ],
    type=gql.String,
    resolver=get_sagemaker_studio_user_presigned_url,
)
