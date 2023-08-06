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
        provinces = "provincia"
        stations = "estacion"

    def __init__(
        self, api_key, date_string=False, return_json=False, exceptions_enabled=True
    ):
        super().__init__()
        self.api_key = api_key
        self.date_string = date_string
        self.return_json = return_json
        self.exceptions_enabled = exceptions_enabled

    @response_json
    @siar_exceptions
    def info_access(self):
        return requests.get(
            "{api_url}info/accesos?ClaveAPI={api_key}".format(
                api_url=API_URL, api_key=self.api_key
            )
        )

    @response_json
    @siar_exceptions
    def info_ccaa(self):
        return requests.get(
            "{api_url}info/ccaa?ClaveAPI={api_key}".format(
                api_url=API_URL, api_key=self.api_key
            )
        )

    @response_json
    @siar_exceptions
    def info_provinces(self):
        return requests.get(
            "{api_url}info/provincias?ClaveAPI={api_key}".format(
                api_url=API_URL, api_key=self.api_key
            )
        )

    @response_json
    @siar_exceptions
    def info_stations(self):
        return requests.get(
            "{api_url}info/estaciones?ClaveAPI={api_key}".format(
                api_url=API_URL, api_key=self.api_key
            )
        )

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

        endpoint = "{api_url}datos/{frequency_type}/{data_type}?".format(
            api_url=API_URL, frequency_type=frequency_type, data_type=data_type
        )
        api_key = "claveAPI={api_key}".format(api_key=self.api_key)
        ids = "&id={ids_str}".format(ids_str="&id=".join(ids))

        if self.date_string:
            start_date = "&fechaInicial={start_date}".format(start_date=start_date)
            end_date = "&fechaFinal={end_date}".format(end_date=end_date)

            if modification_date:
                modification_date = "&fechaUltModificacion={modification_date}".format(
                    modification_date=modification_date
                )
            else:
                modification_date = ""
        else:
            start_date = "&fechaInicial={start_date_str}".format(
                start_date_str=start_date.strftime("%Y-%m-%d")
            )
            end_date = "&fechaFinal={end_date_str}".format(
                end_date_str=end_date.strftime("%Y-%m-%d")
            )

            if modification_date:
                modification_date = "&fechaUltModificacion={modification_date_str}".format(
                    modification_date_str=modification_date.strftime("%Y-%m-%d")
                )
            else:
                modification_date = ""

        response = requests.get(
            "{endpoint}{api_key}{ids}{start_date}{end_date}{modification_date}".format(
                endpoint=endpoint,
                api_key=api_key,
                ids=ids,
                start_date=start_date,
                end_date=end_date,
                modification_date=modification_date,
            )
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
    def data_provinces_by_hours(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.hourly.value,
            self.DataType.provinces.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provinces_by_day(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.daily.value,
            self.DataType.provinces.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provinces_by_week(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.weekly.value,
            self.DataType.provinces.value,
            ids,
            start_date,
            end_date=None,
            modification_date=None,
        )
        return response

    @response_json
    @siar_exceptions
    def data_provinces_by_month(
        self, ids, start_date, end_date=None, modification_date=None
    ):
        response = self.__data_by_type(
            self.FrecuencyType.monthly.value,
            self.DataType.provinces.value,
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
