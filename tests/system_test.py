from selenium import webdriver

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Perform system test
driver.get("http://localhost:8501")  # Assuming Streamlit app runs locally
# Clean up
driver.quit()
