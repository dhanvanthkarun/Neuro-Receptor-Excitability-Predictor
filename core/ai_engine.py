import os
import json

class NeuroAIEngine:
    def __init__(self, provider="claude"):
        """
        Initializes the selected AI provider engine.
        Supported providers: 'claude' (Flagship) or 'openai' (Testing/Fallback)
        """
        self.provider = provider.lower().strip()
        
        if self.provider == "claude":
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                print("[NREP Warning] ANTHROPIC_API_KEY not detected in environment variables.")
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
            self.model = "claude-3-5-haiku-latest"
            
        elif self.provider == "openai":
            # Using OpenRouter gateway format for absolute free-tier testing flexibility
            self.api_key = os.environ.get("OPENROUTER_API_KEY")
            if not self.api_key:
                print("[NREP Warning] OPENROUTER_API_KEY not detected in environment variables.")
            from openai import OpenAI
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            ) if self.api_key else None
            self.model = "openrouter/free"
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def generate_excitability_report(self, structural_metrics, query="Analyze the neuro-evolutionary implications."):
        """
        Routes the structural metadata to the selected engine to perform circuit-level analysis.
        """
        if not self.client:
            raise ValueError(f"Client for '{self.provider}' is not initialized. Ensure your environment variables are exported.")
            
        metrics_json = json.dumps(structural_metrics, indent=2)
        
        system_prompt = (
            "You are an elite Computational Neurobiologist and Structural Bioinformatician. "
            "Analyze the provided protein structural metrics. Predict how this specific "
            "geometry, density, or potential binding pocket alterations might influence ion "
            "channel kinetics and overall neural circuit excitability. Provide a concise, "
            "highly rigorous scientific report."
        )
        
        user_prompt = f"Target Inquiry: {query}\n\nStructural Metrics:\n{metrics_json}"
        
        print(f"[NREP] Initiating connection to {self.model} via {self.provider.upper()}...")
        
        try:
            if self.provider == "claude":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text
                
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"{self.provider.upper()} Engine Execution Error: {e}")

# Test execution block to verify functionality locally
if __name__ == "__main__":
    mock_metrics = {
        "protein_id": "1AIE",
        "total_models": 1,
        "chains": [{"chain_id": "A", "residue_count": 31, "atom_count": 305}],
        "total_residues": 31,
        "total_atoms": 305
    }
    
    # 1. Let's test using the OpenRouter/OpenAI configuration first for free validation
    print("--- Initializing Free Testing Mode (OpenAI/OpenRouter) ---")
    try:
        engine = NeuroAIEngine(provider="openai")
        report = engine.generate_excitability_report(mock_metrics, query="Verify engine pipeline integration.")
        print("\n🔬 TEST REPORT:\n", report)
    except Exception as e:
        print(f"\n[Testing Mode Alert] Could not execute fallback automatically: {e}")
