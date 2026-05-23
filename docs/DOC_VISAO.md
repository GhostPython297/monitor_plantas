# Documento de Visão — Monitor de Plantas

**Instituto Federal de Educação, Ciência e Tecnologia da Paraíba**
Campus Esperança

**Integrantes**
João Augusto Silva de Araújo
Paulo Moura Menezes
Miguel Rodrigo da Silva Normando

---

## Sumário

1. [Introdução](#1-introdução)
2. [Visão Geral do Produto](#2-visão-geral-do-produto)
3. [Escopo do Projeto](#3-escopo-do-projeto)
4. [Benefícios](#4-benefícios)
5. [Processos do Negócio](#5-processos-do-negócio)
6. [Restrições](#5-processos-do-negócio)
7. [Recursos](#7-recursos)
8. [Premissas](#8-premissas)
9. [Pendências](#9-pendências)
10. [Glossário](#10-glossário)

---

## 1. Introdução

### Propósito

Este documento apresenta a visão geral do sistema Monitor de Plantas, desenvolvido como projeto acadêmico da disciplina de Análise e Desenvolvimento de Sistemas do Instituto Federal de Educação, Ciência e Tecnologia da Paraíba, Campus Esperança. Seu propósito é descrever o contexto do problema, os objetivos do sistema e o escopo do projeto, servindo como referência para o desenvolvimento da solução e para o alinhamento entre a equipe e o cliente.

---

## 2. Visão Geral do Produto

### Perspectiva do Produto

O Monitor de Plantas é um sistema web interno voltado para o gerenciamento de cuidados com plantas. O sistema permitirá que colaboradores autenticados cadastrem suas plantas, associem espécies obtidas via API externa, registrem os cuidados realizados — como rega, adubação e poda — e recebam alertas automáticos quando uma planta estiver sem cuidados há mais tempo do que o recomendado. O sistema será desenvolvido com Python e Flask, com persistência de dados em arquivos JSON.

### Resumo dos Objetivos

O sistema será desenvolvido para atender à demanda da empresa Verde Vivo Paisagismo, cujos colaboradores hoje gerenciam os cuidados com plantas de forma manual, por meio de cadernos e lembretes de celular. Esse processo gera perda de informações, esquecimentos e dificuldade de acompanhamento quando a carteira de plantas é grande. O objetivo do Monitor de Plantas é centralizar esse controle em uma interface web simples, reduzindo erros, automatizando alertas e tornando o histórico de cuidados facilmente acessível.

---

## 3. Escopo do Projeto

O sistema afetará diretamente o processo de gestão de cuidados com plantas da Verde Vivo Paisagismo. O valor agregado ao negócio inclui a redução do retrabalho causado por registros perdidos, a automação dos alertas de cuidado — hoje feitos manualmente — e o aumento da confiabilidade das informações sobre o estado das plantas sob responsabilidade da empresa.

O escopo do sistema compreende: autenticação de colaboradores, cadastro e gerenciamento de plantas, consulta a uma API externa para obtenção de dados de espécies (nome comum, nome científico, frequência de rega sugerida, requisitos de luz e temperatura mínima), registro de histórico de cuidados por tipo (rega, adubação e poda), e exibição de um painel de alertas com indicadores visuais de saúde das plantas.

Estão fora do escopo desta versão funcionalidades como notificações por e-mail ou dispositivo móvel, integração com outros sistemas internos e suporte a múltiplos idiomas.

---

## 4. Benefícios

A implantação do Monitor de Plantas trará os seguintes benefícios à Verde Vivo Paisagismo:

- **Centralização das informações:** todas as plantas e seus históricos de cuidados ficam registrados em um único sistema, eliminando o uso de cadernos e lembretes dispersos.
- **Redução de esquecimentos:** os alertas automáticos avisam quando uma planta está sem cuidados há mais tempo do que o recomendado, reduzindo perdas causadas por negligência involuntária.
- **Rastreabilidade:** o histórico de cuidados por tipo (rega, adubação, poda) permite acompanhar a evolução de cada planta ao longo do tempo.
- **Facilidade de uso:** a interface web simples permite que qualquer colaborador da empresa utilize o sistema sem treinamento técnico especializado.

---

## 5. Processos do Negócio

Os principais processos do negócio da Verde Vivo Paisagismo envolvidos com o sistema são:

- **Autenticação de colaboradores:** controle de acesso ao sistema, garantindo que apenas colaboradores autenticados possam utilizá-lo e que cada um acesse exclusivamente seus próprios dados.
- **Consulta de espécies via API externa:** obtenção de informações estruturadas sobre espécies de plantas (nome comum, nome científico, frequência de rega sugerida, requisitos de luz, temperatura mínima) para apoiar o cadastro e as recomendações automáticas.
- **Cadastro de plantas:** registro de novas plantas sob responsabilidade do colaborador, com informações como nome, espécie associada e frequência de rega configurada.
- **Registro de cuidados:** anotação dos cuidados realizados em cada planta, incluindo o tipo (rega, adubação ou poda), a data e observações relevantes.
- **Monitoramento de saúde das plantas:** acompanhamento do estado atual de cada planta com base no tempo decorrido desde o último cuidado registrado.
- **Geração de alertas:** identificação automática das plantas que estão com cuidados em atraso, com destaque visual para facilitar a tomada de decisão dos colaboradores.

---

## 6. Restrições

| Fonte da Restrição | Restrição | Razão |
|--------------------|-----------|-------|
| Tecnologia | O sistema deve ser desenvolvido com Python e Flask. | Escolha da equipe. |
| Persistência | Os dados devem ser armazenados em arquivos JSON. | Escolha da equipe. |
| Paradigma | O sistema deve ser desenvolvido utilizando orientação a objetos. | Requisito da disciplina. |
| Equipe | A equipe é composta por três integrantes com experiência limitada em Python e desenvolvimento web. | Contexto acadêmico. |
| Prazo | O sistema deve ser entregue dentro do prazo da disciplina. | Exigência institucional. |
| Acesso | O sistema será acessado apenas via navegador web, sem versão mobile dedicada. | Escopo definido pela equipe. |

---

## 7. Recursos

Para o desenvolvimento do sistema Monitor de Plantas, serão necessários os seguintes recursos:

- **Humanos:** três desenvolvedores estudantes do curso de Análise e Desenvolvimento de Sistemas do IFPB Campus Esperança, com papéis divididos entre implementação do modelo de classes, persistência de dados em JSON e desenvolvimento da interface web com Flask.
- **Software:** Python 3, Flask, editor de código (VSCode ou similar), navegador web para testes, Git para controle de versão, GitHub para hospedagem do repositório e gerenciamento do projeto, e LucidChart para elaboração dos diagramas UML.
- **Hardware:** computadores pessoais dos integrantes da equipe, com acesso à internet.
- **Gerenciamento:** quadro Kanban no GitHub Projects para acompanhamento das tarefas ao longo do desenvolvimento.

---

## 8. Premissas

As seguintes decisões foram acordadas entre os participantes e devem ser consideradas durante todo o projeto:

- O sistema será desenvolvido para uso via navegador web, sem necessidade de instalação por parte do usuário final.
- A persistência de dados será feita exclusivamente em arquivos JSON, sem uso de banco de dados relacional.
- O código será organizado seguindo o padrão MVC, com separação clara entre modelo, visão e controle.
- As classes do sistema seguirão o paradigma de orientação a objetos, com uso de herança na hierarquia de cuidados.
- O fluxo de trabalho da equipe será gerenciado por um quadro Kanban no GitHub Projects.
- A documentação do código seguirá o padrão PEP 257 para docstrings em Python.

---

## 9. Pendências

As seguintes questões influenciam o projeto e ainda estão pendentes de resolução:

- Conclusão e entrega dos diagramas UML obrigatórios (classes, casos de uso, sequência, atividades e diagrama livre escolhido pela equipe) até o prazo de junho.
- Definição de como cada integrante utilizará ferramentas de inteligência artificial no desenvolvimento — atualmente em uso para planejamento e auxílio na escrita de código, sem padronização formal entre a equipe.

---

## 10. Glossário

- **Monitor de Plantas:** nome do sistema desenvolvido pela equipe para gerenciamento de cuidados com plantas.
- **Verde Vivo Paisagismo:** empresa fictícia utilizada como cliente no contexto deste documento.
- **Colaborador:** usuário autenticado do sistema; funcionário da Verde Vivo Paisagismo com acesso às próprias plantas e registros.
- **Espécie:** conjunto de informações taxonômicas e de cuidado obtidas via API externa e associadas a uma planta durante seu cadastro.
- **Registro:** intervenção realizada em uma planta, composta por tipo de cuidado, data e observação opcional. O histórico de registros é imutável após sua criação.
- **API externa:** serviço web consultado pelo sistema para obtenção de dados estruturados sobre espécies de plantas.
- **Flask:** microframework web para Python utilizado no desenvolvimento da interface e das rotas do sistema.
- **JSON:** formato de arquivo utilizado para persistência dos dados do sistema.
- **MVC:** padrão de arquitetura de software que separa a aplicação em três camadas — Model (modelo), View (visão) e Controller (controle).
- **OO:** orientação a objetos, paradigma de programação adotado no desenvolvimento do sistema.
- **Kanban:** metodologia de gerenciamento de fluxo de trabalho utilizada pela equipe por meio do GitHub Projects.
- **PEP 257:** convenção oficial do Python para escrita de docstrings em classes e métodos.
- **Cuidado:** termo utilizado no sistema para representar qualquer intervenção realizada em uma planta, como rega, adubação ou poda.
- **Alerta:** notificação gerada automaticamente pelo sistema quando uma planta está sem cuidados há mais tempo do que o recomendado.
