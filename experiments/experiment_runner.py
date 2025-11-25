#!/usr/bin/env python3
"""
Framework de Experimentación para Sistema A2A
Ejecuta múltiples simulaciones con diferentes configuraciones para validación científica

Uso:
    python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import yaml
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from tqdm import tqdm

from supervisor import SupervisorOrchestrator
from utils.logging_utils import set_system_status, log_message


class ExperimentRunner:
    """
    Ejecutor de experimentos para validación científica
    """
    
    def __init__(self, config_file: str):
        """
        Inicializa el ejecutor de experimentos
        
        Args:
            config_file: Ruta al archivo de configuración YAML
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.results = []
        self.supervisor = SupervisorOrchestrator()
        
        # Crear directorio de resultados
        self.results_dir = Path("experiments/results") / self.config['experiment']['name']
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📊 Experimento: {self.config['experiment']['name']}")
        print(f"📁 Resultados en: {self.results_dir}")
    
    def _load_config(self) -> Dict:
        """Carga la configuración del experimento"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _generate_task(self, scenario: Dict) -> str:
        """
        Genera la descripción de tarea para un escenario
        
        Args:
            scenario: Diccionario con parámetros del escenario
            
        Returns:
            Descripción de tarea para el sistema
        """
        protocol = scenario.get('protocol', 'AODV')
        nodes = scenario.get('nodes', 20)
        area = scenario.get('area', 1000)
        duration = scenario.get('duration', 200)
        mobility = scenario.get('mobility', 'RandomWaypoint')
        speed = scenario.get('speed', '5-15')
        
        task = (
            f"Simular red MANET con protocolo {protocol}, "
            f"{nodes} nodos móviles con modelo {mobility} "
            f"(velocidad {speed} m/s), "
            f"área de {area}x{area} metros, "
            f"durante {duration} segundos"
        )
        
        return task
    
    def run_experiment(self):
        """Ejecuta el experimento completo"""
        experiment_name = self.config['experiment']['name']
        scenarios = self.config['scenarios']
        repetitions = self.config['experiment'].get('repetitions', 5)
        
        print(f"\n{'='*80}")
        print(f"🚀 INICIANDO EXPERIMENTO: {experiment_name}")
        print(f"{'='*80}")
        print(f"📋 Escenarios: {len(scenarios)}")
        print(f"🔄 Repeticiones por escenario: {repetitions}")
        print(f"📊 Total de simulaciones: {len(scenarios) * repetitions}")
        print(f"{'='*80}\n")
        
        # Calcular total de simulaciones
        total_sims = len(scenarios) * repetitions
        
        # Barra de progreso global
        with tqdm(total=total_sims, desc="Progreso total") as pbar:
            for scenario_idx, scenario in enumerate(scenarios, 1):
                scenario_name = scenario.get('name', f"Scenario_{scenario_idx}")
                
                print(f"\n{'='*60}")
                print(f"📌 Escenario {scenario_idx}/{len(scenarios)}: {scenario_name}")
                print(f"{'='*60}")
                
                # Ejecutar repeticiones
                for rep in range(1, repetitions + 1):
                    print(f"\n🔄 Repetición {rep}/{repetitions}")
                    
                    # Generar tarea
                    task = self._generate_task(scenario)
                    
                    # Configurar semilla para reproducibilidad
                    seed = scenario.get('base_seed', 12345) + rep
                    
                    # Ejecutar simulación
                    start_time = time.time()
                    
                    try:
                        result = self.supervisor.run_experiment(
                            task=task,
                            max_iterations=self.config['experiment'].get('max_iterations', 5)
                        )
                        
                        execution_time = time.time() - start_time
                        
                        if result and 'metrics' in result:
                            # Guardar resultado
                            result_entry = {
                                'experiment': experiment_name,
                                'scenario': scenario_name,
                                'repetition': rep,
                                'seed': seed,
                                'protocol': scenario.get('protocol'),
                                'nodes': scenario.get('nodes'),
                                'area': scenario.get('area'),
                                'duration': scenario.get('duration'),
                                'mobility': scenario.get('mobility'),
                                'speed': scenario.get('speed'),
                                'execution_time': execution_time,
                                'timestamp': datetime.now().isoformat(),
                                **result['metrics']
                            }
                            
                            self.results.append(result_entry)
                            
                            print(f"✅ Completado - PDR: {result['metrics'].get('avg_pdr', 0):.2f}%")
                        else:
                            print(f"⚠️  Simulación falló o sin métricas")
                            
                            # Guardar resultado fallido
                            result_entry = {
                                'experiment': experiment_name,
                                'scenario': scenario_name,
                                'repetition': rep,
                                'seed': seed,
                                'status': 'failed',
                                'execution_time': execution_time,
                                'timestamp': datetime.now().isoformat()
                            }
                            self.results.append(result_entry)
                    
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        execution_time = time.time() - start_time
                        
                        # Guardar resultado con error
                        result_entry = {
                            'experiment': experiment_name,
                            'scenario': scenario_name,
                            'repetition': rep,
                            'seed': seed,
                            'status': 'error',
                            'error': str(e),
                            'execution_time': execution_time,
                            'timestamp': datetime.now().isoformat()
                        }
                        self.results.append(result_entry)
                    
                    # Actualizar barra de progreso
                    pbar.update(1)
                    
                    # Guardar resultados parciales
                    self._save_results()
        
        print(f"\n{'='*80}")
        print(f"🎉 EXPERIMENTO COMPLETADO")
        print(f"{'='*80}")
        print(f"✅ Simulaciones exitosas: {len([r for r in self.results if 'avg_pdr' in r])}")
        print(f"⚠️  Simulaciones fallidas: {len([r for r in self.results if r.get('status') in ['failed', 'error']])}")
        print(f"📁 Resultados guardados en: {self.results_dir}")
        print(f"{'='*80}\n")
        
        # Generar análisis
        self._generate_analysis()
    
    def _save_results(self):
        """Guarda los resultados en CSV y JSON"""
        # Guardar CSV
        df = pd.DataFrame(self.results)
        csv_file = self.results_dir / "results.csv"
        df.to_csv(csv_file, index=False)
        
        # Guardar JSON
        json_file = self.results_dir / "results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def _generate_analysis(self):
        """Genera análisis estadístico de los resultados"""
        print("\n📊 Generando análisis estadístico...")
        
        df = pd.DataFrame(self.results)
        
        # Filtrar solo simulaciones exitosas
        df_success = df[df['avg_pdr'].notna()].copy()
        
        if df_success.empty:
            print("⚠️  No hay simulaciones exitosas para analizar")
            return
        
        # Análisis por escenario
        analysis = []
        
        for scenario in df_success['scenario'].unique():
            scenario_data = df_success[df_success['scenario'] == scenario]
            
            analysis_entry = {
                'scenario': scenario,
                'protocol': scenario_data['protocol'].iloc[0],
                'nodes': scenario_data['nodes'].iloc[0],
                'repetitions': len(scenario_data),
                'pdr_mean': scenario_data['avg_pdr'].mean(),
                'pdr_std': scenario_data['avg_pdr'].std(),
                'pdr_min': scenario_data['avg_pdr'].min(),
                'pdr_max': scenario_data['avg_pdr'].max(),
                'delay_mean': scenario_data['avg_delay'].mean(),
                'delay_std': scenario_data['avg_delay'].std(),
                'throughput_mean': scenario_data['avg_throughput'].mean(),
                'throughput_std': scenario_data['avg_throughput'].std(),
            }
            
            if 'routing_overhead' in scenario_data.columns:
                analysis_entry['overhead_mean'] = scenario_data['routing_overhead'].mean()
                analysis_entry['overhead_std'] = scenario_data['routing_overhead'].std()
            
            analysis.append(analysis_entry)
        
        # Guardar análisis
        analysis_df = pd.DataFrame(analysis)
        analysis_file = self.results_dir / "analysis.csv"
        analysis_df.to_csv(analysis_file, index=False)
        
        # Mostrar resumen
        print("\n📈 Resumen por Escenario:")
        print(analysis_df.to_string(index=False))
        
        # Generar reporte Markdown
        self._generate_markdown_report(analysis_df)
        
        print(f"\n✅ Análisis guardado en: {analysis_file}")
    
    def _generate_markdown_report(self, analysis_df: pd.DataFrame):
        """Genera reporte en formato Markdown"""
        report_file = self.results_dir / "REPORT.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Reporte de Experimento: {self.config['experiment']['name']}\n\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Configuración\n\n")
            f.write(f"- **Escenarios:** {len(self.config['scenarios'])}\n")
            f.write(f"- **Repeticiones:** {self.config['experiment'].get('repetitions', 5)}\n")
            f.write(f"- **Total simulaciones:** {len(self.results)}\n\n")
            
            f.write("## Resultados\n\n")
            f.write("### Resumen por Escenario\n\n")
            f.write(analysis_df.to_markdown(index=False))
            f.write("\n\n")
            
            f.write("## Interpretación\n\n")
            f.write("### PDR (Packet Delivery Ratio)\n\n")
            
            best_pdr = analysis_df.loc[analysis_df['pdr_mean'].idxmax()]
            f.write(f"- **Mejor rendimiento:** {best_pdr['scenario']} ")
            f.write(f"({best_pdr['protocol']}) con PDR de {best_pdr['pdr_mean']:.2f}% ")
            f.write(f"± {best_pdr['pdr_std']:.2f}%\n")
            
            f.write("\n### Delay\n\n")
            best_delay = analysis_df.loc[analysis_df['delay_mean'].idxmin()]
            f.write(f"- **Menor latencia:** {best_delay['scenario']} ")
            f.write(f"({best_delay['protocol']}) con {best_delay['delay_mean']:.2f} ms ")
            f.write(f"± {best_delay['delay_std']:.2f} ms\n")
            
            f.write("\n### Throughput\n\n")
            best_throughput = analysis_df.loc[analysis_df['throughput_mean'].idxmax()]
            f.write(f"- **Mayor throughput:** {best_throughput['scenario']} ")
            f.write(f"({best_throughput['protocol']}) con {best_throughput['throughput_mean']:.2f} Mbps ")
            f.write(f"± {best_throughput['throughput_std']:.2f} Mbps\n")
        
        print(f"✅ Reporte Markdown generado: {report_file}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Ejecutor de experimentos para Sistema A2A',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:

  # Ejecutar experimento de comparación de protocolos
  python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
  
  # Ejecutar experimento de escalabilidad
  python experiments/experiment_runner.py --config experiments/configs/scalability.yaml
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Archivo de configuración YAML del experimento'
    )
    
    args = parser.parse_args()
    
    try:
        runner = ExperimentRunner(args.config)
        runner.run_experiment()
        
        print("\n✅ Experimento completado exitosamente")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error ejecutando experimento: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
