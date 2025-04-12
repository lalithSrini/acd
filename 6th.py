
class FirstFollow:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {non_terminal: set() for non_terminal in grammar}
        self.follow = {non_terminal: set() for non_terminal in grammar}
        self.non_terminals = list(grammar.keys())

    def compute_first(self):
        for non_terminal in self.non_terminals:
            self.first[non_terminal] = self.find_first(non_terminal)

    def find_first(self, symbol):
        if symbol in self.first and self.first[symbol]:
            return self.first[symbol]
        first_set = set()
        if symbol not in self.grammar:  # Terminal case
            return {symbol}
        for production in self.grammar[symbol]:
            for char in production:
                first_char = self.find_first(char)
                first_set.update(first_char - {'ε'})  # Add everything except ε
                if 'ε' not in first_char:
                    break
            else:
                first_set.add('ε')  # If all can be ε, add ε
        return first_set

    def compute_follow(self):
        self.follow[self.non_terminals[0]].add('$')  # Start symbol has '$'

        while True:
            updated = False
            for lhs, productions in self.grammar.items():
                for production in productions:
                    follow_temp = self.follow[lhs].copy()
                    for symbol in reversed(production):
                        if symbol in self.non_terminals:
                            if not self.follow[symbol].issuperset(follow_temp):
                                self.follow[symbol].update(follow_temp)
                                updated = True
                            if 'ε' in self.first[symbol]:
                                follow_temp.update(self.first[symbol] - {'ε'})
                            else:
                                follow_temp = self.first[symbol]
                        else:
                            follow_temp = {symbol}
            if not updated:
                break

    def display_results(self):
        print("\nFIRST SETS:")
        for non_terminal, first_set in self.first.items():
            print(f"First({non_terminal}) =", ', '.join(sorted(first_set)))

        print("\nFOLLOW SETS:")
        for non_terminal, follow_set in self.follow.items():
            print(f"Follow({non_terminal}) =", ', '.join(sorted(follow_set)))

# Example Grammar
grammar = {
    'A': ['aAaB', 'a'],
    'B': ['bBaB', 'b']
}

parser = FirstFollow(grammar)
parser.compute_first()
parser.compute_follow()
parser.display_results()
