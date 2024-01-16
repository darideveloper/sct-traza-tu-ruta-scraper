from time import sleep
from web_scraping import WebScraping

class Scraper(WebScraping):
    """ Get the total price for mexico transpotation """
    
    def __init__(self):
        
        # Start scraper and load home page
        super().__init__()
        self.home_page = "https://app.sct.gob.mx/sibuac_internet/" \
            "ControllerUI?action=cmdEscogeRuta"
    
    def __load_page__(self):
        """ Load home page """
        self.set_page(self.home_page)
        self.refresh_selenium()

    def search(self, from_state: str, from_city: str, to_state: str, to_city: str,
               vehicle: str) -> tuple:
        """ Search for a route and get total price
        
        Args:
            from_state (str): State of origin
            from_city (str): City of origin
            to_state (str): State of destination
            to_city (str): City of destination
            vehicle (str): Vehicle type
            
        Returns:
            tuple:
                str: value (tottal price or error message)
                bool: True if success, False if error
        """
        
        print(
            f"Searching for {vehicle} from {from_state}",
            f"{from_city} to {to_state} {to_city}..."
        )
        
        self.__load_page__()
        
        # css selecrors
        selectors = {
            "btn": 'input[name="cmdEnviar"]'
        }
        
        # Class attribute for drop down elements and values to set
        drop_downs = {
            "from state": {
                "name_attr": "edoOrigen",
                "value": from_state
            },
            "from city": {
                "name_attr": "ciudadOrigen",
                "value": from_city
            },
            "to state": {
                "name_attr": "edoDestino",
                "value": to_state
            },
            "to city": {
                "name_attr": "ciudadDestino",
                "value": to_city
            },
            "vehicle": {
                "name_attr": "vehiculos",
                "value": vehicle
            }
        }
        
        # Set values in select elements
        for name, dropdown_data in drop_downs.items():
        
            name_attr = dropdown_data["name_attr"]
            value = dropdown_data["value"]
            selector = f"select[name='{name_attr}']"
        
            try:
                self.select_drop_down_text(selector, value)
            except Exception:
                error = f'Error setting "{value}" in "{name}"'
                print(error)
                return error, False
            else:
                sleep(1)
            
        # Send form
        self.click_js(selectors["btn"])
        
        
if __name__ == "__main__":
    scraper = Scraper()
    scraper.search("Jalisco", "Guadalajara", "Jalisco", "Zapopan", "Automóvil")
    scraper.search("Jalisco", "Guadalajara", "Sonora", "Hermosillo", "Pick Ups")
    scraper.search("Jalisco", "Guadalajara", "Michoacan", "Morelia", "Automovil")
    scraper.search("Jalisco", "Guadalajara", "Michoacan", "Morelia", "Camión 5 ejes")
        