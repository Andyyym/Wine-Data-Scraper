# Wine Data Scraper

## Overview

The Data Scraper is a software application designed to extract data from the Pick n Pay website, specifically focusing on wine. The application is built using Node.js and Python, leveraging the power of both languages to handle different aspects of the application.

## Architecture

The application is divided into three main components:

- Web Scraper (`main.py`): This is the core of the application. It uses Python's BeautifulSoup and requests libraries to scrape data from the Pick n Pay website. The data includes the wine name, price, image URL, promotion message, promotion end date, and stock status. The scraped data is then saved in a JSON file for further use.

- API (`API.js`): This is a Node.js Express server that serves the scraped data. It reads the data from the JSON file and provides endpoints to access the data.

- Frontend (`index.js`): This is the user interface of the application. It fetches the data from the API and displays it in a user-friendly format.

## Dependencies

The application uses several external libraries:

- Python: BeautifulSoup and requests for web scraping.
- Node.js: Express for the API server, concurrently to run multiple scripts at the same time, cors to handle Cross-Origin Resource Sharing, and nodemon for automatic server restarts during development.

## Running the Application

To run the application, the user must first clone the repository and install the dependencies using `npm install`. The application can then be started with `npm start`, which runs the web scraper, API server, and frontend concurrently.

## Future Improvements

While the application is functional, there are several areas where it could be improved:

- Error Handling: Currently, the application does not handle errors that may occur during the scraping process. Adding robust error handling would make the application more reliable.

- Data Validation: The application assumes that the data on the Pick n Pay website is always correctly formatted. Adding data validation would ensure that the application can handle unexpected data formats.

- Automated Updates: The application currently needs to be manually run to update the data. Implementing a scheduling system would allow the data to be updated automatically at regular intervals.

## Conclusion

The Wine Deals ZA Web Scraper is a powerful tool for collecting data about wine deals from the Pick n Pay website. With further development, it could become an invaluable resource for wine enthusiasts and bargain hunters alike.
