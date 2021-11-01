from graph_api_service import GraphApiService
from live_activity.live_activity_model import LiveActivityIn, LiveActivityOut, LiveActivitiesOut, BasicLiveActivityOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class LiveActivityService:
    """
    Object to handle logic of live activity requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_live_activity(self, live_activity: LiveActivityIn):
        """
        Send request to graph api to create new live activity

        Args:
            live_activity (LiveActivityIn): Live activity to be added

        Returns:
            Result of request as live activity object
        """

        node_response = self.graph_api_service.create_node("`Live Activity`")

        if node_response["errors"] is not None:
            return LiveActivityOut(live_activity=live_activity.live_activity, errors=node_response["errors"])

        live_activity_id = node_response["id"]

        properties_response = self.graph_api_service.create_properties(live_activity_id, live_activity)
        if properties_response["errors"] is not None:
            return LiveActivityOut(errors=properties_response["errors"])

        return LiveActivityOut(live_activity=live_activity.live_activity, id=live_activity_id)

    def get_live_activities(self):
        """
        Send request to graph api to get all live activities

        Returns:
            Result of request as list of live activity objects
        """
        get_response = self.graph_api_service.get_nodes("`Live Activity`")
        if get_response["errors"] is not None:
            return LiveActivitiesOut(errors=get_response["errors"])
        live_activities = [BasicLiveActivityOut(id=live_activity["id"],
                                                live_activity=live_activity["properties"][0]["value"])
                           for live_activity in get_response["nodes"]]

        return LiveActivitiesOut(live_activities=live_activities)

    def get_live_activity(self, live_activity_id: int):
        """
        Send request to graph api to get given live activity

        Args:
        live_activity_id (int): Id of live activity

        Returns:
            Result of request as live activity object
        """
        get_response = self.graph_api_service.get_node(live_activity_id)

        if get_response["errors"] is not None:
            return NotFoundByIdModel(id=live_activity_id, errors=get_response["errors"])
        if get_response["labels"][0] != "Live Activity":
            return NotFoundByIdModel(id=live_activity_id, errors="Node not found.")

        live_activity = {'id': get_response['id'], 'relations': [], 'reversed_relations': []}
        for property in get_response["properties"]:
            live_activity[property["key"]] = property["value"]

        relations_response = self.graph_api_service.get_node_relationships(live_activity_id)

        for relation in relations_response["relationships"]:
            if relation["start_node"] == live_activity_id:
                live_activity['relations'].append(RelationInformation(second_node_id=relation["end_node"],
                                                                      name=relation["name"],
                                                                      relation_id=relation["id"]))
            else:
                live_activity['reversed_relations'].append(RelationInformation(second_node_id=relation["start_node"],
                                                                               name=relation["name"],
                                                                               relation_id=relation["id"]))

        return LiveActivityOut(**live_activity)
