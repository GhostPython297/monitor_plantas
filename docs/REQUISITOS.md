## Requisitos Funcionais

### Gestão de Usuários

- **RF01:** O sistema deve permitir o cadastro de usuários com nome e e-mail, restritos aos colaboradores da Verde Vivo.
- **RF02:** O sistema deve associar cada planta a um único usuário autenticado.
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

### Segurança e Autenticação

- **RNF01:** O sistema é de **uso exclusivamente interno**, acessível apenas para colaboradores autenticados da Verde Vivo.
- **RNF02:** O sistema deve implementar autenticação de usuários antes de permitir acesso a qualquer funcionalidade.
- **RNF03:** Cada usuário deve acessar exclusivamente seus próprios dados, com isolamento completo entre usuários.

### Desempenho e Tecnologia

- **RNF04:** O sistema deve ser desenvolvido em Python com o framework Flask.
- **RNF05:** A persistência de dados deve ser realizada em arquivos JSON utilizando a biblioteca padrão do Python.
- **RNF06:** O sistema deve responder às requisições da interface web em tempo adequado para uso interativo em ambiente local.

### Arquitetura e Organização

- **RNF07:** O sistema deve seguir o padrão arquitetural MVC, com separação clara entre modelos, serviços e templates.
- **RNF08:** O código deve ser estruturado com orientação a objetos, utilizando herança na hierarquia de cuidados (Rega, Adubação, Poda).
- **RNF09:** Os templates HTML devem ser renderizados com Jinja2, com classes CSS atribuídas dinamicamente com base no status de cada planta.

### Qualidade e Manutenibilidade

- **RNF10:** Todas as classes e métodos públicos devem ser documentados com docstrings seguindo o padrão PEP 257.
- **RNF11:** O repositório deve conter um arquivo README.md com instruções de instalação, execução e estrutura do projeto.
- **RNF12:** O código deve ser versionado no GitHub, com as tarefas gerenciadas por um quadro Kanban no GitHub Projects.

### Usabilidade

- **RNF13:** A interface deve apresentar indicadores visuais claros para distinguir plantas saudáveis de plantas que necessitam de cuidado.
- **RNF14:** O painel de alertas deve ser acessível diretamente pela navegação principal da aplicação.