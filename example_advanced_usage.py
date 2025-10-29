"""
Exemplo de uso avançado do Google Maps Ranking Analyzer
Demonstra diferentes cenários e análises comparativas
"""

from gmb_ranking_analyzer import GoogleMapsRankingAnalyzer, generate_reports
import pandas as pd
import yaml
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_config(config_file: str = "config.yaml") -> dict:
    """Carrega configurações do arquivo YAML"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def analyze_single_keyword(config: dict):
    """Análise simples com uma palavra-chave"""
    
    print("\n" + "="*80)
    print("ANÁLISE ÚNICA - PALAVRA-CHAVE")
    print("="*80 + "\n")
    
    api_key = config['api']['key']
    search_params = config['search']
    
    analyzer = GoogleMapsRankingAnalyzer(api_key)
    
    metrics_list, df = analyzer.run_analysis(
        location=search_params['location'],
        radius=search_params['radius'],
        keyword=search_params['keyword'],
        max_pages=search_params['max_pages']
    )
    
    # Gera relatórios
    files = generate_reports(df, search_params['keyword'])
    
    # Exibe insights
    print_insights(df, search_params['keyword'])
    
    return df


def analyze_multiple_keywords(config: dict):
    """Análise comparativa com múltiplas palavras-chave"""
    
    print("\n" + "="*80)
    print("ANÁLISE COMPARATIVA - MÚLTIPLAS PALAVRAS-CHAVE")
    print("="*80 + "\n")
    
    if not config['search']['multiple_keywords']['enabled']:
        print("❌ Análise múltipla desabilitada no config.yaml")
        return None
    
    api_key = config['api']['key']
    search_params = config['search']
    keywords = config['search']['multiple_keywords']['keywords']
    
    analyzer = GoogleMapsRankingAnalyzer(api_key)
    
    all_results = {}
    
    for keyword in keywords:
        print(f"\n📊 Analisando: '{keyword}'...")
        
        metrics_list, df = analyzer.run_analysis(
            location=search_params['location'],
            radius=search_params['radius'],
            keyword=keyword,
            max_pages=search_params['max_pages']
        )
        
        all_results[keyword] = df
        
        # Gera relatórios individuais
        generate_reports(df, keyword)
    
    # Cria relatório comparativo
    create_comparative_report(all_results, search_params['location'])
    
    return all_results


def analyze_competitor(config: dict, target_place_id: str, competitor_place_ids: list):
    """Análise focada em um negócio específico vs concorrentes"""
    
    print("\n" + "="*80)
    print("ANÁLISE COMPETITIVA - SEU NEGÓCIO VS CONCORRENTES")
    print("="*80 + "\n")
    
    api_key = config['api']['key']
    search_params = config['search']
    
    analyzer = GoogleMapsRankingAnalyzer(api_key)
    
    # Executa busca completa
    metrics_list, df = analyzer.run_analysis(
        location=search_params['location'],
        radius=search_params['radius'],
        keyword=search_params['keyword'],
        max_pages=search_params['max_pages']
    )
    
    # Filtra para o negócio alvo e concorrentes
    focus_ids = [target_place_id] + competitor_place_ids
    df_focus = df[df['place_id'].isin(focus_ids)].copy()
    
    if len(df_focus) == 0:
        print("❌ Negócio alvo ou concorrentes não encontrados nos resultados")
        return None
    
    # Identifica o negócio alvo
    df_focus['is_target'] = df_focus['place_id'] == target_place_id
    df_focus = df_focus.sort_values('is_target', ascending=False)
    
    print("\n📊 COMPARAÇÃO COMPETITIVA:\n")
    print("-" * 80)
    
    for idx, row in df_focus.iterrows():
        marker = "🎯 SEU NEGÓCIO" if row['is_target'] else "🔴 CONCORRENTE"
        print(f"\n{marker}")
        print(f"Nome: {row['name']}")
        print(f"Posição no ranking: #{row['rank_position']}")
        print(f"Score geral: {row['overall_strength_score']:.2f} {row['strength_category']}")
        print(f"Rating: {row['rating']:.1f} ⭐ ({row['total_reviews']} reviews)")
        print(f"Percentil: Top {100 - row['percentile_rank']:.1f}%")
        print("-" * 80)
    
    # Identifica gaps e oportunidades
    if df_focus['is_target'].any():
        target_row = df_focus[df_focus['is_target']].iloc[0]
        competitors_df = df_focus[~df_focus['is_target']]
        
        print("\n💡 ANÁLISE DE GAPS E OPORTUNIDADES:\n")
        
        # Compara métricas
        metrics_to_compare = [
            ('rating_quality_score', 'Qualidade das Avaliações'),
            ('review_velocity_score', 'Velocidade de Reviews'),
            ('completeness_score', 'Completude do Perfil'),
            ('authority_score', 'Autoridade'),
            ('relevance_score', 'Relevância')
        ]
        
        for metric, label in metrics_to_compare:
            target_value = target_row[metric]
            competitor_avg = competitors_df[metric].mean()
            competitor_max = competitors_df[metric].max()
            
            gap_vs_avg = target_value - competitor_avg
            gap_vs_best = target_value - competitor_max
            
            status = "✅" if gap_vs_avg > 0 else "⚠️"
            
            print(f"{status} {label}:")
            print(f"   Você: {target_value:.2f} | Média concorrentes: {competitor_avg:.2f} | Melhor: {competitor_max:.2f}")
            print(f"   Gap vs média: {gap_vs_avg:+.2f} | Gap vs melhor: {gap_vs_best:+.2f}")
            print()
    
    # Salva relatório
    output_dir = Path(config['reports']['output_directory'])
    output_dir.mkdir(exist_ok=True)
    
    comp_file = output_dir / f"competitive_analysis_{search_params['keyword']}.xlsx"
    with pd.ExcelWriter(comp_file, engine='openpyxl') as writer:
        df_focus.to_excel(writer, sheet_name='Comparação', index=False)
        
        # Cria tabela de gaps
        if df_focus['is_target'].any():
            gaps_data = []
            for metric, label in metrics_to_compare:
                gaps_data.append({
                    'Métrica': label,
                    'Seu Valor': target_row[metric],
                    'Média Concorrentes': competitors_df[metric].mean(),
                    'Melhor Concorrente': competitors_df[metric].max(),
                    'Gap vs Média': target_row[metric] - competitors_df[metric].mean(),
                    'Gap vs Melhor': target_row[metric] - competitors_df[metric].max()
                })
            
            gaps_df = pd.DataFrame(gaps_data)
            gaps_df.to_excel(writer, sheet_name='Análise de Gaps', index=False)
    
    print(f"\n📁 Relatório competitivo salvo: {comp_file}")
    
    return df_focus


def print_insights(df: pd.DataFrame, keyword: str):
    """Exibe insights principais da análise"""
    
    print("\n" + "="*80)
    print(f"INSIGHTS - {keyword.upper()}")
    print("="*80 + "\n")
    
    # Estatísticas gerais
    print("📈 ESTATÍSTICAS GERAIS:")
    print(f"   Total de perfis: {len(df)}")
    print(f"   Score médio: {df['overall_strength_score'].mean():.2f}")
    print(f"   Rating médio: {df['rating'].mean():.2f} ⭐")
    print(f"   Média de reviews: {df['total_reviews'].mean():.0f}")
    print(f"   Distância média: {df['distance_from_center'].mean():.0f}m")
    
    # Top performer
    top = df.iloc[0]
    print(f"\n🏆 LÍDER DO MERCADO:")
    print(f"   {top['name']}")
    print(f"   Score: {top['overall_strength_score']:.2f} {top['strength_category']}")
    print(f"   Rating: {top['rating']:.1f} ⭐ ({top['total_reviews']} reviews)")
    
    # Distribuição por categoria
    print(f"\n📊 DISTRIBUIÇÃO POR FORÇA:")
    for category, count in df['strength_category'].value_counts().items():
        pct = (count / len(df)) * 100
        bar = "█" * int(pct / 5)
        print(f"   {category}: {count:3d} ({pct:5.1f}%) {bar}")
    
    # Correlações interessantes
    print(f"\n🔍 INSIGHTS AVANÇADOS:")
    
    # Correlação rating vs position
    corr_rating = df[['rank_position', 'rating']].corr().iloc[0, 1]
    print(f"   Correlação Rating x Posição: {corr_rating:.3f}")
    
    # Correlação reviews vs score
    corr_reviews = df[['total_reviews', 'overall_strength_score']].corr().iloc[0, 1]
    print(f"   Correlação Reviews x Score: {corr_reviews:.3f}")
    
    # Perfis com alta completude
    high_completeness = df[df['completeness_score'] >= 80]
    print(f"   Perfis com alta completude (≥80): {len(high_completeness)} ({len(high_completeness)/len(df)*100:.1f}%)")
    
    # Perfis com website
    with_website = df[df['website'].notna()]
    print(f"   Perfis com website: {len(with_website)} ({len(with_website)/len(df)*100:.1f}%)")
    
    print("\n" + "="*80)


def create_comparative_report(results_dict: dict, location: str):
    """Cria relatório comparativo entre múltiplas palavras-chave"""
    
    print("\n" + "="*80)
    print("GERANDO RELATÓRIO COMPARATIVO")
    print("="*80 + "\n")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    comparison_file = output_dir / "comparative_analysis_all_keywords.xlsx"
    
    with pd.ExcelWriter(comparison_file, engine='openpyxl') as writer:
        # Para cada keyword, adiciona uma aba
        for keyword, df in results_dict.items():
            sheet_name = keyword[:31]  # Excel limit
            df.head(20).to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Cria aba de resumo
        summary_data = []
        for keyword, df in results_dict.items():
            summary_data.append({
                'Palavra-chave': keyword,
                'Total Resultados': len(df),
                'Score Médio': df['overall_strength_score'].mean(),
                'Rating Médio': df['rating'].mean(),
                'Reviews Médio': df['total_reviews'].mean(),
                'Top Score': df['overall_strength_score'].max(),
                'Top Rating': df['rating'].max()
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.round(2)
        summary_df.to_excel(writer, sheet_name='Resumo Comparativo', index=False)
    
    print(f"📁 Relatório comparativo salvo: {comparison_file}")


def main():
    """Execução principal com diferentes cenários"""
    
    # Carrega configurações
    config = load_config()
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          GOOGLE MAPS BUSINESS PROFILE ANALYZER & RANKING TOOL              ║
║                    Sistema Profissional de Análise                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Menu de opções
    print("\nEscolha o tipo de análise:")
    print("1. Análise única (uma palavra-chave)")
    print("2. Análise comparativa (múltiplas palavras-chave)")
    print("3. Análise competitiva (seu negócio vs concorrentes)")
    print("0. Sair")
    
    choice = input("\nOpção: ").strip()
    
    if choice == "1":
        analyze_single_keyword(config)
    
    elif choice == "2":
        analyze_multiple_keywords(config)
    
    elif choice == "3":
        print("\nInsira os Place IDs (separados por vírgula):")
        target = input("Seu negócio: ").strip()
        competitors_input = input("Concorrentes: ").strip()
        competitors = [c.strip() for c in competitors_input.split(",") if c.strip()]
        
        if target and competitors:
            analyze_competitor(config, target, competitors)
        else:
            print("❌ Place IDs inválidos")
    
    elif choice == "0":
        print("\n👋 Até logo!")
        return
    
    else:
        print("❌ Opção inválida")
        return
    
    print("\n✅ Análise concluída com sucesso!")
    print("\n📁 Verifique a pasta 'output' para os relatórios gerados.")


if __name__ == "__main__":
    main()
