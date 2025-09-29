import json
import sys

class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, transitions, initial_state, blank_symbol, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.blank_symbol = blank_symbol
        self.final_states = set(final_states)
        
        if blank_symbol not in self.tape_alphabet:
            raise ValueError(f"Blank symbol '{blank_symbol}' must be in tape alphabet")
        
        if initial_state not in self.states:
            raise ValueError(f"Initial state '{initial_state}' must be in states")
        
        for state in final_states:
            if state not in self.states:
                raise ValueError(f"Final state '{state}' must be in states")
    
    def run(self, input_string, max_steps=10000):
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Input symbol '{symbol}' not in alphabet")
        
        tape = list(input_string)
        head_position = 0
        current_state = self.initial_state
        steps = 0
        
        while current_state not in self.final_states and steps < max_steps:
            if head_position < 0:
                tape.insert(0, self.blank_symbol)
                head_position = 0
            elif head_position >= len(tape):
                tape.append(self.blank_symbol)
            
            current_symbol = tape[head_position]
            transition_key = (current_state, current_symbol)
            
            if transition_key not in self.transitions:
                break
            
            next_state, write_symbol, direction = self.transitions[transition_key]
            
            if write_symbol not in self.tape_alphabet:
                raise ValueError(f"Write symbol '{write_symbol}' not in tape alphabet")
            
            tape[head_position] = write_symbol
            
            if direction == 'R':
                head_position += 1
            elif direction == 'L':
                head_position -= 1
            else:
                raise ValueError(f"Invalid direction '{direction}', must be 'R' or 'L'")
            
            current_state = next_state
            steps += 1
        
        accepted = current_state in self.final_states
        tape_str = ''.join(tape)
        
        return tape_str, accepted

def load_json_specification(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    states = data['states']
    alphabet = data['alphabet']
    tape_alphabet = data['tape_alphabet']
    initial_state = data['initial_state']
    blank_symbol = data['blank_symbol']
    final_states = data['final_states']
    
    transitions = {}
    for transition in data['transitions']:
        key = (transition['from'], transition['read'])
        value = (transition['to'], transition['write'], transition['direction'])
        transitions[key] = value
    
    return TuringMachine(states, alphabet, tape_alphabet, transitions, 
                        initial_state, blank_symbol, final_states)

def main():
    if len(sys.argv) != 4:
        print("Uso: python turing_simulator.py <arquivo_json> <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        tm = load_json_specification(json_file)
        
        with open(input_file, 'r', encoding='utf-8') as f:
            input_string = f.read().strip()
        
        tape_result, accepted = tm.run(input_string)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(tape_result)
        
        print(1 if accepted else 0)
        
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
