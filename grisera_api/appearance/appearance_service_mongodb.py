from typing import Union

from appearance.appearance_service import AppearanceService
from graph_api_service import GraphApiService
from appearance.appearance_model import (
    AppearanceOcclusionIn,
    AppearanceOcclusionOut,
    BasicAppearanceOcclusionOut,
    AppearanceSomatotypeIn,
    AppearanceSomatotypeOut,
    BasicAppearanceSomatotypeOut,
    AppearancesOut,
)
from helpers import create_stub_from_response
from models.not_found_model import NotFoundByIdModel
from mongo_service.collection_mapping import Collections
from mongo_service.mongo_api_service import MongoApiService
from mongo_service.service_mixins import GenericMongoServiceMixin
from participant_state.participant_state_service import ParticipantStateService


class AppearanceServiceMongoDB(AppearanceService, GenericMongoServiceMixin):
    """
    Object to handle logic of appearance requests
    """

    def __init__(self):
        self.mongo_api_service = MongoApiService()
        self.participant_state_service: ParticipantStateService = None
        self.model_out_class = None

    def save_appearance_occlusion(self, appearance: AppearanceOcclusionIn):
        """
        Send request to mongo api to create new appearance occlusion model

        Args:
            appearance (AppearanceIn): Appearance to be added

        Returns:
            Result of request as appearance state object
        """
        self.model_out_class = AppearanceOcclusionOut
        return self.create(appearance)

    def save_appearance_somatotype(self, appearance: AppearanceSomatotypeIn):
        """
        Send request to mongo api to create new appearance somatotype model

        Args:
            appearance (AppearanceIn): Appearance to be added

        Returns:
            Result of request as appearance state object
        """

        if (
            not 1 <= appearance.ectomorph <= 7
            or not 1 <= appearance.endomorph <= 7
            or not 1 <= appearance.mesomorph <= 7
        ):
            return AppearanceSomatotypeOut(
                ectomorph=appearance.ectomorph,
                endomorph=appearance.endomorph,
                mesomorph=appearance.mesomorph,
                errors="Scale range not between 1 and 7",
            )
        self.model_out_class = AppearanceSomatotypeOut
        return self.create(appearance)

    def get_single(self, id: Union[str, int], depth: int = 0, source: str = ""):
        appearance = self.get_single_dict(id, depth, source)
        if type(appearance) is NotFoundByIdModel:
            return appearance
        return (
            AppearanceOcclusionOut(**appearance)
            if "glasses" in appearance.keys()
            else AppearanceSomatotypeOut(**appearance)
        )

    def get_appearance(
        self, appearance_id: Union[int, str], depth: int = 0, source: str = ""
    ):
        """
        Send request to mongo api to get given appearance

        Args:
            appearance_id (int | str): identity of appearance
            depth: (int): specifies how many related entities will be traversed to create the response
            source: Helper arguments that specifies direction of collection traversion

        Returns:
            Result of request as appearance object
        """
        return self.get_single(appearance_id, depth, source)

    def get_appearances(self, query: dict = {}):
        """
        Send request to mongo api to get appearances

        Returns:
            Result of request as list of appearances objects
        """
        results_dict = self.get_multiple(query)
        appearances = []
        for appearance_dict in results_dict:
            appearances.append(
                BasicAppearanceOcclusionOut(**appearance_dict)
                if "glasses" in appearance_dict.keys()
                else BasicAppearanceSomatotypeOut(**appearance_dict)
            )
        return AppearancesOut(appearances=appearances)

    def delete_appearance(self, appearance_id: Union[int, str]):
        """
        Send request to mongo api to delete given appearance

        Args:
            appearance_id (int | str): identity of appearance

        Returns:
            Result of request as appearance object
        """
        return self.delete(appearance_id)

    def update_appearance_occlusion(
        self, appearance_id: Union[int, str], appearance: AppearanceOcclusionIn
    ):
        """
        Send request to mongo api to update given appearance occlusion model

        Args:
            appearance_id (int | str): identity of appearance
            appearance (AppearanceOcclusionIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        get_response = self.get_single(appearance_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is AppearanceSomatotypeOut:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.mongo_api_service.update_document(appearance_id, appearance)

        return self.get_single(appearance_id)

    def update_appearance_somatotype(
        self, appearance_id: Union[int, str], appearance: AppearanceSomatotypeIn
    ):
        """
        Send request to mongo api to update given appearance somatotype model

        Args:
            appearance_id (int | str): identity of appearance
            appearance (AppearanceSomatotypeIn): Properties to update

        Returns:
            Result of request as appearance object
        """
        if (
            not 1 <= appearance.ectomorph <= 7
            or not 1 <= appearance.endomorph <= 7
            or not 1 <= appearance.mesomorph <= 7
        ):
            return AppearanceSomatotypeOut(
                **appearance.dict(), errors="Scale range not between 1 and 7"
            )
        get_response = self.get_single(appearance_id)

        if type(get_response) is NotFoundByIdModel:
            return get_response
        if type(get_response) is AppearanceOcclusionOut:
            return NotFoundByIdModel(id=appearance_id, errors="Node not found.")

        self.mongo_api_service.update_document(appearance_id, appearance)

        return self.get_single(appearance_id)

    def _add_related_documents(
        self,
        appearance: dict,
        depth: int,
        source: str,
    ):
        if depth > 0:
            self._add_participant_states(appearance, depth, source)

    def _add_participant_states(self, appearance: dict, depth: int, source: str):
        if source != Collections.PARTICIPANT_STATE:
            query = {"appearance_ids": appearance["id"]}
            appearance[
                "participant_states"
            ] = self.participant_state_service.get_multiple(
                query,
                depth=depth - 1,
                source=Collections.APPEARANCE,
            )
