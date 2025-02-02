import asyncio
import unittest
import unittest.mock as mock

from experiment.experiment_model import ExperimentOut
from scenario.scenario_router import *
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB


class TestScenarioRouter(unittest.TestCase):

    @mock.patch.object(ScenarioServiceGraphDB, 'save_scenario')
    def test_create_scenario_without_error(self, save_scenario_mock):
        save_scenario_mock.return_value = ScenarioOut(experiment=ExperimentOut(id=2, experiment_name="TestExperiment"),
                                                      activity_executions=[ActivityExecutionOut(id=1)])
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=[ActivityExecutionIn(activity_id=1,
                                                                                        arrangement_id=3)])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result, ScenarioOut(experiment=ExperimentOut(id=2, experiment_name="TestExperiment"),
                                             activity_executions=[ActivityExecutionOut(id=1)],
                                             links=get_links(router)))
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioServiceGraphDB, 'save_scenario')
    def test_create_scenario_with_error(self, save_scenario_mock):
        expected = ScenarioOut(experiment=ExperimentOut(id=2, experiment_name="TestExperiment"),
                               activity_executions=[ActivityExecutionOut(id=1)],
                               errors={'errors': ['test']})
        save_scenario_mock.return_value = expected
        response = Response()
        scenario = ScenarioIn(experiment_id=2, activity_executions=
        [ActivityExecutionIn(activity_id=1, arrangement_id=3, )])
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.create_scenario(scenario, response))

        self.assertEqual(result, expected)
        save_scenario_mock.assert_called_once_with(scenario)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(ScenarioServiceGraphDB, 'add_activity_execution')
    def test_add_activity_execution_without_error(self, add_activity_execution_mock):
        expected = ActivityExecutionOut(activity_id=1, arrangement_id=3, id=1)
        add_activity_execution_mock.return_value = expected
        response = Response()
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3, )
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response))

        self.assertEqual(result, expected)
        add_activity_execution_mock.assert_called_once_with(1, activity_execution)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ScenarioServiceGraphDB, 'add_activity_execution')
    def test_add_activity_execution_with_error(self, add_activity_execution_mock):
        expected = ActivityExecutionOut(activity_id=1, arrangement_id=3, errors={'errors': ['test']})
        add_activity_execution_mock.return_value = expected
        response = Response()
        activity_execution = ActivityExecutionIn(activity_id=1, arrangement_id=3, )
        scenario_router = ScenarioRouter()

        result = asyncio.run(scenario_router.add_activity_execution(1, activity_execution, response))

        self.assertEqual(result, expected)
        add_activity_execution_mock.assert_called_once_with(1, activity_execution)
        self.assertEqual(response.status_code, 422)
