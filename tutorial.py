from selenium.webdriver import Chrome

from applitools.selenium import Eyes, Target, BatchInfo, ClassicRunner
from webdriver_manager.chrome import ChromeDriverManager

def set_up(eyes):

    # You can get your api key from the Applitools dashboard
    eyes.configure.set_api_key("97ELuwdIiAilbeumIilysV8yY24tygCeRFFTYEBO7EfE110")

    # set new batch
    eyes.configure.set_batch(BatchInfo("Demo batch"))


def test_demo_app(driver, eyes):
    try:
        # Set AUT's name, test name and viewport size (width X height)
        # We have set it to 800 x 600 to accommodate various screens. Feel free to change it.
        eyes.open(
            driver, "Demo App", "Smoke Test", {"width": 800, "height": 600}
        )

        # Navigate the browser to the "ACME" demo app.
        driver.get("https://demo.applitools.com")

        # To see visual bugs after the first run, use the commented line below instead.
		# driver.get("https://demo.applitools.com/index_v2.html");

        # Visual checkpoint #1 - Check the login page. using the fluent API
        # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html?Highlight=fluent%20api
        eyes.check("", Target.window().fully().with_name("Login Window"))

        #This will create a test with two test steps
        driver.find_element_by_id("log-in").click()

        # Visual checkpoint #2 - Check the app page.
        eyes.check("", Target.window().fully().with_name("App Window"))

        # End the test.
        eyes.close_async()
    except Exception as e:
        #If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort_async()
        print(e)


def tear_down(driver, runner):
    driver.quit()

    # Wait and collect all test results
    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results(False)

    #Print results
    print(all_test_results)


# Use Chrome browser
driver = Chrome(ChromeDriverManager().install())

# Initialize the Runner for your test.
runner = ClassicRunner()

# Initialize the eyes SDK
eyes = Eyes(runner)

set_up(eyes)

try:
    test_demo_app(driver, eyes)
finally:
    tear_down(driver, runner)