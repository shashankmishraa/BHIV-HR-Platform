#!/usr/bin/env python3
"""
AI Model validation and bias detection for BHIV HR Platform
"""

import json
import logging
from typing import Dict, List, Tuple
from datetime import datetime, timezone
import statistics

logger = logging.getLogger(__name__)

class AIModelValidator:
    """AI model performance validation and bias detection"""
    
    def __init__(self):
        self.validation_history = []
        self.bias_thresholds = {
            'gender_bias': 0.1,  # Max 10% difference
            'age_bias': 0.15,    # Max 15% difference
            'location_bias': 0.2  # Max 20% difference
        }
    
    def validate_matching_accuracy(self, predictions: List[Dict], ground_truth: List[Dict]) -> Dict:
        """Validate AI matching accuracy against ground truth"""
        if len(predictions) != len(ground_truth):
            raise ValueError("Predictions and ground truth must have same length")
        
        correct_predictions = 0
        score_differences = []
        
        for pred, truth in zip(predictions, ground_truth):
            # Check if top candidate matches
            if pred.get('top_candidate_id') == truth.get('hired_candidate_id'):
                correct_predictions += 1
            
            # Calculate score difference
            pred_score = pred.get('ai_score', 0)
            truth_score = truth.get('actual_performance', 0)
            score_differences.append(abs(pred_score - truth_score))
        
        accuracy = correct_predictions / len(predictions)
        avg_score_error = statistics.mean(score_differences) if score_differences else 0
        
        return {
            'accuracy': accuracy,
            'precision': accuracy,  # Simplified for this context
            'avg_score_error': avg_score_error,
            'total_predictions': len(predictions),
            'correct_predictions': correct_predictions
        }
    
    def detect_bias(self, candidates: List[Dict], scores: List[float]) -> Dict:
        """Detect potential bias in AI scoring"""
        bias_report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_candidates': len(candidates),
            'bias_detected': False,
            'bias_details': {}
        }
        
        if len(candidates) != len(scores):
            raise ValueError("Candidates and scores must have same length")
        
        # Group by demographics
        groups = {
            'gender': {},
            'age_group': {},
            'location': {}
        }
        
        for candidate, score in zip(candidates, scores):
            # Gender analysis (if available)
            gender = candidate.get('gender', 'unknown')
            if gender not in groups['gender']:
                groups['gender'][gender] = []
            groups['gender'][gender].append(score)
            
            # Age group analysis
            age = candidate.get('age', 0)
            age_group = 'young' if age < 30 else 'middle' if age < 50 else 'senior'
            if age_group not in groups['age_group']:
                groups['age_group'][age_group] = []
            groups['age_group'][age_group].append(score)
            
            # Location analysis
            location = candidate.get('location', 'unknown')
            if location not in groups['location']:
                groups['location'][location] = []
            groups['location'][location].append(score)
        
        # Calculate bias metrics
        for category, group_data in groups.items():
            if len(group_data) < 2:
                continue
            
            group_averages = {}
            for group_name, group_scores in group_data.items():
                if len(group_scores) > 0:
                    group_averages[group_name] = statistics.mean(group_scores)
            
            if len(group_averages) >= 2:
                max_avg = max(group_averages.values())
                min_avg = min(group_averages.values())
                bias_ratio = (max_avg - min_avg) / max_avg if max_avg > 0 else 0
                
                threshold = self.bias_thresholds.get(f'{category}_bias', 0.1)
                
                bias_report['bias_details'][category] = {
                    'bias_ratio': bias_ratio,
                    'threshold': threshold,
                    'biased': bias_ratio > threshold,
                    'group_averages': group_averages
                }
                
                if bias_ratio > threshold:
                    bias_report['bias_detected'] = True
        
        return bias_report
    
    def validate_values_prediction(self, candidates: List[Dict]) -> Dict:
        """Validate values prediction consistency"""
        values_scores = []
        
        for candidate in candidates:
            values = candidate.get('values_prediction', {})
            if values:
                # Check if all values are within valid range (1-5)
                valid_values = all(1 <= v <= 5 for v in values.values() if isinstance(v, (int, float)))
                
                # Check for consistency (no extreme variations)
                if valid_values and len(values) >= 3:
                    scores = [v for v in values.values() if isinstance(v, (int, float))]
                    std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
                    
                    values_scores.append({
                        'candidate_id': candidate.get('id'),
                        'valid': valid_values,
                        'consistency': std_dev < 2.0,  # Standard deviation < 2
                        'std_dev': std_dev,
                        'values': values
                    })
        
        valid_predictions = sum(1 for v in values_scores if v['valid'])
        consistent_predictions = sum(1 for v in values_scores if v['consistency'])
        
        return {
            'total_candidates': len(values_scores),
            'valid_predictions': valid_predictions,
            'consistent_predictions': consistent_predictions,
            'validity_rate': valid_predictions / len(values_scores) if values_scores else 0,
            'consistency_rate': consistent_predictions / len(values_scores) if values_scores else 0
        }
    
    def generate_model_report(self, test_data: Dict) -> Dict:
        """Generate comprehensive model validation report"""
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'model_version': test_data.get('model_version', 'unknown'),
            'validation_results': {}
        }
        
        # Accuracy validation
        if 'predictions' in test_data and 'ground_truth' in test_data:
            accuracy_results = self.validate_matching_accuracy(
                test_data['predictions'], 
                test_data['ground_truth']
            )
            report['validation_results']['accuracy'] = accuracy_results
        
        # Bias detection
        if 'candidates' in test_data and 'scores' in test_data:
            bias_results = self.detect_bias(
                test_data['candidates'], 
                test_data['scores']
            )
            report['validation_results']['bias'] = bias_results
        
        # Values prediction validation
        if 'candidates' in test_data:
            values_results = self.validate_values_prediction(test_data['candidates'])
            report['validation_results']['values'] = values_results
        
        # Overall assessment
        report['overall_assessment'] = self._assess_model_quality(report['validation_results'])
        
        # Store in history
        self.validation_history.append(report)
        
        return report
    
    def _assess_model_quality(self, results: Dict) -> Dict:
        """Assess overall model quality"""
        assessment = {
            'quality_score': 0.0,
            'status': 'unknown',
            'recommendations': []
        }
        
        scores = []
        
        # Accuracy score
        if 'accuracy' in results:
            accuracy = results['accuracy'].get('accuracy', 0)
            scores.append(accuracy * 100)
            
            if accuracy < 0.7:
                assessment['recommendations'].append("Improve model accuracy through better training data")
        
        # Bias score (inverse - lower bias = higher score)
        if 'bias' in results:
            bias_detected = results['bias'].get('bias_detected', False)
            bias_score = 80 if not bias_detected else 40
            scores.append(bias_score)
            
            if bias_detected:
                assessment['recommendations'].append("Address detected bias in model predictions")
        
        # Values consistency score
        if 'values' in results:
            consistency_rate = results['values'].get('consistency_rate', 0)
            scores.append(consistency_rate * 100)
            
            if consistency_rate < 0.8:
                assessment['recommendations'].append("Improve values prediction consistency")
        
        # Calculate overall score
        if scores:
            assessment['quality_score'] = statistics.mean(scores)
            
            if assessment['quality_score'] >= 85:
                assessment['status'] = 'excellent'
            elif assessment['quality_score'] >= 70:
                assessment['status'] = 'good'
            elif assessment['quality_score'] >= 50:
                assessment['status'] = 'needs_improvement'
            else:
                assessment['status'] = 'poor'
        
        return assessment

def main():
    """Main validation function"""
    validator = AIModelValidator()
    
    # Sample test data
    test_data = {
        'model_version': 'v3.0.0-semantic',
        'candidates': [
            {'id': 1, 'gender': 'male', 'age': 28, 'location': 'Mumbai', 'values_prediction': {'integrity': 4, 'honesty': 5, 'discipline': 4}},
            {'id': 2, 'gender': 'female', 'age': 32, 'location': 'Bangalore', 'values_prediction': {'integrity': 5, 'honesty': 4, 'discipline': 5}},
            {'id': 3, 'gender': 'male', 'age': 45, 'location': 'Delhi', 'values_prediction': {'integrity': 3, 'honesty': 4, 'discipline': 4}}
        ],
        'scores': [85.5, 92.3, 78.1],
        'predictions': [
            {'top_candidate_id': 2, 'ai_score': 92.3},
            {'top_candidate_id': 1, 'ai_score': 85.5}
        ],
        'ground_truth': [
            {'hired_candidate_id': 2, 'actual_performance': 90.0},
            {'hired_candidate_id': 1, 'actual_performance': 88.0}
        ]
    }
    
    # Generate report
    report = validator.generate_model_report(test_data)
    
    # Display results
    print("AI Model Validation Report")
    print("=" * 50)
    print(f"Model Version: {report['model_version']}")
    print(f"Timestamp: {report['timestamp']}")
    print()
    
    # Overall assessment
    assessment = report['overall_assessment']
    print(f"Overall Quality Score: {assessment['quality_score']:.1f}/100")
    print(f"Status: {assessment['status'].upper()}")
    print()
    
    # Detailed results
    if 'accuracy' in report['validation_results']:
        acc = report['validation_results']['accuracy']
        print(f"Accuracy: {acc['accuracy']:.1%}")
        print(f"Average Score Error: {acc['avg_score_error']:.1f}")
    
    if 'bias' in report['validation_results']:
        bias = report['validation_results']['bias']
        print(f"Bias Detected: {'Yes' if bias['bias_detected'] else 'No'}")
    
    if 'values' in report['validation_results']:
        values = report['validation_results']['values']
        print(f"Values Consistency: {values['consistency_rate']:.1%}")
    
    # Recommendations
    if assessment['recommendations']:
        print("\nRecommendations:")
        for rec in assessment['recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    main()