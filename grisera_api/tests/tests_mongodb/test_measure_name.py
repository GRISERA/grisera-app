import mongomock
from measure.measure_model import MeasureIn
from measure_name.measure_name_model import MeasureNameIn

from services import Services
from tests.tests_mongodb.utils import MongoTestCase
from models.not_found_model import NotFoundByIdModel
from recording.recording_model import RecordingIn
from registered_channel.registered_channel_model import RegisteredChannelIn
from registered_data.registered_data_model import RegisteredDataIn
from channel.channel_model import ChannelIn, Type
from mongo_service.mongodb_api_config import mongo_api_host, mongo_api_port


class TestMongoMeasureName(MongoTestCase):
    def generate_measure_name(self, name="a name", type="a type"):
        service = Services().measure_name_service()
        measure = MeasureNameIn(name=name, type=type)
        return service.save_measure_name(measure)

    def generate_measure(
        self, measure_name_id, datatype="a datatype", range="a range", unit="s"
    ):
        service = Services().measure_service()
        measure = MeasureIn(
            measure_name_id=measure_name_id, datatype=datatype, range=range, unit=unit
        )
        return service.save_measure(measure)

    def test_save(self):
        service = Services().measure_name_service()
        mn = MeasureNameIn(type="a type", name="a name")
        created_mn = service.save_measure_name(mn)

        self.assertEqual(created_mn.type, mn.type)
        self.assertEqual(created_mn.name, mn.name)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get(self):
        service = Services().measure_name_service()
        created_mn = self.generate_measure_name()
        fetched_mn = service.get_measure_name(created_mn.id)

        self.assertEqual(fetched_mn.id, created_mn.id)
        self.assertEqual(fetched_mn.type, created_mn.type)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get_all(self):
        service = Services().measure_name_service()
        created_mn_count = 10
        created_mn = []
        for _ in range(created_mn_count):
            created_mn.append(self.generate_measure_name())
        result = service.get_measure_names()
        self.assertEqual(len(result.measure_names), created_mn_count)
        created_mn_ids = set(mn.id for mn in created_mn)
        fetched_mn_ids = set(mn.id for mn in result.measure_names)
        self.assertSetEqual(created_mn_ids, fetched_mn_ids)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_traverse_one(self):
        service = Services().measure_name_service()

        created_mn = self.generate_measure_name()
        meaures_count = 10
        created_meaures = []
        for _ in range(meaures_count):
            meaure = self.generate_measure(created_mn.id)
            created_meaures.append(meaure)

        # create registered channels related to other channel
        other_mn = self.generate_measure_name()
        for _ in range(5):
            self.generate_measure(other_mn.id)

        result = service.get_measure_name(created_mn.id, depth=1)
        self.assertFalse(type(result) is NotFoundByIdModel)
        self.assertEqual(len(result.measures), meaures_count)
        expected_created_ids = {measure.id for measure in created_meaures}
        created_ids = {measure.id for measure in result.measures}
        self.assertSetEqual(expected_created_ids, created_ids)
