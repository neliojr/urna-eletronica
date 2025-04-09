# Urna Eletrônica

Bem-vindo ao projeto **Urna Eletrônica**, uma aplicação simples para simular um sistema de votação eletrônica. Este programa permite registrar votos, exibir resultados e garantir uma interface básica para testes ou demonstrações. Desenvolvido em Python e compilado para Linux e Windows.

## Funcionalidades
- Gerenciamento de eleitores: criar, remover, buscar e listar eleitores.
- Gerenciamento de cargos e candidatos: criar, remover, buscar e listar cargos e candidatos.
- Contagem automática e exibição dos resultados da votação.
- Interface de usuário em texto (TUI) no terminal e interface gráfica (GUI).
- Suporte multiplataforma (Linux e Windows).

## Downloads
Baixe a versão mais recente na seção de [Releases](https://github.com/neliojr/urna-eletronica/releases/tag/v1.0.0):
- **Linux**: `urna-eletronica`  
- **Windows**: `urna-eletronica.exe`

## Como usar

### No Linux
1. Baixe o binário `urna-eletronica` da release.
2. Dê permissão de execução:
   ```bash
   chmod +x urna-eletronica
   ```
3. Execute:
   ```bash
   ./urna-eletronica
   ```

### No Windows
1. Baixe o arquivo `urna-eletronica.exe` da release.
2. Clique duas vezes no arquivo para executar.
3. Siga as instruções exibidas no terminal.

## Requisitos
- **Linux**: Testado em distribuições baseadas em Arch Linux (64-bit). Pode funcionar em outras distros com ajustes.
- **Windows**: Compatível com Windows 10/11 (64-bit).

## Instalação do código-fonte (opcional)
Se preferir rodar o projeto a partir do código Python:
1. Clone o repositório:
   ```bash
   git clone https://github.com/neliojr/urna-eletronica.git
   cd urna-eletronica
   ```
2. Instale as dependências:
   ```bash
   pip install tkcalendar gdown fpdf pygame
   ```
3. Execute:
   ```bash
   python main.py
   ```

## Contribuição
Contribuições são bem-vindas! Para sugerir melhorias:
1. Faça um fork do repositório.
2. Crie um branch para sua feature (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -m "Adiciona funcionalidade X"`).
4. Envie um Pull Request.

## Aviso
Este é um projeto experimental para fins educacionais ou de demonstração. Não deve ser usado em eleições reais sem validação oficial e medidas de segurança adequadas.