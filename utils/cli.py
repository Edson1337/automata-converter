import sys


class CLI:
    """
    Classe para gerenciar a interface de linha de comando.
    """
    
    @staticmethod
    def display_final_result(input_string: str, is_accepted: bool):
        """
        Exibe o resultado final da simulação no formato especificado.
        """
        print("\n" + "="*50)
        if input_string == "":
            print("cadeia: ε (épsilon - cadeia vazia)")
        else:
            print(f"cadeia: {input_string}")
        print(f"Resultado: {'Aceita' if is_accepted else 'Rejeitada'}")
        print("Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt")

    @staticmethod
    def get_input_string():
        """
        Obtém a cadeia de entrada via argumento da linha de comando ou input do usuário.
        """
        if len(sys.argv) > 1 and sys.argv[1] not in ['-h', '--help', 'help']:
            # Cadeia passada como argumento
            input_string = sys.argv[1]
            if input_string == "":
                print("Cadeia recebida via argumento: ε (épsilon - cadeia vazia)")
            else:
                print(f"Cadeia recebida via argumento: '{input_string}'")
        else:
            # Solicitar cadeia ao usuário
            input_string = input("Digite a cadeia a ser testada (Enter para ε): ")
            if input_string == "":
                print("Cadeia digitada: ε (épsilon - cadeia vazia)")
            else:
                print(f"Cadeia digitada: '{input_string}'")
        
        return input_string
    
    @staticmethod
    def display_simulation_header():
        """
        Exibe o cabeçalho da seção de simulação.
        """
        print("\n" + "="*50)
        print("SIMULAÇÃO DA CADEIA")
        print("="*50)
    
    @staticmethod
    def display_section_separator(title: str = ""):
        """
        Exibe um separador de seção com título opcional.
        
        Args:
            title: Título opcional para a seção
        """
        print("\n" + "="*50)
        if title:
            print(title)
            print("="*50)
    
    @staticmethod
    def get_simulation_type():
        """
        Pergunta ao usuário que tipo de simulação deseja executar.
        
        Returns:
            bool: True para simulação detalhada, False para simulação completa
        """
        choice = input("Simulação detalhada? (s/N): ").lower().strip()
        return choice.startswith('s')
    
    @staticmethod
    def display_help():
        """
        Exibe informações de ajuda sobre como usar o programa.
        """
        print("Uso: python main.py [cadeia]")
        print("")
        print("Argumentos:")
        print("  cadeia    Cadeia opcional a ser testada (ex: 'abaaab')")
        print("")
        print("Se nenhuma cadeia for fornecida, será solicitada interativamente.")
        print("")
        print("Exemplos:")
        print("  python main.py abaaab")
        print("  python main.py \"\"  # cadeia vazia")
        print("  python main.py       # modo interativo")