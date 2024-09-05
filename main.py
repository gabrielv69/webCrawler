from src.scrapper import Scrapper
import argparse

def main(): 
    parser = argparse.ArgumentParser(description="Scraper de Hacker News")

    parser.add_argument('num_entries', type=int, help='Number of entries to be scraped')
    parser.add_argument('word_limit', type=int, help='Filter word limit')
    parser.add_argument('word_count_filter', type=str, choices=['less', 'more'], help='Word count filter (less or more)')
    parser.add_argument('order_by', type=str, choices=['points', 'comments'], help='Sort by (points or comments)')
    parser.add_argument('order', type=str, choices=['ASC', 'DESC'], help='Descending (DESC) or ascending (ASC)')
    
    # Parsear los argumentos
    args = parser.parse_args()

    # Crear una instancia de Scrapper usando los argumentos de la consola
    scraper = Scrapper('https://news.ycombinator.com/', args.num_entries, args.word_limit, args.word_count_filter, args.order_by, args.order=="DESC")
    scraper.run()


if __name__ == "__main__":
    main()