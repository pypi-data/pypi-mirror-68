## Cliente python para Siar (Sistema de Información Agroclimática para el Riego)
[Pipy Siar 0.3](https://pypi.org/project/siar/0.3/)
### Configuración del Cliente

* **Instalación:**
	```python
        pip install siar
    ```
* **Uso básico:**
    ```python
    	from siar.client import SiarClient
    	siar = SiarClient(api_key="YOUR_API_KEY")
    ```
* **Por defecto:**
	* **Fechas:**: El cliente espera las fechas como un objeto Date, pero podemos inicializarlo con la opción date_string para poder usar una cadena de texto.
    	```python
    		siar = SiarClient(api_key="YOUR_API_KEY", date_string=True)
    	``` 
	* **Return:**: Por defecto devolverá el objeto Response de la petición usando el parámetro return_json podemos hacer que devuelva directamente el json de la petición.
	 	```python
            siar = SiarClient(api_key="YOUR_API_KEY", return_json=True)
        ```
	* **Excepciones:** Por defecto el cliente elevará la excepción correspondiente al código de estado devuelto por el servidor, podemos modificar este comportamiento con exceptions_enabled.
		```python
		    siar = SiarClient(api_key="YOUR_API_KEY", exceptions_enabled=False)
        ```
        
* **Funciones disponibles:**
    * **info_access**()
    * **info_ccaa**()
    * **info_provincies**()
    * **info_stations**()
    * **data_ccaa_by_hours**(ids, start_date, [end_date], [modification_date])
    * **data_ccaa_by_day**(ids, start_date, [end_date], [modification_date])
    * **data_ccaa_by_week**(ids, start_date, [end_date], [modification_date])
    * **data_ccaa_by_month**(ids, start_date, [end_date], [modification_date])
    * **data_provincies_by_hours**(ids, start_date, [end_date], [modification_date])
    * **data_provincies_by_day**(ids, start_date, [end_date], [modification_date])
    * **data_provincies_by_week**(ids, start_date, [end_date], [modification_date])
    * **data_provincies_by_month**(ids, start_date, [end_date], [modification_date])
    * **data_stations_by_hours**(ids, start_date, [end_date], [modification_date])
    * **data_stations_by_day**(ids, start_date, [end_date], [modification_date])
    * **data_stations_by_week**(ids, start_date, [end_date], [modification_date])
    * **data_stations_by_month**(ids, start_date, [end_date], [modification_date])
