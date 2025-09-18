#!/usr/bin/env python3
"""
Automated script to fix CWE-798 hardcoded credentials across the codebase
"""
import os
import re
from pathlib import Path

def fix_hardcoded_credentials():
    """Replace hardcoded credentials with secure environment variable usage"""
    
    replacements = [
        # API Key replacements
        (r'myverysecureapikey123', 'os.getenv("API_KEY_SECRET")'),
        (r'API_KEY\s*=\s*["\']myverysecureapikey123["\']', 'API_KEY = os.getenv("API_KEY_SECRET")'),
        (r'api_key\s*=\s*["\']myverysecureapikey123["\']', 'api_key = os.getenv("API_KEY_SECRET")'),
        
        # Demo password replacements  
        (r'demo123', 'os.getenv("DEMO_PASSWORD", "secure_demo_pass")'),
        
        # TOTP secret replacements
        (r'secret\s*=\s*["\']JBSWY3DPEHPK3PXP["\']', 'secret = os.getenv("TOTP_SECRET")'),
    ]
    
    fixed_files = []
    
    # Process Python files
    for file_path in Path('.').rglob('*.py'):
        if 'fix_hardcoded_credentials.py' in str(file_path):
            continue
            
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Apply replacements
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Add import os if needed and not present
            if content != original_content and 'import os' not in content:
                if content.startswith('#!/usr/bin/env python3'):
                    lines = content.split('\n')
                    # Find first import or first non-comment line
                    insert_pos = 1
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""'):
                            insert_pos = i
                            break
                    lines.insert(insert_pos, 'import os')
                    content = '\n'.join(lines)
                else:
                    content = 'import os\n' + content
            
            # Write back if changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                fixed_files.append(str(file_path))
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    return fixed_files

def main():
    """Run credential cleanup"""
    print("Fixing hardcoded credentials (CWE-798)...")
    
    fixed_files = fix_hardcoded_credentials()
    
    if fixed_files:
        print(f"Fixed {len(fixed_files)} files:")
        for file_path in fixed_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(fixed_files) > 10:
            print(f"  ... and {len(fixed_files) - 10} more files")
    else:
        print("No files needed fixing")
    
    print("\nIMPORTANT: Set these environment variables:")
    print("export API_KEY_SECRET='your_secure_api_key'")
    print("export DEMO_PASSWORD='your_secure_demo_password'") 
    print("export TOTP_SECRET='your_secure_totp_secret'")

if __name__ == "__main__":
    main()