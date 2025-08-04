import numpy as np
from typing import Dict, List, Union

class CardiacDiagnosis:
    def __init__(self):
        # Threshold constants
        self.ST_ELEV_THRESHOLDS = {
            'limb': 0.1,  # mV (I, II, III, aVR, aVL, aVF)
            'precordial': 0.2,  # mV (V1-V6)
            #'posterior': 0.05   # mV (V7-V9)
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
        """Analyze ST segment elevation/depression with localization"""
        regions = {
            'Anterior': ['V1', 'V2', 'V3', 'V4'],
            'Inferior': ['II', 'III', 'aVF'],
            'Lateral': ['I', 'aVL', 'V5', 'V6'],
            'Posterior': ['V7', 'V8', 'V9'],
            #'Right Ventricular': ['V1', 'V4R']
        }
        
        elevated_leads = []
        st_depression = False
        
        for lead, value in st_levels.items():
            threshold = self.ST_ELEV_THRESHOLDS['precordial'] if lead.startswith('V') else self.ST_ELEV_THRESHOLDS['limb']
            if value > threshold:
                elevated_leads.append(lead)
            elif value < -0.05:
                st_depression = True
                
        # Localize ST elevation
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

    def diagnose_blocks(self, qrs_duration: float, qrs_morphology: Dict[str, str]) -> str:
        """Diagnose bundle branch blocks with precise criteria"""
        if qrs_duration < self.QRS_DURATION_THRESHOLDS['partial_block']:
            return None
        # TODO: Here we just consider positive and negative wave in V1, if V1 is + : RBBB , and if V1 is - : LBBB
        # RBBB criteria
        rbbb = (
            qrs_morphology.get('V1', '') == 'rsR_prime' and
            qrs_morphology.get('V6', '') == 'wide_S' and
            qrs_duration >= self.QRS_DURATION_THRESHOLDS['partial_block']
        )
        
        # LBBB criteria
        lbbb = (
            qrs_morphology.get('V1', '') == 'QS' and
            qrs_morphology.get('V6', '') == 'monophasic_R' and
            qrs_duration >= self.QRS_DURATION_THRESHOLDS['complete_block']
        )
        
        if rbbb:
            return 'RBBB'
        elif lbbb:
            return 'LBBB'
        elif qrs_duration >= self.QRS_DURATION_THRESHOLDS['partial_block']:
            return 'IVCD'  # Non-specific intraventricular conduction delay
        return None

    def analyze_av_conduction(self, p_wave_count: int, qrs_count: int, 
                            pr_intervals: List[float]) -> Dict:
        """Analyze AV conduction abnormalities with beat-to-beat precision"""
        beat_diff = p_wave_count - qrs_count
        result = {
            'p_waves': p_wave_count,
            'qrs_complexes': qrs_count,
            'missing_beats': max(0, beat_diff),
            'classification': 'Normal conduction'
        }
        
        if beat_diff > 0:
            # Mobitz I (Wenckebach)
            if len(pr_intervals) >= 3:
                pr_deltas = np.diff(pr_intervals)
                if all(d > 0 for d in pr_deltas[:-1]) and pr_intervals[-1] < pr_intervals[0]:
                    result.update({
                        'classification': 'Mobitz I (Wenckebach)',
                        'pattern': f"{len(pr_intervals)+1}:{len(pr_intervals)}",
                        'pr_progression': [f"{x}ms" for x in pr_intervals]
                    })
                    return result
                    
            # Mobitz II
            if len(pr_intervals) >= 2 and np.std(pr_intervals) < 5:
                result.update({
                    'classification': 'Mobitz II',
                    'pattern': f"{beat_diff+1}:1",
                    'pr_variation': f"{np.std(pr_intervals):.1f}ms"
                })
                return result
                
            # High-grade/Complete block
            if beat_diff >= 2:
                result['classification'] = 'High-grade AV block'
                if beat_diff >= 3 and all(pr < 120 or pr > 240 for pr in pr_intervals):
                    result.update({
                        'classification': '3rd degree AV block',
                        'atrial_rate': p_wave_count,
                        'ventricular_rate': qrs_count
                    })
        return result

    def diagnose_hypertrophy(self, qrs_voltages: Dict[str, float]) -> str:
        """Diagnose ventricular hypertrophy with voltage criteria"""
        # Cornell criteria
        cornell = (qrs_voltages.get('aVL', 0) + qrs_voltages.get('V3', 0)) > 2.8  # Male
        cornell = cornell or (qrs_voltages.get('aVL', 0) + qrs_voltages.get('V3', 0)) > 2.0  # Female
        
        # Sokolow-Lyon
        sv1 = qrs_voltages.get('V1', 0)
        rv5 = qrs_voltages.get('V5', 0)
        rv6 = qrs_voltages.get('V6', 0)
        sokolow = (sv1 + max(rv5, rv6)) > 3.5
        
        if cornell or sokolow:
            return 'LVH'
        elif qrs_voltages.get('V1', 0) > 0.7 and qrs_voltages.get('V6', 0) < 0.3:
            return 'RVH'
        return None

    def analyze_rhythm(self, hr: float, rr_intervals: List[float], 
                      p_wave_presence: bool) -> str:
        """Analyze cardiac rhythm with precise rate and regularity"""
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
        """Complete ECG analysis integrating all components"""
        results = {}
        
        # ST Segment Analysis
        st_results = self.analyze_st_segment(ecg_parameters['st_levels'])
        results.update({'st_analysis': st_results})
        
        # Conduction Abnormalities
        if 'p_wave_count' in ecg_parameters:
            av_results = self.analyze_av_conduction(
                ecg_parameters['p_wave_count'],
                ecg_parameters['qrs_count'],
                ecg_parameters['pr_intervals']
            )
            results.update({'av_conduction': av_results})
        
        # Bundle Branch Blocks
        block_dx = self.diagnose_blocks(
            ecg_parameters['qrs_duration'],
            ecg_parameters['qrs_morphology']
        )
        if block_dx:
            results.update({'conduction_abnormality': block_dx})
        
        # Hypertrophy
        hypertrophy = self.diagnose_hypertrophy(ecg_parameters['qrs_voltages'])
        if hypertrophy:
            results.update({'hypertrophy': hypertrophy})
        
        # Rhythm Analysis
        rhythm = self.analyze_rhythm(
            ecg_parameters['heart_rate'],
            ecg_parameters['rr_intervals'],
            ecg_parameters.get('p_wave_presence', True)
        )
        results.update({'rhythm': rhythm})
        
        return results


# Example Usage
if __name__ == "__main__":
    analyzer = CardiacDiagnosis()
    
    sample_ecg = {
        'heart_rate': 75, # lead II
        'rr_intervals': [800, 810, 805, 800], # usually lead II
        'p_wave_count': 5, # usually lead II
        'qrs_count': 5, # usually lead II
        'pr_intervals': [160, 165, 158, 170], # usually lead II
        'qrs_duration': 115, # usually lead II, it can be a list of durations too, now it is average
        'st_levels': {
            'I': 0.05, 'II': 0.1, 'III': 0.08,
            'aVR': -0.1, 'aVL': 0.05, 'aVF': 0.1,
            'V1': 0.3, 'V2': 0.4, 'V3': 0.35,
            'V4': 0.2, 'V5': 0.1, 'V6': 0.05
        },
        'qrs_voltages': { # vector calculation
            'I': 0.5, 'II': 1.2, 'III': 0.8,
            'aVR': 0.3, 'aVL': 0.6, 'aVF': 1.0,
            'V1': 0.7, 'V2': 1.5, 'V3': 1.8,
            'V4': 2.0, 'V5': 2.5, 'V6': 2.2
        },
        'qrs_morphology': { #TODO: it should be corrected
            'V1': 'rS',
            'V6': 'qR'
        },
        'p_wave_presence': True
    }
    
    diagnosis = analyzer.full_analysis(sample_ecg)
    print("Complete ECG Analysis:")
    print(json.dumps(diagnosis, indent=2))
