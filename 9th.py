class ThreeAddressCode:
    def __init__(self):
        self.temp_count = 1  # Counter for temporary variables
        self.code = []  # List to store the TAC instructions

    def new_temp(self):
        """Generate a new temporary variable"""
        temp_var = f"T{self.temp_count}"
        self.temp_count += 1
        return temp_var

    def generate_tac_expression(self, expression):
        """Generate Three Address Code for an arithmetic expression"""
        operators = {'+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!='}
        stack = []
        postfix = self.infix_to_postfix(expression)

        for token in postfix:
            if token not in operators:
                stack.append(token)  # Push operand to stack
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                temp = self.new_temp()
                self.code.append(f"{temp} = {operand1} {token} {operand2}")
                stack.append(temp)

        return stack.pop()  # Return final result

    def infix_to_postfix(self, expression):
        """Convert infix expression to postfix for easier TAC generation"""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0, '!=': 0}
        output = []
        operators = []
        tokens = expression.split()

        for token in tokens:
            if token.isalnum():
                output.append(token)
            elif token in precedence:
                while (operators and precedence.get(operators[-1], -1) >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        return output

    def generate_tac_if_statement(self, condition, true_label, false_label):
        """Generate Three Address Code for an IF condition"""
        self.code.append(f"If {condition} goto {true_label}")
        self.code.append(f"goto {false_label}")

    def generate_code_for_expressions(self):
        """Generate TAC for given expressions"""
        print("Generating TAC for expression: (a * b) + (c + d) - (a + b + c + d)")
        final_result = self.generate_tac_expression("( a * b ) + ( c + d ) - ( a + b + c + d )")
        print("\n".join(self.code))

        # Clear previous code for next TAC generation
        self.code.clear()
        self.temp_count = 1

        print("\nGenerating TAC for condition: If A < B and C < D then t = 1 else t = 0")
        self.generate_tac_if_statement("A < B", "L1", "L2")
        self.code.append("L2: goto END")
        self.code.append("L1: If C < D goto L3")
        self.code.append("L3: t = 1")
        self.code.append("goto END")
        self.code.append("END: t = 0")
        print("\n".join(self.code))


# Run the TAC generator
tac_generator = ThreeAddressCode()
tac_generator.generate_code_for_expressions()
