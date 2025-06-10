from automata.afn import AFN
from automata.afd import AFD
from typing import Set, Dict, FrozenSet, Tuple
from collections import deque


EPSILON = 'ε'

class Converter:
    def __init__(self, grammar: dict):
        self.grammar = grammar

    def convert_glud_to_afn(self) -> AFN:
        V = set()
        for production in self.grammar['productions']:
            left, _ = production
            V.add(left)
        qf = 'qf'

        afn = {
            'Q': V | {qf},
            'Sigma': set(self.grammar['Sigma']),
            'delta': {},
            'q0': self.grammar['S'],
            'F': {qf}
        }

        # Debug: verificar as produções
        print("Produções encontradas:", self.grammar['productions'])

        for production in self.grammar['productions']:
            left, right = production
            print(f"Processando produção: {left} -> {right}")
            
            if right == 'ε':
                # Produção para epsilon: transição para qf com epsilon
                afn['delta'].setdefault(left, {}).setdefault('', set()).add(qf)
                print(f"  Adicionada transição épsilon: {left} --ε--> qf")
                
            elif len(right) == 2:
                # Produção do tipo A -> aB
                a, B = right[0], right[1]
                afn['delta'].setdefault(left, {}).setdefault(a, set()).add(B)
                print(f"  Adicionada transição: {left} --{a}--> {B}")
                
            elif len(right) == 1:
                symbol = right[0]
                if symbol in self.grammar['Sigma']:
                    # Produção do tipo A -> a (símbolo terminal)
                    afn['delta'].setdefault(left, {}).setdefault(symbol, set()).add(qf)
                    print(f"  Adicionada transição terminal: {left} --{symbol}--> qf")
                elif symbol in V:
                    # Produção unitária do tipo A -> B (não-terminal para não-terminal)
                    # Adicionar transição épsilon de A para B
                    afn['delta'].setdefault(left, {}).setdefault('', set()).add(symbol)
                    print(f"  Adicionada transição unitária (épsilon): {left} --ε--> {symbol}")
                else:
                    print(f"  ERRO: Símbolo '{symbol}' não reconhecido na produção {left} -> {right}")
            else:
                print(f"  ERRO: Produção não reconhecida: {left} -> {right}")

        print("Delta final do AFN:", afn['delta'])
        return AFN(
            Q=afn['Q'],
            Sigma=afn['Sigma'],
            delta=afn['delta'],
            q0=afn['q0'],
            F=afn['F']
        )
    
    def epsilon_closure(self, states: Set[str], afn: AFN) -> Set[str]:
        """
        Calcula o ε-closure de um conjunto de estados do AFN.
        Similar à implementação do seu colega, mas adaptado à nossa estrutura.
        """
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if state in afn.delta and '' in afn.delta[state]:
                for next_state in afn.delta[state]['']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure
    
    def transition(self, afn: AFN, states: Set[str], symbol: str) -> Set[str]:
        """
        Calcula os estados alcançáveis a partir de um conjunto de estados,
        lendo um símbolo específico (sem aplicar ε-closure).
        """
        next_states = set()
        for state in states:
            if state in afn.delta and symbol in afn.delta[state]:
                next_states.update(afn.delta[state][symbol])
        return next_states
    
    def convert_afn_to_afd(self, afn: AFN) -> AFD:
        """
        Converte um AFN em um AFD usando o algoritmo de determinização,
        com visualização de tabela para ajudar no debug.
        """
        # Calcular o estado inicial do AFD
        initial_closure = self.epsilon_closure({afn.q0}, afn)
        initial_afd = frozenset(initial_closure)
        
        states_afd = {initial_afd}
        queue = deque([initial_afd])
        delta_afd = {}
        
        # Tabela para visualização
        print("\n# Tabela de Determinização:")
        header = f"| Estado | {' | '.join(sorted(afn.Sigma))} |"
        print(header)
        print("|" + "-" * (len(header) - 2) + "|")
        
        # Processar todos os estados do AFD
        while queue:
            current_state = queue.popleft()
            
            # Linha da tabela
            current_str = "{" + ",".join(sorted(current_state)) + "}"
            row = f"| {current_str} "
            
            for symbol in sorted(afn.Sigma):
                # Calcular transição - primeiro sem ε-closure
                direct_states = self.transition(afn, current_state, symbol)
                
                if not direct_states:
                    row += "| ∅ "
                    continue
                
                # Aplicar ε-closure
                next_closure = self.epsilon_closure(direct_states, afn)
                next_state = frozenset(next_closure)
                
                # Adicionar transição
                delta_afd[(current_state, symbol)] = next_state
                
                # Se for novo estado, adicionar à fila
                if next_state not in states_afd:
                    states_afd.add(next_state)
                    queue.append(next_state)
                
                # Para a tabela
                next_str = "{" + ",".join(sorted(next_state)) + "}"
                row += f"| {next_str} "
            
            print(row + "|")
        
        # Determinar estados finais
        finals_afd = {state for state in states_afd if any(q in afn.F for q in state)}
        
        return AFD(
            Q=states_afd,
            Sigma=afn.Sigma,
            delta=delta_afd,
            q0=initial_afd,
            F=finals_afd
        )