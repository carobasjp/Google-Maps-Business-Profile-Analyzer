# 🚀 GUIA RÁPIDO DE INÍCIO

## Instalação em 3 Passos

### 1️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure sua API Key
Edite o arquivo `config.yaml` e substitua:
```yaml
api:
  key: "SUA_API_KEY_AQUI"  # ← Cole sua chave aqui
```

### 3️⃣ Configure os parâmetros de busca
No mesmo arquivo `config.yaml`:
```yaml
search:
  location: "-23.55052,-46.633308"  # Suas coordenadas
  radius: 2000                       # Raio em metros
  keyword: "padaria"                 # Sua palavra-chave
  max_pages: 3                       # Quantas páginas analisar
```

---

## 📍 Como Obter Coordenadas

1. Abra [Google Maps](https://maps.google.com)
2. Clique com botão direito no local desejado
3. Clique nas coordenadas que aparecem
4. Cole no formato: `"latitude,longitude"`

**Exemplos de cidades brasileiras:**
- São Paulo: `"-23.55052,-46.633308"`
- Rio de Janeiro: `"-22.9068,-43.1729"`
- Belo Horizonte: `"-19.9167,-43.9345"`
- Brasília: `"-15.7801,-47.9292"`
- Salvador: `"-12.9714,-38.5014"`
- Fortaleza: `"-3.7172,-38.5434"`
- Curitiba: `"-25.4284,-49.2733"`
- Porto Alegre: `"-30.0346,-51.2177"`

---

## ▶️ Executar a Análise

### Opção 1: Modo Simples (automático)
```bash
python gmb_ranking_analyzer.py
```

### Opção 2: Modo Interativo (com menu)
```bash
python example_advanced_usage.py
```

---

## 📊 O Que Você Vai Receber

Após executar, a ferramenta irá:

1. ✅ Coletar todos os perfis do Google Maps para sua palavra-chave
2. ✅ Calcular 6 métricas profissionais para cada perfil
3. ✅ Gerar um score geral de 0-100
4. ✅ Classificar em 7 categorias de força
5. ✅ Criar 4 tipos de relatórios na pasta `output/`:
   - 📄 CSV completo
   - 📊 Excel com múltiplas abas
   - 🔧 JSON para integrações
   - 📝 Relatório resumido em texto

---

## 🎯 Interpretando o Score Geral

| Score | Categoria | Significado |
|-------|-----------|-------------|
| 90-100 | 🏆 DOMINANTE | Líder absoluto do mercado |
| 80-90 | 💪 MUITO FORTE | Posição muito competitiva |
| 70-80 | ✅ FORTE | Boa presença no mercado |
| 60-70 | 📊 BOM | Presença satisfatória |
| 50-60 | ⚠️ MÉDIO | Precisa de melhorias |
| 40-50 | 📉 FRACO | Requer atenção urgente |
| 0-40 | 🚨 MUITO FRACO | Necessita reestruturação |

---

## 💡 Dicas Rápidas

### Para Análise Mais Rápida
```yaml
search:
  max_pages: 1  # Analisa apenas 20 resultados
```

### Para Análise Mais Completa
```yaml
search:
  max_pages: 3  # Analisa até 60 resultados
  radius: 5000  # Aumenta o raio de busca
```

### Para Múltiplas Palavras-chave
```yaml
search:
  multiple_keywords:
    enabled: true
    keywords:
      - "padaria"
      - "confeitaria"
      - "bakery"
```

---

## 🔧 Customização de Pesos

Se você quer dar mais importância para avaliações:

```yaml
weights:
  rating_quality: 0.35      # Mais peso
  review_velocity: 0.25     # Mais peso
  completeness: 0.10        # Menos peso
  authority: 0.15
  prominence: 0.10
  relevance: 0.05
```

---

## ❓ Problemas Comuns

### "API key not valid"
→ Verifique se você:
1. Ativou a **Places API** no Google Cloud
2. Copiou a chave correta para o `config.yaml`
3. Habilitou o faturamento (mesmo no plano grátis)

### "Não encontrou resultados"
→ Tente:
1. Aumentar o `radius`
2. Usar palavra-chave mais genérica
3. Verificar se as coordenadas estão corretas

### "Análise muito lenta"
→ É normal! A ferramenta faz várias requisições detalhadas.
Para acelerar, reduza o `max_pages` para 1 ou 2.

---

## 📞 Obter API Key do Google

1. Acesse: https://console.cloud.google.com/
2. Crie um projeto novo
3. Vá em "APIs e Serviços" → "Biblioteca"
4. Procure por "Places API" e ative
5. Vá em "Credenciais" → "Criar Credenciais" → "Chave de API"
6. Copie a chave gerada

**💰 Custo:** Primeiros $200/mês são GRÁTIS (≈11.700 buscas)

---

## 📁 Onde Ficam os Relatórios?

Todos os arquivos são salvos na pasta `output/` com timestamp:

```
output/
├── ranking_analysis_padaria_20251029_143000.csv
├── ranking_analysis_padaria_20251029_143000.xlsx
├── ranking_analysis_padaria_20251029_143000.json
└── summary_report_padaria_20251029_143000.txt
```

---

## 🎓 Próximos Passos

Depois de fazer sua primeira análise:

1. 📖 Leia o **README.md** completo para funcionalidades avançadas
2. 🧪 Teste a análise competitiva (compare com concorrentes)
3. 📊 Configure análise de múltiplas palavras-chave
4. 🔄 Agende análises semanais/mensais
5. 📈 Use os insights para otimizar seu perfil

---

## ✨ Exemplo Prático Completo

```python
from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer, generate_reports

# Sua API Key
API_KEY = "AIzaSyABCDEFG..."

# Inicializa
analyzer = GoogleMapsRankingAnalyzer(API_KEY)

# Executa análise
metrics_list, df = analyzer.run_analysis(
    location="-23.55052,-46.633308",  # São Paulo
    radius=2000,                       # 2km
    keyword="padaria",                 # Palavra-chave
    max_pages=3                        # 60 resultados
)

# Gera relatórios
files = generate_reports(df, "padaria")

# Exibe resumo
print(f"✅ Analisados: {len(df)} perfis")
print(f"🏆 Líder: {df.iloc[0]['name']}")
print(f"📊 Score médio: {df['overall_strength_score'].mean():.2f}")
```

---

## 🎯 Métricas Explicadas Rapidamente

1. **Rating Quality** (0-100)
   - O quanto as avaliações são boas e confiáveis
   - Combina nota média + volume de reviews

2. **Review Velocity** (0-100)
   - Frequência de novos reviews
   - Indica engajamento ativo

3. **Completeness** (0-100)
   - Preenchimento do perfil
   - Fotos, horários, telefone, site, etc.

4. **Authority** (0-100)
   - Autoridade e credibilidade
   - Reviews + rating + presença web

5. **Prominence** (0-100)
   - Destaque na busca
   - Posição + proximidade

6. **Relevance** (0-100)
   - Relevância para busca
   - Palavra-chave no nome/categoria

**Score Final:** Média ponderada das 6 métricas

---

## 🚀 Pronto para Começar!

1. ✅ Instale: `pip install -r requirements.txt`
2. ✅ Configure: Edite `config.yaml`
3. ✅ Execute: `python gmb_ranking_analyzer.py`
4. ✅ Analise: Veja os relatórios na pasta `output/`

**Boa análise! 🎉**

---

*Precisa de ajuda? Consulte o README.md completo ou entre em contato.*
