# BenGoFrame Python Report

BenGoFrame Python Report is created for the automation test report

You can log the test details for the test steps so that you can check the details in the report

This report will not create html by code

Just generate test data details and modify to index.html in template folder 

Please do not delete or modify the fields in template folder

Pre-views examples:

![](imgs\dashboard.PNG)

![](imgs\Summary.PNG)

![](imgs\TestDetails.PNG)

Installation: 

```python
# Use pipenv to install Pipfile
# pipenv install --skip-lock
[packages]
behave = "*"
selenium = "*"
beautifulsoup4 = "*"
lxml = "*"
# If you have no pipenv. 
# Please copy them to requirenments.txt and pip install -r requirenments.txt
```

`testData.json` is the copy file to display all test results

You can't modify the formatted JSON below keys

If you don't know what the values should be. Please input the "" into the values 

For more details. Please read the `src/report_creator.py` and `src/tests_appender.py`

```json
# Example: testData.json 
{
	"testConfig": {
    "testSuite": "Ben",
    "gridAddress": "http://localhost:4444/wd/hub",
    "logLevel": "INFO",
    "threadCount": "2",
    "database": "Cucumber-QA",
    "reRun": "No",
    "startTime": "2020-04-02 21:31:47",
    "endTime": "2020-04-02 21:31:47",
    "takeTimes": "0 hs 00 mins 00 ss"
  },
  "casesChart": {
    "totalCases": 0,
    "passed": 0,
    "failed": 0
  },
  "stepsChart": {
    "totalSteps": 0,
    "passed": 0,
    "failed": 0
  },
  "featureSummary": [
    {
      "total": "0",
      "passed": "0",
      "failed": "0",
      "featureName": "MyFeature",
      "passRate": "{passed/total %}"
    },
    {
      "total": "0",
      "passed": "0",
      "failed": "0",
      "featureName": "MyFeature2",
      "passRate": "{passed/total %}"
    }
  ],
  "testDetails": [
    {
      "testName": "Hello",
      "featureName": "MyFeature",
      "status": "failed",
      "datas": {
        "name": "selenium"
      },
      "timeTakes": "0:00:00",
      "steps": [
        {
          "stepDescription": "This is for test",
          "stepStatus": "failed",
          "data": "selenium",
          "findBy": "xpath=id",
          "stepDetails": "details",
          "screenShot": ""
        },
        {
          "stepDescription": "This is for test",
          "stepStatus": "passed",
          "data": "selenium",
          "findBy": "xpath=id",
          "stepDetails": "details",
          "screenShot": ""
        }
      ]
    },
    {
      "testName": "Hello2",
      "featureName": "MyFeature2",
      "status": "passed",
      "datas": {
        "name": "selenium2"
      },
      "timeTakes": "0:00:00",
      "steps": [
        {
          "stepDescription": "This is for test2",
          "stepStatus": "passed",
          "data": "selenium2",
          "findBy": "xpath=id",
          "stepDetails": "details2",
          "screenShot": ""
        },
        {
          "stepDescription": "This is for test2",
          "stepStatus": "passed",
          "data": "selenium2",
          "findBy": "xpath=id",
          "stepDetails": "details2",
          "screenShot": ""
        }
      ]
    }
  ]
}
```



