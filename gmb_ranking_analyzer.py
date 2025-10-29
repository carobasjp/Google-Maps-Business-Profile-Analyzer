"""
Google Maps Business Profile Analyzer & Ranking Tool
Sistema profissional de análise de força de perfil e ranqueamento local
"""

import requests
import pandas as pd
import numpy as np
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gmb_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ProfileMetrics:
    """Métricas avançadas de perfil"""
    place_id: str
    name: str
    rank_position: int
    
    # Dados básicos
    address: str
    vicinity: str
    phone: Optional[str]
    website: Optional[str]
    
    # Localização
    latitude: float
    longitude: float
    distance_from_center: float
    
    # Avaliações
    rating: float
    total_reviews: int
    
    # Métricas calculadas
    review_velocity_score: float
    rating_quality_score: float
    completeness_score: float
    authority_score: float
    relevance_score: float
    prominence_score: float
    
    # Score final
    overall_strength_score: float
    strength_category: str
    
    # Análise competitiva
    percentile_rank: float
    gap_to_leader: float
    
    # Timestamp
    analysis_date: str


class GoogleMapsRankingAnalyzer:
    """Analisador profissional de ranqueamento do Google Maps"""
    
    # Pesos para cálculo de score (ajustáveis)
    WEIGHTS = {
        'rating_quality': 0.25,
        'review_velocity': 0.20,
        'completeness': 0.15,
        'authority': 0.20,
        'prominence': 0.10,
        'relevance': 0.10
    }
    
    # Categorias de força
    STRENGTH_CATEGORIES = {
        (90, 100): "🏆 DOMINANTE",
        (80, 90): "💪 MUITO FORTE",
        (70, 80): "✅ FORTE",
        (60, 70): "📊 BOM",
        (50, 60): "⚠️ MÉDIO",
        (40, 50): "📉 FRACO",
        (0, 40): "🚨 MUITO FRACO"
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.cache = {}
        
    def search_places(
        self, 
        location: str, 
        radius: int, 
        keyword: str, 
        pagetoken: Optional[str] = None
    ) -> Dict:
        """Busca lugares no Google Maps"""
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "key": self.api_key,
            "location": location,
            "radius": radius,
            "keyword": keyword
        }
        if pagetoken:
            params["pagetoken"] = pagetoken
            
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na busca: {e}")
            return {"results": [], "status": "ERROR"}
    
    def get_place_details(self, place_id: str) -> Dict:
        """Obtém detalhes completos de um lugar"""
        if place_id in self.cache:
            return self.cache[place_id]
            
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "key": self.api_key,
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,website,rating,"
                     "user_ratings_total,geometry,business_status,opening_hours,"
                     "photos,types,url,reviews,price_level,utc_offset"
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            self.cache[place_id] = data
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao obter detalhes de {place_id}: {e}")
            return {"result": {}, "status": "ERROR"}
    
    def calculate_distance(
        self, 
        lat1: float, 
        lng1: float, 
        lat2: float, 
        lng2: float
    ) -> float:
        """Calcula distância em metros entre dois pontos (Haversine)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Raio da Terra em metros
        
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def calculate_rating_quality_score(self, rating: float, total_reviews: int) -> float:
        """
        Score de qualidade das avaliações
        Considera tanto a nota quanto o volume de avaliações
        """
        if not rating or total_reviews == 0:
            return 0.0
        
        # Normaliza rating (0-5 para 0-100)
        rating_score = (rating / 5.0) * 100
        
        # Fator de confiança baseado no volume de reviews
        # Usa função logarítmica para evitar viés extremo em altos volumes
        confidence_factor = min(np.log10(total_reviews + 1) / np.log10(500), 1.0)
        
        return rating_score * (0.5 + 0.5 * confidence_factor)
    
    def calculate_review_velocity_score(self, total_reviews: int) -> float:
        """
        Score de velocidade de avaliações
        Indica a frequência de novos reviews
        """
        if total_reviews == 0:
            return 0.0
        
        # Assumindo que perfis mais ativos têm mais reviews
        # Normaliza para escala 0-100
        velocity_score = min((total_reviews / 200) * 100, 100)
        
        return velocity_score
    
    def calculate_completeness_score(self, details: Dict) -> float:
        """
        Score de completude do perfil
        Verifica preenchimento de campos importantes
        """
        result = details.get("result", {})
        
        fields = {
            "formatted_address": 15,
            "formatted_phone_number": 15,
            "website": 20,
            "opening_hours": 15,
            "photos": 20,
            "business_status": 5,
            "types": 5,
            "price_level": 5
        }
        
        score = 0.0
        for field, weight in fields.items():
            if field in result and result[field]:
                if field == "photos":
                    # Bonifica por ter múltiplas fotos
                    photo_count = len(result[field])
                    score += weight * min(photo_count / 10, 1.0)
                else:
                    score += weight
        
        return score
    
    def calculate_authority_score(
        self, 
        rating: float, 
        total_reviews: int,
        has_website: bool,
        photos_count: int
    ) -> float:
        """
        Score de autoridade do negócio
        Combina múltiplos sinais de credibilidade
        """
        if total_reviews == 0:
            return 0.0
        
        # Reviews como indicador principal (40 pontos)
        review_authority = min((total_reviews / 300) * 40, 40)
        
        # Rating alto consistente (30 pontos)
        rating_authority = (rating / 5.0) * 30 if rating else 0
        
        # Presença web (15 pontos)
        web_authority = 15 if has_website else 0
        
        # Conteúdo visual (15 pontos)
        photo_authority = min((photos_count / 20) * 15, 15)
        
        return review_authority + rating_authority + web_authority + photo_authority
    
    def calculate_prominence_score(
        self,
        rank_position: int,
        total_results: int,
        distance: float,
        radius: int
    ) -> float:
        """
        Score de proeminência
        Posição nos resultados e proximidade geográfica
        """
        # Score de posição (60% do peso)
        position_score = ((total_results - rank_position + 1) / total_results) * 60
        
        # Score de proximidade (40% do peso)
        proximity_score = max(0, (1 - distance / radius)) * 40
        
        return position_score + proximity_score
    
    def calculate_relevance_score(
        self,
        name: str,
        keyword: str,
        types: List[str],
        vicinity: str
    ) -> float:
        """
        Score de relevância para a palavra-chave
        """
        score = 0.0
        keyword_lower = keyword.lower()
        
        # Nome contém palavra-chave (50 pontos)
        if keyword_lower in name.lower():
            score += 50
        
        # Palavra-chave parcial no nome (25 pontos)
        elif any(word in name.lower() for word in keyword_lower.split()):
            score += 25
        
        # Tipos de negócio relevantes (30 pontos)
        relevant_types = [t for t in types if keyword_lower in t.lower()]
        score += min(len(relevant_types) * 10, 30)
        
        # Menção na localidade (20 pontos)
        if keyword_lower in vicinity.lower():
            score += 20
        
        return min(score, 100)
    
    def calculate_overall_score(self, metrics: Dict[str, float]) -> float:
        """Calcula score geral ponderado"""
        score = 0.0
        for key, weight in self.WEIGHTS.items():
            score += metrics.get(key, 0) * weight
        return round(score, 2)
    
    def get_strength_category(self, score: float) -> str:
        """Retorna categoria de força baseada no score"""
        for (min_score, max_score), category in self.STRENGTH_CATEGORIES.items():
            if min_score <= score < max_score:
                return category
        return "🔍 NÃO CLASSIFICADO"
    
    def analyze_profile(
        self,
        place_data: Dict,
        rank_position: int,
        center_lat: float,
        center_lng: float,
        radius: int,
        keyword: str,
        total_results: int
    ) -> ProfileMetrics:
        """Análise completa de um perfil"""
        
        place_id = place_data.get("place_id")
        name = place_data.get("name", "N/A")
        
        # Obtém detalhes completos
        details = self.get_place_details(place_id)
        result = details.get("result", {})
        
        # Dados básicos
        lat = place_data["geometry"]["location"]["lat"]
        lng = place_data["geometry"]["location"]["lng"]
        distance = self.calculate_distance(center_lat, center_lng, lat, lng)
        
        rating = place_data.get("rating", 0) or 0
        total_reviews = place_data.get("user_ratings_total", 0) or 0
        
        # Dados adicionais dos detalhes
        phone = result.get("formatted_phone_number")
        website = result.get("website")
        address = result.get("formatted_address", place_data.get("vicinity", "N/A"))
        vicinity = place_data.get("vicinity", "N/A")
        photos = result.get("photos", [])
        types = result.get("types", [])
        
        # Calcula todas as métricas
        rating_quality = self.calculate_rating_quality_score(rating, total_reviews)
        review_velocity = self.calculate_review_velocity_score(total_reviews)
        completeness = self.calculate_completeness_score(details)
        authority = self.calculate_authority_score(
            rating, total_reviews, bool(website), len(photos)
        )
        prominence = self.calculate_prominence_score(
            rank_position, total_results, distance, radius
        )
        relevance = self.calculate_relevance_score(name, keyword, types, vicinity)
        
        # Score geral
        metrics_dict = {
            'rating_quality': rating_quality,
            'review_velocity': review_velocity,
            'completeness': completeness,
            'authority': authority,
            'prominence': prominence,
            'relevance': relevance
        }
        
        overall_score = self.calculate_overall_score(metrics_dict)
        strength_category = self.get_strength_category(overall_score)
        
        return ProfileMetrics(
            place_id=place_id,
            name=name,
            rank_position=rank_position,
            address=address,
            vicinity=vicinity,
            phone=phone,
            website=website,
            latitude=lat,
            longitude=lng,
            distance_from_center=round(distance, 2),
            rating=rating,
            total_reviews=total_reviews,
            review_velocity_score=round(review_velocity, 2),
            rating_quality_score=round(rating_quality, 2),
            completeness_score=round(completeness, 2),
            authority_score=round(authority, 2),
            relevance_score=round(relevance, 2),
            prominence_score=round(prominence, 2),
            overall_strength_score=overall_score,
            strength_category=strength_category,
            percentile_rank=0.0,  # Será calculado depois
            gap_to_leader=0.0,    # Será calculado depois
            analysis_date=datetime.now().isoformat()
        )
    
    def run_analysis(
        self,
        location: str,
        radius: int,
        keyword: str,
        max_pages: int = 3
    ) -> Tuple[List[ProfileMetrics], pd.DataFrame]:
        """Executa análise completa"""
        
        logger.info(f"Iniciando análise para '{keyword}' em {location}")
        logger.info(f"Raio: {radius}m | Páginas: {max_pages}")
        
        # Parse location
        center_lat, center_lng = map(float, location.split(","))
        
        # Coleta dados
        all_places = []
        pagetoken = None
        pages = 0
        
        while pages < max_pages:
            data = self.search_places(location, radius, keyword, pagetoken)
            
            if data.get("status") == "ERROR":
                break
            
            places = data.get("results", [])
            all_places.extend(places)
            
            logger.info(f"Página {pages + 1}: {len(places)} resultados")
            
            pages += 1
            pagetoken = data.get("next_page_token")
            
            if not pagetoken:
                break
            
            time.sleep(2.5)
        
        logger.info(f"Total de {len(all_places)} perfis coletados")
        
        # Analisa cada perfil
        metrics_list = []
        for idx, place in enumerate(all_places, 1):
            logger.info(f"Analisando {idx}/{len(all_places)}: {place.get('name')}")
            
            metrics = self.analyze_profile(
                place, idx, center_lat, center_lng, radius, keyword, len(all_places)
            )
            metrics_list.append(metrics)
            
            time.sleep(0.5)  # Rate limiting
        
        # Calcula métricas comparativas
        if metrics_list:
            scores = [m.overall_strength_score for m in metrics_list]
            leader_score = max(scores)
            
            for metrics in metrics_list:
                # Percentil
                percentile = (sum(s <= metrics.overall_strength_score for s in scores) / len(scores)) * 100
                metrics.percentile_rank = round(percentile, 1)
                
                # Gap para o líder
                metrics.gap_to_leader = round(leader_score - metrics.overall_strength_score, 2)
        
        # Cria DataFrame
        df = pd.DataFrame([asdict(m) for m in metrics_list])
        
        logger.info("Análise concluída!")
        
        return metrics_list, df


def generate_reports(df: pd.DataFrame, keyword: str, output_dir: str = "output"):
    """Gera relatórios detalhados"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. CSV completo
    csv_file = output_path / f"ranking_analysis_{keyword}_{timestamp}.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    logger.info(f"CSV salvo: {csv_file}")
    
    # 2. Excel com múltiplas abas
    excel_file = output_path / f"ranking_analysis_{keyword}_{timestamp}.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Aba principal
        df.to_excel(writer, sheet_name='Análise Completa', index=False)
        
        # Top 10
        df.head(10).to_excel(writer, sheet_name='Top 10', index=False)
        
        # Estatísticas
        stats = df[['rating', 'total_reviews', 'overall_strength_score', 
                    'rating_quality_score', 'authority_score']].describe()
        stats.to_excel(writer, sheet_name='Estatísticas')
        
        # Categorias
        category_summary = df.groupby('strength_category').agg({
            'place_id': 'count',
            'overall_strength_score': 'mean',
            'total_reviews': 'mean',
            'rating': 'mean'
        }).round(2)
        category_summary.to_excel(writer, sheet_name='Por Categoria')
    
    logger.info(f"Excel salvo: {excel_file}")
    
    # 3. JSON detalhado
    json_file = output_path / f"ranking_analysis_{keyword}_{timestamp}.json"
    df.to_json(json_file, orient='records', indent=2, force_ascii=False)
    logger.info(f"JSON salvo: {json_file}")
    
    # 4. Relatório resumido em texto
    report_file = output_path / f"summary_report_{keyword}_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"RELATÓRIO DE ANÁLISE DE RANQUEAMENTO - {keyword.upper()}\n")
        f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total de perfis analisados: {len(df)}\n\n")
        
        f.write("TOP 10 RANKINGS:\n")
        f.write("-"*80 + "\n")
        for idx, row in df.head(10).iterrows():
            f.write(f"\n#{row['rank_position']} - {row['name']}\n")
            f.write(f"   Score Geral: {row['overall_strength_score']:.2f} {row['strength_category']}\n")
            f.write(f"   Rating: {row['rating']:.1f} ⭐ ({row['total_reviews']} reviews)\n")
            f.write(f"   Distância: {row['distance_from_center']:.0f}m\n")
            f.write(f"   Percentil: {row['percentile_rank']:.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("ESTATÍSTICAS GERAIS:\n")
        f.write("-"*80 + "\n")
        f.write(f"Score médio: {df['overall_strength_score'].mean():.2f}\n")
        f.write(f"Rating médio: {df['rating'].mean():.2f}\n")
        f.write(f"Média de reviews: {df['total_reviews'].mean():.0f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("DISTRIBUIÇÃO POR CATEGORIA:\n")
        f.write("-"*80 + "\n")
        for category, count in df['strength_category'].value_counts().items():
            f.write(f"{category}: {count} perfis ({count/len(df)*100:.1f}%)\n")
    
    logger.info(f"Relatório resumido salvo: {report_file}")
    
    return {
        'csv': csv_file,
        'excel': excel_file,
        'json': json_file,
        'report': report_file
    }


def main():
    """Função principal"""
    
    # CONFIGURAÇÕES
    API_KEY = "SUA_API_KEY_AQUI"
    LOCATION = "-23.55052,-46.633308"  # São Paulo
    RADIUS = 2000  # metros
    KEYWORD = "padaria"
    MAX_PAGES = 3
    
    # Inicializa analisador
    analyzer = GoogleMapsRankingAnalyzer(API_KEY)
    
    # Executa análise
    metrics_list, df = analyzer.run_analysis(
        location=LOCATION,
        radius=RADIUS,
        keyword=KEYWORD,
        max_pages=MAX_PAGES
    )
    
    # Gera relatórios
    files = generate_reports(df, KEYWORD)
    
    # Exibe resumo
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA!")
    print("="*80)
    print(f"\nTotal de perfis analisados: {len(df)}")
    print(f"\nTOP 5:")
    for idx, row in df.head(5).iterrows():
        print(f"  #{row['rank_position']} {row['name']}")
        print(f"      Score: {row['overall_strength_score']:.2f} {row['strength_category']}")
    
    print(f"\nArquivos gerados:")
    for file_type, filepath in files.items():
        print(f"  - {file_type.upper()}: {filepath}")


if __name__ == "__main__":
    main()
