import re

class DKOrderRun():
    def __init__(self, ori):
        self.orderRunInfo = ori

    def testsFromOrderRun(self):
        try:
            testStr = self.orderRunInfo['servings'][0]['testresults']
        except KeyError:
            #print("Error: No tests in OrderRun Object")
            raise Exception
        return self._parseTestString(testStr)

    def orderStatus(self):
        return self.orderRunInfo['orders'][0]['order-status']

    def _parseTestString(self, testStr):
        tests = list()
        lines = testStr.strip().split('\n')
        state_level = "Failed"
        state_step = ""  # Others are known
        for line in lines:
            line_type = getTypeOfTestLine(line)
            if line_type:
                if line_type[0] == "Level":
                    state_level = line_type[1]
                elif line_type[0] == "Step":
                    state_step = line_type[1]
                elif line_type[0] == "Test":
                    tests.append((line_type[1], state_step, state_level, line_type[2]))
        return tests

    def _getTypeOfTestLine(self, line):
        line = line.strip()
        match = re.match(r'Tests: (\w+)', line)
        if match:
            return ("Level", match.group(1))
        match = re.match(r'Step \((.+)\)', line)
        if match:
            return ("Step", match.group(1))
        match = re.match(r'\d+\. (.+) \((.+)\)', line)
        if match:
            return ("Test", match.group(1), match.group(2))
        return None


