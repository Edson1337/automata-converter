EPSILON = 'ε'

class AutomataFormatter:
    @staticmethod
    def format_afn(afn) -> str:
        """Formata um AFN para exibição/arquivo."""
        result = "# AFN Original\n"
        
        # Mapeamento de estados para nomes amigáveis
        state_map = {state: f"q{i}" for i, state in enumerate(sorted(afn.Q))}
        
        # Estados
        result += f"Q: {', '.join(state_map.values())}\n"
        
        # Alfabeto
        result += f"Σ: {', '.join(sorted(afn.Sigma))}\n"
        
        # Função de transição
        result += "δ:\n"
        
        # Organizar transições
        transitions = []
        for state, trans in afn.delta.items():
            for symbol, targets in trans.items():
                symbol_str = EPSILON if symbol == '' else symbol
                for target in targets:
                    transitions.append((state_map[state], symbol_str, state_map[target]))
        
        # Ordenar e imprimir transições
        for source, symbol, target in sorted(transitions):
            result += f"{source}, {symbol} -> {target}\n"
        
        # Estado inicial
        result += f"{state_map[afn.q0]}: inicial\n"
        
        # Estados finais
        finals_str = [state_map[state] for state in sorted(afn.F)]
        result += f"F: {', '.join(finals_str)}"
        
        return result
    
    @staticmethod
    def format_afd(afd, title="# AFD Determinizado") -> str:
        """Formata um AFD para exibição/arquivo."""
        result = title + "\n"
        
        # Criar mapeamento dos estados originais para nomes simples
        original_state_map = {}
        original_states = set()
        for state_set in afd.Q:
            original_states.update(state_set)
        for i, state in enumerate(sorted(original_states)):
            original_state_map[state] = f"q{i}"
        
        # Estados - mostrar como conjuntos de nomes simples
        states_str = []
        for state in sorted(afd.Q, key=lambda s: ",".join(sorted(s))):
            if len(state) == 1:
                mapped_state = "{" + original_state_map[list(state)[0]] + "}"
            else:
                mapped_states = [original_state_map[s] for s in sorted(state)]
                mapped_state = "{" + ", ".join(mapped_states) + "}"
            states_str.append(mapped_state)
        
        result += f"Q: {', '.join(states_str)}\n"
        
        # Alfabeto
        result += f"Σ: {', '.join(sorted(afd.Sigma))}\n"
        
        # Função de transição
        result += "δ:\n"
        
        # Organizar transições
        transitions = []
        for (state, symbol), target in afd.delta.items():
            # Estado origem
            if len(state) == 1:
                state_str = "{" + original_state_map[list(state)[0]] + "}"
            else:
                mapped_states = [original_state_map[s] for s in sorted(state)]
                state_str = "{" + ", ".join(mapped_states) + "}"
            
            # Estado destino
            if len(target) == 1:
                target_str = "{" + original_state_map[list(target)[0]] + "}"
            else:
                mapped_targets = [original_state_map[s] for s in sorted(target)]
                target_str = "{" + ", ".join(mapped_targets) + "}"
            
            transitions.append((state_str, symbol, target_str))
        
        # Ordenar e imprimir transições
        for source, symbol, target in sorted(transitions, key=lambda x: (x[0], x[1])):
            result += f"{source}, {symbol} -> {target}\n"
        
        # Estado inicial
        if len(afd.q0) == 1:
            initial_str = "{" + original_state_map[list(afd.q0)[0]] + "}"
        else:
            mapped_initials = [original_state_map[s] for s in sorted(afd.q0)]
            initial_str = "{" + ", ".join(mapped_initials) + "}"
        result += f"{initial_str}: inicial\n"
        
        # Estados finais
        finals_str = []
        for state in sorted(afd.F, key=lambda s: ",".join(sorted(s))):
            if len(state) == 1:
                mapped_state = "{" + original_state_map[list(state)[0]] + "}"
            else:
                mapped_states = [original_state_map[s] for s in sorted(state)]
                mapped_state = "{" + ", ".join(mapped_states) + "}"
            finals_str.append(mapped_state)
        
        result += f"F: {', '.join(finals_str)}"
        
        return result
    
    @staticmethod
    def print_afn_transition_table(afn):
        """Imprime uma tabela de transições do AFN."""
        print("\nTabela de Transições do AFN:")
        
        # Cabeçalho
        header = f"| Estado | {' | '.join(sorted(afn.Sigma))} | {EPSILON} |"
        print(header)
        print("|" + "-" * (len(header) - 2) + "|")
        
        # Linhas da tabela
        for state in sorted(afn.Q):
            row = f"| {state} "
            
            # Transições por símbolo
            for symbol in sorted(afn.Sigma):
                if state in afn.delta and symbol in afn.delta[state]:
                    targets = ', '.join(sorted(afn.delta[state][symbol]))
                    row += f"| {targets} "
                else:
                    row += "| - "
            
            # Transições épsilon
            if state in afn.delta and '' in afn.delta[state]:
                targets = ', '.join(sorted(afn.delta[state]['']))
                row += f"| {targets} "
            else:
                row += "| - "
            
            print(row + "|")
    
    @staticmethod
    def print_afd_transition_table(afd):
        """Imprime uma tabela de transições do AFD."""
        print("\nTabela de Transições do AFD:")
        
        # Mapeamento amigável para estados
        state_map = {state: f"q{i}" for i, state in enumerate(sorted(afd.Q, key=lambda s: ",".join(sorted(s))))}
        
        # Cabeçalho
        header = f"| Estado | {' | '.join(sorted(afd.Sigma))} |"
        print(header)
        print("|" + "-" * (len(header) - 2) + "|")
        
        # Linhas da tabela
        for state, state_name in state_map.items():
            full_name = "{" + ",".join(sorted(state)) + "}"
            row = f"| {state_name} ({full_name}) "
            
            for symbol in sorted(afd.Sigma):
                key = (state, symbol)
                if key in afd.delta:
                    target = afd.delta[key]
                    target_name = state_map[target]
                    row += f"| {target_name} "
                else:
                    row += "| - "
            
            print(row + "|")