from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class CalcTest(StageTest):
    def generate(self) -> List[TestCase]:
        cases = {"n = 3\nm=4\na =   5\nb = a\nn\nm\na\nb\ncount = 10\ncount\n/exit": "3\n4\n5\n5\n10\nBye!",
                 "4 + 6 - 8\n\n\n2 - 3 - 4\n\n8 + 7 - 4\n/exit": "2\n-5\n11\nBye!",
                 "a = 3\nb = 4\nc = 5\na + b - c\nb - c + 4 - a\na = 800\na + b + c\n/exit": "2\n0\n809\nBye!",
                 "/command\n/exit": "Unknown command\nBye!",
                 "a = 1\na = 2\na = 3\na\n/exit": "3\nBye!",
                 "q\nr\nq = 10\nr = 20\nq\nr\nR\n/exit": "Unknown variable\nUnknown variable\n10\n20\nUnknown variable\nBye!",
                 "a1 = 8\nn = a2a\na = 7 = 8\nnum = 10\n/exit": "Invalid identifier\nInvalid assignment\nInvalid assignment\nBye!"}
        return [TestCase(stdin=case,
                         attach=cases[case])
                for case in cases]

    def check(self, reply: str, attach) -> CheckResult:
        return CheckResult(reply.strip() == attach.strip(), "")


if __name__ == '__main__':
    CalcTest("calculator.calculator").run_tests()
