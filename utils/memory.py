"""
Módulo de Memoria Episódica

Permite a los agentes almacenar y recuperar experiencias pasadas para aprender de errores.
Utiliza ChromaDB para almacenamiento vectorial.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from config.settings import CHROMA_PATH, MODEL_EMBEDDING

class EpisodicMemory:
    """
    Gestor de memoria episódica para agentes.
    Almacena tuplas (tarea, código, error, solución).
    """
    
    def __init__(self, collection_name: str = "agent_experiences"):
        """
        Inicializa la memoria episódica.
        
        Args:
            collection_name: Nombre de la colección en ChromaDB
        """
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
    def add_experience(self, task: str, code: str, error: str, solution: str) -> None:
        """
        Almacena una nueva experiencia de aprendizaje.
        
        Args:
            task: Descripción de la tarea original
            code: Código que falló (o contexto relevante)
            error: Error encontrado
            solution: Código corregido o explicación de la solución
        """
        import hashlib
        import datetime
        
        # Crear ID único basado en contenido
        content_hash = hashlib.md5(f"{task}{error}".encode()).hexdigest()
        timestamp = datetime.datetime.now().isoformat()
        
        # El documento principal es la combinación de tarea y error, que es lo que buscaremos
        document = f"Task: {task}\nError: {error}"
        
        self.collection.add(
            documents=[document],
            metadatas=[{
                "task": task,
                "error": error,
                "solution": solution,
                "timestamp": timestamp,
                "type": "error_resolution"
            }],
            ids=[f"exp_{content_hash}_{timestamp}"]
        )
        print(f"🧠 Memoria: Experiencia almacenada (ID: exp_{content_hash}...)")

    def retrieve_experience(self, task: str, error: str, n_results: int = 1) -> List[Dict[str, Any]]:
        """
        Recupera experiencias similares pasadas.
        
        Args:
            task: Tarea actual
            error: Error actual
            n_results: Número de resultados a recuperar
            
        Returns:
            Lista de experiencias relevantes (soluciones)
        """
        query_text = f"Task: {task}\nError: {error}"
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        experiences = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                experiences.append({
                    "task": metadata['task'],
                    "error": metadata['error'],
                    "solution": metadata['solution'],
                    "relevance": 1.0 - results['distances'][0][i] if results['distances'] else 0.0
                })
                
        return experiences

# Instancia global para uso fácil
memory = EpisodicMemory()
