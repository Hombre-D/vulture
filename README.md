# VULture
Vulnerability Detection using Machine Learning

# Database
These files are used to build a complete, populated sqlite3 database from scratch. The web scraping portion takes a few hours, so be prepared. To avoid this, you can find the database 'vulture.db' at https://drive.google.com/drive/u/0/folders/1wOp8v815nbLFAzvJJIOratD6YwikUbP1

# How to build from scratch
1. After cloning, you'll want to cd to the project directory and run $pipenv shell in the terminal, to set up dependencies.
2. You'll also want to set up a sqlite3 database called vulture.db in the project directory. Instructions for this can be found online. Most major Linux distros have it installed.
3. Run processJSON.py to extract what you need from the JSON files in the 'Linux' folder.
4. Run scrape_repo.py to get the code files. This is going to be a lot of data.
5. Run scrape_func_names to get the function names we need for step 7.
6. Run process_text.py to remove any comments from the code.
7. Run build_functions.py to build the functions.