import os
import requests
from Bio.PDB import PDBList

class PDBFetcher:
    def __init__(self, cache_dir="data/cache"):
        """
        Initializes the fetcher with a local caching directory.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.pdbl = PDBList(server='ftp://ftp.wwpdb.org')

    def fetch_by_pdb_id(self, pdb_id):
        """
        Downloads a PDB file directly from the RCSB Protein Data Bank via HTTPS.
        """
        pdb_id = pdb_id.lower().strip()
        print(f"[NREP] Attempting to fetch PDB ID: {pdb_id} via HTTPS...")
        
        final_path = os.path.join(self.cache_dir, f"{pdb_id}.pdb")
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        
        try:
            # Fetch directly via HTTPS, bypassing FTP blocks
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(final_path, 'wb') as f:
                    f.write(response.content)
                print(f"[NREP] Successfully cached: {final_path}")
                return final_path
            elif response.status_code == 404:
                raise FileNotFoundError(f"PDB ID '{pdb_id}' not found on RCSB servers.")
            else:
                raise Exception(f"Failed to download. HTTP Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Network error while fetching PDB ID {pdb_id}: {e}")

    def fetch_by_uniprot_id(self, uniprot_id):
        """
        Queries UniProt API to find associated PDB IDs, chooses the optimal 
        structure, and fetches it.
        """
        uniprot_id = uniprot_id.upper().strip()
        print(f"[NREP] Querying UniProt mapping for ID: {uniprot_id}...")
        
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise ValueError(f"Invalid UniProt ID or API connection issue (Status: {response.status_code})")
        
        data = response.json()
        uni_db_cross_refs = data.get("uniProtKBCrossReferences", [])
        
        pdb_structures = []
        for ref in uni_db_cross_refs:
            if ref.get("database") == "PDB":
                properties = ref.get("properties", [])
                pdb_id = ref.get("id")
                
                # Extract resolution method and value to prioritize high-quality data
                resolution = 999.0  # Default fallback for unlisted resolutions
                for prop in properties:
                    if prop.get("key") == "Resolution":
                        try:
                            resolution = float(prop.get("value").split()[0])
                        except ValueError:
                            pass
                
                pdb_structures.append({"id": pdb_id, "resolution": resolution})
        
        if not pdb_structures:
            raise FileNotFoundError(f"No valid PDB structural cross-references found for UniProt ID: {uniprot_id}")
        
        # Sort structures by resolution (lower number = clearer atomic detail)
        pdb_structures.sort(key=lambda x: x["resolution"])
        best_pdb_id = pdb_structures[0]["id"]
        print(f"[NREP] Identified best structural match: {best_pdb_id} (Resolution: {pdb_structures[0]['resolution']} Å)")
        
        return self.fetch_by_pdb_id(best_pdb_id)

# Test execution block
if __name__ == "__main__":
    fetcher = PDBFetcher()
    # Test with a classic neuroreceptor-associated crystal structure or protein
    try:
        # Example: Fetching directly via PDB ID
        path_by_pdb = fetcher.fetch_by_pdb_id("1AIE")
        print(f"Test 1 Passed. File stored at: {path_by_pdb}")
    except Exception as e:
        print(f"Test 1 Failed: {e}")
