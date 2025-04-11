import collections

class PredictiveParsingTable:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = {}
        self.follow = {}
        self.parsing_table = {}
        self.non_terminals = list(grammar.keys())

    def compute_first(self):
        for non_terminal in self.non_terminals:
            self.first[non_terminal] = self.find_first(non_terminal)

    def find_first(self, symbol):
        if symbol in self.first:
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
                first_set.add('ε')  # Add ε if all can be ε
        return first_set

    def compute_follow(self):
        for non_terminal in self.non_terminals:
            self.follow[non_terminal] = set()
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

    def construct_table(self):
        self.compute_first()
        self.compute_follow()
        self.parsing_table = {nt: {} for nt in self.non_terminals}

        for lhs, productions in self.grammar.items():
            for production in productions:
                first_set = set()
                for char in production:
                    first_set.update(self.find_first(char) - {'ε'})
                    if 'ε' not in self.find_first(char):
                        break
                else:
                    first_set.add('ε')

                for terminal in first_set:
                    if terminal != 'ε':
                        self.parsing_table[lhs][terminal] = production
                if 'ε' in first_set:
                    for terminal in self.follow[lhs]:
                        self.parsing_table[lhs][terminal] = production

    def display_table(self):
        print("\nPredictive Parsing Table:")
        print("{:<10} {:<30}".format("Non-Term", "Terminals -> Production"))
        print("="*50)
        for non_terminal, rules in self.parsing_table.items():
            for terminal, production in rules.items():
                print("{:<10} {:<30}".format(non_terminal, f"{terminal} -> {non_terminal} → {production}"))

# Example Grammar (LL(1))
grammar = {
    'E': ['TG'],
    'G': ['+TG', 'ε'],
    'T': ['FH'],
    'H': ['*FH', 'ε'],
    'F': ['(E)', 'id']
}

parser = PredictiveParsingTable(grammar)
parser.construct_table()
parser.display_table()
