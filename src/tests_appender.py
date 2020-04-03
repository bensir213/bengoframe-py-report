from datetime import datetime


class TestAppender:
    def __init__(self, test_name, feature_name, reporter):
        self.test_name = test_name
        self.feature_name = feature_name
        self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.datas = {}
        self.status = ""
        self.time_takes = ""
        self.steps = []
        self.reporter = reporter
        self.test = {}

    def appender_step(self, step_status="", step_description="", use_data="", find_by="", step_details="",
                      screenshot_name=""):
        """
        :param step_description: Optional field -- To log the description for current step
        :param step_status: Required field -- To log current step status
        :param use_data: Optional field -- To log the test data for current step
        :param find_by: Optional field -- To log the object locator for current step
        :param step_details: Optional field -- To log the step logs for current step
        :param screenshot_name: Optional field -- To log the screenshot name for current step
        """
        if not step_status:
            step_status = "failed"
        if not step_description:
            step_description = "N/A"
        if not use_data:
            use_data = "N/A"
        if not find_by:
            find_by = "N/A"
        if not step_details:
            step_details = "N/A"
        wrap_step = {"stepDescription": step_description,
                     "stepStatus": step_status,
                     "data": use_data,
                     "findBy": find_by,
                     "stepDetails": step_details,
                     "screenShot": screenshot_name}
        self.steps.append(wrap_step)

    def completed(self):
        time_format = '%Y-%m-%d %H:%M:%S'
        try:
            # To log the end time when test was completed
            end_time = datetime.now().strftime(time_format)
            self.time_takes = str(
                datetime.strptime(end_time, time_format) - datetime.strptime(self.start_time, time_format))
            # To set the case status if the case steps contains failed or passed.
            self._set_case_status()
            # Build the test details to object test
            self.test = {
                "testName": self.test_name,
                "featureName": self.feature_name,
                "status": self.status,
                "datas": self.datas,
                "timeTakes": self.time_takes,
                "steps": self.steps}
            # Add the test details to the reporter
            self.reporter.add_test_details(self.test)
        except Exception as e:
            raise e

    def set_test_data(self, datas: dict):
        """
        :param datas: Optional. To log all the datas were used for the current case
        """
        if type(datas) == dict:
            self.datas = datas
        else:
            # Set test data unSuccess
            self.datas = {}
            print("Your input datas type is not correct. Case data set will set to {}. Please use dict by next time")

    def _set_case_status(self):
        if self.steps:
            for step in self.steps:
                if step['stepStatus'] == "failed":
                    self.status = "failed"
                    break
                self.status = "passed"
        else:
            self.status = "failed"
