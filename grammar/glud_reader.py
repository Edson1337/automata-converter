import re

class GLUDReader:
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        result = {}
        with open(self.filename, 'r', encoding='utf-8') as f:
            header = f.readline()
            match = re.search(r'G\s*=\s*\(\{(.+?)\},\s*\{(.+?)\},\s*P,\s*(\w)\)', header)
            if not match:
                raise ValueError("Formato da gramática não reconhecido.")
            
            # Usar lista para preservar a ordem
            result['V'] = [x.strip() for x in match.group(1).split(',')]
            result['Sigma'] = [x.strip() for x in match.group(2).split(',')]
            result['S'] = match.group(3).strip()
            
            result['productions'] = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                print(f"Lendo linha: '{line}'")
                
                prod_match = re.match(r'(\w+)\s*->\s*(.+)', line)
                if not prod_match:
                    print(f"Linha não reconhecida como produção: {line}")
                    continue
                    
                left = prod_match.group(1).strip()
                right_full = prod_match.group(2).strip()
                
                # Dividir por '|' para múltiplas alternativas
                alternatives = [alt.strip() for alt in right_full.split('|')]
                
                for right in alternatives:
                    print(f"Processando alternativa: {left} -> {right}")
                    
                    # Validar se o lado esquerdo está em V
                    if left not in result['V']:
                        print(f"Aviso: {left} não está em V, mas adicionando produção")
                    
                    # Processar o lado direito
                    if right == 'ε':
                        result['productions'].append((left, 'ε'))
                        print(f"Adicionada produção epsilon: {left} -> ε")
                    elif len(right) == 2:
                        # Produção do tipo A -> aB
                        symbol, non_terminal = right[0], right[1]
                        if symbol in result['Sigma'] and non_terminal in result['V']:
                            result['productions'].append((left, right))
                            print(f"Adicionada produção: {left} -> {right}")
                        else:
                            print(f"Produção inválida: {left} -> {right}")
                            print(f"  Símbolo '{symbol}' em Sigma: {symbol in result['Sigma']}")
                            print(f"  Não-terminal '{non_terminal}' em V: {non_terminal in result['V']}")
                    elif len(right) == 1:
                        # Pode ser A -> a (terminal) ou A -> B (não-terminal)
                        symbol = right[0]
                        if symbol in result['Sigma']:
                            # É um símbolo terminal
                            result['productions'].append((left, right))
                            print(f"Adicionada produção terminal: {left} -> {right}")
                        elif symbol in result['V']:
                            # É um não-terminal (produção unitária)
                            result['productions'].append((left, right))
                            print(f"Adicionada produção unitária: {left} -> {right}")
                        else:
                            print(f"Produção inválida: {left} -> {right}")
                            print(f"  '{symbol}' não é terminal nem não-terminal")
                    else:
                        print(f"Produção com formato não reconhecido: {left} -> {right}")
                        
        return result