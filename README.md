# 🎯 Google Maps Business Profile Analyzer & Ranking Tool

Sistema **ultra profissional** para análise de força de perfil e ranqueamento local no Google Maps. Ferramenta completa para SEO local, análise competitiva e otimização de presença online.

---

## 📋 Índice

- [Características](#-características)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso Básico](#-uso-básico)
- [Uso Avançado](#-uso-avançado)
- [Métricas e Scores](#-métricas-e-scores)
- [Relatórios Gerados](#-relatórios-gerados)
- [Exemplos Práticos](#-exemplos-práticos)
- [FAQ](#-faq)
- [Suporte](#-suporte)

---

## 🚀 Características

### Análise Multidimensional
- ✅ **Rating Quality Score** - Qualidade das avaliações ponderada por volume
- ✅ **Review Velocity Score** - Velocidade de aquisição de novos reviews
- ✅ **Completeness Score** - Completude do perfil (fotos, horários, contato, etc.)
- ✅ **Authority Score** - Autoridade do negócio no mercado
- ✅ **Prominence Score** - Proeminência na busca local
- ✅ **Relevance Score** - Relevância para palavra-chave pesquisada

### Funcionalidades Profissionais
- 📊 **Ranking Position Tracking** - Monitoramento preciso de posições
- 🎯 **Análise Competitiva** - Compare seu negócio com concorrentes
- 📈 **Análise Comparativa** - Múltiplas palavras-chave simultaneamente
- 💡 **Gap Analysis** - Identifique oportunidades de melhoria
- 🏆 **Categorização Automática** - 7 níveis de força (Dominante → Muito Fraco)
- 📁 **Múltiplos Formatos** - CSV, Excel, JSON, TXT

### Relatórios Detalhados
- Top 10 Rankings
- Estatísticas descritivas
- Distribuição por categoria
- Análise de gaps competitivos
- Insights acionáveis
- Recomendações personalizadas

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Conta Google Cloud Platform
- Google Maps API Key habilitada para:
  - Places API
  - Geocoding API (opcional)

### Passo 1: Clone ou baixe os arquivos

```bash
# Se usar git
git clone <repositório>
cd gmb-ranking-analyzer

# Ou baixe e extraia os arquivos
```

### Passo 2: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Configure sua API Key

Edite o arquivo `config.yaml`:

```yaml
api:
  key: "SUA_API_KEY_AQUI"  # ← Substitua aqui
```

---

## ⚙️ Configuração

### Arquivo config.yaml

O arquivo de configuração permite personalizar todos os aspectos da análise:

```yaml
# Parâmetros de busca
search:
  location: "-23.55052,-46.633308"  # Coordenadas (lat,lng)
  radius: 2000                       # Raio em metros
  keyword: "padaria"                 # Palavra-chave
  max_pages: 3                       # Páginas de resultados

# Pesos para cálculo de score (customize conforme sua estratégia)
weights:
  rating_quality: 0.25
  review_velocity: 0.20
  completeness: 0.15
  authority: 0.20
  prominence: 0.10
  relevance: 0.10
```

### Obter Coordenadas

1. Acesse [Google Maps](https://maps.google.com)
2. Clique com botão direito no local desejado
3. Clique em "Latitude, Longitude"
4. Copie as coordenadas (formato: `-23.55052,-46.633308`)

---

## 🎮 Uso Básico

### Método 1: Script Principal

```python
from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer, generate_reports

# Inicializa
API_KEY = "sua_chave_aqui"
analyzer = GoogleMapsRankingAnalyzer(API_KEY)

# Executa análise
metrics_list, df = analyzer.run_analysis(
    location="-23.55052,-46.633308",
    radius=2000,
    keyword="padaria",
    max_pages=3
)

# Gera relatórios
files = generate_reports(df, "padaria")

print(f"✅ Análise concluída! {len(df)} perfis analisados.")
```

### Método 2: Script Interativo

```bash
python example_advanced_usage.py
```

Menu interativo com opções:
1. Análise única
2. Análise comparativa
3. Análise competitiva

---

## 🔬 Uso Avançado

### Análise Competitiva

Compare seu negócio com concorrentes específicos:

```python
from example_advanced_usage import analyze_competitor, load_config

config = load_config()

# Place IDs do seu negócio e concorrentes
target_id = "ChIJN1t_tDeuEmsRUsoyG83frY4"
competitor_ids = [
    "ChIJrTLr-GyuEmsRBfy61i59si0",
    "ChIJ-WP3K3KuEmsRi5UPW9V-CmM"
]

# Executa análise
df_competitive = analyze_competitor(config, target_id, competitor_ids)
```

**Resultado:**
```
🎯 SEU NEGÓCIO
Nome: Padaria Exemplo
Posição no ranking: #5
Score geral: 72.45 ✅ FORTE

💡 ANÁLISE DE GAPS:
✅ Qualidade das Avaliações: +5.2 vs média
⚠️ Velocidade de Reviews: -8.5 vs melhor
✅ Completude do Perfil: +12.3 vs média
```

### Análise de Múltiplas Palavras-chave

Compare o desempenho em diferentes buscas:

```python
from example_advanced_usage import analyze_multiple_keywords

# Configure no config.yaml:
# multiple_keywords:
#   enabled: true
#   keywords:
#     - "padaria"
#     - "confeitaria"
#     - "bakery"

results = analyze_multiple_keywords(config)
```

### Customização de Pesos

Ajuste os pesos conforme sua estratégia:

```python
# Para priorizar avaliações
analyzer.WEIGHTS = {
    'rating_quality': 0.35,      # ↑ aumentado
    'review_velocity': 0.25,     # ↑ aumentado
    'completeness': 0.10,        # ↓ reduzido
    'authority': 0.15,
    'prominence': 0.10,
    'relevance': 0.05
}
```

---

## 📊 Métricas e Scores

### 1. Rating Quality Score (0-100)

Avalia a qualidade das avaliações considerando:
- Nota média (0-5 estrelas)
- Volume de avaliações
- Fator de confiança (logarítmico)

**Fórmula:**
```
Score = (Rating/5 × 100) × (0.5 + 0.5 × log₁₀(reviews+1)/log₁₀(500))
```

**Exemplo:**
- 4.5★ com 10 reviews → Score: ~67
- 4.5★ com 100 reviews → Score: ~86
- 4.5★ com 500 reviews → Score: ~90

### 2. Review Velocity Score (0-100)

Mede a frequência de novos reviews:

```
Score = min((total_reviews / 200) × 100, 100)
```

**Interpretação:**
- 0-25: Baixa atividade
- 26-50: Atividade moderada
- 51-75: Boa atividade
- 76-100: Excelente atividade

### 3. Completeness Score (0-100)

Avalia preenchimento do perfil:

| Campo | Peso |
|-------|------|
| Website | 20 |
| Fotos | 20 |
| Telefone | 15 |
| Endereço | 15 |
| Horários | 15 |
| Status | 5 |
| Tipos | 5 |
| Preço | 5 |

**Meta:** ≥ 80 pontos

### 4. Authority Score (0-100)

Indica credibilidade do negócio:

- **40%** Volume de reviews
- **30%** Rating consistente
- **15%** Presença web
- **15%** Conteúdo visual

### 5. Prominence Score (0-100)

Combina posição e proximidade:

- **60%** Posição no ranking
- **40%** Proximidade geográfica

### 6. Relevance Score (0-100)

Relevância para palavra-chave:

- **50%** Palavra-chave no nome
- **30%** Tipos de negócio relevantes
- **20%** Menção na localidade

### Overall Strength Score

Score final ponderado:

```
Overall = (Rating_Quality × 0.25) +
          (Review_Velocity × 0.20) +
          (Completeness × 0.15) +
          (Authority × 0.20) +
          (Prominence × 0.10) +
          (Relevance × 0.10)
```

**Categorias:**
- 90-100: 🏆 DOMINANTE
- 80-90: 💪 MUITO FORTE
- 70-80: ✅ FORTE
- 60-70: 📊 BOM
- 50-60: ⚠️ MÉDIO
- 40-50: 📉 FRACO
- 0-40: 🚨 MUITO FRACO

---

## 📁 Relatórios Gerados

### 1. CSV Completo
`ranking_analysis_{keyword}_{timestamp}.csv`

Todas as métricas em formato tabular para análise.

### 2. Excel Multi-abas
`ranking_analysis_{keyword}_{timestamp}.xlsx`

**Abas:**
- **Análise Completa** - Todos os dados
- **Top 10** - Melhores perfis
- **Estatísticas** - Análise descritiva
- **Por Categoria** - Agrupamento por força

### 3. JSON Estruturado
`ranking_analysis_{keyword}_{timestamp}.json`

Dados estruturados para integração com outras ferramentas.

### 4. Relatório Resumido
`summary_report_{keyword}_{timestamp}.txt`

Resumo executivo em texto puro:
```
================================================================================
RELATÓRIO DE ANÁLISE DE RANQUEAMENTO - PADARIA
Data: 29/10/2025 14:30:00
================================================================================

Total de perfis analisados: 60

TOP 10 RANKINGS:
--------------------------------------------------------------------------------

#1 - Padaria Exemplo
   Score Geral: 87.45 💪 MUITO FORTE
   Rating: 4.7 ⭐ (234 reviews)
   Distância: 450m
   Percentil: 95.0%

[...]
```

### 5. Análise Competitiva
`competitive_analysis_{keyword}.xlsx`

**Abas:**
- **Comparação** - Seu negócio vs concorrentes
- **Análise de Gaps** - Oportunidades detalhadas

---

## 💼 Exemplos Práticos

### Caso 1: Monitorar Posição Semanal

```python
# script_monitoramento_semanal.py
import schedule
import time
from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer, generate_reports
from datetime import datetime

def analise_semanal():
    analyzer = GoogleMapsRankingAnalyzer("SUA_API_KEY")
    
    metrics_list, df = analyzer.run_analysis(
        location="-23.55052,-46.633308",
        radius=2000,
        keyword="padaria",
        max_pages=3
    )
    
    # Salva com timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    generate_reports(df, f"padaria_semana_{timestamp}")
    
    print(f"✅ Análise semanal concluída: {timestamp}")

# Agenda para toda segunda às 9h
schedule.every().monday.at("09:00").do(analise_semanal)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Verifica a cada hora
```

### Caso 2: Análise Multi-cidade

```python
cidades = {
    "São Paulo": "-23.55052,-46.633308",
    "Rio de Janeiro": "-22.9068,-43.1729",
    "Belo Horizonte": "-19.9167,-43.9345"
}

analyzer = GoogleMapsRankingAnalyzer("SUA_API_KEY")

for cidade, coords in cidades.items():
    print(f"\n📍 Analisando: {cidade}")
    
    metrics_list, df = analyzer.run_analysis(
        location=coords,
        radius=3000,
        keyword="restaurante italiano",
        max_pages=3
    )
    
    generate_reports(df, f"restaurante_italiano_{cidade}")
```

### Caso 3: Alerta de Mudança de Posição

```python
import json
from pathlib import Path

def verificar_mudanca_posicao(place_id, keyword):
    """Verifica se houve mudança de posição"""
    
    cache_file = Path(f"cache_posicao_{place_id}.json")
    
    # Análise atual
    analyzer = GoogleMapsRankingAnalyzer("SUA_API_KEY")
    metrics_list, df = analyzer.run_analysis(
        location="-23.55052,-46.633308",
        radius=2000,
        keyword=keyword,
        max_pages=3
    )
    
    current_row = df[df['place_id'] == place_id]
    if current_row.empty:
        return None
    
    current_position = int(current_row.iloc[0]['rank_position'])
    
    # Compara com cache
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            previous = json.load(f)
            previous_position = previous['position']
            
            delta = previous_position - current_position
            
            if delta != 0:
                direction = "⬆️ subiu" if delta > 0 else "⬇️ caiu"
                print(f"🚨 ALERTA: Posição {direction} {abs(delta)} posições!")
                print(f"   Anterior: #{previous_position} → Atual: #{current_position}")
                
                # Enviar notificação (email, SMS, Slack, etc.)
                enviar_notificacao(direction, delta, current_position)
    
    # Salva posição atual
    with open(cache_file, 'w') as f:
        json.dump({'position': current_position, 'date': str(datetime.now())}, f)
    
    return current_position

# Uso
verificar_mudanca_posicao("ChIJN1t_tDeuEmsRUsoyG83frY4", "padaria")
```

---

## ❓ FAQ

### Como obter uma API Key do Google Maps?

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a **Places API**
4. Vá em "Credenciais" → "Criar Credenciais" → "Chave de API"
5. Restrinja a chave para maior segurança

### Qual o custo da API?

- **Places API**: $17 por 1.000 requisições
- **Crédito grátis**: $200/mês (≈ 11.700 buscas grátis/mês)
- Detalhes: [Preços Google Maps](https://mapsplatform.google.com/pricing/)

### Quantos resultados posso analisar?

- Cada página retorna até 20 resultados
- `max_pages: 3` = até 60 resultados
- Total máximo: 60 resultados por busca (limitação da API)

### Como interpretar o Overall Score?

| Score | Categoria | Ação Recomendada |
|-------|-----------|------------------|
| 90-100 | 🏆 DOMINANTE | Manter liderança |
| 80-90 | 💪 MUITO FORTE | Pequenos ajustes |
| 70-80 | ✅ FORTE | Otimizações focadas |
| 60-70 | 📊 BOM | Melhorias necessárias |
| 50-60 | ⚠️ MÉDIO | Ação urgente |
| <50 | 🚨 FRACO | Reestruturação completa |

### Posso customizar os pesos?

Sim! Edite o arquivo `config.yaml`:

```yaml
weights:
  rating_quality: 0.30      # Seu peso personalizado
  review_velocity: 0.15
  completeness: 0.20
  authority: 0.20
  prominence: 0.10
  relevance: 0.05
```

### Como lidar com erros de API?

A ferramenta inclui:
- ✅ Retry automático (3 tentativas)
- ✅ Logging detalhado
- ✅ Tratamento de exceções
- ✅ Cache de resultados

Verifique o arquivo `gmb_analyzer.log` para detalhes.

---

## 🎓 Casos de Uso

### 1. Agências de Marketing Digital
- Relatórios mensais para clientes
- Análise competitiva
- Benchmarking de mercado
- ROI de otimizações

### 2. Empresas Locais
- Monitoramento de posição
- Identificação de gaps
- Estratégia de reviews
- Otimização de perfil

### 3. Consultores SEO
- Auditoria técnica
- Análise multi-cidade
- Comparação com concorrentes
- Recomendações estratégicas

### 4. Pesquisadores
- Análise de mercado
- Tendências locais
- Estudos competitivos
- Dados para publicações

---

## 🛠️ Troubleshooting

### Erro: "API key not valid"
✅ Verifique se a Places API está ativada
✅ Confirme que a chave está correta no config.yaml
✅ Verifique restrições da chave

### Erro: "REQUEST_DENIED"
✅ Ative o faturamento no Google Cloud
✅ Verifique cotas e limites
✅ Aguarde alguns minutos após criar a chave

### Poucos resultados retornados
✅ Aumente o `radius` no config.yaml
✅ Use palavras-chave mais genéricas
✅ Verifique se há negócios na área

### Análise muito lenta
✅ Reduza `max_pages`
✅ Desabilite análise detalhada de reviews
✅ Use cache quando possível

---

## 📈 Roadmap

Funcionalidades planejadas:

- [ ] Dashboard web interativo
- [ ] Integração com Google Analytics
- [ ] Análise de sentimento de reviews
- [ ] Predição de tendências
- [ ] Relatórios PDF automatizados
- [ ] API REST para integração
- [ ] Suporte a múltiplos idiomas
- [ ] Machine Learning para recomendações

---

## 📄 Licença

Este projeto é fornecido "como está", sem garantias. Use por sua própria responsabilidade.

---

## 👨‍💻 Suporte

Para dúvidas, sugestões ou reportar bugs:

- 📧 Email: suporte@exemplo.com
- 💬 Issues: GitHub Issues
- 📚 Documentação: [Wiki do projeto]

---

## 🙏 Agradecimentos

- Google Maps Platform
- Comunidade Python
- Contribuidores do projeto

---

**Desenvolvido com ❤️ para profissionais de SEO local e Marketing Digital**

*Versão 1.0.0 - Outubro 2025*
