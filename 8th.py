class SLRParser:
    def __init__(self):
        self.grammar = {
            "E": ["E+T", "T"],
            "T": ["T*F", "F"],
            "F": ["(E)", "a"]
        }
        self.action_table = {
            (0, 'a'): "s5", (0, '('): "s4",
            (1, '+'): "s6", (1, '$'): "accept",
            (2, '+'): "r2", (2, '*'): "s7", (2, ')'): "r2", (2, '$'): "r2",
            (3, '+'): "r4", (3, '*'): "r4", (3, ')'): "r4", (3, '$'): "r4",
            (4, 'a'): "s5", (4, '('): "s4",
            (5, '+'): "r6", (5, '*'): "r6", (5, ')'): "r6", (5, '$'): "r6",
            (6, 'a'): "s5", (6, '('): "s4",
            (7, 'a'): "s5", (7, '('): "s4",
            (8, '+'): "s6", (8, ')'): "s11",
            (9, '+'): "r1", (9, '*'): "s7", (9, ')'): "r1", (9, '$'): "r1",
            (10, '+'): "r3", (10, '*'): "r3", (10, ')'): "r3", (10, '$'): "r3",
            (11, '+'): "r5", (11, '*'): "r5", (11, ')'): "r5", (11, '$'): "r5"
        }
        self.goto_table = {
            (0, 'E'): 1, (0, 'T'): 2, (0, 'F'): 3,
            (4, 'E'): 8, (4, 'T'): 2, (4, 'F'): 3,
            (6, 'T'): 9, (6, 'F'): 3,
            (7, 'F'): 10
        }
        self.reductions = {
            1: ("E", "E+T"),
            2: ("E", "T"),
            3: ("T", "T*F"),
            4: ("T", "F"),
            5: ("F", "(E)"),
            6: ("F", "a")
        }

    def parse(self, input_string):
        input_string = list(input_string)
        stack = [0]  # Stack initialized with state 0
        pointer = 0

        print("\nParsing Steps:")
        while True:
            state = stack[-1]
            symbol = input_string[pointer] if pointer < len(input_string) else '$'

            print(f"Stack: {stack}   Input: {''.join(input_string[pointer:])}")

            if (state, symbol) in self.action_table:
                action = self.action_table[(state, symbol)]
                if action.startswith("s"):  # Shift
                    stack.append(symbol)
                    stack.append(int(action[1:]))
                    pointer += 1
                elif action.startswith("r"):  # Reduce
                    rule_number = int(action[1:])
                    lhs, rhs = self.reductions[rule_number]
                    for _ in range(len(rhs) * 2):  # Pop 2 * len(rhs) items
                        stack.pop()
                    goto_state = self.goto_table.get((stack[-1], lhs), None)
                    if goto_state is not None:
                        stack.append(lhs)
                        stack.append(goto_state)
                elif action == "accept":
                    print("Given String is ACCEPTED!")
                    return
            else:
                print("Error: String not accepted!")
                return

# Example Usage
parser = SLRParser()
input_string = "a+a*a$"
parser.parse(input_string)
