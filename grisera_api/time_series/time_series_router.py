from typing import Union, Optional

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from services import Services
from time_series.time_series_model import TimeSeriesIn, TimeSeriesNodesOut, TimeSeriesOut, \
    TimeSeriesPropertyIn, TimeSeriesRelationIn
from time_series.time_series_service import TimeSeriesService

router = InferringRouter()


@cbv(router)
class TimeSeriesRouter:
    """
    Class for routing time series based requests

    Attributes:
        time_series_service (TimeSeriesService): Service instance for time series
    """
    def __init__(self):
        self.time_series_service = Services().time_series_service()

    @router.post("/time_series", tags=["time series"], response_model=TimeSeriesOut)
    async def create_time_series(self, time_series: TimeSeriesIn, response: Response):
        """
        Create time series in database
        """

        create_response = self.time_series_service.save_time_series(time_series)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/time_series", tags=["time series"], response_model=TimeSeriesNodesOut)
    async def get_time_series_nodes(self, response: Response, request: Request,
                                    recording_id: Optional[int] = None,
                                    participant_date_of_birth: Optional[str] = None,
                                    participant_id: Optional[int] = None):
        """
        Get time series nodes from database
        """

        get_response = self.time_series_service.get_time_series_nodes(request.query_params)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/time_series/{time_series_id}", tags=["time series"],
                response_model=Union[TimeSeriesOut, NotFoundByIdModel])
    async def get_time_series(self, time_series_id: int, response: Response):
        """
        Get time series from database
        """

        get_response = self.time_series_service.get_time_series(time_series_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/time_series/{time_series_id}", tags=["time series"],
                   response_model=Union[TimeSeriesOut, NotFoundByIdModel])
    async def delete_time_series(self, time_series_id: int, response: Response):
        """
        Delete time series from database
        """
        get_response = self.time_series_service.delete_time_series(time_series_id)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/time_series/{time_series_id}", tags=["time series"],
                response_model=Union[TimeSeriesOut, NotFoundByIdModel])
    async def update_time_series(self, time_series_id: int, time_series: TimeSeriesPropertyIn,
                                       response: Response):
        """
        Update time series model in database
        """
        update_response = self.time_series_service.update_time_series(time_series_id,
                                                                                  time_series)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response

    @router.put("/time_series/{time_series_id}/relationships", tags=["time series"],
                response_model=Union[TimeSeriesOut, NotFoundByIdModel])
    async def update_time_series_relationships(self, time_series_id: int,
                                                     time_series: TimeSeriesRelationIn, response: Response):
        """
        Update time series relations in database
        """
        update_response = self.time_series_service.update_time_series_relationships(time_series_id,
                                                                                                time_series)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
