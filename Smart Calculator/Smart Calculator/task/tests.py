from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class CalcTest(StageTest):
    def generate(self) -> List[TestCase]:
        cases = {"4 + 6 - 8\n\n\n2 - 3 - 4\n\n8 + 7 - 4\n1 +++ 2 * 3 -- 4\n/exit": "2\n-5\n11\n11\nBye!",
                 "/command\n/exit": "Unknown command\nBye!",
                 "3 + 8 * ((4 + 3) * 2 + 1) - 6 / (2 + 1)\n/exit": "121\nBye!",
                 "8 * 3 + 12 * (4 - 2)\n4 * (2 + 3\n4 + 3)\n/exit": "48\nInvalid expression\nInvalid expression\nBye!",
                 "a = 4\nb = 5\nc = 6\na*2+b*3+c*(2+3)\n/exit": "53\nBye!",
                 "a = 1\na = 2\na = 3\na\n/exit": "3\nBye!"}
        return [TestCase(stdin=case,
                         attach=cases[case])
                for case in cases]

    def check(self, reply: str, attach) -> CheckResult:
        return CheckResult(reply.strip() == attach.strip(), "")


if __name__ == '__main__':
    CalcTest("calculator.calculator").run_tests()
