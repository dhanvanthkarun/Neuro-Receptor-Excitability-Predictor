import warnings
from Bio.PDB import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning

class StructuralParser:
    def __init__(self):
        """
        Initializes the BioPython parser. 
        We suppress standard construction warnings because real-world crystal 
        structures often have minor missing atoms which we can safely ignore.
        """
        warnings.simplefilter('ignore', PDBConstructionWarning)
        self.parser = PDBParser(PERMISSIVE=1)

    def extract_metrics(self, filepath):
        """
        Parses a .pdb file and extracts key biophysical metrics for AI analysis.
        """
        print(f"[NREP] Parsing structure: {filepath}...")
        
        # Extract an ID from the filename (e.g., '1aie' from 'data/cache/1aie.pdb')
        structure_id = filepath.split('/')[-1].split('.')[0].upper()
        
        # Load the structure into BioPython's hierarchy
        structure = self.parser.get_structure(structure_id, filepath)
        
        metrics = {
            "protein_id": structure_id,
            "total_models": len(structure),
            "chains": [],
            "total_residues": 0,
            "total_atoms": 0,
        }

        # Iterate through the structural hierarchy to gather statistics
        for model in structure:
            for chain in model:
                chain_id = chain.get_id()
                # Filter out water molecules (HOH) and heteroatoms to focus on the protein
                residues = [res for res in chain.get_residues() if res.get_id()[0] == ' ']
                atoms = list(chain.get_atoms())
                
                metrics["chains"].append({
                    "chain_id": chain_id,
                    "residue_count": len(residues),
                    "atom_count": len(atoms)
                })
                
                metrics["total_residues"] += len(residues)
                metrics["total_atoms"] += len(atoms)
                
        print(f"[NREP] Extraction complete. Found {len(metrics['chains'])} chains and {metrics['total_atoms']} atoms.")
        return metrics

# Test execution block
if __name__ == "__main__":
    parser = StructuralParser()
    try:
        # Test with the file you just successfully downloaded
        target_file = "data/cache/1aie.pdb"
        results = parser.extract_metrics(target_file)
        
        print("\n--- Structural Metrics Extracted ---")
        for key, value in results.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")
                
    except Exception as e:
        print(f"Test Failed: {e}")
