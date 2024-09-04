from scrapper import Scrapper

def main():
    # Crear una instancia de la clase Scrapper
    scraper = Scrapper('https://news.ycombinator.com/',30,5,'less','comments', True)
    scraper.run()


if __name__ == "__main__":
    main()