# Function to parse input and generate intermediate code
import re

def generate_intermediate_code():
    print("OUTPUT:")
    num_values = int(input("Enter no of values: "))
    intermediate_code = []

    for _ in range(num_values):
        left = input("left: ").strip()
        right = input("right: ").strip()
        intermediate_code.append(f"{left} = {right}")

    print("\nIntermediate Code:")
    for line in intermediate_code:
        print(line)

    return intermediate_code

# Function to perform Dead Code Elimination
def dead_code_elimination(code):
    used_variables = set()
    optimized_code = []

    # Step 1: Identify used variables
    # Assume the last variable is the output (e.g., 'r' in the sample input)
    last_assignment = code[-1].split(" = ")[0]
    used_variables.add(last_assignment)

    # Traverse the code in reverse to find dependencies
    for line in reversed(code):
        left, right = line.split(" = ")
        if left in used_variables:
            # Add all variables on the right-hand side to used_variables
            used_variables.update(re.findall(r'[a-zA-Z]', right))

    # Step 2: Remove unused assignments
    for line in code:
        left, right = line.split(" = ")
        if left in used_variables:
            optimized_code.append(line)

    print("\nAfter Dead Code Elimination:")
    for line in optimized_code:
        print(line)

    return optimized_code

# Function to perform Common Subexpression Elimination
def common_subexpression_elimination(code):
    expression_map = {}
    optimized_code = []

    for line in code:
        left, right = line.split(" = ")
        # Replace variables in the right-hand side with their mapped values
        for var, replacement in expression_map.items():
            right = right.replace(var, replacement)
        if right in expression_map:
            # Replace with existing variable
            optimized_code.append(f"{left} = {expression_map[right]}")
        else:
            # Store the expression
            expression_map[right] = left
            optimized_code.append(line)

    print("\nAfter Common Subexpression Elimination:")
    for line in optimized_code:
        print(line)

    return optimized_code

# Function to generate optimized code
def generate_optimized_code(code):
    print("\nOptimized Code:")
    for line in code:
        print(line)

# Main function
def main():
    # Step 1: Generate intermediate code
    intermediate_code = generate_intermediate_code()

    # Step 2: Perform Dead Code Elimination
    code_after_dce = dead_code_elimination(intermediate_code)

    # Step 3: Perform Common Subexpression Elimination
    code_after_cse = common_subexpression_elimination(code_after_dce)

    # Step 4: Generate optimized code
    generate_optimized_code(code_after_cse)

# Run the program
if __name__ == "__main__":
    main()