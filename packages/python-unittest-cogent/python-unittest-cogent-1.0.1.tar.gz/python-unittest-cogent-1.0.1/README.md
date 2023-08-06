## python-unittest-cogent
A custom tests runner which gives output in three different formats (xml, json and html).

### Quickstart
Installation:
```shell
pip install python-unittest-cogent
```
Usage: In example.py
```python
import cogent
from cogent.tests import TestCase

class TestClassOne(TestCase):
    def test1(self):
        expected_number = 90
        actual_number = 90
        print('Test output foe test case 1')
        self.assertEqual(expected_number, actual_number)

if __name__ == "__main__":
    cogent.main()
```

### To change the settings:
You can change the different-different settings like - 
```python
PROJECT_NAME = "Test Report"
APPLICATION_NAME = "Test APP"
APP_VERSION = "App Version 5.3"
PLATFORM = "Linux/Ubuntu 14.04"

HTML_TEST_REPORT_FILENAME = "Report.html"
XML_TEST_REPORT_FILENAME = "Report.xml"
JSON_TEST_REPORT_FILENAME = "Report.json"

DEFAULT_CONVERTER = "HTML" 
```
In example.py
```python
import cogent
from cogent.tests import TestCase
from cogent import settings

settings.DEFAULT_CONVERTER = "XML"

class TestClassOne(TestCase):
    def test1(self):
        expected_number = 90
        actual_number = 90
        print('Test output foe test case 1')
        self.assertEqual(expected_number, actual_number)

if __name__ == "__main__":
    cogent.main.settings = settings
    cogent.main()
```

In case any queries you can contact me on my email - harshittrivedi78@gmail.com
