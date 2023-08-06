import jinja2

from httprunner.new_loader import load_testcase_file

__TMPL__ = """
from httprunner.runner import TestCaseRunner
from httprunner.schema import TestsConfig, TestStep
from examples.postman_echo import debugtalk


class TestCase{{ name }}(TestCaseRunner):
    config = TestsConfig(**{{ config }})

    teststeps = [
        {% for teststep in teststeps %}
            TestStep(**{{ teststep }}),
        {% endfor %}
    ]


if __name__ == '__main__':
    TestCase{{ name }}().run()
"""


def make_testcase(path: str):
    testcase = load_testcase_file(path)
    print(testcase)
    template = jinja2.Template(__TMPL__)
    name = "XXX"

    data = {
        "name": name,
        "config": testcase["config"],
        "teststeps": testcase["teststeps"],
    }
    content = template.render(data)
    print(content)
    with open(f"{name}_test.py", "w") as f:
        f.write(content)


if __name__ == "__main__":
    path = "/Users/debugtalk/MyProjects/HttpRunner-dev/HttpRunner/examples/postman_echo/request_methods/request_with_variables.yml"
    make_testcase(path)
