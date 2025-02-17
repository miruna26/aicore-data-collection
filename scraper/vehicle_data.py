from uuid import uuid4
import json
import os
import urllib.request
import pandas as pd

class Vehicle_data:
    """
    Template class for storing vehicle data for each vehicle.
    """
    def __init__(self, vehicle_id, uuid=None):
        self.__vehicle_id = vehicle_id
        self.__UUID = str(uuid4()) if not uuid else uuid
        self.__data = {
            "href" : None,
            "title" : None,
            "subtitle" : None,
            "price" : None,
            "location" : None,
            "mileage" : None,
            "description" : None,
            "img" : []
        }

    def __download_images(self, path):
        """
        Downloads image data from the given img src addresses stored within Vehicle_data.
        File are output in the following location:
            path/vehicle_id/images/vehicle_id_index.jpg
        """
        if not os.path.exists(f"{path}/{self.__vehicle_id}/images"):
            os.makedirs(f"{path}/{self.__vehicle_id}/images")
        img_index = 0
        for img_url in self.__data['img']:
            img_path = f"{path}/{self.__vehicle_id}/images/{self.__vehicle_id}_{img_index}.jpg"
            urllib.request.urlretrieve(img_url, img_path)
            img_index += 1
    def __save_JSON(self, path):
        """
        Saves Vehicle_data to JSON format in the following location:
            path/vehicle_id/data.json
        """
        if not os.path.exists(f"{path}/{self.__vehicle_id}"):
            os.makedirs(f"{path}/{self.__vehicle_id}")
        else:
            print(f"Veh id {self.__vehicle_id} already exists!")
            
        json_object = json.dumps(self.get_data(), indent=4)
        with open(f"{path}/{self.__vehicle_id}/data.json", 'w') as of:
            of.write(json_object)

    def add_data(self, **kwargs):
        """
        Adds data to the existing Vehicle_data object.
        Args:
            **kwargs (key = value): Input key/value pairs which are present in the Vehicle_data class template.
        """
        for key, value in kwargs.items():
            if key == "img":
                if not isinstance(value, list):
                    raise TypeError("img type must be a list.")
                for v in value:
                    if v not in self.__data[key]:
                        self.__data[key].append(v)
            elif key in self.__data:
                if self.__data[key]:
                    print(f"Overwriting vehicle data ID {self.__vehicle_id}: {key} : {self.__data[key]} -> {value}")
                self.__data[key] = value
            else:
                raise KeyError("Invalid key in vehicle data entry")
    def get_data(self, flattened=False) -> dict:
        """
        Returns Vehicle_data in dictionary format.
        Returns:
            dict: Vehicle_data in {id:, uuid:, data:{}} format.
        """
        data_dict = {
            "id" : self.__vehicle_id,
            "uuid" : self.__UUID
        }
        if flattened:
            data_dict.update(self.__data)
        else:
            data_dict['data'] = self.__data
        return data_dict
    def get_url(self) -> str:
        """
        Returns:
            str: URL for Vehicle_data
        """
        return self.__data["href"]
    def get_id(self) -> str:
        """
        Returns:
            str: Autotrader unique ID for Vehicle_data
        """
        return self.__vehicle_id
    def save_data(self, path="raw_data"):
        """
        Downloads images and saves JSON data for Vehicle_data in file structure:
            path/vehicle_id/
        """
        self.__save_JSON(path)
        self.__download_images(path)

    @staticmethod
    def import_vehicle_data_list(path) -> list:
        """
        Reads a JSON file containing a list of Vehicle_data objects and outputs list
        """
        with open(path, 'r') as of:
            vehicle_data_list_from_json = json.load(of)
        vehicle_data_list = []
        for vehicle in vehicle_data_list_from_json:
            vehicle_data = Vehicle_data(vehicle['id'], vehicle['uuid'])
            vehicle_data.add_data(**vehicle['data'])
            vehicle_data_list.append(vehicle_data)
        return vehicle_data_list

    @staticmethod
    def get_pandas_vehicle_data_list(vehicle_data_list) -> pd.DataFrame:
        """
        Returns list of Vehicle_data objects as pandas df.
        Args:
            vehicle_data_list (list[Vehicle_data]): List of Vehicle_data objects
        Returns:
            (Dataframe): Vehicle data
        """
        data = []
        for vehicle in vehicle_data_list:
            vehicle_data = vehicle.get_data(flattened=True)
            data.append(vehicle_data)
        return pd.DataFrame(data)
