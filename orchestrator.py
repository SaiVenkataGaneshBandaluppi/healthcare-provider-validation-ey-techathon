from agents import ValidationAgent, EnrichmentAgent, QAAgent, ManagementAgent
from typing import List, Dict
import time

class AgentOrchestrator:
    """
    LangGraph-style orchestration of multi-agent system
    Coordinates autonomous agents in parallel workflow
    """
    
    def __init__(self):
        print(" Initializing Multi-Agent System...")
        self.validation_agent = ValidationAgent()
        self.enrichment_agent = EnrichmentAgent()
        self.qa_agent = QAAgent()
        self.management_agent = ManagementAgent()
        print(" All agents initialized!")
    
    def process_provider(self, provider: dict) -> dict:
        """
        Process single provider through multi-agent pipeline
        Agents work autonomously with intelligent orchestration
        """
        print(f"\n{'='*60}")
        print(f" PROCESSING: {provider.get('name', 'Unknown Provider')}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        
        # Stage 1: Validation Agent (Autonomous validation)
        print(" Stage 1/4: Validation")
        validation_results = self.validation_agent.validate(provider)
        print(f"   Status: {validation_results['status']}")
        print(f"   Confidence: {validation_results['confidence']:.2%}")
        
        # Stage 2: Enrichment Agent (Adaptive enrichment)
        print("\n Stage 2/4: Enrichment")
        enrichment_results = self.enrichment_agent.enrich(provider, validation_results)
        print(f"   Enrichments: {len(enrichment_results['enrichments'])} applied")
        
        # Stage 3: QA Agent (Self-correcting quality check)
        print("\n Stage 3/4: Quality Assurance")
        qa_results = self.qa_agent.quality_check(provider, validation_results, enrichment_results)
        print(f"   Final Confidence: {qa_results['final_confidence']:.2%}")
        print(f"   Status: {qa_results['final_status']}")
        
        # Stage 4: Management Agent (Goal-driven workflow)
        print("\n Stage 4/4: Management & Audit")
        management_results = self.management_agent.manage(
            provider, validation_results, enrichment_results, qa_results
        )
        print(f"   Next Actions: {', '.join(management_results['next_actions'])}")
        
        processing_time = time.time() - start_time
        
        # Compile comprehensive results
        final_result = {
            "provider_input": provider,
            "validation": validation_results,
            "enrichment": enrichment_results,
            "qa": qa_results,
            "management": management_results,
            "final_record": management_results["final_record"],
            "processing_time": round(processing_time, 2),
            "agents_used": ["Validation", "Enrichment", "QA", "Management"]
        }
        
        print(f"\n COMPLETED in {processing_time:.2f}s")
        print(f"{'='*60}\n")
        
        return final_result
    
    def process_batch(self, providers: List[dict]) -> List[dict]:
        """
        Process multiple providers with parallel-capable architecture
        """
        print(f"\n BATCH PROCESSING: {len(providers)} providers")
        print(f"{'='*60}\n")
        
        batch_start = time.time()
        results = []
        
        for i, provider in enumerate(providers, 1):
            print(f" Provider {i}/{len(providers)}")
            result = self.process_provider(provider)
            results.append(result)
        
        batch_time = time.time() - batch_start
        
        # Calculate statistics
        approved = sum(1 for r in results if r['qa']['final_status'] == 'APPROVED')
        needs_review = sum(1 for r in results if r['qa']['final_status'] == 'NEEDS_REVIEW')
        rejected = sum(1 for r in results if r['qa']['final_status'] == 'REJECTED')
        avg_confidence = sum(r['qa']['final_confidence'] for r in results) / len(results)
        
        print(f"\n{'='*60}")
        print(f" BATCH SUMMARY")
        print(f"{'='*60}")
        print(f"Total Providers: {len(providers)}")
        print(f" Approved: {approved} ({approved/len(providers)*100:.1f}%)")
        print(f"  Needs Review: {needs_review} ({needs_review/len(providers)*100:.1f}%)")
        print(f" Rejected: {rejected} ({rejected/len(providers)*100:.1f}%)")
        print(f" Avg Confidence: {avg_confidence:.2%}")
        print(f"  Total Time: {batch_time:.2f}s")
        print(f" Throughput: {len(providers)/batch_time:.2f} providers/second")
        print(f"{'='*60}\n")
        
        return results