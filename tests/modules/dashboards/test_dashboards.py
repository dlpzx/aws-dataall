import typing
import pytest

import dataall


def test_update_dashboard(
    client, env1, org1, group, module_mocker, patch_es, dashboard
):
    response = client.query(
        """
            mutation updateDashboard(
                $input:UpdateDashboardInput,
            ){
                updateDashboard(input:$input){
                    dashboardUri
                    name
                    label
                    DashboardId
                    created
                    owner
                    SamlGroupName
                }
            }
        """,
        input={
            'dashboardUri': dashboard.dashboardUri,
            'label': f'1234',
            'terms': ['term2'],
        },
        username='alice',
        groups=[group.name],
    )
    assert response.data.updateDashboard.owner == 'alice'
    assert response.data.updateDashboard.SamlGroupName == group.name


def test_list_dashboards(client, env1, db, org1, dashboard):
    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                }
            }
        }
        """,
        filter={},
        username='alice',
    )
    assert len(response.data.searchDashboards['nodes']) == 1


def test_nopermissions_list_dashboards(client, env1, db, org1, dashboard):
    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                }
            }
        }
        """,
        filter={},
        username='bob',
    )
    assert len(response.data.searchDashboards['nodes']) == 0


def test_get_dashboard(client, env1, db, org1, dashboard, group):
    response = client.query(
        """
        query GetDashboard($dashboardUri:String!){
                getDashboard(dashboardUri:$dashboardUri){
                    dashboardUri
                    name
                    owner
                    SamlGroupName
                    description
                    label
                    created
                    tags
                    environment{
                        label
                        region
                    }
                    organization{
                        organizationUri
                        label
                        name
                    }
                }
            }
        """,
        dashboardUri=dashboard.dashboardUri,
        username='alice',
        groups=[group.name],
    )
    assert response.data.getDashboard.owner == 'alice'
    assert response.data.getDashboard.SamlGroupName == group.name


def test_request_dashboard_share(
    client,
    env1,
    db,
    org1,
    user,
    group,
    module_mocker,
    dashboard,
    patch_es,
    group2,
    user2,
):
    module_mocker.patch(
        'dataall.aws.handlers.service_handlers.Worker.queue', return_value=True
    )
    response = client.query(
        """
        mutation requestDashboardShare($dashboardUri:String!, $principalId:String!){
            requestDashboardShare(dashboardUri:$dashboardUri, principalId:$principalId){
                shareUri
                status
            }
        }
        """,
        dashboardUri=dashboard.dashboardUri,
        principalId=group2.name,
        username=user2.userName,
        groups=[group2.name],
    )
    share = response.data.requestDashboardShare
    assert share.shareUri
    assert share.status == 'REQUESTED'

    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                    userRoleForDashboard
                }
            }
        }
        """,
        filter={},
        username=user2.userName,
        groups=[group2.name],
    )
    assert len(response.data.searchDashboards['nodes']) == 0

    response = client.query(
        """
        mutation approveDashboardShare($shareUri:String!){
            approveDashboardShare(shareUri:$shareUri){
                shareUri
                status
            }
        }
        """,
        shareUri=share.shareUri,
        username=user.userName,
        groups=[group.name],
    )
    assert response.data.approveDashboardShare.status == 'APPROVED'

    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                    userRoleForDashboard
                }
            }
        }
        """,
        filter={},
        username=user2.userName,
        groups=[group2.name],
    )
    assert len(response.data.searchDashboards['nodes']) == 1

    response = client.query(
        """
        query listDashboardShares($dashboardUri:String!,$filter:DashboardShareFilter!){
            listDashboardShares(dashboardUri:$dashboardUri,filter:$filter){
                count
                nodes{
                    dashboardUri
                    shareUri
                }
            }
        }
        """,
        filter={},
        dashboardUri=dashboard.dashboardUri,
        username=user.userName,
        groups=[group.name],
    )
    assert len(response.data.listDashboardShares['nodes']) == 1

    response = client.query(
        """
        query GetDashboard($dashboardUri:String!){
                getDashboard(dashboardUri:$dashboardUri){
                    dashboardUri
                    name
                    owner
                    SamlGroupName
                    description
                    label
                    created
                    tags
                    environment{
                        label
                        region
                    }
                    organization{
                        organizationUri
                        label
                        name
                    }
                }
            }
        """,
        dashboardUri=dashboard.dashboardUri,
        username=user2.userName,
        groups=[group2.name],
    )
    assert response.data.getDashboard.owner == 'alice'
    assert response.data.getDashboard.SamlGroupName == group.name

    response = client.query(
        """
        mutation rejectDashboardShare($shareUri:String!){
            rejectDashboardShare(shareUri:$shareUri){
                shareUri
                status
            }
        }
        """,
        shareUri=share.shareUri,
        username=user.userName,
        groups=[group.name],
    )
    assert response.data.rejectDashboardShare.status == 'REJECTED'

    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                    userRoleForDashboard
                }
            }
        }
        """,
        filter={},
        username=user2.userName,
        groups=[group2.name],
    )
    assert len(response.data.searchDashboards['nodes']) == 0

    response = client.query(
        """
        mutation shareDashboard($dashboardUri:String!, $principalId:String!){
            shareDashboard(dashboardUri:$dashboardUri, principalId:$principalId){
                shareUri
                status
            }
        }
        """,
        dashboardUri=dashboard.dashboardUri,
        principalId=group2.name,
        username=user.userName,
        groups=[group.name],
    )
    assert response.data.shareDashboard.shareUri

    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                    userRoleForDashboard
                }
            }
        }
        """,
        filter={},
        username=user2.userName,
        groups=[group2.name],
    )
    assert len(response.data.searchDashboards['nodes']) == 1


def test_delete_dashboard(
    client, env1, db, org1, user, group, module_mocker, dashboard, patch_es
):
    module_mocker.patch(
        'dataall.aws.handlers.service_handlers.Worker.queue', return_value=True
    )
    response = client.query(
        """
        mutation deleteDashboard($dashboardUri:String!){
            deleteDashboard(dashboardUri:$dashboardUri)
        }
        """,
        dashboardUri=dashboard.dashboardUri,
        username=user.userName,
        groups=[group.name],
    )
    assert response.data.deleteDashboard
    response = client.query(
        """
        query searchDashboards($filter:DashboardFilter!){
            searchDashboards(filter:$filter){
                count
                nodes{
                    dashboardUri
                }
            }
        }
        """,
        filter={},
        username='alice',
    )
    assert len(response.data.searchDashboards['nodes']) == 0