# 🤝 Como contribuir com o GardenTrack

## Pré-requisitos

- **Git**: [git-scm.com](https://git-scm.com) — instale com as opções padrão
- **Python**: [python.org/downloads](https://www.python.org/downloads) — marque **"Add Python to PATH"** durante a instalação

---

## Configuração inicial

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/NOME_DO_REPO.git
cd NOME_DO_REPO

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o projeto
python app.py
```

Acesse no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔄 Fluxo de Pull Requests (obrigatório)

Toda e qualquer alteração ao projeto **deve ser feita através de um Pull Request (PR)**. Isso garante que o código seja revisado antes de integrado à `main`.

### Processo de contribuição

1. **Crie uma branch** para sua alteração:
   ```bash
   git checkout -b minha-feature
   # ou
   git checkout -b fix/descricao-do-bug
   ```

2. **Faça seus commits** com mensagens claras e descritivas:
   ```bash
   git commit -m "feat: adiciona validação de email"
   git commit -m "fix: corrige bug na autenticação"
   ```

3. **Envie sua branch** para o repositório:
   ```bash
   git push origin minha-feature
   ```

4. **Abra um Pull Request** no GitHub com uma descrição clara do que foi mudado

5. **Aguarde aprovação**: Sua PR precisa ser revisada e aprovada por **pelo menos uma pessoa** da equipe antes de fazer merge na `main`

6. **Resolva comentários**: Se houver solicitações de mudança, faça os ajustes e envie os novos commits