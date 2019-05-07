from Elevator import Elevator

class testClass (Elevator):

    def __init__(self, threadName):
        return super().__init__(threadName)
    

if __name__ == "__main__":
    t = testClass("helloWorld")
    print(t.getName())