## Requisitos Funcionais

### Entidade: Colaborador

#### Criar
- **RF01:** O sistema deve permitir o cadastro de colaboradores com nome e e-mail, restritos aos colaboradores da Verde Vivo.

### Entidade: Espécie

> Dados obtidos via API externa. O sistema não realiza cadastro local de espécies.

#### Consultar
- **RF02:** O sistema deve consultar uma API externa para obter dados de espécies de plantas, incluindo nome comum, nome científico, frequência de rega sugerida, requisitos de luz e temperatura mínima.
- **RF03:** O sistema deve permitir a associação de uma espécie a uma planta durante o seu cadastro.

#### Aplicar recomendações
- **RF04:** O sistema deve utilizar a frequência de rega sugerida pela espécie como valor padrão no cadastro da planta, podendo ser ajustada pelo colaborador.

---

### Entidade: Planta

#### Criar
- **RF05:** O sistema deve permitir o cadastro de uma nova planta com nome, espécie e frequência de rega em dias.
- **RF06:** O sistema deve associar cada planta ao colaborador autenticado no momento do seu cadastro.

#### Listar / Consultar
- **RF07:** O sistema deve permitir que o colaborador liste todas as suas plantas cadastradas.
- **RF08:** O sistema deve permitir a visualização dos detalhes de uma planta específica.
- **RF09:** O sistema deve calcular automaticamente quantos dias se passaram desde o último cuidado registrado.
- **RF10:** O sistema deve indicar visualmente se uma planta precisa de cuidado (status: ok / precisa de cuidado).

#### Editar
- **RF11:** O sistema deve permitir que o colaborador edite os dados de configuração de uma planta cadastrada: nome, espécie e frequência de rega.
- **RF12:** Apenas o colaborador proprietário da planta pode editá-la. Colaboradores não autenticados ou que não sejam donos não podem modificar dados alheios.
- **RF13:** As edições devem atualizar imediatamente os dados persistidos no arquivo JSON e afetar cálculos futuros de alertas (nova frequência de rega é aplicada prospectivamente).
- **RF14:** O sistema deve registrar um log simples de alterações contendo: campo editado, valor anterior, valor novo e data/hora da edição.

---

### Entidade: Registro

#### Registrar
- **RF15:** O sistema deve permitir o registro de um cuidado para uma planta, informando o tipo (Rega, Adubação ou Poda), a data e uma observação opcional.
- **RF16:** O sistema deve atualizar automaticamente a data do último cuidado após cada registro.

#### Consultar
- **RF17:** O sistema deve armazenar e permitir a consulta do histórico completo de registros vinculados a cada planta.

---

### Entidade: Alerta

#### Gerar
- **RF18:** O sistema deve gerar alertas automáticos para plantas cujo número de dias sem cuidado seja maior ou igual à frequência de rega configurada.

#### Visualizar
- **RF19:** O sistema deve exibir uma página dedicada de alertas listando todas as plantas que precisam de atenção.

#### Ação Rápida
- **RF20:** O sistema deve permitir o registro rápido de rega a partir do painel de alertas, sem necessidade de navegar para outra tela.

---

## Requisitos Não Funcionais

### Segurança e Autenticação
- **RNF01:** O sistema é de **uso exclusivamente interno**, acessível apenas para colaboradores autenticados da Verde Vivo.
- **RNF02:** O sistema deve implementar autenticação de colaboradores antes de permitir acesso a qualquer funcionalidade.
- **RNF03:** Cada colaborador deve acessar exclusivamente seus próprios dados, com isolamento completo entre colaboradores.

### Desempenho e Tecnologia
- **RNF04:** O sistema deve ser desenvolvido em Python com o framework Flask.
- **RNF05:** A persistência de dados deve ser realizada em arquivos JSON utilizando a biblioteca padrão do Python.
- **RNF06:** O sistema deve consumir uma API externa para obtenção de dados de espécies de plantas.
- **RNF07:** O sistema deve responder às requisições da interface web em tempo adequado para uso interativo em ambiente local.

### Arquitetura e Organização
- **RNF08:** O sistema deve seguir o padrão arquitetural MVC, com separação clara entre modelos, serviços e templates.
- **RNF09:** O código deve ser estruturado com orientação a objetos, utilizando herança na hierarquia de cuidados (Rega, Adubação, Poda).
- **RNF10:** Os templates HTML devem ser renderizados com Jinja2, com classes CSS atribuídas dinamicamente com base no status de cada planta.

### Qualidade e Manutenibilidade
- **RNF11:** Todas as classes e métodos públicos devem ser documentados com docstrings seguindo o padrão PEP 257.
- **RNF12:** O repositório deve conter um arquivo README.md com instruções de instalação, execução e estrutura do projeto.
- **RNF13:** O código deve ser versionado no GitHub, com as tarefas gerenciadas por um quadro Kanban no GitHub Projects.

### Usabilidade
- **RNF14:** A interface deve apresentar indicadores visuais claros para distinguir plantas saudáveis de plantas que necessitam de cuidado.
- **RNF15:** O painel de alertas deve ser acessível diretamente pela navegação principal da aplicação.

### Imutabilidade de Dados
- **RNF16:** O histórico de registros (RF17) é imutável. Registros de cuidados não podem ser editados ou deletados após sua criação, garantindo integridade histórica.