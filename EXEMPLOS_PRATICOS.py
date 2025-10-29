"""
EXEMPLOS PRÁTICOS - CÓDIGOS PRONTOS PARA USAR
Google Maps Business Profile Analyzer

Copie e cole os exemplos abaixo conforme sua necessidade.
Lembre-se de substituir "SUA_API_KEY" pela sua chave real.
"""

# ============================================================================
# EXEMPLO 1: ANÁLISE SIMPLES E RÁPIDA
# ============================================================================

from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer, generate_reports

def exemplo_basico():
    """Análise básica - copie e execute"""
    
    # Configure aqui
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"  # São Paulo
    KEYWORD = "padaria"
    
    # Executa
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=2
    )
    
    # Salva resultados
    generate_reports(df, KEYWORD)
    
    # Exibe top 5
    print("\n🏆 TOP 5 RANKINGS:")
    for idx, row in df.head(5).iterrows():
        print(f"#{row['rank_position']} - {row['name']}")
        print(f"   Score: {row['overall_strength_score']:.2f}")
        print(f"   Rating: {row['rating']}⭐ ({row['total_reviews']} reviews)\n")

# exemplo_basico()


# ============================================================================
# EXEMPLO 2: ANÁLISE DE MÚLTIPLAS CIDADES
# ============================================================================

def analise_multi_cidade():
    """Compara o mesmo negócio em diferentes cidades"""
    
    API_KEY = "SUA_API_KEY"
    KEYWORD = "pizzaria"
    
    cidades = {
        "São Paulo": "-23.55052,-46.633308",
        "Rio de Janeiro": "-22.9068,-43.1729",
        "Belo Horizonte": "-19.9167,-43.9345",
        "Brasília": "-15.7801,-47.9292",
        "Salvador": "-12.9714,-38.5014"
    }
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    resultados = {}
    
    for cidade, coordenadas in cidades.items():
        print(f"\n📍 Analisando: {cidade}...")
        
        metrics_list, df = analyzer.run_analysis(
            location=coordenadas,
            radius=3000,
            keyword=KEYWORD,
            max_pages=2
        )
        
        resultados[cidade] = df
        generate_reports(df, f"{KEYWORD}_{cidade.replace(' ', '_')}")
        
        # Estatísticas da cidade
        print(f"   Perfis encontrados: {len(df)}")
        print(f"   Score médio: {df['overall_strength_score'].mean():.2f}")
        print(f"   Rating médio: {df['rating'].mean():.2f}⭐")
    
    # Resumo comparativo
    print("\n" + "="*80)
    print("RESUMO COMPARATIVO POR CIDADE")
    print("="*80)
    
    for cidade, df in resultados.items():
        print(f"\n{cidade}:")
        print(f"  Total de negócios: {len(df)}")
        print(f"  Score médio: {df['overall_strength_score'].mean():.2f}")
        print(f"  Melhor score: {df['overall_strength_score'].max():.2f}")
        print(f"  Rating médio: {df['rating'].mean():.2f}⭐")

# analise_multi_cidade()


# ============================================================================
# EXEMPLO 3: ENCONTRAR SEU NEGÓCIO E ANALISAR POSIÇÃO
# ============================================================================

def encontrar_meu_negocio(nome_do_negocio):
    """Encontra seu negócio nos resultados e mostra posição"""
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "restaurante"
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=3000,
        keyword=KEYWORD,
        max_pages=3
    )
    
    # Busca o negócio
    meu_negocio = df[df['name'].str.contains(nome_do_negocio, case=False, na=False)]
    
    if meu_negocio.empty:
        print(f"❌ Negócio '{nome_do_negocio}' não encontrado nos resultados")
        print("\nNegócios encontrados:")
        for idx, row in df.head(10).iterrows():
            print(f"  - {row['name']}")
        return None
    
    # Exibe informações
    row = meu_negocio.iloc[0]
    
    print("\n" + "="*80)
    print(f"🎯 SEU NEGÓCIO: {row['name']}")
    print("="*80)
    print(f"\n📊 POSIÇÃO: #{row['rank_position']} de {len(df)}")
    print(f"🏆 CATEGORIA: {row['strength_category']}")
    print(f"💯 SCORE GERAL: {row['overall_strength_score']:.2f}/100")
    print(f"⭐ RATING: {row['rating']:.1f} ({row['total_reviews']} reviews)")
    print(f"📍 DISTÂNCIA: {row['distance_from_center']:.0f}m do centro da busca")
    print(f"📈 PERCENTIL: Top {100 - row['percentile_rank']:.1f}%")
    
    print("\n📊 BREAKDOWN DE SCORES:")
    print(f"  • Qualidade das Avaliações: {row['rating_quality_score']:.2f}/100")
    print(f"  • Velocidade de Reviews: {row['review_velocity_score']:.2f}/100")
    print(f"  • Completude do Perfil: {row['completeness_score']:.2f}/100")
    print(f"  • Autoridade: {row['authority_score']:.2f}/100")
    print(f"  • Proeminência: {row['prominence_score']:.2f}/100")
    print(f"  • Relevância: {row['relevance_score']:.2f}/100")
    
    # Oportunidades de melhoria
    print("\n💡 OPORTUNIDADES DE MELHORIA:")
    scores = {
        'Qualidade Avaliações': row['rating_quality_score'],
        'Velocidade Reviews': row['review_velocity_score'],
        'Completude': row['completeness_score'],
        'Autoridade': row['authority_score'],
        'Proeminência': row['prominence_score'],
        'Relevância': row['relevance_score']
    }
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1])
    
    for i, (metric, score) in enumerate(sorted_scores[:3], 1):
        gap = 100 - score
        print(f"  {i}. {metric}: {score:.2f}/100 (gap de {gap:.2f} pontos)")
    
    return row

# Uso:
# encontrar_meu_negocio("Nome do Meu Restaurante")


# ============================================================================
# EXEMPLO 4: ANÁLISE COMPETITIVA DETALHADA
# ============================================================================

def analise_competitiva_detalhada():
    """Compara seu negócio com 3 concorrentes específicos"""
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "academia"
    
    # IDs dos concorrentes (obtenha do Google Maps)
    MEU_PLACE_ID = "ChIJ..."  # Substitua pelo seu
    CONCORRENTES = [
        "ChIJ...",  # Concorrente 1
        "ChIJ...",  # Concorrente 2
        "ChIJ..."   # Concorrente 3
    ]
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=3
    )
    
    # Filtra apenas os perfis relevantes
    todos_ids = [MEU_PLACE_ID] + CONCORRENTES
    df_foco = df[df['place_id'].isin(todos_ids)].copy()
    df_foco['tipo'] = df_foco['place_id'].apply(
        lambda x: '🎯 VOCÊ' if x == MEU_PLACE_ID else '🔴 CONCORRENTE'
    )
    
    print("\n" + "="*80)
    print("ANÁLISE COMPETITIVA DETALHADA")
    print("="*80)
    
    for idx, row in df_foco.iterrows():
        print(f"\n{row['tipo']} - {row['name']}")
        print(f"  Posição: #{row['rank_position']}")
        print(f"  Score: {row['overall_strength_score']:.2f} {row['strength_category']}")
        print(f"  Rating: {row['rating']}⭐ ({row['total_reviews']} reviews)")
        print(f"  Website: {'✅' if row['website'] else '❌'}")
        print(f"  Telefone: {'✅' if row['phone'] else '❌'}")
    
    # Matriz de comparação
    print("\n" + "="*80)
    print("MATRIZ DE COMPARAÇÃO (você vs média dos concorrentes)")
    print("="*80)
    
    if not df_foco[df_foco['place_id'] == MEU_PLACE_ID].empty:
        seu_perfil = df_foco[df_foco['place_id'] == MEU_PLACE_ID].iloc[0]
        concorrentes_df = df_foco[df_foco['place_id'] != MEU_PLACE_ID]
        
        metricas = [
            ('overall_strength_score', 'Score Geral'),
            ('rating_quality_score', 'Qualidade Avaliações'),
            ('review_velocity_score', 'Velocidade Reviews'),
            ('completeness_score', 'Completude'),
            ('authority_score', 'Autoridade'),
            ('prominence_score', 'Proeminência')
        ]
        
        for campo, nome in metricas:
            seu_valor = seu_perfil[campo]
            media_concorrentes = concorrentes_df[campo].mean()
            diferenca = seu_valor - media_concorrentes
            
            status = "✅" if diferenca > 0 else "⚠️"
            sinal = "+" if diferenca > 0 else ""
            
            print(f"\n{status} {nome}:")
            print(f"   Você: {seu_valor:.2f} | Média concorrentes: {media_concorrentes:.2f}")
            print(f"   Diferença: {sinal}{diferenca:.2f}")

# analise_competitiva_detalhada()


# ============================================================================
# EXEMPLO 5: MONITORAMENTO SEMANAL AUTOMATIZADO
# ============================================================================

def monitoramento_semanal():
    """Salva análise com timestamp para comparação histórica"""
    
    import json
    from datetime import datetime
    from pathlib import Path
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "salao de beleza"
    MEU_PLACE_ID = "ChIJ..."  # Seu place_id
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=2
    )
    
    # Encontra seu negócio
    meu_negocio = df[df['place_id'] == MEU_PLACE_ID]
    
    if meu_negocio.empty:
        print("❌ Seu negócio não encontrado")
        return
    
    row = meu_negocio.iloc[0]
    
    # Dados desta semana
    dados_semana = {
        'data': datetime.now().isoformat(),
        'posicao': int(row['rank_position']),
        'score': float(row['overall_strength_score']),
        'rating': float(row['rating']),
        'total_reviews': int(row['total_reviews']),
        'percentil': float(row['percentile_rank'])
    }
    
    # Salva histórico
    historico_file = Path('historico_semanal.json')
    
    if historico_file.exists():
        with open(historico_file, 'r') as f:
            historico = json.load(f)
    else:
        historico = []
    
    historico.append(dados_semana)
    
    with open(historico_file, 'w') as f:
        json.dump(historico, f, indent=2)
    
    # Compara com semana anterior
    if len(historico) > 1:
        anterior = historico[-2]
        
        print("\n📊 COMPARAÇÃO COM SEMANA ANTERIOR:")
        print("="*60)
        
        delta_pos = anterior['posicao'] - dados_semana['posicao']
        delta_score = dados_semana['score'] - anterior['score']
        delta_reviews = dados_semana['total_reviews'] - anterior['total_reviews']
        
        print(f"\nPosição: #{dados_semana['posicao']}", end='')
        if delta_pos > 0:
            print(f" ⬆️ (subiu {delta_pos} posições)")
        elif delta_pos < 0:
            print(f" ⬇️ (caiu {abs(delta_pos)} posições)")
        else:
            print(" ➡️ (manteve)")
        
        print(f"Score: {dados_semana['score']:.2f} ({delta_score:+.2f})")
        print(f"Reviews: {dados_semana['total_reviews']} (+{delta_reviews})")
    
    print(f"\n✅ Dados salvos em {historico_file}")

# Agende esta função para rodar toda segunda-feira às 9h
# monitoramento_semanal()


# ============================================================================
# EXEMPLO 6: EXPORTAR PARA GOOGLE SHEETS (REQUER GSPREAD)
# ============================================================================

def exportar_para_sheets():
    """Exporta resultados diretamente para Google Sheets"""
    
    # Instale: pip install gspread oauth2client
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "pet shop"
    
    # Análise
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=2
    )
    
    # Conecta ao Google Sheets
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', scope
    )
    client = gspread.authorize(creds)
    
    # Abre ou cria planilha
    try:
        sheet = client.open('Análise GMB - Rankings')
    except:
        sheet = client.create('Análise GMB - Rankings')
        sheet.share('seu-email@gmail.com', perm_type='user', role='writer')
    
    # Adiciona dados
    worksheet = sheet.get_worksheet(0)
    
    # Cabeçalhos
    headers = ['Posição', 'Nome', 'Score', 'Rating', 'Reviews', 
               'Categoria', 'Telefone', 'Website']
    worksheet.update('A1:H1', [headers])
    
    # Dados (top 20)
    rows = []
    for idx, row in df.head(20).iterrows():
        rows.append([
            row['rank_position'],
            row['name'],
            row['overall_strength_score'],
            row['rating'],
            row['total_reviews'],
            row['strength_category'],
            row['phone'] or 'N/A',
            row['website'] or 'N/A'
        ])
    
    worksheet.update('A2', rows)
    
    print(f"✅ Dados exportados para Google Sheets!")
    print(f"🔗 Link: {sheet.url}")

# exportar_para_sheets()


# ============================================================================
# EXEMPLO 7: ALERTAS POR EMAIL
# ============================================================================

def enviar_alerta_email(assunto, mensagem):
    """Envia alerta por email quando detecta mudanças significativas"""
    
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Configurações SMTP (Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = "seu-email@gmail.com"
    senha = "sua-senha-app"  # Use senha de app, não sua senha normal
    destinatario = "destinatario@gmail.com"
    
    # Cria mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    
    msg.attach(MIMEText(mensagem, 'plain'))
    
    # Envia
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()
        print("✅ Email enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")


def monitorar_com_alertas():
    """Monitora e envia alertas se detectar mudanças"""
    
    import json
    from pathlib import Path
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "clinica veterinaria"
    MEU_PLACE_ID = "ChIJ..."
    
    # Análise atual
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=2
    )
    
    meu_negocio = df[df['place_id'] == MEU_PLACE_ID]
    if meu_negocio.empty:
        return
    
    row = meu_negocio.iloc[0]
    posicao_atual = int(row['rank_position'])
    
    # Carrega posição anterior
    cache_file = Path('posicao_anterior.json')
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            dados_anteriores = json.load(f)
            posicao_anterior = dados_anteriores['posicao']
            
            # Detecta mudanças significativas
            mudanca = posicao_anterior - posicao_atual
            
            if abs(mudanca) >= 3:  # Mudança de 3+ posições
                if mudanca > 0:
                    assunto = f"🎉 Seu ranking SUBIU {mudanca} posições!"
                    mensagem = f"""
Ótimas notícias!

Seu negócio subiu {mudanca} posições no Google Maps!

Palavra-chave: {KEYWORD}
Posição anterior: #{posicao_anterior}
Posição atual: #{posicao_atual}
Score: {row['overall_strength_score']:.2f}

Continue o ótimo trabalho!
                    """
                else:
                    assunto = f"⚠️ ALERTA: Ranking caiu {abs(mudanca)} posições"
                    mensagem = f"""
Atenção necessária!

Seu negócio caiu {abs(mudanca)} posições no Google Maps.

Palavra-chave: {KEYWORD}
Posição anterior: #{posicao_anterior}
Posição atual: #{posicao_atual}
Score: {row['overall_strength_score']:.2f}

Recomendações:
1. Incentive mais reviews
2. Atualize fotos do perfil
3. Responda todos os comentários
4. Verifique informações de contato

Acesse o relatório completo para mais detalhes.
                    """
                
                enviar_alerta_email(assunto, mensagem)
    
    # Salva posição atual
    with open(cache_file, 'w') as f:
        json.dump({'posicao': posicao_atual, 'data': str(datetime.now())}, f)

# monitorar_com_alertas()


# ============================================================================
# EXEMPLO 8: DASHBOARD SIMPLES NO TERMINAL
# ============================================================================

def dashboard_terminal():
    """Exibe dashboard colorido no terminal"""
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "hamburgueria"
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    
    print("\n🔄 Carregando dados...\n")
    
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=2000,
        keyword=KEYWORD,
        max_pages=2
    )
    
    # Header
    print("╔" + "═"*78 + "╗")
    print("║" + f"  DASHBOARD - {KEYWORD.upper()}".center(78) + "║")
    print("╚" + "═"*78 + "╝\n")
    
    # Estatísticas gerais
    print("📊 ESTATÍSTICAS GERAIS")
    print("─" * 80)
    print(f"  Total de perfis: {len(df)}")
    print(f"  Score médio: {df['overall_strength_score'].mean():.2f}")
    print(f"  Rating médio: {df['rating'].mean():.2f}⭐")
    print(f"  Média de reviews: {df['total_reviews'].mean():.0f}\n")
    
    # Top 5
    print("🏆 TOP 5 RANKINGS")
    print("─" * 80)
    for idx, row in df.head(5).iterrows():
        categoria_emoji = row['strength_category'].split()[0]
        print(f"  {categoria_emoji} #{row['rank_position']:2d} │ {row['name'][:40]:40s} │ Score: {row['overall_strength_score']:5.2f}")
    
    print("\n" + "═" * 80)
    
    # Distribuição
    print("\n📈 DISTRIBUIÇÃO POR CATEGORIA")
    print("─" * 80)
    
    for categoria in df['strength_category'].value_counts().index:
        count = (df['strength_category'] == categoria).sum()
        pct = (count / len(df)) * 100
        barra = "█" * int(pct / 2)
        print(f"  {categoria:20s} │ {count:3d} │ {pct:5.1f}% │ {barra}")
    
    print("\n" + "═" * 80 + "\n")

# dashboard_terminal()


# ============================================================================
# DICA FINAL: COMO DESCOBRIR O PLACE_ID DO SEU NEGÓCIO
# ============================================================================

def descobrir_meu_place_id(nome_aproximado):
    """Ajuda a encontrar o Place ID do seu negócio"""
    
    API_KEY = "SUA_API_KEY"
    LOCATION = "-23.55052,-46.633308"
    KEYWORD = "seu tipo de negocio"  # ex: "restaurante"
    
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=3000,
        keyword=KEYWORD,
        max_pages=3
    )
    
    # Busca por nome similar
    resultados = df[df['name'].str.contains(nome_aproximado, case=False, na=False)]
    
    if resultados.empty:
        print(f"❌ Nenhum negócio encontrado com '{nome_aproximado}'\n")
        print("Primeiros 10 resultados encontrados:")
        for idx, row in df.head(10).iterrows():
            print(f"  - {row['name']}")
        return
    
    print(f"\n✅ Encontrados {len(resultados)} negócio(s):\n")
    
    for idx, row in resultados.iterrows():
        print("─" * 60)
        print(f"Nome: {row['name']}")
        print(f"Place ID: {row['place_id']}")
        print(f"Endereço: {row['address']}")
        print(f"Posição: #{row['rank_position']}")
        print(f"Telefone: {row['phone'] or 'N/A'}")
        print(f"Website: {row['website'] or 'N/A'}")
        print("─" * 60)

# Uso:
# descobrir_meu_place_id("Nome Parcial do Meu Negócio")


print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                      EXEMPLOS PRÁTICOS - PRONTO PARA USAR                  ║
║                                                                            ║
║  Escolha o exemplo que mais se adequa à sua necessidade e execute!        ║
║                                                                            ║
║  1. exemplo_basico() - Análise simples e rápida                          ║
║  2. analise_multi_cidade() - Compara várias cidades                      ║
║  3. encontrar_meu_negocio() - Encontra seu negócio                       ║
║  4. analise_competitiva_detalhada() - VS concorrentes                    ║
║  5. monitoramento_semanal() - Histórico semanal                          ║
║  6. exportar_para_sheets() - Integração Google Sheets                   ║
║  7. monitorar_com_alertas() - Alertas por email                         ║
║  8. dashboard_terminal() - Dashboard visual                              ║
║  9. descobrir_meu_place_id() - Encontra seu Place ID                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
