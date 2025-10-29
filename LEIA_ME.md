# 📁 ÍNDICE DE ARQUIVOS - Google Maps Ranking Analyzer

Bem-vindo à ferramenta profissional de análise de ranqueamento do Google Maps!

---

## 🚀 COMECE POR AQUI

### Para iniciantes (nunca usou a ferramenta):
1. 📖 Leia o **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** (5 minutos)
2. ⚙️ Configure o **[config.yaml](config.yaml)** com sua API Key
3. ▶️ Execute: `python gmb_ranking_analyzer.py`

### Para usuários intermediários:
1. 📚 Consulte o **[README.md](README.md)** completo
2. 🧪 Explore os **[EXEMPLOS_PRATICOS.py](EXEMPLOS_PRATICOS.py)**
3. 🔧 Use o **[example_advanced_usage.py](example_advanced_usage.py)**

### Para tomadores de decisão:
1. 📊 Leia o **[DOCUMENTO_EXECUTIVO.md](DOCUMENTO_EXECUTIVO.md)**

---

## 📂 ESTRUTURA DE ARQUIVOS

### 🔧 Arquivos Principais (Código)

**1. `gmb_ranking_analyzer.py` (20KB)**
- Código principal da ferramenta
- Classes e funções de análise
- Cálculo de todas as métricas
- Geração de relatórios
- **Quando usar:** É o arquivo que você executa para fazer análises

**2. `example_advanced_usage.py` (13KB)**
- Script interativo com menu
- Exemplos de análise comparativa
- Análise competitiva
- Monitoramento histórico
- **Quando usar:** Para análises mais avançadas com interface amigável

**3. `EXEMPLOS_PRATICOS.py` (22KB)**
- 9 exemplos prontos para copiar
- Códigos comentados e explicados
- Casos de uso reais
- Integrações (Sheets, Email, etc.)
- **Quando usar:** Para implementar funcionalidades específicas

### ⚙️ Arquivos de Configuração

**4. `config.yaml` (5.3KB)**
- Configurações da ferramenta
- API Key
- Parâmetros de busca
- Pesos das métricas
- Opções de relatórios
- **Quando usar:** Sempre que quiser mudar parâmetros de análise

**5. `requirements.txt` (660B)**
- Lista de dependências Python
- Versões recomendadas
- **Quando usar:** Na instalação inicial (`pip install -r requirements.txt`)

### 📚 Documentação

**6. `GUIA_RAPIDO.md` (6.3KB)**
- Tutorial de início rápido
- Instalação em 3 passos
- Exemplos simples
- Dicas básicas
- **Para quem:** Iniciantes que querem começar rapidamente

**7. `README.md` (15KB)**
- Documentação completa
- Explicação detalhada de todas as métricas
- Casos de uso extensos
- FAQ
- Troubleshooting
- **Para quem:** Todos os usuários (referência completa)

**8. `DOCUMENTO_EXECUTIVO.md` (14KB)**
- Visão executiva da ferramenta
- ROI e casos de negócio
- Comparação com outras soluções
- Roadmap e planos futuros
- **Para quem:** Gestores, decisores, investidores

**9. `LEIA_ME.md` (este arquivo)**
- Índice de navegação
- Guia de uso por perfil
- **Para quem:** Ponto de partida para todos

---

## 🎯 GUIA POR PERFIL DE USUÁRIO

### 👤 Dono de Negócio Local
**Seu objetivo:** Melhorar posicionamento do meu negócio no Google Maps

**Leia:**
1. GUIA_RAPIDO.md (entenda o básico)
2. README.md → seção "Como interpretar o Overall Score"
3. EXEMPLOS_PRATICOS.py → `encontrar_meu_negocio()`

**Execute:**
```bash
python gmb_ranking_analyzer.py
# Depois localize seu negócio nos resultados e veja seu score
```

**Foque em:**
- Overall Strength Score do seu negócio
- Gap vs concorrentes
- Métricas com score mais baixo (oportunidades)

---

### 👤 Profissional de Marketing Digital
**Seu objetivo:** Gerar relatórios para clientes e otimizar campanhas

**Leia:**
1. README.md completo
2. DOCUMENTO_EXECUTIVO.md → seção "Casos de Uso"
3. EXEMPLOS_PRATICOS.py → todos os exemplos

**Execute:**
```bash
python example_advanced_usage.py
# Escolha opção 3: Análise competitiva
```

**Foque em:**
- Análise competitiva detalhada
- Relatórios em Excel profissionais
- Monitoramento mensal para clientes
- Demonstração de ROI

---

### 👤 Consultor SEO
**Seu objetivo:** Auditar perfis e dar recomendações estratégicas

**Leia:**
1. README.md → seção "Métricas e Scores"
2. DOCUMENTO_EXECUTIVO.md → seção "Métricas Explicadas"
3. config.yaml → ajuste pesos conforme estratégia

**Execute:**
```bash
# Edite config.yaml com parâmetros específicos
python gmb_ranking_analyzer.py
```

**Foque em:**
- Breakdown detalhado de cada métrica
- Customização de pesos no config.yaml
- Gap analysis para identificar prioridades
- Comparação multi-cidade/keyword

---

### 👤 Desenvolvedor / Analista de Dados
**Seu objetivo:** Integrar a ferramenta ou estender funcionalidades

**Leia:**
1. gmb_ranking_analyzer.py (código fonte)
2. EXEMPLOS_PRATICOS.py → integrações
3. README.md → seção "API e Integrações"

**Execute:**
```python
from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer
# Importe e use as classes diretamente
```

**Foque em:**
- Estrutura de classes e métodos
- Formato dos DataFrames retornados
- Extensão de funcionalidades
- Integrações (Sheets, webhooks, etc.)

---

### 👤 Gestor / Tomador de Decisão
**Seu objetivo:** Entender o valor da ferramenta e ROI

**Leia:**
1. DOCUMENTO_EXECUTIVO.md (completo)
2. README.md → seção "Casos de Uso"

**Não precisa executar nada** - peça para sua equipe técnica

**Foque em:**
- ROI esperado
- Comparação com ferramentas pagas
- Custo operacional (Google API)
- Casos de sucesso

---

## 📖 ORDEM DE LEITURA RECOMENDADA

### Caminho Rápido (30 minutos)
1. GUIA_RAPIDO.md (5 min)
2. Configurar config.yaml (5 min)
3. Executar primeira análise (10 min)
4. Explorar relatórios gerados (10 min)

### Caminho Completo (2 horas)
1. GUIA_RAPIDO.md (10 min)
2. README.md (40 min)
3. Configurar e executar (20 min)
4. EXEMPLOS_PRATICOS.py (30 min)
5. Testar análise competitiva (20 min)

### Caminho Executivo (20 minutos)
1. DOCUMENTO_EXECUTIVO.md (15 min)
2. Ver exemplos de relatórios (5 min)

---

## ⚡ AÇÕES RÁPIDAS

### Quero fazer uma análise AGORA (5 minutos)
```bash
# 1. Instale
pip install -r requirements.txt

# 2. Edite config.yaml e coloque sua API Key

# 3. Execute
python gmb_ranking_analyzer.py
```

### Quero entender as métricas (10 minutos)
📖 Leia: README.md → seção "Métricas e Scores"

### Quero comparar com concorrentes (15 minutos)
```bash
python example_advanced_usage.py
# Escolha opção 3
```

### Quero automatizar análises semanais (20 minutos)
📖 Leia: EXEMPLOS_PRATICOS.py → `monitoramento_semanal()`

### Quero integrar com Google Sheets (30 minutos)
📖 Leia: EXEMPLOS_PRATICOS.py → `exportar_para_sheets()`

---

## 🔧 PERGUNTAS FREQUENTES

**Q: Por onde começo?**
A: GUIA_RAPIDO.md → Configure config.yaml → Execute

**Q: Como obtenho a API Key?**
A: GUIA_RAPIDO.md → seção "Obter API Key do Google"

**Q: Qual arquivo executar?**
A: Para análise simples: `gmb_ranking_analyzer.py`
   Para menu interativo: `example_advanced_usage.py`

**Q: Como customizar os pesos?**
A: Edite `config.yaml` → seção `weights`

**Q: Onde ficam os relatórios?**
A: Pasta `output/` (criada automaticamente)

**Q: Quanto custa?**
A: Primeiros $200/mês são GRÁTIS (≈11.700 buscas)

**Q: Como interpretar o score?**
A: README.md → seção "Métricas e Scores"

**Q: Posso comparar múltiplas cidades?**
A: Sim! EXEMPLOS_PRATICOS.py → `analise_multi_cidade()`

**Q: Como encontrar meu Place ID?**
A: EXEMPLOS_PRATICOS.py → `descobrir_meu_place_id()`

**Q: A ferramenta funciona offline?**
A: Não, requer conexão com Google Maps API

---

## 📊 FORMATO DOS RELATÓRIOS

Cada análise gera 4 arquivos na pasta `output/`:

1. **CSV** - Dados tabulares para análise
2. **Excel** - Múltiplas abas (Completo, Top 10, Stats, Categorias)
3. **JSON** - Dados estruturados para integrações
4. **TXT** - Relatório resumido legível

Exemplo de nome: `ranking_analysis_padaria_20251029_143000.xlsx`

---

## 🎓 PRÓXIMOS PASSOS

Após dominar o básico:

### Nível Intermediário
- [ ] Configurar monitoramento semanal
- [ ] Criar análises comparativas multi-keyword
- [ ] Exportar para Google Sheets
- [ ] Configurar alertas por email

### Nível Avançado
- [ ] Customizar pesos das métricas
- [ ] Integrar com outras ferramentas (Analytics, CRM)
- [ ] Criar dashboards personalizados
- [ ] Desenvolver automações com a API

### Nível Expert
- [ ] Contribuir com código no GitHub
- [ ] Criar extensões personalizadas
- [ ] Implementar Machine Learning
- [ ] Desenvolver integrações empresariais

---

## 🆘 PRECISA DE AJUDA?

### Problemas Técnicos
- Consulte: README.md → seção "Troubleshooting"
- Verifique: Logs em `gmb_analyzer.log`

### Dúvidas sobre Métricas
- Leia: README.md → seção "Métricas e Scores"
- Ou: DOCUMENTO_EXECUTIVO.md → "Métricas Explicadas"

### Exemplos de Código
- Veja: EXEMPLOS_PRATICOS.py (9 exemplos prontos)

### Estratégia e ROI
- Leia: DOCUMENTO_EXECUTIVO.md

### Suporte da Comunidade
- Stack Overflow (tag: google-maps-api)
- GitHub Issues
- Reddit r/LocalSEO

---

## ✅ CHECKLIST DE SETUP

Antes de começar, verifique:

- [ ] Python 3.8+ instalado
- [ ] Conta Google Cloud criada
- [ ] API Key do Google Maps obtida
- [ ] Places API ativada
- [ ] Faturamento habilitado (mesmo para uso grátis)
- [ ] Arquivos baixados
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] config.yaml configurado com sua API Key
- [ ] Coordenadas do local definidas
- [ ] Palavra-chave definida

**Tudo OK?** Execute: `python gmb_ranking_analyzer.py`

---

## 🎉 BEM-VINDO!

Você agora tem acesso a uma ferramenta profissional de análise de ranqueamento do Google Maps.

**Boa análise! 🚀**

---

*Última atualização: Outubro 2025*
*Versão: 1.0.0*
