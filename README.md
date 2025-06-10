# Automata Converter

Um conversor de gramáticas GLUD (Gramáticas Livres de Contexto Unidirecionais) para autômatos finitos, com operações de fecho e simulação de cadeias.

## 📁 Estrutura do Projeto

```
automata-converter/
├── automata/
│   ├── __init__.py
│   ├── af.py               # Classe base para autômatos finitos
│   ├── afn.py              # Autômato Finito Não-Determinístico
│   ├── afd.py              # Autômato Finito Determinístico
│   ├── formatter.py        # Formatação de autômatos para exibição/arquivo
│   └── converter.py        # Conversores GLUD→AFN e AFN→AFD
├── grammar/
│   ├── __init__.py
│   ├── glud.py             # Classe para representar gramáticas GLUD
│   ├── glud_reader.py      # Leitor de arquivos de gramática
│   └── glud.txt            # Arquivo de entrada da gramática
├── utils/
│   ├── __init__.py
│   ├── cli.py              # Interface de linha de comando
│   └── file_operations.py  # Operações de arquivo
├── output/                 # Diretório de saída (gerado automaticamente)
│   ├── AFN.txt            # AFN original
│   ├── AFD.txt            # AFD determinizado
│   ├── COMP.txt           # AFD complemento
│   └── REV.txt            # AFD reverso
├── main.py                # Programa principal
└── README.md
```

## 🚀 Funcionalidades

### 1. **Conversão de Gramáticas**
- **GLUD → AFN**: Converte gramáticas GLUD para Autômatos Finitos Não-Determinísticos
- **AFN → AFD**: Determinização de AFN usando algoritmo de construção de subconjuntos

### 2. **Operações de Fecho**
- **Complemento**: Gera o AFD complemento (inverte estados finais)
- **Reverso**: Gera o AFD reverso (inverte transições e cria novo estado inicial)

### 3. **Simulação de Cadeias**
- Simula a execução de cadeias de entrada no AFD
- Exibe passo a passo as transições realizadas
- Indica se a cadeia é aceita ou rejeitada

### 4. **Geração de Arquivos**
- Salva todos os autômatos em formato texto legível
- Organiza saídas no diretório `output/`

### 5. **Interface de Linha de Comando**
- Aceita cadeias como argumentos da linha de comando
- Modo interativo para entrada de cadeias
- Formatação padronizada de saídas

## 📖 Como Usar

### Pré-requisitos
- Python 3.7+
- Arquivo `grammar/glud.txt` com a gramática GLUD

### Execução

#### 1. Com cadeia como argumento:
```bash
python main.py abaaab
```

#### 2. Modo interativo:
```bash
python main.py
# O programa solicitará a cadeia de entrada
```

#### 3. Ajuda:
```bash
python main.py --help
```

### Exemplo de Saída

```
cadeia: abaaab
Resultado: Aceita
Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt
```

## 📝 Formato da Gramática GLUD

O arquivo `grammar/glud.txt` deve seguir o formato:

```
NT: S, A, B
T: a, b
S: S
P:
S -> aA | bB
A -> aS | b
B -> bS | a
```

Onde:
- **NT**: Símbolos não-terminais
- **T**: Símbolos terminais
- **S**: Símbolo inicial
- **P**: Produções da gramática

## 📊 Arquivos de Saída

### AFN.txt
```
# AFN Original
Q: q0, q1, q2, q3, q4, q5
Σ: a, b
δ:
q0, a -> q1
q1, b -> q0
q1, ε -> q2
...
```

### AFD.txt
```
# AFD Determinizado
Q: {q0}, {q0, q2, q4}, {q1, q2}, {q1, q2, q3, q5}, {q2, q3, q5}
Σ: a, b
δ:
{q0, q2, q4}, a -> {q1, q2, q3, q5}
...
```

### COMP.txt
```
# AFD Complemento
Q: {q0}, {q0, q2, q4}, {q1, q2}, {q1, q2, q3, q5}, {q2, q3, q5}
Σ: a, b
δ:
...
F: {q0}, {q0, q2, q4}, {q1, q2}  # Estados finais invertidos
```

### REV.txt
```
# AFD Reverso
Q: {q0, q4, q5}, {q1, q2}, {q1, q2, q3, q4, q5}, {q2, q3, q4, q5}, {q3, q4}
Σ: a, b
δ:
...  # Transições invertidas
```

## 🔧 Detalhes Técnicos

### Algoritmos Implementados

1. **Construção de AFN a partir de GLUD**
   - Conversão direta das produções em transições
   - Tratamento de transições ε (épsilon)

2. **Determinização (AFN → AFD)**
   - Algoritmo de construção de subconjuntos
   - Cálculo de ε-fechos
   - Eliminação de não-determinismo

3. **Operação de Complemento**
   - Inversão simples dos estados finais
   - Preservação da estrutura do autômato

4. **Operação de Reverso**
   - Inversão de todas as transições
   - Criação de novo estado inicial com transições ε
   - Determinização do AFN resultante

### Estrutura de Classes

- **AF**: Classe base abstrata para autômatos
- **AFN**: Implementa autômatos não-determinísticos
- **AFD**: Implementa autômatos determinísticos com operações de fecho
- **GLUD**: Representa gramáticas livres de contexto unidirecionais
- **Converter**: Implementa algoritmos de conversão
- **AutomataFormatter**: Formatação padronizada para exibição

## 🧪 Exemplo de Execução Completa

```bash
$ python main.py abaa

# Saída:
=== Aplicando Complemento ===
Estados originais: 5
Estados finais originais: 2
Estados finais após complemento: 3

=== Aplicando Reverso ===
AFD original tem 5 estados
Passo 1: Criando AFN reverso (invertendo transições)...
Passo 2: Adicionando transições ε do novo estado inicial...
Passo 3: Determinizando AFN reverso para obter AFD...
AFD reverso final tem 5 estados

==================================================
SIMULAÇÃO DA CADEIA
==================================================

Simulando cadeia: 'abaa'
Estado inicial: {q0,q2,q4}
Passo 1: Lendo símbolo 'a'
  {q0,q2,q4} --a--> {q1,q2,q3,q5}
Passo 2: Lendo símbolo 'b'
  {q1,q2,q3,q5} --b--> {q0}
Passo 3: Lendo símbolo 'a'
  {q0} --a--> {q1,q2}
Passo 4: Lendo símbolo 'a'
  {q1,q2} --a--> {q2,q3,q5}
Estado final: {q2,q3,q5}
Estado final é de aceitação? Sim

==================================================
cadeia: abaa
Resultado: Aceita
Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt
```

## 📚 Teoria dos Autômatos

Este projeto implementa conceitos fundamentais da Teoria da Computação:

- **Gramáticas Livres de Contexto**: Representação formal de linguagens
- **Autômatos Finitos**: Reconhecedores de linguagens regulares
- **Determinização**: Conversão de não-determinismo para determinismo
- **Operações de Fecho**: Complemento e reverso de linguagens regulares
- **Simulação**: Verificação de aceitação de cadeias

## 📄 Licença

Este projeto é desenvolvido para fins educacionais na disciplina de Teoria da Computação.