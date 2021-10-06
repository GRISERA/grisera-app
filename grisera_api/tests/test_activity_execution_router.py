import asyncio
import unittest
import unittest.mock as mock

from activity_execution.activity_execution_router import *


def return_activity_execution(*args, **kwargs):
    activity_execution_out = ActivityExecutionOut(activity='group',  id=1)
    return activity_execution_out


class TestActivityExecutionRouter(unittest.TestCase):

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    def test_create_activity_execution_without_error(self, save_activity_execution_mock):
        save_activity_execution_mock.side_effect = return_activity_execution
        response = Response()
        activity_execution = ActivityExecutionIn(activity='group')
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.create_activity_execution(activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(activity='group', id=1, links=get_links(router)))
        save_activity_execution_mock.assert_called_once_with(activity_execution)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ActivityExecutionService, 'save_activity_execution')
    def test_create_activity_execution_with_error(self, save_activity_execution_mock):
        save_activity_execution_mock.return_value = ActivityExecutionOut(activity='group', errors={'errors': ['test']})
        response = Response()
        activity_execution = ActivityExecutionIn(activity='group')
        activity_execution_router = ActivityExecutionRouter()

        result = asyncio.run(activity_execution_router.create_activity_execution(activity_execution, response))

        self.assertEqual(result, ActivityExecutionOut(activity='group', errors={'errors': ['test']}, links=get_links(router)))
        save_activity_execution_mock.assert_called_once_with(activity_execution)
        self.assertEqual(response.status_code, 422)
