import os
import pytest

from selenium import webdriver
from applitools.selenium import Eyes, Target, BatchInfo, ClassicRunner
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def batch_info():
    """
    Use one BatchInfo for all tests inside module
    """
    return BatchInfo("Demo batch")


@pytest.fixture(name="driver", scope="function")
def driver_setup():
    """
    New browser instance per test and quite.
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    # Close the browser.
    driver.quit()


@pytest.fixture(name="runner", scope="session")
def runner_setup():
    """
    One test runner for all tests. Print test results in the end of execution.
    """
    runner = ClassicRunner()
    yield runner
    # Wait and collect all test results
    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results(False)
    # Print results
    print(all_test_results)


@pytest.fixture(name="eyes", scope="function")
def eyes_setup(runner, batch_info):
    """
    Basic Eyes setup. It'll abort test if wasn't closed properly.
    """
    eyes = Eyes(runner)
    # Initialize the eyes SDK and set your private API key.
    # eyes.api_key = os.environ["APPLITOOLS_API_KEY"] #good practice to set ApiKey in your env var
    eyes.api_key = "APPLITOOLS_API_KEY"
    eyes.configure.batch = batch_info
    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort()


def test_tutorial(eyes, driver):
    # Start the test and set the browser's viewport size to 800x600.
    eyes.open(driver, "Demo App", "Smoke Test", {"width": 800, "height": 600})
    # Navigate the browser to the "ACME" demo app. To see visual bugs after the first run, use the commented line below instead.
    driver.get("https://demo.applitools.com")
    # driver.get("https://demo.applitools.com/index_v2.html")

    # Visual checkpoint #1. - Check the login page. using the fluent API
    # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html?Highlight=fluent%20api
    eyes.check("", Target.window().fully().with_name("Login Window"))

    # This will create a test with two test steps.
    driver.find_element_by_id("log-in").click()

    # Visual checkpoint  #2 - Check the app page.
    eyes.check("", Target.window().fully().with_name("App Window"))

    # End the test.
    eyes.close_async()
