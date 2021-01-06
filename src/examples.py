from datetime import datetime
from src.reporter import ReportCreator, TestAppender
from concurrent.futures import ThreadPoolExecutor, as_completed


def single_run():
    # Set the default config
    suite_name = "Ben"
    grid_address = "http://localhost:4444/wd/hub"
    log_level = "INFO"
    thread_count = "2"
    database = "Cucumber-QA"
    re_run = "No"
    # Set the output path
    output_path = "../report/single_thread"
    # Create the reporter object
    reporter = ReportCreator(suite_name=suite_name, grid_address=grid_address,
                             log_level=log_level,
                             thread_count=thread_count, database=database,
                             re_run=re_run, output_path=output_path)
    # Create a test1 object to appender the logs
    test1 = TestAppender(test_name="Hello", feature_name="MyFeature", reporter=reporter)
    test1.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Set the run-time test data if you want
    test1.set_test_data(datas={"name": "selenium"})
    # Add steps
    test1.appender_step(step_status="failed", step_description="This is for test",
                        use_data="selenium",
                        find_by="xpath=id",
                        step_details="details")
    test1.appender_step(step_status="passed", step_description="This is for test",
                        use_data="selenium",
                        find_by="xpath=id",
                        step_details="details")
    # Completed if you finished your test1
    test1.completed()
    # Create a test2 object to appender the logs
    test2 = TestAppender(test_name="Hello2", feature_name="MyFeature2", reporter=reporter)
    test2.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Set the run-time test data if you want
    test2.set_test_data(datas={"name": "selenium2"})
    # Add steps
    test2.appender_step(step_status="passed", step_description="This is for test2",
                        use_data="selenium2",
                        find_by="xpath=id",
                        step_details="details2")
    test2.appender_step(step_status="passed", step_description="This is for test2",
                        use_data="selenium2",
                        find_by="xpath=id",
                        step_details="details2")
    # Completed if you finished your test2
    test2.completed()
    # Completed if you finished your tests
    reporter.completed(add_excel=True, screenshot_folder="../screenshots")


def test_runner(reporter_object, number):
    number = str(number)
    test = TestAppender(test_name="Hello" + number,
                        feature_name="MyFeature" + number, reporter=reporter_object)
    test.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Set the run-time test data if you want
    test.set_test_data(datas={"name": "selenium" + number})
    # Add steps
    test.appender_step(step_status="failed", step_description="This is for test" + number,
                       use_data="selenium",
                       find_by="xpath=id",
                       step_details="details" + number)
    test.appender_step(step_status="passed", step_description="This is for test" + number,
                       use_data="selenium",
                       find_by="xpath=id",
                       step_details="details" + number)
    test.completed()
    return f"Done task:{number}"


def multiple_run():
    # Set the default config
    suite_name = "Ben"
    grid_address = "http://localhost:4444/wd/hub"
    log_level = "INFO"
    thread_count = "2"
    database = "Cucumber-QA"
    re_run = "No"
    # Set the output path
    output_path = "../report/multiple_thread"
    # Create the reporter object
    reporter = ReportCreator(suite_name=suite_name, grid_address=grid_address,
                             log_level=log_level,
                             thread_count=thread_count, database=database, re_run=re_run,
                             output_path=output_path)
    with ThreadPoolExecutor(max_workers=9) as t:
        task_list = []
        for i in range(10):
            task = t.submit(test_runner, reporter_object=reporter, number=i)
            task_list.append(task)
        for future in as_completed(task_list):
            data = future.result()
            print(f"{data}")
    # Input the screenshots folder.
    # Please note the folder is up to what you have already created
    reporter.completed(add_excel=True, screenshot_folder="../screenshots")


def api_run():
    # Set the default config
    suite_name = "Ben"
    grid_address = "N/A"
    log_level = "INFO"
    thread_count = "2"
    database = "Cucumber-QA"
    re_run = "No"
    # Set the output path
    output_path = "../report/api"
    # Create the reporter object
    reporter = ReportCreator(suite_name=suite_name, grid_address=grid_address,
                             log_level=log_level,
                             thread_count=thread_count, database=database,
                             re_run=re_run, output_path=output_path)
    # Create a test object to appender the logs
    test = TestAppender(test_name="ApiHello", feature_name="ApiFeature",
                        reporter=reporter, client="api")
    test.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    test.appender_step(step_status="passed", step_description="Request url:/baidu",
                       step_details="Current request full url: http://www.baidu.com")
    test.set_test_data(datas={"api": "api"})
    # You have to add the request api details for each case:
    api_details = [
        {"method": "GET", "url": "http://www.baidu.com", "body": "{\"body\":\"ssss\"}",
         "statusCode": "200",
         "header": "{\"header\":\"ssss\"}",
         "responseHeader": "{\"responseHeade\":\"ssss\"}",
         "responseBody": "{\"responseBody\":\"ssss\"}"}]
    test.set_api_details(api_details)
    test.completed()
    reporter.completed(add_excel=False)


if __name__ == '__main__':
    # Single thread to generate the report
    single_run()
    # # Multiple thread to generate the report
    multiple_run()
    # # Api run
    api_run()
