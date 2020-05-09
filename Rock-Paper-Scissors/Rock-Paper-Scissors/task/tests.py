from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class RPSTest(StageTest):
    def generate(self) -> List[TestCase]:
        cases = ["rock",
                 "paper",
                 "scissors"]
        return [TestCase(stdin=cases[case],
                         attach=(cases + cases)[case + 1])
                for case in range(len(cases))]

    def check(self, reply: str, attach) -> CheckResult:
        return CheckResult("Sorry, but computer chose {}".format(attach.strip()) == reply.strip(),
                           "Your answer on \"{}\" was \"{}\". That's pretty wrong".format(attach, reply))


if __name__ == '__main__':
    RPSTest("rps.game").run_tests()
