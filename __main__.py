import os
from libs.logs import logger
from libs.scraper import Scraper
from libs.xlsx import SpreadsheetManager


def main():
    """ Get routes total price, using and saving data from in excel """
    
    input("Close the excel. Press enter to continue")
    
    # Initialize scraper
    scraper = Scraper()
    
    # Validate excel file
    current_folder = os.path.dirname(__file__)
    file_name = os.path.join(current_folder, "data.xlsx")
    if not os.path.exists(file_name):
        logger.error(f"File {file_name} not found")
        quit()
        
    # Initialize excel file
    ss_manager = SpreadsheetManager(file_name)
    
    # Validate sheet
    try:
        ss_manager.set_sheet("Scraper")
    except Exception:
        logger.info('Sheet "Scraper" not found')
        quit()
        
    # Get data from excel and clean it
    excel_data = ss_manager.get_data()
    excel_data = list(filter(lambda row: row[1], excel_data[2:]))

    # Scraper each route from excel
    for row in excel_data:
        
        # Get total (or error message)
        total = scraper.search(
            from_state=row[1],
            from_city=row[2],
            to_state=row[3],
            to_city=row[4],
            vehicle=row[5]
        )
        
        # Save total in excel
        row_index = excel_data.index(row) + 3
        ss_manager.write_cell(total, row_index, 7)
        ss_manager.save()
        
    input("Done. Press enter to exit")
        
        
if __name__ == "__main__":
    main()