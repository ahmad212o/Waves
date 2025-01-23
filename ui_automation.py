import logging
from database.db import execute_or_fetch_query
from txt_parser import categorize_result
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from time import sleep
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@contextmanager
def get_service(driver_path: str = "./chromedriver"):
    """
    Context manager for managing the WebDriver service.
    It starts the service at the beginning and stops it once done.
    """
    try:
        service = Service(driver_path)
        logging.info("Starting WebDriver service...")
        yield service
    except Exception as e:
        logging.error(f"Error starting WebDriver service: {e}")
        raise
    finally:
        logging.info("Stopping WebDriver service...")
        service.stop()


@contextmanager
def get_webdriver(service: Service):
    """
    Context manager for managing the WebDriver.
    Initializes the WebDriver, and ensures it's closed after use.
    """
    options = Options()
    options.add_argument("--headless")

    try:
        logging.info("Initializing WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)
        yield driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise
    finally:
        logging.info("Closing WebDriver...")
        driver.quit()


def get_term_id(term: str):
    """
    Retrieves the ID of a search term from the database.
    Returns the term's ID or None if not found.
    """
    try:
        res = execute_or_fetch_query(
            query=f"SELECT id FROM search_terms WHERE query = '{term}'", fetch=True
        )
        if res:
            return res[-1][-1]
        else:
            logging.warning(f"No ID found for term: {term}")
            return None
    except Exception as e:
        logging.error(f"Error fetching term ID for {term}: {e}")
        return None


def find_term_10_results(driver, term: str):
    """
    Finds the top 10 search results for a given term using Bing.
    Extracts the link, headline, and description from each result.
    Returns a list of tuples with the result information.
    """
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "q")))
        input_element = driver.find_element(By.NAME, "q")
        input_element.clear()
        input_element.send_keys(term + Keys.ENTER)

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//li[contains(@class, "b_algo")]')
            )
        )

        search_elements = driver.find_elements(By.XPATH, '//li[contains(@class, "b_algo")]')
        results = []

        for element in search_elements[: min(10, len(search_elements))]:
            try:
                link_element = element.find_element(By.XPATH, ".//h2/a")
                link = link_element.get_attribute("href")
                headline = link_element.text.strip()
            except Exception as e:
                logging.error(f"Error fetching link or headline: {e}")
                link, headline = "No link available", "No headline available"

            try:
                description_element = element.find_element(
                    By.XPATH, './/p[contains(@class, "b_lineclamp3")]'
                )
                description = description_element.text.strip()
            except Exception as e:
                logging.error(f"Error fetching description: {e}")
                description = "No description available"

            results.append(
                (
                    link,
                    headline,
                    description,
                    get_term_id(term=term),
                    categorize_result(link, description),
                )
            )
        
        return results
    except Exception as e:
        logging.error(f"Error during search result processing for term {term}: {e}")
        return []


def get_terms_results(terms: list, website: str = "https://www.bing.com") -> dict:
    """
    Fetches the top 10 results for each term from a search engine.
    Returns a list of results, each containing the link, headline, description, term ID, and category.
    """
    try:
        with get_service() as svc:
            with get_webdriver(svc) as driver:
                driver.get(website)
                sleep(10)  # Allow time for the page to load
                terms_results = []
                for term in terms:
                    logging.info(f"Fetching results for term: {term}")
                    terms_results.extend(
                        tuple(find_term_10_results(driver=driver, term=term))
                    )
                logging.info("Successfully fetched results for all terms")
                return terms_results
    except Exception as e:
        logging.error(f"Error fetching results for terms: {e}")
        return {}
