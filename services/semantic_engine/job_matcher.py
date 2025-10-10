class SemanticJobMatcher:
    """Fallback matcher - will be replaced with real AI in Phase 2"""
    def __init__(self):
        self.enabled = False
        print("INFO: Using fallback matcher (Phase 1)")
    
    def match_candidates(self, job_desc: str, candidates: list) -> list:
        """Placeholder for semantic matching"""
        return []