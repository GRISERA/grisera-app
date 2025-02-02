import unittest
import unittest.mock as mock

from graph_api_service import GraphApiService
from measure.measure_model import *
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure_name.measure_name_model import MeasureNameOut, BasicMeasureNameOut
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB


class TestMeasureServicePost(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_relationships')
    @mock.patch.object(GraphApiService, 'create_properties')
    @mock.patch.object(MeasureNameServiceGraphDB, 'get_measure_name')
    @mock.patch.object(GraphApiService, 'get_node')
    def test_save_measure_without_error(self, get_node_mock, get_measure_name_mock, create_properties_mock,
                                        create_relationships_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        get_node_mock.return_value = {'id': id_node, 'labels': ['Measure'],
                                      'properties': [{'key': 'datatype', 'value': 'Test'},
                                                     {'key': 'range', 'value': 'Unknown'},
                                                     {'key': 'unit', 'value': 'cm'}],
                                      "errors": None, 'links': None}

        create_relationships_mock.return_value = {'id': 3, 'start_node': 1, 'end_node': 6, "errors": None,
                                                  'links': None}\

        measure_service = MeasureServiceGraphDB()
        measure_service.measure_name_service = mock.create_autospec(MeasureNameServiceGraphDB)
        get_measure_name_mock.return_value = BasicMeasureNameOut(id=6, name="Test", type="Test")
        measure_service.measure_name_service.get_measure_name = get_measure_name_mock

        calls = [mock.call(start_node=id_node, end_node=6, name="hasMeasureName")]
        measure = MeasureIn(measure_name_id=6, datatype="Test", range="Unknown", unit="cm")

        result = measure_service.save_measure(measure)

        self.assertEqual(result, BasicMeasureOut(measure_name_id=6, datatype="Test", range="Unknown", unit="cm",
                                                 id=id_node))
        create_node_mock.assert_called_once_with('Measure')
        get_measure_name_mock.assert_called_once()
        create_relationships_mock.assert_has_calls(calls)
        create_properties_mock.assert_called_once_with(id_node, measure)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_measure_with_node_error(self, create_node_mock):
        create_node_mock.return_value = {'properties': None, "errors": ['error'], 'links': None}
        measure = MeasureIn(measure_name_id=1, datatype="Test", range="Unknown", unit="cm")
        measure_service = MeasureServiceGraphDB()

        result = measure_service.save_measure(measure)

        self.assertEqual(result,
                         MeasureOut(datatype="Test", range="Unknown", unit="cm", errors=['error']))
        create_node_mock.assert_called_once_with('Measure')
