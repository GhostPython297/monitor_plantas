# Minimundo e Levantamento de Requisitos — Monitor de Plantas

## Minimundo

O Monitor de Plantas é um sistema de monitoramento de plantas domésticas e de jardim desenvolvido para auxiliar usuários no acompanhamento e registro dos cuidados realizados com suas plantas. O sistema permite que cada usuário cadastre suas plantas, informe a espécie e a frequência necessária de rega, e registre os cuidados executados ao longo do tempo.

Cada planta pertence a um único usuário e pode receber diferentes tipos de cuidado: rega, adubação e poda. Cada registro de cuidado é composto por uma data, o tipo de cuidado realizado e uma observação opcional. O sistema acompanha automaticamente a data do último cuidado prestado a cada planta.

Com base na frequência de rega configurada e na data do último cuidado, o sistema é capaz de identificar quais plantas estão necessitando de atenção. Quando uma planta ultrapassa o intervalo estipulado sem receber cuidado, o sistema gera um alerta visível ao usuário, que pode então registrar o cuidado diretamente a partir do painel de alertas.

O sistema é acessado via interface web, onde o usuário pode visualizar a lista completa de suas plantas com indicadores visuais de saúde, cadastrar novas plantas, registrar cuidados e consultar o histórico de cada planta. O objetivo principal é facilitar a rotina de cuidados e evitar que plantas sejam esquecidas sem atenção por períodos prolongados.

## Requisitos Funcionais

### Gestão de Usuários

- **RF01:** O sistema deve permitir o cadastro de usuários com nome e e-mail.
- **RF02:** O sistema deve associar cada planta a um único usuário.
- **RF03:** O sistema deve permitir que o usuário liste todas as suas plantas cadastradas.

### Gestão de Plantas

- **RF04:** O sistema deve permitir o cadastro de uma nova planta com nome, espécie e frequência de rega em dias.
- **RF05:** O sistema deve permitir a visualização dos detalhes de uma planta específica.
- **RF06:** O sistema deve calcular automaticamente quantos dias se passaram desde o último cuidado registrado.
- **RF07:** O sistema deve indicar visualmente se uma planta precisa de cuidado (status: ok / precisa de cuidado).

### Registro de Cuidados

- **RF08:** O sistema deve permitir o registro de um cuidado para uma planta, informando o tipo (Rega, Adubação ou Poda), a data e uma observação opcional.
- **RF09:** O sistema deve armazenar o histórico completo de cuidados vinculado a cada planta.
- **RF10:** O sistema deve atualizar automaticamente a data do último cuidado após cada registro.

### Painel de Alertas

- **RF11:** O sistema deve gerar alertas automáticos para plantas cujo número de dias sem cuidado seja maior ou igual à frequência de rega configurada.
- **RF12:** O sistema deve exibir uma página dedicada de alertas listando todas as plantas que precisam de atenção.
- **RF13:** O sistema deve permitir o registro rápido de rega a partir do painel de alertas, sem necessidade de navegar para outra tela.

## Requisitos Não Funcionais

### Desempenho e Tecnologia

- **RNF01:** O sistema deve ser desenvolvido em Python com o framework Flask.
- **RNF02:** A persistência de dados deve ser realizada em arquivos JSON utilizando a biblioteca padrão do Python.
- **RNF03:** O sistema deve responder às requisições da interface web em tempo adequado para uso interativo em ambiente local.

### Arquitetura e Organização

- **RNF04:** O sistema deve seguir o padrão arquitetural MVC, com separação clara entre modelos, serviços e templates.
- **RNF05:** O código deve ser estruturado com orientação a objetos, utilizando herança na hierarquia de cuidados (Rega, Adubação, Poda).
- **RNF06:** Os templates HTML devem ser renderizados com Jinja2, com classes CSS atribuídas dinamicamente com base no status de cada planta.

### Qualidade e Manutenibilidade

- **RNF07:** Todas as classes e métodos públicos devem ser documentados com docstrings seguindo o padrão PEP 257.
- **RNF08:** O repositório deve conter um arquivo README.md com instruções de instalação, execução e estrutura do projeto.
- **RNF09:** O código deve ser versionado no GitHub, com as tarefas gerenciadas por um quadro Kanban no GitHub Projects.

### Usabilidade

- **RNF10:** A interface deve apresentar indicadores visuais claros para distinguir plantas saudáveis de plantas que necessitam de cuidado.
- **RNF11:** O painel de alertas deve ser acessível diretamente pela navegação principal da aplicação.
