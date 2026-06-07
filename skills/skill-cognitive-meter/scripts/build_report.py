import json
import os
from datetime import datetime
from pathlib import Path

def main():
    # Resolve project root relative to the script position
    # Script location: <root>/skills/skill-cognitive-meter/scripts/build_report.py
    script_path = Path(__file__).resolve()
    root = script_path.parents[3]
    
    runs_dir = root / "output" / "runs"
    template_path = root / "skills" / "skill-cognitive-meter" / "assets" / "report-template.html"
    output_path = root / "pages" / "index.html"
    
    print(f"Project root resolved to: {root}")
    print(f"Scanning run data in: {runs_dir}")
    
    runs = []
    
    if runs_dir.exists():
        for subfolder in runs_dir.iterdir():
            if not subfolder.is_dir():
                continue
            
            # Look for JSON and Markdown files inside the subdirectory
            json_file = None
            md_file = None
            
            for file in subfolder.iterdir():
                if file.suffix == '.json':
                    json_file = file
                elif file.suffix == '.md':
                    md_file = file
            
            if not json_file or not md_file:
                print(f"[-] Skipping directory {subfolder.name}: must contain both a .json and .md file.")
                continue
            
            try:
                # Load JSON metrics
                with open(json_file, 'r', encoding='utf-8') as f:
                    complexity_data = json.load(f)
                
                # Load narrative Markdown
                with open(md_file, 'r', encoding='utf-8') as f:
                    narrative_md = f.read()
                
                skill_name = complexity_data.get("skill_name", subfolder.name)
                overall_rating = complexity_data.get("overall_vulnerability_rating", "MODERATE")
                heatmap_data = complexity_data.get("heatmap_data", [])
                
                # Use JSON file's modification time as the execution time
                mtime = os.path.getmtime(json_file)
                created_at = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                runs.append({
                    "skill_name": skill_name,
                    "created_at": created_at,
                    "overall_vulnerability_rating": overall_rating,
                    "heatmap_data": heatmap_data,
                    "narrative_md": narrative_md,
                    "_timestamp": mtime
                })
                print(f"[+] Loaded run data for skill '{skill_name}' from {subfolder.name}")
                
            except Exception as e:
                print(f"[!] Error parsing run directory {subfolder.name}: {e}")
    else:
        print(f"[-] Runs directory {runs_dir} does not exist.")
        
    if not runs:
        print("[-] No valid run data found to compile.")
    
    # Sort runs chronologically (most recent run first)
    runs.sort(key=lambda x: x["_timestamp"], reverse=True)
    
    # Clean up temporary timestamp sorting key
    for run in runs:
        del run["_timestamp"]
        
    # Read the template file
    if not template_path.exists():
        print(f"[!] Template file not found at {template_path}")
        return
        
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        placeholder = "/* RUNS_DATA_PLACEHOLDER */"
        if placeholder not in template_content:
            print(f"[!] Placeholder '{placeholder}' was not found in the report template HTML.")
            return
            
        # Serialize runs data to JS declaration
        runs_json_str = json.dumps(runs, indent=4, ensure_ascii=False)
        runs_js_decl = f"const runs = {runs_json_str};"
        
        # Inject the runs array into the HTML
        final_html = template_content.replace(placeholder, runs_js_decl)
        
        # Ensure pages directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to pages/index.html
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print(f"[+] Report compiled successfully! Saved to: {output_path}")
        
    except Exception as e:
        print(f"[!] Failed to generate report: {e}")

if __name__ == "__main__":
    main()
