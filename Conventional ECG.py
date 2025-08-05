import numpy as np
from typing import Dict, List, Union
import json

class CardiacDiagnosis:
    def __init__(self):
        # Threshold constants
        self.ST_ELEV_THRESHOLDS = {
            'limb': 0.1,  # mV (I, II, III, aVR, aVL, aVF)
            'precordial': 0.2,  # mV (V1-V6)
        }
        self.QRS_DURATION_THRESHOLDS = {
            'normal': 110,
            'partial_block': 120,
            'complete_block': 150
        }
        self.HR_THRESHOLDS = {
            'bradycardia': 60,
            'tachycardia': 100
        }

    def analyze_st_segment(self, st_levels: Dict[str, float]) -> Dict:
        regions = {
            'Anterior': ['V1', 'V2', 'V3', 'V4'],
            'Inferior': ['II', 'III', 'aVF'],
            'Lateral': ['I', 'aVL', 'V5', 'V6'],
            'Posterior': ['V7', 'V8', 'V9'],
        }
        elevated_leads = []
        st_depression = False
        for lead, value in st_levels.items():
            threshold = self.ST_ELEV_THRESHOLDS['precordial'] if lead.startswith('V') else self.ST_ELEV_THRESHOLDS['limb']
            if value > threshold:
                elevated_leads.append(lead)
            elif value < -0.05:
                st_depression = True
        localization = None
        for region, leads in regions.items():
            region_elev = [lead for lead in leads if lead in elevated_leads]
            if len(region_elev) >= 2:
                localization = {
                    'region': region,
                    'leads': region_elev,
                    'max_st_elev': max(st_levels[lead] for lead in region_elev)
                }
                break
        return {
            'st_elevation': bool(localization),
            'localization': localization,
            'st_depression': st_depression
        }

    def diagnose_blocks(self,
                        qrs_duration: float,
                        qrs_voltages: Dict[str, float]) -> Union[str, None]:
        """Diagnose bundle branch blocks using net QRS voltage in V1/V2"""
        if qrs_duration < self.QRS_DURATION_THRESHOLDS['partial_block']:
            return None
        net_sum = qrs_voltages.get('V1', 0) + qrs_voltages.get('V2', 0)
        rbbb = (
            qrs_duration >= self.QRS_DURATION_THRESHOLDS['partial_block'] and
            net_sum > 0
        )
        lbbb = (
            qrs_duration >= self.QRS_DURATION_THRESHOLDS['complete_block'] and
            net_sum < 0
        )
        if rbbb:
            return 'RBBB'
        elif lbbb:
            return 'LBBB'
        elif qrs_duration >= self.QRS_DURATION_THRESHOLDS['partial_block']:
            return 'IVCD'
        return None

    def analyze_av_conduction(self, p_wave_count: int, qrs_count: int,
                               pr_intervals: List[float]) -> Dict:
        beat_diff = p_wave_count - qrs_count
        result = {
            'p_waves': p_wave_count,
            'qrs_complexes': qrs_count,
            'missing_beats': max(0, beat_diff),
            'classification': 'Normal conduction'
        }
        if beat_diff > 0:
            if len(pr_intervals) >= 3:
                pr_deltas = np.diff(pr_intervals)
                if all(d > 0 for d in pr_deltas[:-1]) and pr_intervals[-1] < pr_intervals[0]:
                    result.update({
                        'classification': 'Mobitz I (Wenckebach)',
                        'pattern': f"{len(pr_intervals)+1}:{len(pr_intervals)}",
                        'pr_progression': [f"{x}ms" for x in pr_intervals]
                    })
                    return result
            if len(pr_intervals) >= 2 and np.std(pr_intervals) < 5:
                result.update({
                    'classification': 'Mobitz II',
                    'pattern': f"{beat_diff+1}:1",
                    'pr_variation': f"{np.std(pr_intervals):.1f}ms"
                })
                return result
            if beat_diff >= 2:
                result['classification'] = 'High-grade AV block'
                if beat_diff >= 3 and all(pr < 120 or pr > 240 for pr in pr_intervals):
                    result.update({
                        'classification': '3rd degree AV block',
                        'atrial_rate': p_wave_count,
                        'ventricular_rate': qrs_count
                    })
        return result

    def diagnose_hypertrophy(self, qrs_voltages: Dict[str, float]) -> Union[str, None]:
        cornell = (qrs_voltages.get('aVL', 0) + qrs_voltages.get('V3', 0)) > 2.8 or \
                  (qrs_voltages.get('aVL', 0) + qrs_voltages.get('V3', 0)) > 2.0
        sokolow = (qrs_voltages.get('V1', 0) + max(qrs_voltages.get('V5', 0), qrs_voltages.get('V6', 0))) > 3.5
        if cornell or sokolow:
            return 'LVH'
        elif qrs_voltages.get('V1', 0) > 0.7 and qrs_voltages.get('V6', 0) < 0.3:
            return 'RVH'
        return None

    def analyze_rhythm(self, hr: float, rr_intervals: List[float],
                      p_wave_presence: bool) -> str:
        rr_var = np.std(rr_intervals) if len(rr_intervals) > 1 else 0
        if hr < self.HR_THRESHOLDS['bradycardia']:
            if not p_wave_presence:
                return 'Junctional bradycardia'
            elif rr_var > 100:
                return 'Sinus arrhythmia'
            return 'Sinus bradycardia'
        elif hr > self.HR_THRESHOLDS['tachycardia']:
            if rr_var > 50:
                return 'Atrial fibrillation'
            elif p_wave_presence:
                return 'Sinus tachycardia'
            return 'SVT'
        if 60 <= hr <= 100 and rr_var < 30 and p_wave_presence:
            return 'Normal sinus rhythm'
        return 'Unclassified rhythm'

    def full_analysis(self, ecg_parameters: Dict) -> Dict:
        results = {}
        results['st_analysis'] = self.analyze_st_segment(ecg_parameters['st_levels'])
        if 'p_wave_count' in ecg_parameters:
            results['av_conduction'] = self.analyze_av_conduction(
                ecg_parameters['p_wave_count'],
                ecg_parameters['qrs_count'],
                ecg_parameters['pr_intervals']
            )
        block_dx = self.diagnose_blocks(
            ecg_parameters['qrs_duration'],
            ecg_parameters['qrs_voltages']
        )
        if block_dx:
            results['conduction_abnormality'] = block_dx
        hypertrophy = self.diagnose_hypertrophy(ecg_parameters['qrs_voltages'])
        if hypertrophy:
            results['hypertrophy'] = hypertrophy
        results['rhythm'] = self.analyze_rhythm(
            ecg_parameters['heart_rate'],
            ecg_parameters['rr_intervals'],
            ecg_parameters.get('p_wave_presence', True)
        )
        return results


# Example Usage
if __name__ == "__main__":
    analyzer = CardiacDiagnosis()

    # RBBB example
    ecg_rbbb = { 'qrs_duration': 130, 'qrs_voltages': {'V1': 0.8, 'V2': 0.5} }
    print("RBBB Test:", analyzer.diagnose_blocks(ecg_rbbb['qrs_duration'], ecg_rbbb['qrs_voltages']))

    # LBBB example
    ecg_lbbb = { 'qrs_duration': 160, 'qrs_voltages': {'V1': -0.6, 'V2': -0.7} }
    print("LBBB Test:", analyzer.diagnose_blocks(ecg_lbbb['qrs_duration'], ecg_lbbb['qrs_voltages']))

    # Full ECG Analysis example
    sample_ecg = {
        'heart_rate': 75,
        'rr_intervals': [800, 805, 810, 800],
        'p_wave_count': 4,
        'qrs_count': 4,
        'pr_intervals': [160, 165, 162, 168],
        'qrs_duration': 130,
        'st_levels': {'V1': 0.1, 'V2': 0.15, 'V3': 0.05, 'II': 0.08, 'III': 0.1},
        'qrs_voltages': {'V1': 0.8, 'V2': 0.5, 'V5': 2.0, 'V6': 2.1},
        'p_wave_presence': True
    }
    result = analyzer.full_analysis(sample_ecg)
    print("\nFull Analysis:\n", json.dumps(result, indent=2))
