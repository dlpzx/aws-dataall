""""
Creates a CloudFormation stack for SageMaker Studio users using cdk
"""
import logging
import os

from aws_cdk import (
    cloudformation_include as cfn_inc,
    Stack,
)

from dataall.modules.mlstudio.db.models import SagemakerStudioUser
from dataall.db.models import EnvironmentGroup

from dataall.cdkproxy.stacks.manager import stack
from dataall.db import Engine, get_engine
from dataall.db.api import Environment as EnvironmentRepository
from dataall.utils.cdk_nag_utils import CDKNagUtil
from dataall.utils.runtime_stacks_tagging import TagsUtil

logger = logging.getLogger(__name__)


@stack(stack='sagemakerstudiouser')
class SagemakerStudioUser(Stack):
    """
    Creation of a sagemaker studio user stack.
    Having imported the mlstudio module, the class registers itself using @stack
    Then it will be reachable by HTTP request / using SQS from GraphQL lambda
    """
    module_name = __file__

    def get_engine(self) -> Engine:
        envname = os.environ.get('envname', 'local')
        engine = get_engine(envname=envname)
        return engine

    def get_target(self, target_uri) -> SagemakerStudioUser:
        engine = self.get_engine()
        with engine.scoped_session() as session:
            sm_user = session.query(SagemakerStudioUser).get(
                target_uri
            )
        return sm_user

    def get_env_group(
        self, sm_user: SagemakerStudioUser
    ) -> EnvironmentGroup:
        engine = self.get_engine()
        with engine.scoped_session() as session:
            env_group = EnvironmentRepository.get_environment_group(
                session, sm_user.SamlAdminGroupName, sm_user.environmentUri,
            )
        return env_group

    def __init__(self, scope, id: str, target_uri: str = None, **kwargs) -> None:
        super().__init__(scope,
                         id,
                         description="Cloud formation stack of SM STUDIO USER: {}; URI: {}; DESCRIPTION: {}".format(
                             self.get_target(target_uri=target_uri).label,
                             target_uri,
                             self.get_target(target_uri=target_uri).description,
                         )[:1024],
                         **kwargs)

        # Required for dynamic stack tagging
        self.target_uri = target_uri

        sm_user: SagemakerStudioUser = self.get_target(target_uri=self.target_uri)

        env_group = self.get_env_group(sm_user)

        cfn_template_user = os.path.join(
            os.path.dirname(__file__), '..', 'cfnstacks', 'sagemaker-user-template.yaml'
        )
        user_parameters = dict(
            sagemaker_domain_id=sm_user.sagemakerStudioDomainID,
            user_name=sm_user.sagemakerStudioUserNameSlugify,
            execution_role=env_group.environmentIAMRoleArn,
        )
        logger.info(f'Creating the SageMaker Studio user {user_parameters}')

        my_sagemaker_studio_user_template = cfn_inc.CfnInclude(
            self,
            f'SagemakerStudioUser{self.target_uri}',
            template_file=cfn_template_user,
            parameters=user_parameters,
        )

        self.sm_user_arn = (
            my_sagemaker_studio_user_template.get_resource('SagemakerUser')
            .get_att('UserProfileArn')
            .to_string()
        )

        TagsUtil.add_tags(stack=self, model=SagemakerStudioUser, target_type="smstudiouser")

        CDKNagUtil.check_rules(self)
