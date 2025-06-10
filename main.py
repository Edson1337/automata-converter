import os
import sys
from grammar.glud_reader import GLUDReader
from automata.converter import Converter
from utils.file_operations import FileOperations
from utils.cli import CLI


grammar_file_path = './grammar/glud.txt'

def main():
    # Verificar se o usuário solicitou ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        CLI.display_help()
        return
    
    try:
        reader = GLUDReader(grammar_file_path)
        grammar = reader.parse()
        print(grammar)

        converter = Converter(grammar)
        afn = converter.convert_glud_to_afn()
        print(afn)

        afd = converter.convert_afn_to_afd(afn)
        print(afd)

        # Testar operações de fecho
        CLI.display_section_separator()
        
        # Complemento
        afd_complement = afd.apply_complement_verbose()
        print("\n# AFD Complemento:")
        print(afd_complement)
        
        CLI.display_section_separator()
        
        # Reverso
        afd_reverse = afd.apply_reverse_verbose()
        print("\n# AFD Reverso:")
        print(afd_reverse)
        
        # Salvar arquivos
        output_dir = FileOperations.create_output_directory()
        
        afn_path = os.path.join(output_dir, 'AFN.txt')
        afd_path = os.path.join(output_dir, 'AFD.txt')
        complement_path = os.path.join(output_dir, 'COMP.txt')
        reverse_path = os.path.join(output_dir, 'REV.txt')
        
        FileOperations.write_afn_to_file(afn, afn_path)
        FileOperations.write_afd_to_file(afd, afd_path)
        FileOperations.write_afd_to_file(afd_complement, complement_path, "# AFD Complemento")
        FileOperations.write_afd_to_file(afd_reverse, reverse_path, "# AFD Reverso")
        
        print(f"\nArquivos salvos:")
        print(f"- AFN original: {afn_path}")
        print(f"- AFD original: {afd_path}")
        print(f"- AFD complemento: {complement_path}")
        print(f"- AFD reverso: {reverse_path}")
        
        # Simulação da cadeia
        CLI.display_simulation_header()
        
        input_string = CLI.get_input_string()
        
        # Simular no AFD original
        print(f"\nSimulando no AFD original:")
        is_accepted = afd.simulate(input_string, verbose=True)
        
        # Resultado final - APENAS UMA CHAMADA
        CLI.display_final_result(input_string, is_accepted)

    except ValueError as e:
        print(f"Erro ao ler a gramática: {e}")
    except FileNotFoundError:
        print("Arquivo de gramática não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()