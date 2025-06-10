from .af import AF
from .formatter import AutomataFormatter
from typing import Dict, Set, Tuple, FrozenSet

class AFD(AF):
    def __init__(
        self,
        Q: Set[FrozenSet[str]],  # Estados compostos como conjuntos imutáveis
        Sigma: Set[str],
        delta: Dict[Tuple[FrozenSet[str], str], FrozenSet[str]],  # Transições entre conjuntos
        q0: FrozenSet[str],  # Estado inicial como conjunto
        F: Set[FrozenSet[str]]  # Estados finais como conjuntos
    ):
        super().__init__(Q, Sigma, delta, q0, F)
    
    def __repr__(self):
        return AutomataFormatter.format_afd(self)
    
    def simulate(self, input_string: str, verbose=True) -> bool:
        """
        Simula a execução de uma cadeia no AFD.
        
        Args:
            input_string: A cadeia a ser testada (string vazia = cadeia ε)
            verbose: Se True, exibe o processo passo a passo
            
        Returns:
            bool: True se a cadeia é aceita, False caso contrário
        """
        current_state = self.q0
        
        if verbose:
            if input_string == "":
                print(f"Simulando cadeia épsilon (ε) - cadeia vazia")
            else:
                print(f"Simulando cadeia: '{input_string}'")
            print(f"Estado inicial: {{{','.join(sorted(current_state))}}}")
        
        # Caso especial: cadeia vazia (épsilon)
        if input_string == "":
            if verbose:
                print("Cadeia vazia - nenhuma transição executada")
                print(f"Permanece no estado inicial: {{{','.join(sorted(current_state))}}}")
            
            # Para cadeia épsilon, verificamos se o estado inicial é final
            is_accepted = current_state in self.F
            
            if verbose:
                print(f"Estado inicial é final? {'Sim' if is_accepted else 'Não'}")
            
            return is_accepted
        
        # Processar cada símbolo da cadeia (caso normal)
        for i, symbol in enumerate(input_string):
            if verbose:
                print(f"Passo {i+1}: Lendo símbolo '{symbol}'")
            
            # Verificar se o símbolo está no alfabeto
            if symbol not in self.Sigma:
                if verbose:
                    print(f"  ERRO: Símbolo '{symbol}' não está no alfabeto {{{','.join(sorted(self.Sigma))}}}")
                return False
            
            # Buscar transição
            transition_key = (current_state, symbol)
            if transition_key in self.delta:
                next_state = self.delta[transition_key]
                if verbose:
                    current_str = "{" + ",".join(sorted(current_state)) + "}"
                    next_str = "{" + ",".join(sorted(next_state)) + "}"
                    print(f"  {current_str} --{symbol}--> {next_str}")
                current_state = next_state
            else:
                if verbose:
                    current_str = "{" + ",".join(sorted(current_state)) + "}"
                    print(f"  ERRO: Não há transição de {current_str} com símbolo '{symbol}'")
                return False
        
        # Verificar se o estado final é de aceitação
        is_accepted = current_state in self.F
        
        if verbose:
            final_str = "{" + ",".join(sorted(current_state)) + "}"
            print(f"Estado final: {final_str}")
            print(f"Estado final é de aceitação? {'Sim' if is_accepted else 'Não'}")
        
        return is_accepted
    
    def simulate_quiet(self, input_string: str) -> bool:
        """
        Simula a execução de uma cadeia no AFD sem prints.
        
        Args:
            input_string: A cadeia a ser testada
            
        Returns:
            bool: True se a cadeia é aceita, False caso contrário
        """
        return self.simulate(input_string, verbose=False)
    
    def print_transition_table(self):
        AutomataFormatter.print_afd_transition_table(self)

    def apply_complement(self):
        """
        Aplica a operação de complemento no AFD.
        Estados finais se tornam não-finais e vice-versa.
        """
        # Novos estados finais são todos os estados que não são finais no AFD original
        new_accept_states = {state for state in self.Q if state not in self.F}
        
        return AFD(
            Q=self.Q.copy(),
            Sigma=self.Sigma.copy(),
            delta=self.delta.copy(),
            q0=self.q0,
            F=new_accept_states
        )
    
    def apply_complement_verbose(self):
        """
        Versão detalhada do complemento que mostra o processo.
        """
        print("=== Aplicando Complemento ===")
        print(f"Estados originais: {len(self.Q)}")
        print(f"Estados finais originais: {len(self.F)}")
        
        complement_afd = self.apply_complement()
        
        print(f"Estados finais após complemento: {len(complement_afd.F)}")
        print("Estados que mudaram de status:")
        
        # Mostrar mudanças
        from .formatter import AutomataFormatter
        
        # Estados que eram finais e agora não são
        became_non_final = self.F - complement_afd.F
        if became_non_final:
            print("  Deixaram de ser finais:")
            for state in became_non_final:
                state_str = "{" + ",".join(sorted(state)) + "}"
                print(f"    {state_str}")
        
        # Estados que não eram finais e agora são
        became_final = complement_afd.F - self.F
        if became_final:
            print("  Tornaram-se finais:")
            for state in became_final:
                state_str = "{" + ",".join(sorted(state)) + "}"
                print(f"    {state_str}")
        
        return complement_afd
    
    def apply_reverse(self):
        """
        Aplica a operação de reverso no AFD e retorna um AFD determinizado.
        """
        from .afn import AFN  # Import local para evitar circulares
        from automata.converter import Converter  # Import absoluto (não relativo)
        
        # Primeiro, criar o AFN reverso
        new_initial_state = 'R'
        new_states = set()
        state_mapping = {}
        
        for i, state in enumerate(sorted(self.Q, key=lambda s: ",".join(sorted(s)))):
            state_name = f"q{i}"
            state_mapping[state] = state_name
            new_states.add(state_name)
        
        new_states.add(new_initial_state)
        new_delta = {}
        
        # Inverter transições
        for (source_state, symbol), target_state in self.delta.items():
            source_name = state_mapping[target_state]  # Inverter: destino vira origem
            target_name = state_mapping[source_state]  # Inverter: origem vira destino
            
            if source_name not in new_delta:
                new_delta[source_name] = {}
            if symbol not in new_delta[source_name]:
                new_delta[source_name][symbol] = set()
            
            new_delta[source_name][symbol].add(target_name)
        
        # Conectar novo estado inicial aos antigos estados finais com ε
        new_delta[new_initial_state] = {'': set()}
        for final_state in self.F:
            final_name = state_mapping[final_state]
            new_delta[new_initial_state][''].add(final_name)
        
        # Estado final
        old_initial_name = state_mapping[self.q0]
        new_accept_states = {old_initial_name}
        
        # Criar AFN reverso
        afn_reverse = AFN(
            Q=new_states,
            Sigma=self.Sigma.copy(),
            delta=new_delta,
            q0=new_initial_state,
            F=new_accept_states
        )
        
        # Determinizar o AFN para obter AFD
        converter = Converter({})  # Converter vazio só para usar o método
        afd_reverse = converter.convert_afn_to_afd(afn_reverse)
        
        return afd_reverse

    def apply_reverse_verbose(self):
        """
        Versão detalhada do reverso que mostra o processo e retorna AFD determinizado.
        """
        print("=== Aplicando Reverso ===")
        print(f"AFD original tem {len(self.Q)} estados")
        print(f"Estado inicial original: {{{','.join(sorted(self.q0))}}}")
        print(f"Estados finais originais: {len(self.F)}")
        
        print("Passo 1: Criando AFN reverso (invertendo transições)...")
        print("Passo 2: Adicionando transições ε do novo estado inicial...")
        print("Passo 3: Determinizando AFN reverso para obter AFD...")
        
        # Usar o método não-verbose para fazer o trabalho
        afd_reverse = self.apply_reverse()
        
        print(f"AFD reverso final tem {len(afd_reverse.Q)} estados")
        print(f"Estados finais do AFD reverso: {len(afd_reverse.F)}")
        
        return afd_reverse