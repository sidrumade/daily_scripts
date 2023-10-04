from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import sqlite3


# Specify the directory path where the Edge WebDriver executable is located
edge_driver_directory = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\"  # Replace with the actual directory path

# Add the directory to the PATH environment variable
os.environ['PATH'] += os.pathsep + edge_driver_directory

# Set up Edge WebDriver options
edge_options = webdriver.EdgeOptions()

# Enable headless mode
edge_options.add_argument("--headless")


#load executable from 
driver = webdriver.Edge(edge_options)

# Load the Amazon page
url = "https://www.amazon.in/Acer-Display-Premium-Windows-SFG14-71/dp/B0C3CKFMK8/"

driver.get(url)

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(5)

# Get the page source
page_source = driver.page_source


# Close the browser
driver.quit()

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Now you can work with the parsed HTML content (e.g., extract data)
# Example: title of the page
title = soup.find('title').text
price_element = soup.find('div', class_="a-section a-spacing-none aok-align-center")
price_str = price_element.find('span', class_="a-offscreen").text

# Remove non-numeric characters (such as currency symbol and commas)
numeric_price_str = ''.join(filter(str.isdigit, price_str))
# Convert the numeric string to an integer
price_int = int(numeric_price_str)

print('*****************************',price_int)


conn = sqlite3.connect('my_database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()


if 'amazondb.db' not in os.listdir():

    # Define the table schema
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    '''

    # Execute the SQL statement to create the table
    cursor.execute(create_table_sql)
    # Commit the changes to the database
    conn.commit()


# Insert the data into the table
insert_data_sql = '''
INSERT INTO products (title, price) VALUES (?, ?)
'''

# Execute the SQL statement to insert data
cursor.execute(insert_data_sql, (title, price_int))

# Commit the changes to the database
conn.commit()


