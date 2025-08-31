import pandas as pd

def show_extraction_results():
    """Show final extraction results"""
    df = pd.read_csv("data/candidates.csv")
    
    print("BHIV Precise Resume Extraction Results")
    print("=" * 50)
    print(f"Total Candidates: {len(df)}")
    
    print(f"\nExtraction Success Rate:")
    print(f"- Names: {len(df)}/28 (100%)")
    print(f"- Emails: {df['email'].notna().sum()}/28 ({df['email'].notna().sum()/28*100:.0f}%)")
    print(f"- Phones: {df['phone'].notna().sum()}/28 ({df['phone'].notna().sum()/28*100:.0f}%)")
    print(f"- Locations: {df['location'].notna().sum()}/28 ({df['location'].notna().sum()/28*100:.0f}%)")
    print(f"- Designations: {df['designation'].notna().sum()}/28 ({df['designation'].notna().sum()/28*100:.0f}%)")
    
    print(f"\nExperience Breakdown:")
    exp_counts = df['experience'].value_counts()
    for exp, count in exp_counts.items():
        print(f"- {exp}: {count}")
    
    print(f"\nEducation Levels:")
    edu_counts = df['education'].value_counts()
    for edu, count in edu_counts.items():
        print(f"- {edu}: {count}")
    
    print(f"\nDesignations Found:")
    des_counts = df['designation'].value_counts()
    for des, count in des_counts.items():
        if des:
            print(f"- {des}: {count}")
    
    print(f"\nSample Records:")
    sample = df[['name', 'designation', 'experience', 'location']].head()
    for _, row in sample.iterrows():
        print(f"- {row['name']} | {row['designation'] or 'No designation'} | {row['experience']} | {row['location'] or 'No location'}")

if __name__ == "__main__":
    show_extraction_results()