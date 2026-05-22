# Decisões do projeto Monitor de Plantas

Flask: Escolhemos Flask por ser leve, fácil de aprender e adequado para projetos pequenos a médios. Ele nos permite criar rotas e lidar com requisições HTTP de forma simples, além de ter uma comunidade ativa e muitos recursos disponíveis.

JSON: Optamos por usar JSON para persistência de dados por ser um formato leve, fácil de ler e escrever, e amplamente suportado em Python. Ele é adequado para armazenar informações estruturadas sobre plantas, cuidados e usuários sem a complexidade de um banco de dados relacional.

MVC: Adotamos a arquitetura MVC (Model-View-Controller) para organizar nosso código de forma clara e modular. As classes de modelo representam as entidades do sistema, os serviços lidam com a lógica de negócios e a persistência, e as rotas do Flask atuam como controladores que conectam o frontend ao backend.

planejamento/: Para manter o contexto do projeto acessível a toda a equipe e a ferramentas de IA, evitando que decisões importantes fiquem só na cabeça de uma pessoa.

Autenticação de usuário foi descartada para manter o escopo simples. Upload de foto das plantas foi descartado. Notificações por e-mail foram descartadas.

Usamos Kanban no lugar de Scrum para ter um fluxo de trabalho mais flexível, já que o projeto é pequeno e a equipe é reduzida. Isso nos permite focar na entrega contínua de valor sem a necessidade de sprints fixos.

GitHub Projects: Optamos por usar GitHub Projects para organizar nossas tarefas e acompanhar o progresso do projeto. Ele se integra bem com nosso repositório e facilita a colaboração entre os membros da equipe, permitindo que todos vejam o status das tarefas e contribuam de forma transparente.
