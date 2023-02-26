from parametrization import Parametrization

from elementary.monitor.alerts.group_of_alerts import (
    ErrorComponent,
    FailureComponent,
    GroupOfAlertsByAll,
    GroupOfAlertsBySingleAlert,
    GroupOfAlertsByTable,
    OwnersComponent,
    SubsComponent,
    TagsComponent,
    WarningComponent,
)
from elementary.monitor.data_monitoring.data_monitoring_alerts import (
    DataMonitoringAlerts,
)
from tests.unit.monitor.alerts.group_alerts_by_table.mock_classes import MockConfig
from tests.unit.monitor.alerts.group_alerts_by_table.mock_data import (
    AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
    AL_ERROR_MODEL3_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
    AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
    AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
    AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
    DEFAULT_CHANNEL,
    OTHER_CHANNEL,
    OWNER_1,
    OWNER_2,
    OWNER_3,
    TAGS_3,
)
from tests.unit.monitor.alerts.group_alerts_by_table.utils import (
    check_eq_group_alerts,
    mock_data_monitoring_alerts,
)


@Parametrization.autodetect_parameters()
@Parametrization.default_parameters(
    default_channel=DEFAULT_CHANNEL,
    default_grouping="alert",
    expected_execution_properties=None,
)
@Parametrization.case(
    name="empty_list_goes_to_empty_list",
    list_of_alerts=[],
    expected_alert_groups=[],
    expected_execution_properties={
        "had_group_by_alert": False,
        "had_group_by_table": False,
        "had_group_by_all": False,
    },
)
@Parametrization.case(
    name="one_warning_goes_to_one_warning",
    list_of_alerts=[AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING],
    expected_alert_groups=[
        GroupOfAlertsBySingleAlert(
            alerts=[AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING],
            default_channel_destination=DEFAULT_CHANNEL,
        )
    ],
    expected_execution_properties={
        "had_group_by_alert": True,
        "had_group_by_table": False,
        "had_group_by_all": False,
    },
)
@Parametrization.case(
    name="one_fail_group_by_all_channel_selection_is_default",
    default_grouping="all",
    list_of_alerts=[AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING],
    expected_alert_groups=[
        GroupOfAlertsByAll(
            alerts=[AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING],
            default_channel_destination=DEFAULT_CHANNEL,
        )
    ],
    expected_execution_properties={
        "had_group_by_alert": False,
        "had_group_by_table": False,
        "had_group_by_all": True,
    },
)
@Parametrization.case(
    name="one_fail_one_warn_same_model_group_by_table_groups_them_together",
    default_grouping="table",
    list_of_alerts=[
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
    ],
    expected_alert_groups=[
        GroupOfAlertsByTable(
            alerts=[
                AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
                AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
            ],
            default_channel_destination=DEFAULT_CHANNEL,
        )
    ],
    expected_execution_properties={
        "had_group_by_alert": False,
        "had_group_by_table": True,
        "had_group_by_all": False,
    },
)
@Parametrization.case(
    name="one_fail_one_warn_same_table_one_other_table_group_by_table_groups_them_to_2_groups",
    default_grouping="table",
    list_of_alerts=[
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
    ],
    expected_alert_groups=[
        GroupOfAlertsByTable(
            alerts=[
                AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
                AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
            ],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsByTable(
            alerts=[AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
    ],
    expected_execution_properties={
        "had_group_by_alert": False,
        "had_group_by_table": True,
        "had_group_by_all": False,
    },
)
@Parametrization.case(
    name="two_alerts_on_model_1_two_alerts_on_model_2_default_grouping_is_by_table_by_one_alert_has_group_by_alert",
    default_grouping="table",
    list_of_alerts=[
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    ],
    expected_alert_groups=[
        GroupOfAlertsByTable(
            alerts=[
                AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
                AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
            ],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsByTable(
            alerts=[AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsBySingleAlert(
            alerts=[AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
    ],
    expected_execution_properties={
        "had_group_by_alert": True,
        "had_group_by_table": True,
        "had_group_by_all": False,
    },
)
@Parametrization.case(
    name="default_grouping_all_and_overrides_existing_by_alert_and_by_table_to_2_out_of_3_of_model_2_s_alerts",
    default_grouping="all",
    list_of_alerts=[
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL3_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    ],
    expected_alert_groups=[
        GroupOfAlertsByAll(
            alerts=[
                AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
                AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
                AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
            ],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsByTable(
            alerts=[
                AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
                AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
            ],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsBySingleAlert(
            alerts=[AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
        GroupOfAlertsBySingleAlert(
            alerts=[AL_ERROR_MODEL3_NO_CHANNEL_WITH_GROUPING_BY_ALERT],
            default_channel_destination=DEFAULT_CHANNEL,
        ),
    ],
    expected_execution_properties={
        "had_group_by_alert": True,
        "had_group_by_table": True,
        "had_group_by_all": True,
    },
)
def test_grouping_logic(
    default_channel,
    default_grouping,
    list_of_alerts,
    expected_alert_groups,
    expected_execution_properties,
):
    # init
    conf = MockConfig(
        slack_group_alerts_by=default_grouping, slack_channel_name=default_channel
    )
    data_monitoring_alerts = mock_data_monitoring_alerts(conf)

    # business logic
    list_of_groups = DataMonitoringAlerts._group_alerts_per_config(
        data_monitoring_alerts, list_of_alerts
    )

    # assertions
    if expected_alert_groups is not None:
        assert len(list_of_groups) == len(expected_alert_groups)
        for grp1, grp2 in zip(list_of_groups, expected_alert_groups):
            assert check_eq_group_alerts(grp1, grp2)

    if expected_execution_properties is not None:
        assert (
            data_monitoring_alerts.execution_properties == expected_execution_properties
        )


@Parametrization.autodetect_parameters()
@Parametrization.default_parameters(
    grouping_class=GroupOfAlertsByAll,
    default_channel=DEFAULT_CHANNEL,
    expected_owners=None,
    expected_tags=None,
    expected_subs=None,
    expected_warnings=None,
    expected_fails=None,
    expected_errors=None,
    expected_channel=None,
)
@Parametrization.case(
    name="single_alert_no_channel_goes_to_default_channel",
    grouping_class=GroupOfAlertsBySingleAlert,
    alerts_list=[AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING],
    expected_channel=DEFAULT_CHANNEL,
)
@Parametrization.case(
    name="single_alert_with_non_default_channel_goes_to_non_default_channel",
    grouping_class=GroupOfAlertsBySingleAlert,
    alerts_list=[AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING],
    expected_channel=OTHER_CHANNEL,
)
@Parametrization.case(
    name="group_by_table_forces_use_of_the_model_channel",
    grouping_class=GroupOfAlertsByTable,
    alerts_list=[
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
    ],
    expected_channel=OTHER_CHANNEL,
)
@Parametrization.case(
    name="group_by_all_forces_use_of_the_default_channel",
    grouping_class=GroupOfAlertsByAll,
    alerts_list=[
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
    ],
    expected_channel=DEFAULT_CHANNEL,
)
@Parametrization.case(
    name="owners_are_deduplicated",
    grouping_class=GroupOfAlertsByAll,
    alerts_list=[
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
    ],
    expected_owners=[OWNER_1, OWNER_2, OWNER_3],
)
@Parametrization.case(
    name="tags_are_deduplicated",
    grouping_class=GroupOfAlertsByAll,
    alerts_list=[
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
    ],
    expected_tags=TAGS_3,
)
@Parametrization.case(
    name="errors_warnings_and_fails_are_routed_properly",
    grouping_class=GroupOfAlertsByAll,
    alerts_list=[
        AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL3_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    ],
    expected_errors=[
        AL_ERROR_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
        AL_ERROR_MODEL3_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
    ],
    expected_warnings=[AL_WARN_MODEL1_NO_CHANNEL_NO_GROUPING],
    expected_fails=[
        AL_FAIL_MODEL1_WITH_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_NO_GROUPING,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_ALERT,
        AL_FAIL_MODEL2_NO_CHANNEL_WITH_GROUPING_BY_TABLE,
    ],
)
def test_alert_group_construction(
    grouping_class,
    alerts_list,
    default_channel,
    expected_owners,
    expected_tags,
    expected_subs,
    expected_warnings,
    expected_fails,
    expected_errors,
    expected_channel,
):
    # business logic
    alerts_group = grouping_class(alerts_list, default_channel)

    # assertions
    if expected_owners is not None:
        assert sorted(
            alerts_group._components_to_attention_required[OwnersComponent].split(", ")
        ) == sorted(expected_owners)
    if expected_tags is not None:
        assert sorted(
            [
                x.replace("#", "")
                for x in alerts_group._components_to_attention_required[TagsComponent].split(
                    ", "
                )
            ]
        ) == sorted(expected_tags.split(", "))
    if expected_subs is not None:
        assert sorted(
            alerts_group._components_to_attention_required[SubsComponent]
        ) == sorted(expected_subs)
    if expected_errors is not None:
        assert alerts_group._components_to_alerts[ErrorComponent] == expected_errors
    if expected_warnings is not None:
        assert alerts_group._components_to_alerts[WarningComponent] == expected_warnings
    if expected_fails is not None:
        assert alerts_group._components_to_alerts[FailureComponent] == expected_fails
    if expected_channel is not None:
        assert alerts_group.channel_destination == expected_channel
