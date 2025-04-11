def generate_assembly_code():
    def get_register():
        nonlocal register_count
        reg = f"R{register_count}"
        register_count += 1
        return reg

    print("8086 Assembly Code Generator")
    print("===========================")

    # Step 1: Get the number of statements from the user
    num_statements = int(input("Enter the number of three-address statements: "))

    assembly_code = []
    register_count = 0
    address_descriptor = {}  # Tracks where variables are stored
    register_descriptor = {}  # Tracks what is in each register

    # Step 2: Process each three-address statement
    for _ in range(num_statements):
        statement = input("Enter the three-address statement (e.g., a = b + c): ").replace(" ", "")
        if '=' not in statement:
            print("Invalid statement format. Must contain '='.")
            continue

        lhs, rhs = statement.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()

        # Tokenize the RHS to handle variables and operators
        import re
        tokens = re.findall(r'[a-zA-Z]+|\d+|[+\-*/]', rhs)

        if not tokens or len(tokens) != 3:
            print(f"Invalid expression format: RHS of '{statement}' must be in the form 'y op z'.")
            continue

        y, op, z = tokens

        # Step 3: Generate code for y
        if y not in address_descriptor:
            reg_y = get_register()
            assembly_code.append(f"LOAD {reg_y}, {y}")
            address_descriptor[y] = reg_y
        else:
            reg_y = address_descriptor[y]

        # Step 4: Generate code for z
        if z not in address_descriptor:
            reg_z = get_register()
            assembly_code.append(f"LOAD {reg_z}, {z}")
            address_descriptor[z] = reg_z
        else:
            reg_z = address_descriptor[z]

        # Step 5: Generate the operation
        if op == '+':
            assembly_code.append(f"ADD {reg_y}, {reg_z}")
        elif op == '-':
            assembly_code.append(f"SUB {reg_y}, {reg_z}")
        elif op == '*':
            assembly_code.append(f"MUL {reg_y}, {reg_z}")
        elif op == '/':
            assembly_code.append(f"DIV {reg_y}, {reg_z}")
        else:
            print(f"Unsupported operator '{op}' in statement '{statement}'.")
            continue

        # Step 6: Store the result
        assembly_code.append(f"STORE {lhs}, {reg_y}")
        address_descriptor[lhs] = reg_y

    # Step 7: Output the generated assembly code
    print("\nGenerated 8086 Assembly Code:")
    print("===========================")
    for line in assembly_code:
        print(line)

# Run the code generator
generate_assembly_code()
