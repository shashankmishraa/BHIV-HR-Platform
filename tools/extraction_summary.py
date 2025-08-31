import pandas as pd

def show_extraction_summary():
    """Show summary of extracted candidate data"""
    
    # Read the standard candidates CSV
    df = pd.read_csv("data/standard_candidates.csv")
    
    print("BHIV Resume Extraction Summary")
    print("=" * 50)
    print(f"Total Candidates: {len(df)}")
    print(f"Complete Records: {df.dropna().shape[0]}")
    
    print(f"\nData Quality:")
    print(f"- Names: {df['name'].notna().sum()}/{len(df)}")
    print(f"- Emails: {df['email'].notna().sum()}/{len(df)}")
    print(f"- Phones: {df['phone'].notna().sum()}/{len(df)}")
    print(f"- Locations: {df['location'].notna().sum()}/{len(df)}")
    print(f"- Designations: {df['designation'].notna().sum()}/{len(df)}")
    
    print(f"\nExperience Distribution:")
    exp_ranges = {
        '0-2 years': len(df[df['experience_years'] <= 2]),
        '3-5 years': len(df[(df['experience_years'] >= 3) & (df['experience_years'] <= 5)]),
        '6-10 years': len(df[(df['experience_years'] >= 6) & (df['experience_years'] <= 10)]),
        '10+ years': len(df[df['experience_years'] > 10])
    }
    for range_name, count in exp_ranges.items():
        print(f"- {range_name}: {count}")
    
    print(f"\nTop Designations:")
    designations = df['designation'].value_counts().head(5)
    for designation, count in designations.items():
        if designation and designation != 'Not Specified':
            print(f"- {designation}: {count}")
    
    print(f"\nTop Skills:")
    all_skills = []
    for skills_str in df['skills'].dropna():
        all_skills.extend([s.strip() for s in skills_str.split(';')])
    
    skill_counts = pd.Series(all_skills).value_counts().head(10)
    for skill, count in skill_counts.items():
        print(f"- {skill}: {count}")
    
    print(f"\nLocation Distribution:")
    locations = df['location'].value_counts().head(5)
    for location, count in locations.items():
        if location:
            print(f"- {location}: {count}")

if __name__ == "__main__":
    show_extraction_summary()