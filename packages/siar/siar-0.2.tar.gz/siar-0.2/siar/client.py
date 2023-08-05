import requests
from siar.decorators import siar_exceptions, response_json
from enum import Enum

API_URL = "https://servicio.mapama.gob.es/apisiar/API/v1/"


class SiarClient(object):
    class FrecuencyType(Enum):
        hourly = "horarios"
        daily = "diarios"
        weekly = "semanales"
        monthly = "mensuales"

    class DataType(Enum):
        ccaa = "ccaa"
        provincies = "provincia"
        stations = "estacion"

    def __init__(self, api_key, date_string=False, return_json=False, exceptions_enabled=True):
        super().__init__()
        self.api_key = api_key
        self.date_string = date_string
        self.return_json = return_json
        self.exceptions_enabled = exceptions_enabled

    @response_json
    @siar_exceptions
    def info_access(self):
        return requests.get(f"{API_URL}info/accesos?ClaveAPI={self.api_key}",)

    @response_json
    @siar_exceptions
    def info_ccaa(self):
        return requests.get(f"{API_URL}info/ccaa?ClaveAPI={self.api_key}",)

    @response_json
    @siar_exceptions
    def info_provincies(self):
        return requests.get(f"{API_URL}info/provincias?ClaveAPI={self.api_key}",)

    @response_json
    @siar_exceptions
    def info_stations(self):
        return requests.get(f"{API_URL}info/estaciones?ClaveAPI={self.api_key}",)

    def __data_by_type(
        self,
        frequency_type,
        data_type,
        ids,
        start_date,
        end_date=None,
        modification_date=None,
    ):
        if not end_date:
            end_date = start_date

        if isinstance(ids, str):
            ids = [ids]

        endpoint = f"{API_URL}datos/{frequency_type}/{data_type}?"
        api_key = f"claveAPI={self.api_key}"
        ids = f'&id={"&id=".join(ids)}'

        if self.date_string:
            start_date = f"&fechaInicial={start_date}"
            end_date = f"&fechaFinal={end_date}"

            if modification_date:
                modification_date = f"&fechaUltModificacion={modification_date}"
            else:
                modification_date = ""
        else:
            start_date = f'&fechaInicial={start_date.strftime("%Y-%m-%d")}'
            end_date = f'&fechaFinal={end_date.strftime("%Y-%m-%d")}'

            if modification_date:
                modification_date = f'&fechaUltModificacion={modification_date.strftime("%Y-%m-%d")}'
            else:
                modification_date = ""


        response = requests.get(
            f"{endpoint}{api_key}{ids}{start_date}{end_date}{modification_date}"
        )

        return response

    @response_json
    @siar_exceptions
    def data_ccaa_by_hours(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.hourly.value,
            self.DataType.ccaa.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_ccaa_by_day(self, ids, start_date, end_date=None, modification_date=None):
        response = self.__data_by_type(
            self.FrecuencyType.daily.value,
            self.DataType.ccaa.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_ccaa_by_week(self, ids, start_date, end_date=None, modification_date=None):
        response = self.__data_by_type(
            self.FrecuencyType.weekly.value,
            self.DataType.ccaa.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_ccaa_by_month(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.monthly.value,
            self.DataType.ccaa.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provincies_by_hours(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.hourly.value,
            self.DataType.provincies.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provincies_by_day(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.daily.value,
            self.DataType.provincies.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provincies_by_week(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.weekly.value,
            self.DataType.provincies.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provincies_by_month(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.monthly.value,
            self.DataType.provincies.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_stations_by_hours(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.hourly.value,
            self.DataType.stations.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_stations_by_day(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.daily.value,
            self.DataType.stations.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_stations_by_week(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.weekly.value,
            self.DataType.stations.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_stations_by_month(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.monthly.value,
            self.DataType.stations.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response
