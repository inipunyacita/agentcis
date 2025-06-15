from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import mysql.connector

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


def scrape_to_db():
    """Scrape today's macro events from FinancialJuice and store them in the DB."""
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    def insert_to_db(data):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_cisscrapper",
            )
            cursor = conn.cursor()
            for item in data:
                try:
                    cursor.execute(
                        """
                        INSERT IGNORE INTO events (data_time, time_str, title, actual, forecast, previous)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            item["data_time"],
                            item["time"],
                            item["title"],
                            item["actual"],
                            item["forecast"],
                            item["previous"],
                        ),
                    )
                except Exception as insert_error:
                    print(f"Insert error: {insert_error}")
                    continue
            conn.commit()
            print(f"{cursor.rowcount} rows inserted into DB.")
            cursor.close()
            conn.close()
        except mysql.connector.Error as db_err:
            print(f"Database error: {db_err}")

    try:
        # Step 1: Navigate to homepage
        driver.get("https://www.financialjuice.com/home")
        time.sleep(2)  # Allow initial page load

        # Step 2: Click Sign In link
        sign_in_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#LoginTab' and contains(text(), 'Sign In')]")
        ))
        sign_in_link.click()
        time.sleep(5)

        # Step 3: Enter email
        email_field = wait.until(
            EC.presence_of_element_located((By.NAME, "ctl00$SignInSignUp$loginForm1$inputEmail"))
        )
        email_field.send_keys(EMAIL)

        # Step 4: Enter password
        password_field = driver.find_element(By.NAME, "ctl00$SignInSignUp$loginForm1$inputPassword")
        password_field.send_keys(PASSWORD)

        # Step 5: Click login button
        login_button = driver.find_element(By.XPATH, "//input[@value='Login' and @type='submit']")
        login_button.click()

        # Verify login using the user span element
        logged_in_element = wait.until(
            EC.visibility_of_element_located((By.ID, "ctl00_header1_Login1_lblLoggedInUser"))
        )
        print(f"Login successful! Welcome message: {logged_in_element.text}")

        print("Starting data scraping process...")

        # Click filter icon
        filter_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-filter")))
        filter_icon.click()
        time.sleep(1)

        # Uncheck checkboxes
        for checkbox_id in ["2", "3"]:
            checkbox = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input.cal-imp-checkbox[id='{checkbox_id}']"))
            )
            if checkbox.is_selected():
                checkbox.click()
            time.sleep(0.5)

        # Close filter menu
        close_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'CloseCalenderFilters')]")
        ))
        close_button.click()
        time.sleep(2)

        current_date = datetime.now().date()
        print(f"Scraping events for date: {current_date}")

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event-header")))
        elements = driver.find_elements(By.CSS_SELECTOR, "div.event-header")

        scraped = []
        for event in elements:
            try:
                data_time = event.get_attribute("data-time")
                event_date = datetime.fromisoformat(data_time).date()
                if event_date != current_date:
                    continue

                first_row = event.find_element(By.CSS_SELECTOR, ".div-table-row:first-child")
                time_el = first_row.find_element(By.CSS_SELECTOR, ".event-time")
                title_el = first_row.find_element(By.CSS_SELECTOR, ".event-title")

                second_row = event.find_element(By.CSS_SELECTOR, ".div-table-row:nth-child(2)")
                actual_el = second_row.find_element(By.CSS_SELECTOR, "[class*='event-actual']")
                forecast_el = second_row.find_element(By.CSS_SELECTOR, "[class*='event-forcast']")
                previous_el = second_row.find_element(By.CSS_SELECTOR, ".event-previous")

                scraped.append(
                    {
                        "data_time": data_time,
                        "time": time_el.text.strip() if time_el.text.strip() != "-" else "N/A",
                        "title": title_el.text.strip() if title_el.text.strip() != "-" else "N/A",
                        "actual": actual_el.text.strip() if actual_el.text.strip() != "-" else "N/A",
                        "forecast": forecast_el.text.strip() if forecast_el.text.strip() != "-" else "N/A",
                        "previous": previous_el.text.strip() if previous_el.text.strip() != "-" else "N/A",
                    }
                )
            except Exception as e:
                print(f"Error processing event: {e}")

        if scraped:
            insert_to_db(scraped)
        print(f"Found {len(scraped)} events for {current_date}")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot('error_screenshot.png')
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_to_db()
