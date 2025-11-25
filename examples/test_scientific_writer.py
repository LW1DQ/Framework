#!/usr/bin/env python3
"""
Script de Prueba del Agente de Escritura Científica
Genera documentos de ejemplo para demostrar las capacidades del agente
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.scientific_writer import scientific_writer_node
from datetime import datetime


def create_sample_results():
    """Crea resultados de ejemplo para pruebas"""
    return {
        "experiment_name": "Comparación de Protocolos AODV vs OLSR",
        "timestamp": datetime.now().isoformat(),
        "configuration": {
            "protocols": ["AODV", "OLSR"],
            "nodes": 20,
            "area": "1000x1000m",
            "duration": "200s",
            "mobility": "RandomWaypoint",
            "speed": "5-15 m/s",
            "traffic": "CBR (4 pkt/s)",
            "packet_size": "512 bytes",
            "repetitions": 10,
            "seeds": [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 1234]
        },
        "metrics": {
            "AODV": {
                "pdr": {
                    "mean": 0.87,
                    "std": 0.05,
                    "ci": [0.85, 0.89],
                    "min": 0.79,
                    "max": 0.94
                },
                "delay": {
                    "mean": 45.2,
                    "std": 8.3,
                    "ci": [42.1, 48.3],
                    "min": 32.1,
                    "max": 61.5,
                    "unit": "ms"
                },
                "throughput": {
                    "mean": 2.3,
                    "std": 0.4,
                    "ci": [2.1, 2.5],
                    "min": 1.7,
                    "max": 2.9,
                    "unit": "Mbps"
                },
                "overhead": {
                    "mean": 0.15,
                    "std": 0.03,
                    "ci": [0.14, 0.16],
                    "min": 0.11,
                    "max": 0.21
                }
            },
            "OLSR": {
                "pdr": {
                    "mean": 0.91,
                    "std": 0.04,
                    "ci": [0.89, 0.93],
                    "min": 0.84,
                    "max": 0.97
                },
                "delay": {
                    "mean": 38.7,
                    "std": 6.2,
                    "ci": [36.2, 41.2],
                    "min": 28.3,
                    "max": 49.1,
                    "unit": "ms"
                },
                "throughput": {
                    "mean": 2.5,
                    "std": 0.3,
                    "ci": [2.3, 2.7],
                    "min": 2.0,
                    "max": 3.1,
                    "unit": "Mbps"
                },
                "overhead": {
                    "mean": 0.22,
                    "std": 0.04,
                    "ci": [0.20, 0.24],
                    "min": 0.16,
                    "max": 0.29
                }
            }
        },
        "statistical_analysis": {
            "pdr_comparison": {
                "test": "t-test",
                "p_value": 0.003,
                "significant": True,
                "conclusion": "OLSR tiene PDR significativamente mayor que AODV"
            },
            "delay_comparison": {
                "test": "t-test",
                "p_value": 0.012,
                "significant": True,
                "conclusion": "OLSR tiene delay significativamente menor que AODV"
            },
            "throughput_comparison": {
                "test": "t-test",
                "p_value": 0.089,
                "significant": False,
                "conclusion": "No hay diferencia significativa en throughput"
            },
            "overhead_comparison": {
                "test": "t-test",
                "p_value": 0.001,
                "significant": True,
                "conclusion": "OLSR tiene overhead significativamente mayor que AODV"
            }
        }
    }


def test_briefing():
    """Prueba generación de briefing"""
    print("\n" + "="*70)
    print("🧪 TEST 1: Generación de Briefing")
    print("="*70)
    
    results = create_sample_results()
    
    state = {
        "document_type": "briefing",
        "experiment_results": results,
        "messages": []
    }
    
    result_state = scientific_writer_node(state)
    
    if "generated_document" in result_state:
        print("✅ Briefing generado exitosamente!")
        print(f"📁 Guardado en: {result_state.get('document_path')}")
        print(f"📊 Longitud: {len(result_state['generated_document'])} caracteres")
        print("\n📄 Primeras 500 caracteres:")
        print("-" * 70)
        print(result_state["generated_document"][:500] + "...")
        print("-" * 70)
        return True
    else:
        print(f"❌ Error: {result_state.get('error')}")
        return False


def test_detailed_report():
    """Prueba generación de informe detallado"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Generación de Informe Detallado")
    print("="*70)
    
    results = create_sample_results()
    
    state = {
        "document_type": "detailed_report",
        "experiment_results": results,
        "messages": []
    }
    
    result_state = scientific_writer_node(state)
    
    if "generated_document" in result_state:
        print("✅ Informe detallado generado exitosamente!")
        print(f"📁 Guardado en: {result_state.get('document_path')}")
        print(f"📊 Longitud: {len(result_state['generated_document'])} caracteres")
        print("\n📄 Primeras 500 caracteres:")
        print("-" * 70)
        print(result_state["generated_document"][:500] + "...")
        print("-" * 70)
        return True
    else:
        print(f"❌ Error: {result_state.get('error')}")
        return False


def test_thesis_section():
    """Prueba generación de sección de tesis"""
    print("\n" + "="*70)
    print("🧪 TEST 3: Generación de Sección de Tesis (Resultados)")
    print("="*70)
    
    results = create_sample_results()
    
    state = {
        "document_type": "thesis_section",
        "thesis_section_type": "results",
        "experiment_results": results,
        "messages": []
    }
    
    result_state = scientific_writer_node(state)
    
    if "generated_document" in result_state:
        print("✅ Sección de tesis generada exitosamente!")
        print(f"📁 Guardado en: {result_state.get('document_path')}")
        print(f"📊 Longitud: {len(result_state['generated_document'])} caracteres")
        print("\n📄 Primeras 500 caracteres:")
        print("-" * 70)
        print(result_state["generated_document"][:500] + "...")
        print("-" * 70)
        return True
    else:
        print(f"❌ Error: {result_state.get('error')}")
        return False


def test_paper_draft():
    """Prueba generación de borrador de paper"""
    print("\n" + "="*70)
    print("🧪 TEST 4: Generación de Borrador de Paper")
    print("="*70)
    
    results = create_sample_results()
    
    state = {
        "document_type": "paper_draft",
        "experiment_results": results,
        "messages": []
    }
    
    result_state = scientific_writer_node(state)
    
    if "generated_document" in result_state:
        print("✅ Borrador de paper generado exitosamente!")
        print(f"📁 Guardado en: {result_state.get('document_path')}")
        print(f"📊 Longitud: {len(result_state['generated_document'])} caracteres")
        print("\n📄 Primeras 500 caracteres:")
        print("-" * 70)
        print(result_state["generated_document"][:500] + "...")
        print("-" * 70)
        return True
    else:
        print(f"❌ Error: {result_state.get('error')}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print("🖊️  PRUEBA DEL AGENTE DE ESCRITURA CIENTÍFICA")
    print("="*70)
    print("\nEste script generará 4 tipos de documentos de ejemplo:")
    print("1. Briefing (2 páginas)")
    print("2. Informe Detallado (5-10 páginas)")
    print("3. Sección de Tesis (Resultados)")
    print("4. Borrador de Paper (formato IEEE)")
    print("\nLos documentos se guardarán en: generated_documents/")
    print("="*70)
    
    results = []
    
    # Ejecutar tests
    results.append(("Briefing", test_briefing()))
    results.append(("Informe Detallado", test_detailed_report()))
    results.append(("Sección de Tesis", test_thesis_section()))
    results.append(("Borrador de Paper", test_paper_draft()))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}  {name}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n📁 Revisa los documentos generados en: generated_documents/")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
