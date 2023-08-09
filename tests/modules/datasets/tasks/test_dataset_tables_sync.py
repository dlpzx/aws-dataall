from unittest.mock import MagicMock

import pytest
from dataall.core.environment.db.models import Environment, EnvironmentGroup
from dataall.core.organizations.api.enums import OrganisationUserRole
from dataall.core.organizations.db.organization_models import Organization
from dataall.core.permissions.db.permission import Permission
from dataall.modules.datasets_base.db.models import DatasetTable, Dataset
from dataall.modules.datasets.tasks.tables_syncer import sync_tables


@pytest.fixture(scope='module', autouse=True)
def org(db):
    with db.scoped_session() as session:
        org = Organization(
            label='org',
            owner='alice',
            tags=[],
            description='desc',
            SamlGroupName='admins',
            userRoleInOrganization=OrganisationUserRole.Owner.value,
        )
        session.add(org)
    yield org


@pytest.fixture(scope='module', autouse=True)
def env(org, db):
    with db.scoped_session() as session:
        env = Environment(
            organizationUri=org.organizationUri,
            AwsAccountId='12345678901',
            region='eu-west-1',
            label='org',
            owner='alice',
            tags=[],
            description='desc',
            SamlGroupName='admins',
            EnvironmentDefaultIAMRoleName='EnvRole',
            EnvironmentDefaultIAMRoleArn='arn:aws::123456789012:role/EnvRole/GlueJobSessionRunner',
            CDKRoleArn='arn:aws::123456789012:role/EnvRole',
            userRoleInEnvironment='999',
        )
        session.add(env)
        session.commit()
    yield env


@pytest.fixture(scope='module', autouse=True)
def sync_dataset(org, env, db):
    with db.scoped_session() as session:
        dataset = Dataset(
            organizationUri=org.organizationUri,
            environmentUri=env.environmentUri,
            label='label',
            owner='foo',
            SamlAdminGroupName='foo',
            businessOwnerDelegationEmails=['foo@amazon.com'],
            businessOwnerEmail=['bar@amazon.com'],
            name='name',
            S3BucketName='S3BucketName',
            GlueDatabaseName='GlueDatabaseName',
            KmsAlias='kmsalias',
            AwsAccountId='123456789012',
            region='eu-west-1',
            IAMDatasetAdminUserArn=f'arn:aws:iam::123456789012:user/dataset',
            IAMDatasetAdminRoleArn=f'arn:aws:iam::123456789012:role/dataset',
        )
        session.add(dataset)
        session.commit()
        env_group = EnvironmentGroup(
            environmentUri=env.environmentUri,
            groupUri=dataset.SamlAdminGroupName,
            environmentIAMRoleArn=env.EnvironmentDefaultIAMRoleArn,
            environmentIAMRoleName=env.EnvironmentDefaultIAMRoleName,
            environmentAthenaWorkGroup='workgroup',
        )
        session.add(env_group)
    yield dataset


@pytest.fixture(scope='module', autouse=True)
def table(org, env, db, sync_dataset):
    with db.scoped_session() as session:
        table = DatasetTable(
            datasetUri=sync_dataset.datasetUri,
            AWSAccountId='12345678901',
            S3Prefix='S3prefix',
            label='label',
            owner='foo',
            name='name',
            GlueTableName='table1',
            S3BucketName='S3BucketName',
            GlueDatabaseName='GlueDatabaseName',
            region='eu-west-1',
        )
        session.add(table)
    yield table


@pytest.fixture(scope='module', autouse=True)
def permissions(db):
    with db.scoped_session() as session:
        yield Permission.init_permissions(session)


def test_tables_sync(db, org, env, sync_dataset, table, mocker):
    mock_crawler = MagicMock()
    mocker.patch('dataall.modules.datasets.tasks.tables_syncer.DatasetCrawler', mock_crawler)
    mock_crawler().list_glue_database_tables.return_value = [
            {
                'Name': 'new_table',
                'DatabaseName': sync_dataset.GlueDatabaseName,
                'StorageDescriptor': {
                    'Columns': [
                        {
                            'Name': 'col1',
                            'Type': 'string',
                            'Comment': 'comment_col',
                            'Parameters': {'colp1': 'p1'},
                        },
                    ],
                    'Location': f's3://{sync_dataset.S3BucketName}/table1',
                    'Parameters': {'p1': 'p1'},
                },
                'PartitionKeys': [
                    {
                        'Name': 'partition1',
                        'Type': 'string',
                        'Comment': 'comment_partition',
                        'Parameters': {'partition_1': 'p1'},
                    },
                ],
            },
            {
                'Name': 'table1',
                'DatabaseName': sync_dataset.GlueDatabaseName,
                'StorageDescriptor': {
                    'Columns': [
                        {
                            'Name': 'col1',
                            'Type': 'string',
                            'Comment': 'comment_col',
                            'Parameters': {'colp1': 'p1'},
                        },
                    ],
                    'Location': f's3://{sync_dataset.S3BucketName}/table1',
                    'Parameters': {'p1': 'p1'},
                },
                'PartitionKeys': [
                    {
                        'Name': 'partition1',
                        'Type': 'string',
                        'Comment': 'comment_partition',
                        'Parameters': {'partition_1': 'p1'},
                    },
                ],
            },
        ]

    mocker.patch(
        'dataall.modules.datasets.tasks.tables_syncer.is_assumable_pivot_role', return_value=True
    )

    mock_client = MagicMock()
    mocker.patch("dataall.modules.datasets.tasks.tables_syncer.LakeFormationTableClient", mock_client)
    mock_client.grant_principals_all_table_permissions = True

    processed_tables = sync_tables(engine=db)
    assert len(processed_tables) == 2
    with db.scoped_session() as session:
        saved_table: DatasetTable = (
            session.query(DatasetTable)
            .filter(DatasetTable.GlueTableName == 'table1')
            .first()
        )
        assert saved_table
        assert saved_table.GlueTableName == 'table1'