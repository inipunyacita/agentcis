from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta

# Configure your credentials
EMAIL = "cita25xfiles@gmail.com"
PASSWORD = "Neya12rcita!"

# Set up headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # New headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Set up driver (update path if needed)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    # Step 1: Navigate to homepage
    driver.get("https://www.financialjuice.com/home")
    time.sleep(2)  # Allow initial page load

    # Step 2: Click Sign In link
    sign_in_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='#LoginTab' and contains(text(), 'Sign In')]")
    ))
    sign_in_link.click()

    # Wait for login form to appear
    time.sleep(5)

    # Step 3: Enter email
    email_field = wait.until(EC.presence_of_element_located(
        (By.NAME, "ctl00$SignInSignUp$loginForm1$inputEmail")
    ))
    email_field.send_keys(EMAIL)

    # Step 4: Enter password
    password_field = driver.find_element(By.NAME, "ctl00$SignInSignUp$loginForm1$inputPassword")
    password_field.send_keys(PASSWORD)

    # Step 5: Click login button
    login_button = driver.find_element(By.XPATH, "//input[@value='Login' and @type='submit']")
    login_button.click()

    # Verify login using the user span element
    logged_in_element = wait.until(EC.visibility_of_element_located(
        (By.ID, "ctl00_header1_Login1_lblLoggedInUser")
    ))
    print(f"Login successful! Welcome message: {logged_in_element.text}")

    # Add your scraping logic here after successful login
        # ... [Previous login code] ...

    # After successful login
    print("Starting data scraping process...")

    # 1. Click filter icon
    filter_icon = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "i.fa-filter")
    ))
    filter_icon.click()
    print("Opened filters menu")
    time.sleep(1)

    # 2. Uncheck checkboxes
    checkbox_ids = ["2", "3"]
    for checkbox_id in checkbox_ids:
        checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input.cal-imp-checkbox[id='{checkbox_id}']")
        ))
        if checkbox.is_selected():
            checkbox.click()
            print(f"Unchecked checkbox {checkbox_id}")
        time.sleep(0.5)

    # 3. Click Close button
    close_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@onclick, 'CloseCalenderFilters')]")
    ))
    close_button.click()
    print("Closed filters menu")
    time.sleep(2)

    try:
        # ... [Previous login and filter setup code] ...

        # 4. Get and process events with the specific structure
        current_date = datetime.now().date()  # Adjust timezone if needed
        print(f"Scraping events for date: {current_date}")

        # Get all event headers
        events = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.event-header")
        ))
        elements = driver.find_elements(By.CSS_SELECTOR, "div.event-header")

        scraped_data = []
        for event in elements:
            try:
                # Get data-time attribute
                data_time = event.get_attribute("data-time")
                event_date = datetime.fromisoformat(data_time).date()
                
                # Filter by current date
                if event_date != current_date:
                    continue

                # Extract main information from first div-table-row
                first_row = event.find_element(By.CSS_SELECTOR, ".div-table-row:first-child")
                time_element = first_row.find_element(By.CSS_SELECTOR, ".event-time")
                title_element = first_row.find_element(By.CSS_SELECTOR, ".event-title")
                
                # Extract details from second div-table-row
                second_row = event.find_element(By.CSS_SELECTOR, ".div-table-row:nth-child(2)")
                actual_element = second_row.find_element(By.CSS_SELECTOR, "[class*='event-actual']")
                forecast_element = second_row.find_element(By.CSS_SELECTOR, "[class*='event-forcast']")
                previous_element = second_row.find_element(By.CSS_SELECTOR, ".event-previous")

                event_data = {
                    "data_time": data_time,
                    "time": time_element.text.strip() if time_element.text.strip() != "-" else "N/A",
                    "title": title_element.text.strip() if title_element.text.strip() != "-" else "N/A",
                    "actual": actual_element.text.strip() if actual_element.text.strip() != "-" else "N/A",
                    "forecast": forecast_element.text.strip() if forecast_element.text.strip() != "-" else "N/A",
                    "previous": previous_element.text.strip() if previous_element.text.strip() != "-" else "N/A",
                }
                
                scraped_data.append(event_data)
                # insert scraping result to db_cis
                import mysql.connector

                def insert_to_db(data):
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",        # Default XAMPP user
                            password="",        # Default XAMPP password is empty
                            database="db_cisscrapper"
                        )
                        cursor = conn.cursor()

                        for item in data:
                            try:
                                cursor.execute("""
                                    INSERT IGNORE INTO events (data_time, time_str, title, actual, forecast, previous)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    item["data_time"],
                                    item["time"],
                                    item["title"],
                                    item["actual"],
                                    item["forecast"],
                                    item["previous"],
                                ))
                            except Exception as insert_error:
                                print(f"Insert error: {insert_error}")
                                continue

                        conn.commit()
                        print(f"{cursor.rowcount} rows inserted into DB.")
                        cursor.close()
                        conn.close()

                    except mysql.connector.Error as db_err:
                        print(f"Database error: {db_err}")


            except Exception as e:
                print(f"Error processing event: {str(e)}")
                continue
        if scraped_data:
            insert_to_db(scraped_data)

        print(f"\nFound {len(scraped_data)} events for {current_date}")
        
        # Print results
        for idx, event in enumerate(scraped_data, 1):
            print(f"\nEvent #{idx}:")
            print(f"Time: {event['time']}")
            print(f"Title: {event['title']}")
            print(f"Actual: {event['actual']}")
            print(f"Forecast: {event['forecast']}")
            print(f"Previous: {event['previous']}")
            print(f"Full Timestamp: {event['data_time']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.save_screenshot('error_screenshot.png')

    finally:
        driver.quit()

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Keep browser open or close it
    # driver.quit()
    pass

