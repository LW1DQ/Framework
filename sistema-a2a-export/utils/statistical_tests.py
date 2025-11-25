"""
Tests Estadísticos para Rigor Académico

Implementa tests de hipótesis y análisis estadístico avanzado
según feedback del director de tesis.
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import pandas as pd


def calculate_confidence_interval(data: np.ndarray, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Calcula intervalo de confianza para una muestra
    
    Args:
        data: Array de datos
        confidence: Nivel de confianza (default 0.95 para 95%)
        
    Returns:
        Tupla (límite_inferior, límite_superior)
    """
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    margin = std_err * stats.t.ppf((1 + confidence) / 2, n - 1)
    
    return (mean - margin, mean + margin)


def t_test_two_samples(sample1: np.ndarray, sample2: np.ndarray, 
                       alpha: float = 0.05) -> Dict:
    """
    Realiza T-Test para comparar dos muestras independientes
    
    Args:
        sample1: Primera muestra
        sample2: Segunda muestra
        alpha: Nivel de significancia (default 0.05)
        
    Returns:
        Diccionario con resultados del test
    """
    # T-test de dos muestras
    t_statistic, p_value = stats.ttest_ind(sample1, sample2)
    
    # Determinar si hay diferencia significativa
    is_significant = p_value < alpha
    
    # Calcular tamaño del efecto (Cohen's d)
    pooled_std = np.sqrt((np.std(sample1, ddof=1)**2 + np.std(sample2, ddof=1)**2) / 2)
    cohens_d = (np.mean(sample1) - np.mean(sample2)) / pooled_std if pooled_std > 0 else 0
    
    # Interpretar tamaño del efecto
    if abs(cohens_d) < 0.2:
        effect_size = "pequeño"
    elif abs(cohens_d) < 0.5:
        effect_size = "mediano"
    else:
        effect_size = "grande"
    
    return {
        't_statistic': float(t_statistic),
        'p_value': float(p_value),
        'is_significant': is_significant,
        'alpha': alpha,
        'cohens_d': float(cohens_d),
        'effect_size': effect_size,
        'sample1_mean': float(np.mean(sample1)),
        'sample2_mean': float(np.mean(sample2)),
        'sample1_std': float(np.std(sample1, ddof=1)),
        'sample2_std': float(np.std(sample2, ddof=1)),
        'interpretation': (
            f"Diferencia {'SIGNIFICATIVA' if is_significant else 'NO significativa'} "
            f"(p={p_value:.4f}, α={alpha}). "
            f"Tamaño del efecto: {effect_size} (d={cohens_d:.3f})"
        )
    }


def anova_test(samples: List[np.ndarray], group_names: List[str] = None,
               alpha: float = 0.05) -> Dict:
    """
    Realiza ANOVA para comparar múltiples grupos
    
    Args:
        samples: Lista de muestras (una por grupo)
        group_names: Nombres de los grupos (opcional)
        alpha: Nivel de significancia
        
    Returns:
        Diccionario con resultados del ANOVA
    """
    # ANOVA de una vía
    f_statistic, p_value = stats.f_oneway(*samples)
    
    # Determinar si hay diferencia significativa
    is_significant = p_value < alpha
    
    # Calcular estadísticas por grupo
    group_stats = []
    for i, sample in enumerate(samples):
        name = group_names[i] if group_names else f"Grupo {i+1}"
        group_stats.append({
            'name': name,
            'mean': float(np.mean(sample)),
            'std': float(np.std(sample, ddof=1)),
            'n': len(sample)
        })
    
    # Calcular eta cuadrado (tamaño del efecto)
    grand_mean = np.mean(np.concatenate(samples))
    ss_between = sum(len(s) * (np.mean(s) - grand_mean)**2 for s in samples)
    ss_total = sum((x - grand_mean)**2 for s in samples for x in s)
    eta_squared = ss_between / ss_total if ss_total > 0 else 0
    
    # Interpretar tamaño del efecto
    if eta_squared < 0.01:
        effect_size = "pequeño"
    elif eta_squared < 0.06:
        effect_size = "mediano"
    else:
        effect_size = "grande"
    
    return {
        'f_statistic': float(f_statistic),
        'p_value': float(p_value),
        'is_significant': is_significant,
        'alpha': alpha,
        'eta_squared': float(eta_squared),
        'effect_size': effect_size,
        'group_stats': group_stats,
        'interpretation': (
            f"Diferencia entre grupos {'SIGNIFICATIVA' if is_significant else 'NO significativa'} "
            f"(F={f_statistic:.3f}, p={p_value:.4f}, α={alpha}). "
            f"Tamaño del efecto: {effect_size} (η²={eta_squared:.3f})"
        )
    }


def paired_t_test(before: np.ndarray, after: np.ndarray, alpha: float = 0.05) -> Dict:
    """
    Realiza T-Test pareado (para medidas repetidas)
    
    Args:
        before: Mediciones antes de la intervención
        after: Mediciones después de la intervención
        alpha: Nivel de significancia
        
    Returns:
        Diccionario con resultados del test
    """
    # T-test pareado
    t_statistic, p_value = stats.ttest_rel(before, after)
    
    # Determinar si hay diferencia significativa
    is_significant = p_value < alpha
    
    # Calcular diferencia promedio
    diff = after - before
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    
    # Calcular tamaño del efecto (Cohen's d para muestras pareadas)
    cohens_d = mean_diff / std_diff if std_diff > 0 else 0
    
    # Interpretar tamaño del efecto
    if abs(cohens_d) < 0.2:
        effect_size = "pequeño"
    elif abs(cohens_d) < 0.5:
        effect_size = "mediano"
    else:
        effect_size = "grande"
    
    # Determinar dirección del cambio
    if mean_diff > 0:
        direction = "mejora"
    elif mean_diff < 0:
        direction = "empeoramiento"
    else:
        direction = "sin cambio"
    
    return {
        't_statistic': float(t_statistic),
        'p_value': float(p_value),
        'is_significant': is_significant,
        'alpha': alpha,
        'mean_difference': float(mean_diff),
        'std_difference': float(std_diff),
        'cohens_d': float(cohens_d),
        'effect_size': effect_size,
        'direction': direction,
        'before_mean': float(np.mean(before)),
        'after_mean': float(np.mean(after)),
        'interpretation': (
            f"{direction.capitalize()} {'SIGNIFICATIVA' if is_significant else 'NO significativa'} "
            f"(t={t_statistic:.3f}, p={p_value:.4f}, α={alpha}). "
            f"Diferencia promedio: {mean_diff:.3f}. "
            f"Tamaño del efecto: {effect_size} (d={cohens_d:.3f})"
        )
    }


def mann_whitney_u_test(sample1: np.ndarray, sample2: np.ndarray, 
                        alpha: float = 0.05) -> Dict:
    """
    Realiza test de Mann-Whitney U (alternativa no paramétrica al T-Test)
    
    Args:
        sample1: Primera muestra
        sample2: Segunda muestra
        alpha: Nivel de significancia
        
    Returns:
        Diccionario con resultados del test
    """
    # Mann-Whitney U test
    u_statistic, p_value = stats.mannwhitneyu(sample1, sample2, alternative='two-sided')
    
    # Determinar si hay diferencia significativa
    is_significant = p_value < alpha
    
    # Calcular tamaño del efecto (r = Z / sqrt(N))
    n1, n2 = len(sample1), len(sample2)
    z_score = stats.norm.ppf(1 - p_value/2)
    r = abs(z_score) / np.sqrt(n1 + n2)
    
    # Interpretar tamaño del efecto
    if r < 0.1:
        effect_size = "pequeño"
    elif r < 0.3:
        effect_size = "mediano"
    else:
        effect_size = "grande"
    
    return {
        'u_statistic': float(u_statistic),
        'p_value': float(p_value),
        'is_significant': is_significant,
        'alpha': alpha,
        'r': float(r),
        'effect_size': effect_size,
        'sample1_median': float(np.median(sample1)),
        'sample2_median': float(np.median(sample2)),
        'interpretation': (
            f"Diferencia {'SIGNIFICATIVA' if is_significant else 'NO significativa'} "
            f"(U={u_statistic:.1f}, p={p_value:.4f}, α={alpha}). "
            f"Tamaño del efecto: {effect_size} (r={r:.3f})"
        )
    }


def calculate_all_confidence_intervals(df: pd.DataFrame, 
                                       metrics: List[str],
                                       confidence: float = 0.95) -> Dict[str, Tuple[float, float]]:
    """
    Calcula intervalos de confianza para múltiples métricas
    
    Args:
        df: DataFrame con datos
        metrics: Lista de nombres de métricas
        confidence: Nivel de confianza
        
    Returns:
        Diccionario con intervalos de confianza por métrica
    """
    intervals = {}
    
    for metric in metrics:
        if metric in df.columns:
            data = df[metric].dropna().values
            if len(data) > 1:
                intervals[metric] = calculate_confidence_interval(data, confidence)
    
    return intervals


def generate_statistical_report(results: Dict) -> str:
    """
    Genera un reporte en texto de los resultados estadísticos
    
    Args:
        results: Diccionario con resultados de tests
        
    Returns:
        Reporte formateado en texto
    """
    report = []
    report.append("=" * 80)
    report.append("ANÁLISIS ESTADÍSTICO - RIGOR ACADÉMICO")
    report.append("=" * 80)
    report.append("")
    
    # T-Test
    if 't_test' in results:
        report.append("T-TEST (Comparación de dos muestras):")
        report.append("-" * 80)
        t = results['t_test']
        report.append(f"  Estadístico t: {t['t_statistic']:.4f}")
        report.append(f"  Valor p: {t['p_value']:.4f}")
        report.append(f"  Significativo: {'SÍ' if t['is_significant'] else 'NO'} (α={t['alpha']})")
        report.append(f"  Cohen's d: {t['cohens_d']:.3f} ({t['effect_size']})")
        report.append(f"  Interpretación: {t['interpretation']}")
        report.append("")
    
    # ANOVA
    if 'anova' in results:
        report.append("ANOVA (Comparación de múltiples grupos):")
        report.append("-" * 80)
        a = results['anova']
        report.append(f"  Estadístico F: {a['f_statistic']:.4f}")
        report.append(f"  Valor p: {a['p_value']:.4f}")
        report.append(f"  Significativo: {'SÍ' if a['is_significant'] else 'NO'} (α={a['alpha']})")
        report.append(f"  Eta cuadrado: {a['eta_squared']:.3f} ({a['effect_size']})")
        report.append(f"  Interpretación: {a['interpretation']}")
        report.append("")
        report.append("  Estadísticas por grupo:")
        for g in a['group_stats']:
            report.append(f"    {g['name']}: μ={g['mean']:.3f}, σ={g['std']:.3f}, n={g['n']}")
        report.append("")
    
    # Intervalos de confianza
    if 'confidence_intervals' in results:
        report.append("INTERVALOS DE CONFIANZA (95%):")
        report.append("-" * 80)
        for metric, (lower, upper) in results['confidence_intervals'].items():
            report.append(f"  {metric}: [{lower:.3f}, {upper:.3f}]")
        report.append("")
    
    report.append("=" * 80)
    
    return "\n".join(report)


if __name__ == "__main__":
    # Prueba de las funciones estadísticas
    print("Prueba de funciones estadísticas\n")
    
    # Generar datos de ejemplo
    np.random.seed(42)
    sample1 = np.random.normal(85, 10, 30)  # PDR protocolo 1
    sample2 = np.random.normal(90, 8, 30)   # PDR protocolo 2
    
    # T-Test
    print("T-TEST:")
    result = t_test_two_samples(sample1, sample2)
    print(result['interpretation'])
    print()
    
    # Intervalo de confianza
    print("INTERVALO DE CONFIANZA:")
    ci = calculate_confidence_interval(sample1)
    print(f"95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]")
    print()
    
    # ANOVA
    print("ANOVA:")
    sample3 = np.random.normal(88, 9, 30)   # PDR protocolo 3
    result = anova_test([sample1, sample2, sample3], ['AODV', 'OLSR', 'DSDV'])
    print(result['interpretation'])
