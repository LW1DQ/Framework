"""
Memoria Episódica para el Sistema A2A

Permite al sistema recordar experiencias pasadas (código, errores, soluciones)
y recuperarlas cuando enfrenta problemas similares.
"""

import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

# Intentar importar sklearn, si no está disponible usar fallback simple
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️  scikit-learn no disponible. Memoria episódica usará búsqueda simple.")


class EpisodicMemory:
    """
    Almacena y recupera experiencias pasadas del sistema.
    
    Cada experiencia contiene:
    - task: Tarea que se estaba realizando
    - code: Código que se generó
    - error: Error que ocurrió
    - solution: Solución que funcionó
    - timestamp: Cuándo ocurrió
    """
    
    def __init__(self, memory_file: str = "data/episodic_memory.json"):
        """
        Inicializa la memoria episódica
        
        Args:
            memory_file: Ruta al archivo de memoria
        """
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.experiences = self._load()
        
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(max_features=100)
        else:
            self.vectorizer = None
    
    def _load(self) -> List[Dict]:
        """Carga experiencias desde archivo"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error cargando memoria: {e}")
                return []
        return []
    
    def _save(self):
        """Guarda experiencias a archivo"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.experiences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Error guardando memoria: {e}")
    
    def add_experience(self, task: str, code: str, error: str, solution: str):
        """
        Añade una nueva experiencia a la memoria
        
        Args:
            task: Descripción de la tarea
            code: Código que causó el error
            error: Mensaje de error
            solution: Código que solucionó el problema
        """
        experience = {
            'task': task[:500],  # Truncar para no ocupar mucho espacio
            'code': code[:1000],
            'error': error[:500],
            'solution': solution[:1000],
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        self.experiences.append(experience)
        
        # Limitar a últimas 100 experiencias
        if len(self.experiences) > 100:
            self.experiences = self.experiences[-100:]
        
        self._save()
        print(f"🧠 Experiencia guardada en memoria ({len(self.experiences)} total)")
    
    def retrieve_experience(self, task: str, error: str, top_k: int = 3) -> List[Dict]:
        """
        Recupera experiencias similares de la memoria
        
        Args:
            task: Tarea actual
            error: Error actual
            top_k: Número de experiencias a recuperar
            
        Returns:
            Lista de experiencias similares con score de relevancia
        """
        if not self.experiences:
            return []
        
        query = f"{task} {error}"
        
        if HAS_SKLEARN and len(self.experiences) >= 2:
            return self._retrieve_with_tfidf(query, top_k)
        else:
            return self._retrieve_simple(query, top_k)
    
    def _retrieve_with_tfidf(self, query: str, top_k: int) -> List[Dict]:
        """Recuperación usando TF-IDF y similitud coseno"""
        try:
            # Crear documentos de experiencias
            docs = [f"{exp['task']} {exp['error']}" for exp in self.experiences]
            
            # Vectorizar
            all_docs = [query] + docs
            vectors = self.vectorizer.fit_transform(all_docs)
            
            # Calcular similitud
            query_vector = vectors[0:1]
            doc_vectors = vectors[1:]
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # Obtener top_k más similares
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Umbral mínimo de similitud
                    exp = self.experiences[idx].copy()
                    exp['relevance'] = float(similarities[idx])
                    results.append(exp)
            
            return results
        except Exception as e:
            print(f"⚠️  Error en recuperación TF-IDF: {e}")
            return self._retrieve_simple(query, top_k)
    
    def _retrieve_simple(self, query: str, top_k: int) -> List[Dict]:
        """Recuperación simple basada en palabras clave"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_experiences = []
        
        for exp in self.experiences:
            # Calcular score simple: palabras en común
            exp_text = f"{exp['task']} {exp['error']}".lower()
            exp_words = set(exp_text.split())
            
            common_words = query_words.intersection(exp_words)
            score = len(common_words) / max(len(query_words), 1)
            
            if score > 0.1:  # Umbral mínimo
                exp_copy = exp.copy()
                exp_copy['relevance'] = score
                scored_experiences.append(exp_copy)
        
        # Ordenar por score y retornar top_k
        scored_experiences.sort(key=lambda x: x['relevance'], reverse=True)
        return scored_experiences[:top_k]
    
    def clear(self):
        """Limpia toda la memoria"""
        self.experiences = []
        self._save()
        print("🧠 Memoria episódica limpiada")
    
    def get_stats(self) -> Dict:
        """Retorna estadísticas de la memoria"""
        return {
            'total_experiences': len(self.experiences),
            'memory_file': str(self.memory_file),
            'has_sklearn': HAS_SKLEARN
        }


# Instancia global de memoria
memory = EpisodicMemory()


if __name__ == "__main__":
    # Prueba de la memoria episódica
    print("🧠 Prueba de Memoria Episódica\n")
    
    # Añadir experiencias de prueba
    memory.add_experience(
        task="Simular AODV con 20 nodos",
        code="import ns.core\nns.core.Simulator.Run()",
        error="AttributeError: module 'ns' has no attribute 'core'",
        solution="import ns.core\nimport ns.network\nns.core.Simulator.Run()"
    )
    
    memory.add_experience(
        task="Simular OLSR con 30 nodos",
        code="import ns.olsr",
        error="ModuleNotFoundError: No module named 'ns.olsr'",
        solution="import ns.olsr\nolsr = ns.olsr.OlsrHelper()"
    )
    
    # Recuperar experiencias similares
    print("\n🔍 Buscando experiencias similares...\n")
    results = memory.retrieve_experience(
        task="Simular AODV con 15 nodos",
        error="AttributeError: module 'ns' has no attribute 'core'"
    )
    
    print(f"Encontradas {len(results)} experiencias relevantes:\n")
    for i, exp in enumerate(results, 1):
        print(f"{i}. Relevancia: {exp['relevance']:.2f}")
        print(f"   Tarea: {exp['task'][:50]}...")
        print(f"   Error: {exp['error'][:50]}...")
        print(f"   Solución: {exp['solution'][:50]}...")
        print()
    
    # Estadísticas
    stats = memory.get_stats()
    print(f"📊 Estadísticas:")
    print(f"   Total experiencias: {stats['total_experiences']}")
    print(f"   Archivo: {stats['memory_file']}")
    print(f"   Sklearn disponible: {stats['has_sklearn']}")
