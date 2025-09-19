# Operação TORRE 1978 - Simulador de CLI

**Implementado por:** `Bruno Henrique Botelho dos Santos`
**Prazo de Entrega da Atividade:** `19/09/2025`

Este repositório contém a implementação de uma Interface de Linha de Comando (CLI) em Python que simula as operações de uma torre de controle de aeroporto na década de 70. O projeto foi desenvolvido como parte da atividade "Operação TORRE 1978" e utiliza apenas bibliotecas padrão do Python, rodando em um ambiente WSL/Ubuntu.

---

## 🚀 Como Executar

Para rodar a aplicação, siga os passos abaixo no seu terminal.

1.  **Navegue até a pasta raiz do projeto:**
    ```bash
    cd ~/aero70
    ```

2.  **Ative o ambiente virtual:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Guia de Comandos da CLI**
    A aplicação é controlada por subcomandos. Abaixo está a lista completa de todos os comandos e suas opções.

    * **Obter ajuda**
      Mostra todos os comandos disponíveis e suas descrições.
        ```bash
        python3 torre/torre.py --help
        ```

    * **Comando: `importar-dados`**
      Verifica se todos os arquivos de dados necessários (`planos_voo.csv`, `pistas.txt`, etc.) existem.
        ```bash
        python3 torre/torre.py importar-dados
        ```

    * **Comando: `listar`**
      Mostra a tabela de voos planejados. Pode ser ordenada por diferentes critérios.
        ```bash
        # Ordenação padrão (por ETD - Estimated Time of Departure)
        python3 torre/torre.py listar

        # Ordenando pela prioridade (emergências no topo)
        python3 torre/torre.py listar --por prioridade
        ```

    * **Comando: `enfileirar`**
      Adiciona um voo a uma das filas de operação, após passar por validações.
        ```bash
        # Adicionar voo à fila de decolagem
        python3 torre/torre.py enfileirar decolagem --voo ALT123

        # Adicionar voo à fila de pouso
        python3 torre/torre.py enfileirar pouso --voo ALT901
        ```

    * **Comando: `autorizar`**
      Autoriza a próxima operação de uma fila para uma pista específica, validando as condições atuais.
        ```bash
        # Autorizar decolagem na pista 10/28
        python3 torre/torre.py autorizar decolagem --pista 10/28
        ```

    * **Comando: `status`**
      Exibe um painel com o status atual das pistas, tamanho das filas e ocorrências ativas.
        ```bash
        python3 torre/torre.py status
        ```

    * **Comando: `relatorio`**
      Processa o arquivo de log e gera um relatório consolidado do turno na pasta `relatorios/`.
        ```bash
        python3 torre/torre.py relatorio
        ```
    
    * **Comando: `limpar`**
      Utilitário para limpar os arquivos gerados pela simulação (logs, filas e relatórios), preparando o ambiente para um novo turno.
        ```bash
        python3 torre/torre.py limpar
        ```

---

## ⚙️ Regras de Negócio Implementadas

O sistema segue um conjunto de regras para simular as decisões da torre de controle:

* **Validação de Pilotos**: Antes de um voo ser enfileirado, o sistema verifica se a licença do piloto associado à aeronave está válida (não expirada no ano de 1978) e se ele possui a habilitação correta para a aeronave.
* **Validação de Pistas e NOTAMs**: Uma operação só é autorizada se a pista designada estiver com status "ABERTA" e se não houver um NOTAM (Notice to Airmen) ativo que feche a pista no horário simulado da operação.
* **Controle de Duplicidade**: A aplicação impede que o mesmo código de voo seja adicionado mais de uma vez na mesma fila, evitando redundância.
* **Logs e Relatórios**: Todas as ações significativas (autorizações, recusas, falhas) são registradas com data e hora no arquivo `logs/torre.log`. O comando `relatorio` processa este log para gerar um sumário estatístico do turno.

---

## 📂 Estrutura de Arquivos

O projeto está organizado da seguinte forma, conforme a árvore sugerida no documento da atividade:

* `dados/`: Contém todos os arquivos de entrada (`.csv` e `.txt`) que servem de base para a simulação.
* `logs/`: Armazena o `torre.log`, o registro detalhado de todas as operações.
* `relatorios/`: Destino dos relatórios de turno gerados, como `operacao_YYYYMMDD.txt`.
* `torre/`: Contém o script principal da aplicação, `torre.py`.
* `docs/`: Contém a documentação, incluindo este `README.md`.
* `.gitignore`: Especifica os arquivos e pastas que o Git deve ignorar (como o ambiente `.venv`).

---

## 🚧 Limitações e Próximos Passos

Esta implementação possui algumas simplificações e pontos para melhoria futura:

* **Clima (METAR)**: A regra de negócio que restringe as operações a uma por vez quando a visibilidade é inferior a 6KM não foi implementada na lógica de `autorizar`.
* **Tempo Simulado**: O "horário atual" usado para validar os NOTAMs foi fixado em `14:30` para garantir testes consistentes, em vez de usar a hora dinâmica do sistema. Esta abordagem simula a funcionalidade bônus `-hora`.
* **Prioridade de Autorização**: O comando `autorizar` exige que o controlador especifique a fila (`pouso` ou `decolagem`). Ele não seleciona automaticamente a operação de maior prioridade geral (por exemplo, um pouso pendente sobre uma decolagem pendente), conforme a regra de EMERGENCIA > pousos > decolagens.