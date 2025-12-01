#!/usr/bin/env python3
"""
Analizador Estadístico Avanzado para Experimentos
Genera análisis estadístico riguroso para publicación científica
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

# Configurar estilo de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


class StatisticalAnalyzer:
    """
    Analizador estadístico para resultados de experimentos
    """
    
    def __init__(self, results_file: str):
        """
        Inicializa el analizador
        
        Args:
            results_file: Ruta al archivo CSV con resultados
        """
        self.results_file = Path(results_file)
        self.df = pd.read_csv(results_file)
        self.output_dir = self.results_file.parent / "analysis"
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"📊 Analizador Estadístico")
        print(f"📁 Resultados: {results_file}")
        print(f"📈 Simulaciones: {len(self.df)}")
        print(f"📁 Análisis en: {self.output_dir}")
    
    def descriptive_statistics(self) -> pd.DataFrame:
        """Calcula estadísticas descriptivas por escenario"""
        print("\n📊 Calculando estadísticas descriptivas...")
        
        # Filtrar solo simulaciones exitosas
        df_success = self.df[self.df['avg_pdr'].notna()].copy()
        
        # Agrupar por escenario
        grouped = df_success.groupby('scenario')
        
        stats_list = []
        
        for scenario, group in grouped:
            stats_dict = {
                'scenario': scenario,
                'protocol': group['protocol'].iloc[0],
                'n': len(group),
                
                # PDR
                'pdr_mean': group['avg_pdr'].mean(),
                'pdr_std': group['avg_pdr'].std(),
                'pdr_min': group['avg_pdr'].min(),
                'pdr_max': group['avg_pdr'].max(),
                'pdr_median': group['avg_pdr'].median(),
                'pdr_ci_lower': self._confidence_interval(group['avg_pdr'])[0],
                'pdr_ci_upper': self._confidence_interval(group['avg_pdr'])[1],
                
                # Delay
                'delay_mean': group['avg_delay'].mean(),
                'delay_std': group['avg_delay'].std(),
                'delay_min': group['avg_delay'].min(),
                'delay_max': group['avg_delay'].max(),
                'delay_median': group['avg_delay'].median(),
                'delay_ci_lower': self._confidence_interval(group['avg_delay'])[0],
                'delay_ci_upper': self._confidence_interval(group['avg_delay'])[1],
                
                # Throughput
                'throughput_mean': group['avg_throughput'].mean(),
                'throughput_std': group['avg_throughput'].std(),
                'throughput_ci_lower': self._confidence_interval(group['avg_throughput'])[0],
                'throughput_ci_upper': self._confidence_interval(group['avg_throughput'])[1],
            }
            
            stats_list.append(stats_dict)
        
        stats_df = pd.DataFrame(stats_list)
        
        # Guardar
        output_file = self.output_dir / "descriptive_statistics.csv"
        stats_df.to_csv(output_file, index=False)
        
        print(f"✅ Estadísticas guardadas en: {output_file}")
        
        return stats_df
    
    def _confidence_interval(self, data: pd.Series, confidence: float = 0.95) -> Tuple[float, float]:
        """Calcula intervalo de confianza"""
        n = len(data)
        mean = data.mean()
        se = stats.sem(data)
        margin = se * stats.t.ppf((1 + confidence) / 2, n - 1)
        return (mean - margin, mean + margin)
    
    def compare_protocols(self) -> Dict:
        """Compara protocolos usando tests estadísticos"""
        print("\n📊 Comparando protocolos...")
        
        df_success = self.df[self.df['avg_pdr'].notna()].copy()
        
        protocols = df_success['protocol'].unique()
        
        if len(protocols) < 2:
            print("⚠️  Se necesitan al menos 2 protocolos para comparar")
            return {}
        
        results = {}
        
        # T-test para cada par de protocolos
        for i, prot1 in enumerate(protocols):
            for prot2 in protocols[i+1:]:
                data1 = df_success[df_success['protocol'] == prot1]
                data2 = df_success[df_success['protocol'] == prot2]
                
                # T-test para PDR
                t_stat_pdr, p_value_pdr = stats.ttest_ind(
                    data1['avg_pdr'],
                    data2['avg_pdr']
                )
                
                # T-test para Delay
                t_stat_delay, p_value_delay = stats.ttest_ind(
                    data1['avg_delay'],
                    data2['avg_delay']
                )
                
                results[f"{prot1}_vs_{prot2}"] = {
                    'pdr_t_statistic': t_stat_pdr,
                    'pdr_p_value': p_value_pdr,
                    'pdr_significant': p_value_pdr < 0.05,
                    'delay_t_statistic': t_stat_delay,
                    'delay_p_value': p_value_delay,
                    'delay_significant': p_value_delay < 0.05
                }
        
        # ANOVA si hay 3+ protocolos
        if len(protocols) >= 3:
            groups_pdr = [df_success[df_success['protocol'] == p]['avg_pdr'].values 
                         for p in protocols]
            f_stat, p_value = stats.f_oneway(*groups_pdr)
            
            results['anova_pdr'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        # Guardar resultados
        output_file = self.output_dir / "protocol_comparison.json"
        import json
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Comparación guardada en: {output_file}")
        
        return results
    
    def generate_plots(self):
        """Genera gráficos para publicación"""
        print("\n📈 Generando gráficos...")
        
        df_success = self.df[self.df['avg_pdr'].notna()].copy()
        
        # Gráfico 1: PDR por protocolo
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_success, x='protocol', y='avg_pdr')
        plt.title('Packet Delivery Ratio por Protocolo')
        plt.ylabel('PDR (%)')
        plt.xlabel('Protocolo')
        plt.tight_layout()
        plt.savefig(self.output_dir / "pdr_by_protocol.png", dpi=300)
        plt.close()
        
        # Gráfico 2: Delay por protocolo
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_success, x='protocol', y='avg_delay')
        plt.title('End-to-End Delay por Protocolo')
        plt.ylabel('Delay (ms)')
        plt.xlabel('Protocolo')
        plt.tight_layout()
        plt.savefig(self.output_dir / "delay_by_protocol.png", dpi=300)
        plt.close()
        
        # Gráfico 3: Throughput por protocolo
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_success, x='protocol', y='avg_throughput')
        plt.title('Throughput por Protocolo')
        plt.ylabel('Throughput (Mbps)')
        plt.xlabel('Protocolo')
        plt.tight_layout()
        plt.savefig(self.output_dir / "throughput_by_protocol.png", dpi=300)
        plt.close()
        
        # Gráfico 4: Comparación múltiple
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        sns.barplot(data=df_success, x='protocol', y='avg_pdr', ax=axes[0, 0], ci=95)
        axes[0, 0].set_title('PDR (95% CI)')
        axes[0, 0].set_ylabel('PDR (%)')
        
        sns.barplot(data=df_success, x='protocol', y='avg_delay', ax=axes[0, 1], ci=95)
        axes[0, 1].set_title('Delay (95% CI)')
        axes[0, 1].set_ylabel('Delay (ms)')
        
        sns.barplot(data=df_success, x='protocol', y='avg_throughput', ax=axes[1, 0], ci=95)
        axes[1, 0].set_title('Throughput (95% CI)')
        axes[1, 0].set_ylabel('Throughput (Mbps)')
        
        if 'routing_overhead' in df_success.columns:
            sns.barplot(data=df_success, x='protocol', y='routing_overhead', ax=axes[1, 1], ci=95)
            axes[1, 1].set_title('Routing Overhead (95% CI)')
            axes[1, 1].set_ylabel('Overhead')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "comparison_summary.png", dpi=300)
        plt.close()
        
        print(f"✅ Gráficos guardados en: {self.output_dir}")
    
    def generate_latex_table(self, stats_df: pd.DataFrame):
        """Genera tabla en formato LaTeX para paper"""
        print("\n📝 Generando tabla LaTeX...")
        
        latex_file = self.output_dir / "results_table.tex"
        
        with open(latex_file, 'w') as f:
            f.write("\\begin{table}[htbp]\n")
            f.write("\\centering\n")
            f.write("\\caption{Resultados de Simulación por Protocolo}\n")
            f.write("\\label{tab:results}\n")
            f.write("\\begin{tabular}{lcccc}\n")
            f.write("\\hline\n")
            f.write("Protocolo & PDR (\\%) & Delay (ms) & Throughput (Mbps) & n \\\\\n")
            f.write("\\hline\n")
            
            for _, row in stats_df.iterrows():
                f.write(f"{row['protocol']} & ")
                f.write(f"{row['pdr_mean']:.2f} $\\pm$ {row['pdr_std']:.2f} & ")
                f.write(f"{row['delay_mean']:.2f} $\\pm$ {row['delay_std']:.2f} & ")
                f.write(f"{row['throughput_mean']:.2f} $\\pm$ {row['throughput_std']:.2f} & ")
                f.write(f"{int(row['n'])} \\\\\n")
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n")
        
        print(f"✅ Tabla LaTeX guardada en: {latex_file}")
    
    def run_full_analysis(self):
        """Ejecuta análisis completo"""
        print("\n" + "="*60)
        print("🚀 ANÁLISIS ESTADÍSTICO COMPLETO")
        print("="*60)
        
        # 1. Estadísticas descriptivas
        stats_df = self.descriptive_statistics()
        
        # 2. Comparación de protocolos
        comparison = self.compare_protocols()
        
        # 3. Gráficos
        self.generate_plots()
        
        # 4. Tabla LaTeX
        self.generate_latex_table(stats_df)
        
        print("\n" + "="*60)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*60)
        print(f"📁 Resultados en: {self.output_dir}")
        print("="*60)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analizador estadístico de experimentos')
    parser.add_argument('results_file', help='Archivo CSV con resultados')
    
    args = parser.parse_args()
    
    try:
        analyzer = StatisticalAnalyzer(args.results_file)
        analyzer.run_full_analysis()
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
