import logging
from database.db import execute_or_fetch_query, init_db
from txt_parser import terms_file_parser
from ui_automation import get_terms_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    try:
        # Initialize the database
        init_db()
        logging.info("Database initialized or verified.")

        # Parse search terms from file
        terms = terms_file_parser()
        logging.info(f"Retrieved {len(terms)} search terms from the file.")

        # Fetch search results for the terms
        results = get_terms_results(terms=terms)
        logging.info(f"Retrieved search results for {len(terms)} terms.")

        # Insert terms into the search_terms table, ignoring duplicates
        execute_or_fetch_query(
            query="INSERT OR IGNORE INTO search_terms (query) VALUES (?)",
            params=[(term,) for term in terms],
        )
        logging.info(f"Inserted {len(terms)} terms into the search_terms table.")

        # Insert search results into the search_results table
        execute_or_fetch_query(
            query="INSERT OR IGNORE INTO search_results (url,title,snippet, search_term_id,content_type) VALUES (?,?,?,?,?)",
            params=results,
        )
        logging.info(f"Inserted {len(results)} results into the search_results table.")

        # Fetch and print all results to confirm insertion
        all_results = execute_or_fetch_query(
            query="select * from search_results", fetch=True
        )
        logging.info(f"Fetched {len(all_results)} search results from the database.")
        logging.debug(f"Data Fetched From Table {all_results}")

    except Exception as e:
        logging.error(f"An error occurred during the execution: {e}")
        print(f"An error occurred: {e}")


if "__main__" == __name__:
    main()
