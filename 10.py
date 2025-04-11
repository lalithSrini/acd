import re

class ThreeAddressCode:
    def __init__(self):
        self.temp_count = 0
        self.triples = []
        self.quadruples = []
        self.indirect_triples = []
        self.variables = {}

    def generate_temp(self):
        """Generate a new temporary variable."""
        self.temp_count += 1
        return f't{self.temp_count}'

    def parse_expression(self, expression):
        """Evaluate the expression and generate the corresponding TAC."""
        # Remove spaces and handle multi-operator expressions
        expression = expression.replace(" ", "")

        # Use regex to tokenize the expression into operands and operators
        tokens = re.findall(r'[a-zA-Z]+|\d+\.?\d*|[+\-*/^()]', expression)

        # Process the expression to handle precedence using a stack-based approach
        return self.handle_expression(tokens)

    def handle_expression(self, tokens):
        """Handle multi-operator expressions and generate TAC."""
        # Initialize a stack to handle intermediate expressions
        stack = []

        # Order of precedence for operators
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

        def apply_operator(op, operand1, operand2):
            """Helper to apply an operator on operands."""
            result = self.generate_temp()
            self.quadruples.append((op, operand1, operand2, result))
            self.triples.append((op, operand1, operand2))
            self.indirect_triples.append((operand1, operand2, op))
            return result

        # Shunting Yard Algorithm to handle operator precedence and parentheses
        operators = []
        operands = []

        for token in tokens:
            if token.isalpha() or re.match(r'\d+\.?\d*', token):  # Operand (variable or number)
                operands.append(token)
            elif token == '(':  # Left parenthesis
                operators.append(token)
            elif token == ')':  # Right parenthesis
                while operators and operators[-1] != '(':
                    op = operators.pop()
                    right = operands.pop()
                    left = operands.pop()
                    result = apply_operator(op, left, right)
                    operands.append(result)
                operators.pop()  # Pop the '('
            else:  # Operator
                while (operators and operators[-1] != '(' and
                       precedence[operators[-1]] >= precedence[token]):
                    op = operators.pop()
                    right = operands.pop()
                    left = operands.pop()
                    result = apply_operator(op, left, right)
                    operands.append(result)
                operators.append(token)

        # Apply remaining operators
        while operators:
            op = operators.pop()
            right = operands.pop()
            left = operands.pop()
            result = apply_operator(op, left, right)
            operands.append(result)

        return operands[0]  # Final result

    def print_triples(self):
        print("Triples:")
        for index, triple in enumerate(self.triples, 1):
            print(f"({index}) {triple[0]} {triple[1]} {triple[2]}")

    def print_quadruples(self):
        print("\nQuadruples:")
        for quad in self.quadruples:
            print(f"({quad[0]}, {quad[1]}, {quad[2]}, {quad[3]})")

    def print_indirect_triples(self):
        print("\nIndirect Triples:")
        for index, indirect in enumerate(self.indirect_triples, 1):
            print(f"({index}) {indirect[0]} {indirect[1]} {indirect[2]}")

def main():
    tac = ThreeAddressCode()

    # Get the expression from the user
    expression = input("Enter a complex expression (e.g., 'a + n + h * m + h / k'): ")

    # Generate TAC (triples, quadruples, indirect triples) from the expression
    result = tac.parse_expression(expression)

    # Output the generated TAC
    tac.print_triples()
    tac.print_quadruples()
    tac.print_indirect_triples()

if __name__ == "__main__":
    main()
