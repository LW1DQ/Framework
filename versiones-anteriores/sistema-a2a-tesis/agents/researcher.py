"""
Agente Investigador

Responsable de buscar y sintetizar literatura académica relevante
usando Semantic Scholar, arXiv y ChromaDB para RAG local.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
from langchain_ollama import ChatOllama
from chromadb import Client
import requests

from config.settings import (
    OLLAMA_BASE_URL,
    MODEL_REASONING,
    MODEL_EMBEDDING,
    CHROMA_PATH,
    SEMANTIC_SCHOLAR_MAX_RESULTS
)
from utils.state import AgentState, add_audit_entry


def search_semantic_scholar(query: str, max_results: int = 10) -> list:
    """
    Busca papers en Semantic Scholar con filtros avanzados
    
    Args:
        query: Consulta de búsqueda
        max_results: Número máximo de resultados
        
    Returns:
        Lista de papers encontrados
    """
    try:
        # API de Semantic Scholar con campos extendidos
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': query,
            'limit': max_results,
            'fields': 'title,abstract,year,authors,citationCount,url,venue,publicationTypes,influentialCitationCount',
            'year': '2018-',  # Solo papers recientes (últimos 7 años)
            'minCitationCount': 5  # Filtrar papers con al menos 5 citas
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            papers = []
            
            for paper in data.get('data', []):
                # Filtrar papers sin abstract
                if not paper.get('abstract'):
                    continue
                
                papers.append({
                    'title': paper.get('title', ''),
                    'abstract': paper.get('abstract', ''),
                    'year': paper.get('year', ''),
                    'authors': [a.get('name', '') for a in paper.get('authors', [])],
                    'citations': paper.get('citationCount', 0),
                    'influential_citations': paper.get('influentialCitationCount', 0),
                    'venue': paper.get('venue', ''),
                    'url': paper.get('url', ''),
                    'relevance_score': calculate_relevance_score(paper)
                })
            
            # Ordenar por relevancia
            papers.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return papers
        else:
            print(f"⚠️  Semantic Scholar API error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error buscando en Semantic Scholar: {e}")
        return []


def calculate_relevance_score(paper: dict) -> float:
    """
    Calcula score de relevancia basado en múltiples factores
    
    Args:
        paper: Diccionario con datos del paper
        
    Returns:
        Score de relevancia (0-100)
    """
    score = 0.0
    
    # Factor 1: Citas (peso 40%)
    citations = paper.get('citationCount', 0)
    score += min(citations / 10, 40)  # Max 40 puntos
    
    # Factor 2: Citas influyentes (peso 30%)
    influential = paper.get('influentialCitationCount', 0)
    score += min(influential * 3, 30)  # Max 30 puntos
    
    # Factor 3: Recencia (peso 20%)
    year = paper.get('year', 2018)
    if year >= 2023:
        score += 20
    elif year >= 2020:
        score += 15
    elif year >= 2018:
        score += 10
    
    # Factor 4: Venue de calidad (peso 10%)
    venue = paper.get('venue', '').lower()
    quality_venues = ['ieee', 'acm', 'springer', 'elsevier', 'nature', 'science']
    if any(v in venue for v in quality_venues):
        score += 10
    
    return score


def store_in_chromadb(papers: list, collection_name: str = "thesis_papers"):
    """
    Almacena papers en ChromaDB para RAG
    
    Args:
        papers: Lista de papers
        collection_name: Nombre de la colección
    """
    try:
        client = Client()
        collection = client.get_or_create_collection(collection_name)
        
        for i, paper in enumerate(papers):
            # Combinar título y abstract
            content = f"Title: {paper['title']}\n\nAbstract: {paper['abstract']}"
            
            # Almacenar
            collection.add(
                documents=[content],
                metadatas=[{
                    'title': paper['title'],
                    'year': str(paper['year']),
                    'citations': paper['citations'],
                    'url': paper['url']
                }],
                ids=[f"paper_{i}_{hash(paper['title'])}"]
            )
        
        print(f"✅ {len(papers)} papers almacenados en ChromaDB")
        
    except Exception as e:
        print(f"⚠️  Error almacenando en ChromaDB: {e}")


def synthesize_research(task: str, papers: list) -> str:
    """
    Sintetiza hallazgos de investigación usando LLM con análisis profundo
    
    Args:
        task: Tarea de investigación
        papers: Lista de papers encontrados
        
    Returns:
        Síntesis de hallazgos
    """
    try:
        llm = ChatOllama(
            model=MODEL_REASONING,
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )
        
        # Preparar contexto con top 7 papers ordenados por relevancia
        papers_summary = "\n\n".join([
            f"**Paper {i+1}** (Relevancia: {p.get('relevance_score', 0):.1f}/100):\n"
            f"Título: {p['title']}\n"
            f"Año: {p['year']} | Citas: {p['citations']} | Venue: {p.get('venue', 'N/A')}\n"
            f"Abstract: {p['abstract'][:400]}..."
            for i, p in enumerate(papers[:7])
        ])
        
        prompt = f"""
Eres un investigador experto en redes de telecomunicaciones, protocolos de enrutamiento y ciudades inteligentes.

**TAREA DE INVESTIGACIÓN:**
{task}

**PAPERS ENCONTRADOS (ordenados por relevancia):**
{papers_summary}

**ANÁLISIS REQUERIDO:**

1. **Estado del Arte** (3-4 párrafos):
   - Técnicas y algoritmos más prometedores mencionados
   - Métricas de rendimiento reportadas (PDR, latencia, throughput, overhead)
   - Comparación entre enfoques (tradicionales vs ML/DL)
   - Limitaciones y desafíos identificados

2. **Implementación en NS-3**:
   - Protocolos de enrutamiento específicos mencionados (AODV, OLSR, DSDV, etc.)
   - Configuraciones de red sugeridas (número de nodos, área, movilidad)
   - Parámetros críticos a ajustar
   - Módulos de NS-3 relevantes

3. **Oportunidades de Investigación con Deep Learning**:
   - Arquitecturas de redes neuronales aplicables (DQN, A3C, GNN, Transformer)
   - Variables de estado para el agente RL
   - Espacio de acciones posibles
   - Función de recompensa sugerida
   - Métricas de evaluación

4. **Brechas y Contribuciones Potenciales**:
   - Qué no se ha explorado suficientemente
   - Combinaciones novedosas de técnicas
   - Escenarios no evaluados

**FORMATO:**
- Sé específico y técnico
- Cita números de paper cuando sea relevante [Paper X]
- Incluye valores numéricos cuando estén disponibles
- Prioriza información implementable
"""
        
        response = llm.invoke(prompt)
        
        # Añadir metadata de papers al final
        metadata = "\n\n---\n**REFERENCIAS:**\n"
        for i, p in enumerate(papers[:7], 1):
            metadata += f"{i}. {p['title']} ({p['year']}) - {p['citations']} citas\n"
            metadata += f"   {p.get('url', 'N/A')}\n"
        
        return response.content + metadata
        
    except Exception as e:
        print(f"❌ Error en síntesis: {e}")
        return f"Error al sintetizar investigación: {str(e)}"


def query_vectordb(query: str, collection_name: str = "thesis_papers", n_results: int = 5) -> list:
    """
    Consulta la base de datos vectorial para RAG
    
    Args:
        query: Consulta de búsqueda
        collection_name: Nombre de la colección
        n_results: Número de resultados
        
    Returns:
        Lista de documentos relevantes
    """
    try:
        client = Client()
        collection = client.get_or_create_collection(collection_name)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results.get('documents', [[]])[0]
    except Exception as e:
        print(f"⚠️  Error consultando ChromaDB: {e}")
        return []


def search_arxiv(query: str, max_results: int = 5) -> list:
    """
    Busca papers en arXiv
    
    Args:
        query: Consulta de búsqueda
        max_results: Número máximo de resultados
        
    Returns:
        Lista de papers encontrados
    """
    try:
        import arxiv
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        client = arxiv.Client()
        
        for result in client.results(search):
            papers.append({
                'title': result.title,
                'abstract': result.summary,
                'year': result.published.year,
                'authors': [author.name for author in result.authors],
                'citations': 0,
                'url': result.pdf_url
            })
        
        return papers
    except Exception as e:
        print(f"⚠️  Error buscando en arXiv: {e}")
        return []


def research_node(state: AgentState) -> Dict:
    """
    Nodo del agente investigador para LangGraph
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("🔍 AGENTE INVESTIGADOR ACTIVADO")
    print("="*80)
    
    task = state['task']
    print(f"📋 Tarea: {task}\n")
    
    all_papers = []
    
    # 1. Buscar en Semantic Scholar
    print("🔎 Buscando en Semantic Scholar...")
    query_ss = f"routing protocols optimization {task} ns-3 smart cities"
    papers_ss = search_semantic_scholar(query_ss, SEMANTIC_SCHOLAR_MAX_RESULTS)
    
    if papers_ss:
        print(f"✅ Semantic Scholar: {len(papers_ss)} papers")
        all_papers.extend(papers_ss)
    
    # 2. Buscar en arXiv
    print("🔎 Buscando en arXiv...")
    query_arxiv = f"routing protocols {task} machine learning"
    papers_arxiv = search_arxiv(query_arxiv, max_results=5)
    
    if papers_arxiv:
        print(f"✅ arXiv: {len(papers_arxiv)} papers")
        all_papers.extend(papers_arxiv)
    
    # 3. Consultar base de datos local (RAG)
    print("🔎 Consultando base de datos local...")
    local_docs = query_vectordb(task, n_results=3)
    
    if local_docs:
        print(f"✅ Base local: {len(local_docs)} documentos relevantes")
    
    if all_papers:
        print(f"\n📚 Total: {len(all_papers)} papers encontrados")
        
        # Almacenar en ChromaDB
        print("💾 Almacenando en base de datos vectorial...")
        store_in_chromadb(all_papers)
        
        # Sintetizar hallazgos
        print("📝 Sintetizando hallazgos...")
        synthesis = synthesize_research(task, all_papers)
        
        # Añadir contexto de documentos locales si existen
        if local_docs:
            synthesis += "\n\n**Contexto de investigaciones previas:**\n"
            synthesis += "\n".join([f"- {doc[:200]}..." for doc in local_docs[:2]])
        
        print("\n📚 Síntesis completada")
        print(f"   Longitud: {len(synthesis)} caracteres")
        print(f"   Papers: {len(all_papers)}")
        
        # Actualizar estado
        return {
            "research_notes": [synthesis],
            "papers_found": all_papers,
            **add_audit_entry(state, "researcher", "literature_review", {
                'papers_count': len(all_papers),
                'sources': ['semantic_scholar', 'arxiv', 'local_db'],
                'query': query_ss
            })
        }
    else:
        print("⚠️  No se encontraron papers. Continuando con conocimiento base...")
        
        # Síntesis básica sin papers
        synthesis = f"""
No se encontraron papers específicos para la consulta, pero basándose en 
conocimiento general sobre {task}:

1. **Protocolos Estándar**: AODV, OLSR, DSDV son protocolos comunes en MANETs
2. **Métricas Clave**: PDR, latencia, throughput, overhead de enrutamiento
3. **Configuración NS-3**: Usar WiFi 802.11, modelos de movilidad apropiados
4. **Recomendación**: Implementar simulación baseline para comparación

Se recomienda ejecutar simulaciones con diferentes configuraciones para 
obtener resultados empíricos.
"""
        
        # Añadir contexto local si existe
        if local_docs:
            synthesis += "\n\n**Contexto de investigaciones previas:**\n"
            synthesis += "\n".join([f"- {doc[:200]}..." for doc in local_docs[:2]])
        
        return {
            "research_notes": [synthesis],
            "papers_found": [],
            **add_audit_entry(state, "researcher", "no_papers_found", {
                'query': query_ss
            })
        }


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    test_state = create_initial_state(
        "Comparar AODV y OLSR en redes vehiculares"
    )
    
    result = research_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA")
    print("="*80)
    print(f"Papers encontrados: {len(result['papers_found'])}")
    print(f"\nSíntesis:\n{result['research_notes'][0][:500]}...")
