import os
from automata.afn import AFN
from automata.afd import AFD
from automata.formatter import AutomataFormatter


class FileOperations:
    @staticmethod
    def create_output_directory():
        """Cria o diretório 'output' na raiz do projeto se não existir."""
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Diretório '{output_dir}' criado.")
        return output_dir

    @staticmethod
    def write_afn_to_file(afn: AFN, filename: str):
        """Escreve o AFN no formato especificado em um arquivo .txt."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(AutomataFormatter.format_afn(afn))

    @staticmethod
    def write_afd_to_file(afd: AFD, filename: str, title="# AFD Determinizado"):
        """Escreve o AFD no formato especificado em um arquivo .txt."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(AutomataFormatter.format_afd(afd, title))