#!/usr/bin/env python3
"""
Database Verification - Check if dynamic test data was stored correctly
"""

import requests
import json
from datetime import datetime

def verify_database_integration():
    """Verify that dynamic test data was stored in database"""
    
    gateway_url = "https://bhiv-hr-gateway-46pz.onrender.com"
    api_key = "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": api_key}
    
    print("DATABASE INTEGRATION VERIFICATION")
    print("=" * 50)
    
    verification_results = {}
    
    # Load test report to get created data IDs
    try:
        with open('test_report_3a9c011b.json', 'r') as f:
            test_report = json.load(f)
        created_data = test_report['created_data']
        print(f"Test Session: {test_report['test_session_id']}")
        print(f"Test Time: {test_report['timestamp']}")
        print()
    except FileNotFoundError:
        print("Test report not found. Running verification with general queries.")
        created_data = {'jobs': [], 'candidates': [], 'feedback': [], 'interviews': [], 'offers': []}
    
    # 1. Verify Jobs
    print("1. VERIFYING JOBS:")
    try:
        response = requests.get(f"{gateway_url}/v1/jobs", headers=headers, timeout=10)
        if response.status_code == 200:
            jobs_data = response.json()
            total_jobs = len(jobs_data.get('jobs', []))
            
            # Look for dynamic test jobs
            dynamic_jobs = [job for job in jobs_data.get('jobs', []) 
                          if 'DynamicTest_' in job.get('title', '')]
            
            verification_results['jobs'] = {
                'total_jobs': total_jobs,
                'dynamic_test_jobs': len(dynamic_jobs),
                'status': 'VERIFIED' if dynamic_jobs else 'NO_DYNAMIC_DATA',
                'sample_dynamic_job': dynamic_jobs[0] if dynamic_jobs else None
            }
            
            print(f"  Total Jobs in DB: {total_jobs}")
            print(f"  Dynamic Test Jobs: {len(dynamic_jobs)}")
            print(f"  Status: {'✓ VERIFIED' if dynamic_jobs else '- NO DYNAMIC DATA'}")
            
        else:
            verification_results['jobs'] = {'status': 'ERROR', 'code': response.status_code}
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        verification_results['jobs'] = {'status': 'ERROR', 'error': str(e)}
        print(f"  ERROR: {str(e)[:50]}")
    
    # 2. Verify Candidates
    print("\n2. VERIFYING CANDIDATES:")
    try:
        response = requests.get(f"{gateway_url}/v1/candidates?limit=100", headers=headers, timeout=10)
        if response.status_code == 200:
            candidates_data = response.json()
            total_candidates = candidates_data.get('total', 0)
            candidates_list = candidates_data.get('candidates', [])
            
            # Look for dynamic test candidates
            dynamic_candidates = [cand for cand in candidates_list 
                                if 'TestCandidate_' in cand.get('name', '') or 
                                   'dynamictest.com' in cand.get('email', '')]
            
            verification_results['candidates'] = {
                'total_candidates': total_candidates,
                'dynamic_test_candidates': len(dynamic_candidates),
                'status': 'VERIFIED' if dynamic_candidates else 'NO_DYNAMIC_DATA',
                'sample_dynamic_candidate': dynamic_candidates[0] if dynamic_candidates else None
            }
            
            print(f"  Total Candidates in DB: {total_candidates}")
            print(f"  Dynamic Test Candidates: {len(dynamic_candidates)}")
            print(f"  Status: {'✓ VERIFIED' if dynamic_candidates else '- NO DYNAMIC DATA'}")
            
        else:
            verification_results['candidates'] = {'status': 'ERROR', 'code': response.status_code}
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        verification_results['candidates'] = {'status': 'ERROR', 'error': str(e)}
        print(f"  ERROR: {str(e)[:50]}")
    
    # 3. Verify Feedback
    print("\n3. VERIFYING FEEDBACK:")
    try:
        response = requests.get(f"{gateway_url}/v1/feedback", headers=headers, timeout=10)
        if response.status_code == 200:
            feedback_data = response.json()
            total_feedback = len(feedback_data.get('feedback', []))
            
            # Look for dynamic test feedback
            dynamic_feedback = [fb for fb in feedback_data.get('feedback', []) 
                              if fb.get('comments') and 'Dynamic test feedback' in fb.get('comments', '')]
            
            verification_results['feedback'] = {
                'total_feedback': total_feedback,
                'dynamic_test_feedback': len(dynamic_feedback),
                'status': 'VERIFIED' if dynamic_feedback else 'NO_DYNAMIC_DATA',
                'sample_dynamic_feedback': dynamic_feedback[0] if dynamic_feedback else None
            }
            
            print(f"  Total Feedback in DB: {total_feedback}")
            print(f"  Dynamic Test Feedback: {len(dynamic_feedback)}")
            print(f"  Status: {'✓ VERIFIED' if dynamic_feedback else '- NO DYNAMIC DATA'}")
            
        else:
            verification_results['feedback'] = {'status': 'ERROR', 'code': response.status_code}
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        verification_results['feedback'] = {'status': 'ERROR', 'error': str(e)}
        print(f"  ERROR: {str(e)[:50]}")
    
    # 4. Verify Interviews
    print("\n4. VERIFYING INTERVIEWS:")
    try:
        response = requests.get(f"{gateway_url}/v1/interviews", headers=headers, timeout=10)
        if response.status_code == 200:
            interviews_data = response.json()
            total_interviews = len(interviews_data.get('interviews', []))
            
            # Look for dynamic test interviews
            dynamic_interviews = [iv for iv in interviews_data.get('interviews', []) 
                                if 'DynamicTester_' in str(iv.get('interviewer', '')) or
                                   'Dynamic test interview' in str(iv.get('notes', ''))]
            
            verification_results['interviews'] = {
                'total_interviews': total_interviews,
                'dynamic_test_interviews': len(dynamic_interviews),
                'status': 'VERIFIED' if dynamic_interviews else 'NO_DYNAMIC_DATA',
                'sample_dynamic_interview': dynamic_interviews[0] if dynamic_interviews else None
            }
            
            print(f"  Total Interviews in DB: {total_interviews}")
            print(f"  Dynamic Test Interviews: {len(dynamic_interviews)}")
            print(f"  Status: {'✓ VERIFIED' if dynamic_interviews else '- NO DYNAMIC DATA'}")
            
        else:
            verification_results['interviews'] = {'status': 'ERROR', 'code': response.status_code}
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        verification_results['interviews'] = {'status': 'ERROR', 'error': str(e)}
        print(f"  ERROR: {str(e)[:50]}")
    
    # 5. Verify Offers
    print("\n5. VERIFYING OFFERS:")
    try:
        response = requests.get(f"{gateway_url}/v1/offers", headers=headers, timeout=10)
        if response.status_code == 200:
            offers_data = response.json()
            total_offers = len(offers_data.get('offers', []))
            
            # Look for dynamic test offers
            dynamic_offers = [offer for offer in offers_data.get('offers', []) 
                            if 'Dynamic test offer' in str(offer.get('terms', ''))]
            
            verification_results['offers'] = {
                'total_offers': total_offers,
                'dynamic_test_offers': len(dynamic_offers),
                'status': 'VERIFIED' if dynamic_offers else 'NO_DYNAMIC_DATA',
                'sample_dynamic_offer': dynamic_offers[0] if dynamic_offers else None
            }
            
            print(f"  Total Offers in DB: {total_offers}")
            print(f"  Dynamic Test Offers: {len(dynamic_offers)}")
            print(f"  Status: {'✓ VERIFIED' if dynamic_offers else '- NO DYNAMIC DATA'}")
            
        else:
            verification_results['offers'] = {'status': 'ERROR', 'code': response.status_code}
            print(f"  ERROR: {response.status_code}")
    except Exception as e:
        verification_results['offers'] = {'status': 'ERROR', 'error': str(e)}
        print(f"  ERROR: {str(e)[:50]}")
    
    # Generate Summary
    print("\n" + "=" * 50)
    print("DATABASE VERIFICATION SUMMARY")
    print("=" * 50)
    
    verified_count = sum(1 for result in verification_results.values() 
                        if result.get('status') == 'VERIFIED')
    total_checks = len(verification_results)
    
    print(f"Database Integration Checks: {verified_count}/{total_checks}")
    print(f"Success Rate: {(verified_count/total_checks)*100:.1f}%")
    
    # Detailed status
    for entity, result in verification_results.items():
        status = result.get('status', 'UNKNOWN')
        if status == 'VERIFIED':
            print(f"✓ {entity.upper()}: Data successfully stored and retrieved")
        elif status == 'NO_DYNAMIC_DATA':
            print(f"- {entity.upper()}: No dynamic test data found (may be expected)")
        else:
            print(f"✗ {entity.upper()}: Error - {result.get('error', result.get('code', 'Unknown'))}")
    
    # Save verification report
    verification_report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'verified_count': verified_count,
            'total_checks': total_checks,
            'success_rate': (verified_count/total_checks)*100
        },
        'detailed_results': verification_results
    }
    
    with open('database_verification_report.json', 'w') as f:
        json.dump(verification_report, f, indent=2)
    
    print(f"\nDetailed verification report saved: database_verification_report.json")
    
    return verification_report

if __name__ == "__main__":
    verify_database_integration()