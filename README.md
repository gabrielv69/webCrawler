# webCrawler
A web crawler using scraping techniques to extract the first 30 entries from https://news.ycombinator.com/.

## Installation

Use [git](https://git-scm.com/downloads) to clone the repository


This project was generated with [Python](https://www.python.org/) version 3.12.5

```bash
git clone https://github.com/gabrielv69/webCrawler.git
```
Open the project, it is recommended to use [VisualStudio] (https://code.visualstudio.com/)

Inside the ide, open a terminal and execute the following line to create a virtual environment
```bash
python -m virtualenv venv
```
Execute the following line to activate the environment
Windows
```bash
.\venv\Scripts\activate
```
Linux
```bash
source venv/bin/activate
```

Optional: If you get an error about disabling scripts in Windows run the following command and then run the previous command again:
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

With the following command we install the libraries in the environment
```bash
pip install -r .\requirements.txt
```
After installing angular, we can run the project, using the command:
```bash
python scrapper.py <url> <num_entries> <word_limit> <word_count_filter> <order_by> <order>
```
Arguments description:

    <num_entries>: The number of entries you wish to scrape (for example, 30 for the first 30 entries).
    <word_limit>: The word limit to use for filtering entries by title (e.g., 5 for entries with titles of 5 words or less).
    <word_count_filter>: The filter criteria based on the length of the title. It can be:
        less: To filter titles with less than or equal to <word_limit> words.
        more: To filter titles with more than <word_limit> words.
    <order_by>: The sorting criteria for the entries. It can be:
        points: To sort entries by points.
        comments: To sort the entries by number of comments.
    <order>: Descending or ascending order. Can be:
        DESC: Order descending (highest to lowest).
        ASC: Sort in ascending order (lowest to highest).
Example
```bash
python main.py 30 5 less comments ASC
```
Tests can be run using
```bash
python -m unittest discover tests
```
