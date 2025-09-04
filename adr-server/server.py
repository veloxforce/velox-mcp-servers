from fastmcp import FastMCP
import requests
import frontmatter

mcp = FastMCP("Velox ADR Server (GitHub)")

# Configuration
REPO = "veloxforce/velox-global-adrs"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

@mcp.resource("adr://list")
def list_adrs() -> dict:
    """List ADRs with descriptions from YAML frontmatter"""
    try:
        # Get file list from GitHub API
        response = requests.get(f"https://api.github.com/repos/{REPO}/contents", timeout=5)
        response.raise_for_status()
        files = response.json()
        
        adr_files = []
        for file_info in files:
            if file_info["name"].endswith(".md") and file_info["name"] != "README.md":
                try:
                    # Fetch and parse YAML frontmatter
                    adr_response = requests.get(f"{BASE_URL}/{file_info['name']}", timeout=5)
                    if adr_response.status_code == 200:
                        post = frontmatter.loads(adr_response.text)
                        
                        adr_files.append({
                            "filename": file_info["name"],
                            "description": post.metadata.get("description", "No description available")
                        })
                except Exception as parse_error:
                    # If parsing fails, include file with minimal info
                    adr_files.append({
                        "filename": file_info["name"],
                        "description": f"Parse error: {str(parse_error)}"
                    })
        
        return {
            "repository": REPO,
            "branch": BRANCH,
            "count": len(adr_files),
            "adrs": sorted(adr_files, key=lambda x: x["filename"])
        }
    except Exception as e:
        return {"error": f"Failed to fetch enhanced ADR list: {str(e)}"}

@mcp.resource("adr://{filename}")
def get_adr(filename: str) -> str:
    """Fetch ADR content from GitHub"""
    if not filename.endswith(".md"):
        filename = f"{filename}.md"
    
    try:
        response = requests.get(f"{BASE_URL}/{filename}", timeout=5)
        if response.status_code == 404:
            return f"ADR '{filename}' not found"
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching ADR: {str(e)}"

@mcp.resource("adr://metadata")
def get_metadata() -> dict:
    """Fetch repository metadata"""
    try:
        response = requests.get(f"{BASE_URL}/.mcp/resources.json", timeout=5)
        response.raise_for_status()
        return response.json()
    except:
        return {"error": "Metadata unavailable"}

if __name__ == "__main__":
    print(f"🚀 Velox ADR Server (GitHub Direct)")
    print(f"📦 Repository: {REPO}")
    print(f"🌐 No local storage - fetching from GitHub!")
    mcp.run()