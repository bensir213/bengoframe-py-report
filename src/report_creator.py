from datetime import datetime
import shutil
from threading import Lock
import json
from bs4 import BeautifulSoup
import os

root_path = os.path.dirname(__file__)


# Only for BenGoFrame Report
# This report will not create html by code
# Just generate test data details and modify to index.html in template folder
# Please do not delete or modify the fields in template folder
# testData.json is the copy file to display all test results.
class ReportCreator:
    def __init__(self, suite_name, grid_address, log_level, thread_count, database, re_run,
                 output_path, start_time=""):
        """
        :param suite_name: Required
        :param grid_address: Required
        :param log_level: Required
        :param thread_count: Required
        :param database: Required
        :param re_run: Required
        :param output_path: Required
        :param start_time: string and Format (%Y-%m-%d %H:%M:%S).
        Will generate the start time when you create the reporter object if you don't input the start_time
        """
        self.output_path = output_path
        self.suite_name = suite_name
        self.grid_address = grid_address
        self.log_level = log_level
        self.thread_count = thread_count
        self.database = database
        self.re_run = re_run
        if not start_time:
            self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.start_time = start_time
        self.end_time = ""
        self.take_times = ""
        self.testDetails = []
        self.testAll = {}
        self.config = self._set_config()
        self.appender = {}
        self.lock = Lock()

    def set_appender(self, name, appender):
        self.lock.acquire()
        try:
            self.appender[name] = appender
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def get_appender(self, name):
        return self.appender[name]

    def _set_config(self):
        config = {
            "testSuite": self.suite_name,
            "gridAddress": self.grid_address,
            "logLevel": self.log_level,
            "threadCount": self.thread_count,
            "database": self.database,
            "reRun": self.re_run,
            "startTime": self.start_time
        }
        return config

    def add_test_details(self, test_details):
        self.lock.acquire()
        try:
            self.testDetails.append(test_details)
            self.lock.release()
        except Exception as e:
            self.lock.release()
            raise e

    def completed(self, screenshot_folder=""):
        time_format = '%Y-%m-%d %H:%M:%S'
        try:
            if not self.testDetails:
                raise Exception("You need create TestAppender and log test steps")
            # Reporter will log the end time when user call completed
            self.end_time = datetime.now().strftime(time_format)
            self.config['endTime'] = self.end_time
            take_times = str(
                datetime.strptime(self.end_time, time_format) - datetime.strptime(self.start_time, time_format))
            group_times = take_times.split(":")
            self.config['takeTimes'] = f'{group_times[0]} hs {group_times[1]} mins {group_times[2]} ss'
            # To build the summary details
            self._summary()
            # To build the feature summary details
            self._feature_summary()
            self.testAll['testDetails'] = self.testDetails
            self.testAll['testConfig'] = self.config
            # Copy the template report
            self._create_report_to()
            if not screenshot_folder:
                print("Your report will not display the screenshot if you didn't package your screenshot folder")
            else:
                # Copy the input screenshot folder to report path src/static/img
                shutil.copytree(f'{screenshot_folder}', f'{self.output_path}/static/img', dirs_exist_ok=True)
            # Set the json into the html
            self._modify_html()
        except Exception:
            raise Exception("Create report failed. Please make sure you had appended the test steps")

    def _create_report_to(self):
        try:
            template_path = os.path.join(root_path, "template")
            index_path = os.path.join(root_path, "template/index.html")
            static_path = os.path.join(root_path, "template/static")
            if not os.path.exists(template_path):
                raise Exception("Please check if your template folder exist in src folder")
            elif not os.path.exists(index_path):
                raise Exception("Please check if your index.html exist in src/template folder")
            elif not os.path.exists(static_path):
                raise Exception("Please check if your static folder exist in src/template folder")
            shutil.copytree(template_path, self.output_path, dirs_exist_ok=True)
        except Exception as e:
            raise e

    def _summary(self):
        try:
            total_cases = len(self.testDetails)
            total_passed = 0
            total_failed = 0
            total_steps = 0
            total_passed_steps = 0
            total_failed_steps = 0
            for detail in self.testDetails:
                steps = detail['steps']
                total_steps += len(steps)
                if detail['status'] == 'passed':
                    total_passed += 1
                else:
                    total_failed += 1
                for step in steps:
                    if step['stepStatus'] == 'passed':
                        total_passed_steps += 1
                    else:
                        total_failed_steps += 1
            cases_chart = {'totalCases': total_cases, "passed": total_passed, "failed": total_failed}
            steps_chart = {'totalSteps': total_steps, "passed": total_passed_steps, "failed": total_failed_steps}
            self.testAll['casesChart'] = cases_chart
            self.testAll['stepsChart'] = steps_chart
        except Exception as e:
            raise e

    def _feature_summary(self):
        try:
            features = {}
            for detail in self.testDetails:
                summary = {"total": 0, "passed": 0, "failed": 0}
                feature_name = detail['featureName']
                feature_status = detail['status']
                if feature_name not in features:
                    if feature_status == 'passed':
                        summary['passed'] = 1
                    else:
                        summary['failed'] = 1
                    summary['total'] = 1
                    features[feature_name] = summary
                else:
                    if feature_status == 'passed':
                        features[feature_name]['passed'] += 1
                    else:
                        features[feature_name]['failed'] += 1
                    features[feature_name]['total'] += 1
            feature_summary = []
            for key, value in features.items():
                value['featureName'] = key
                value['passRate'] = f'{value["passed"] / value["total"] * 100:.2f}%'
                value["total"] = str(value['total'])
                value["passed"] = str(value['passed'])
                value["failed"] = str(value['failed'])
                feature_summary.append(value)
            self.testAll['featureSummary'] = feature_summary
        except Exception as e:
            raise e

    def _modify_html(self):
        try:
            test_data_json = json.dumps(self.testAll, indent=2)
            with open(f'{self.output_path}/testData.json', mode='w') as f:
                f.write(test_data_json)
                f.close()
            soup = BeautifulSoup(open(f'{self.output_path}/index.html', mode='r'), 'lxml')
            with open(f'{self.output_path}/index.html', mode='w', encoding='utf-8') as fs:
                tag_script = soup.script
                tag_script.string = "var testData = " + str(self.testAll)
                fs.write(soup.prettify())
                fs.close()
        except Exception as e:
            raise e
