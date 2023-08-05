"""The gyxi module"""

from typing import Any, Mapping
from enum import Enum
from http import HTTPStatus

import requests
import attr


class GyxiRegion(Enum):
    """Available Gyxi regions"""

    WEST_EUROPE = "westeurope"
    NORTH_EUROPE = "northeurope"
    GERMANY = "germany"
    FRANCE = "france"
    UK = "uk"
    NORWAY = "norway"


@attr.s
class GyxiView:
    """Represents a Gyxi view"""

    name = attr.ib(type=str)
    data_type = attr.ib(type=str)
    partition_by = attr.ib(type=str)
    id_by = attr.ib(type=str)

    def as_request(self):
        """Returns view as a request."""

        return {
            "name": self.name,
            "type": self.data_type,
            **({'partitionBy': self.partition_by}
               if self.partition_by else {}),
            **({'idBy': self.id_by}
               if self.id_by else {})
        }


class GyxiClient:
    """Gyxi client"""

    def __init__(self, database_id: str, region: GyxiRegion):
        self.__database_id = database_id
        self.__region = region

    def save(self, data_type: str, partition: str, item_id: str, content: Any):
        """
        Saves a single item in Gyxi

        :param data_type: The data type. It is likely that it corresponds
            to a class. It is an advantage, but not a requirement, that items
            of the same type have the same properties.

        :param partition: Partition, usually by the primary foreign key
            on this item. If not partitioned, set a static value, such as "all"

        :param item_id: The unique id of this item.
            Must be unique within the partition.

        :param content: The actual item
        """

        endpoint = self.__get_endpoint("save", data_type, partition, item_id)
        response = requests.post(endpoint, json=content)

        if not response.ok:
            raise Exception("Error when saving in Gyxi {}".format(response.text))

    def save_batch(self, data_type: str, partition: str, content: Mapping[str, Any]):
        """
        Saves up to 100 items in one call, which is far faster than saving 100 individual items.
        Useful for data migrations.

        :param data_type: The type name of the data being saved

        :param partition: The partition of the items being saved.
            All items must be part of the same partition.

        :param content: A dictionary with all the items.
            The key is the id of each item and the value is the full content.
        """

        endpoint = self.__get_endpoint("batch", data_type, partition)
        response = requests.post(endpoint, json=content)

        if not response.ok:
            raise Exception(
                "Error {} when batch saving in Gyxi: {}".format(response.status_code, response.text)
            )

    def get(self, data_type: str, partition: str, item_id: str):
        """
        Gets a single item very efficiently.

        :param data_type: The name of the data type

        :param partition: The partition where the item is located

        :param item_id: The id of the item

        :return: The deserialized item or None if the item was not found.
        """

        endpoint = self.__get_endpoint("get", data_type, partition, item_id)
        response = requests.get(endpoint)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if not response.ok:
            raise Exception("Error when getting from Gyxi: {}".format(response.text))

        return response.json()

    def list(self, data_type: str, partition: str):
        """
        Gets every item of a certain type in a certain partition. Please note
        that this will get all items of that type, even if there are millions and
        it may take a while. It will get 1000 per call.

        Returns a continuation token to get the next 1000 items

        :param data_type: The name of the data type

        :param partition: The partition. It is only possible to list items from a single partition.

        :return: A list of items
        """

        endpoint = self.__get_endpoint("list", data_type, partition)
        response = requests.get(endpoint)

        if not response.ok:
            raise Exception("Error when getting list from Gyxi: {}".format(response.text))

        response_data = response.json()

        list_items = response_data["result"]
        next_page_token = response_data["nextPageToken"]

        while next_page_token is not None:
            next_list_response = requests.get(endpoint + next_page_token)

            if not next_list_response.ok:
                raise Exception("Error when getting list "
                                "with next page token from Gyxi: {}".format(response.text))

            next_list_response_data = next_list_response.json()
            next_page_token = next_list_response_data["nextPageToken"]

            list_items.extend(next_list_response_data["result"])

        return list_items

    def delete(self, data_type: str, partition: str, item_id: str):
        """
        Deletes a single item.

        :param data_type: The name of the data type

        :param partition: The partition where the item is located

        :param item_id: The id of the item
        """

        endpoint = self.__get_endpoint("delete", data_type, partition, item_id)
        response = requests.delete(endpoint)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return

        if not response.ok:
            raise Exception("Error when deleting in Gyxi: {}".format(response.text))

    def __get_endpoint(self, action: str, data_type: str, partition: str, item_id: str = ""):
        assert action in ["save", "batch", "get", "list", "delete"]

        base_url = "https://{}-{}.gyxi.com/".format(action, self.__region.value)
        path = "{}/{}/{}/{}".format(self.__database_id, data_type, partition, item_id)

        return base_url + path

    def add_view(self, view: GyxiView):
        """
        Add a new view to your database.
        The type is mandatory and it is mandatory to fill in at least
        one more field. The rest can be left blank if desired. For example,
        by filling in type and region
        only, your data will be replicated unchanged to that region.
        If you fill in partition_by then your data will be replicated to that partition.

        :param view: The view
        """

        endpoint = "https://config.gyxi.com/{}/views".format(self.__database_id)
        response = requests.post(endpoint, json=view.as_request())

        if not response.ok:
            raise Exception("Error when adding a view to Gyxi: {}".format(response.text))

    def list_view(self, data_type: str, view: str, partition: str):
        """
        Gets every item from a view. Please note
        that this will get all items of that type, even if there are millions and
        it may take a while. It will get 1000 per call.

        Returns a continuation token to get the next 1000 items

        :param data_type: The name of the data type

        :param view: The name of the view

        :param partition: The partition. It is only possible to list items from a single partition.

        :return: A list of items
        """

        endpoint = self.__get_view_endpoint("list", data_type, view, partition)
        response = requests.get(endpoint)

        if not response.ok:
            raise Exception("Error when getting list view from Gyxi: {}".format(response.text))

        response_data = response.json()

        list_items = response_data["result"]
        next_page_token = response_data["nextPageToken"]

        while next_page_token is not None:
            next_list_response = requests.get(endpoint + next_page_token)

            if not next_list_response.ok:
                raise Exception("Error when getting list view "
                                "with next page token from Gyxi: {}".format(response.text))

            next_list_response_data = next_list_response.json()
            next_page_token = next_list_response_data["nextPageToken"]

            list_items.extend(next_list_response_data["result"])

        return list_items

    def single_view(self, data_type: str, view: str, partition: str, item_id: str):
        """
        Gets a single item from a view.

        :param data_type: The name of the data type

        :param view: The name of the view

        :param partition: The partition where the item is located

        :param item_id: The id of the item

        :return: The deserialized item or None if the item was not found.
        """

        endpoint = self.__get_view_endpoint("get", data_type, view, partition, item_id)
        response = requests.get(endpoint)

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if not response.ok:
            raise Exception("Error when getting view from Gyxi: {}".format(response.text))

        return response.json()

    def __get_view_endpoint(
            self, action: str, view: str, data_type: str, partition: str, item_id: str = ""
    ):
        assert action in ["get", "list"]

        base_url = "https://{}-{}.gyxi.com/".format(action, self.__region.value)
        path = "{}/{}/view/{}/{}/{}".format(self.__database_id, data_type, view, partition, item_id)

        return base_url + path
