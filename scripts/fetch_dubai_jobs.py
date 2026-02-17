#!/usr/bin/env python3
"""
Dubai Job Fetcher
Fetches full stack developer jobs from Dubai/Series A companies
Run: python3 fetch_dubai_jobs.py
"""

import urllib.request
import json
import csv
from datetime import datetime
from urllib.parse import urlencode

# Known Dubai-based Series A+ and Mid-size Tech Companies
DUBAI_COMPANIES = [
    {"name": "Kitopi", "stage": "Series C", "sector": "FoodTech"},
    {"name": "Mumzworld", "stage": "Series B", "sector": "E-commerce"},
    {"name": "Namshi", "stage": "Acquired", "sector": "E-commerce"},
    {"name": "Awqaf", "stage": "Government", "sector": "FinTech"},
    {"name": "YallaCompare", "stage": "Series A", "sector": "FinTech"},
    {"name": "Policybazaar UAE", "stage": "Series C", "sector": "InsurTech"},
    {"name": "Bayt", "stage": "Mid-size", "sector": "HR Tech"},
    {"name": "Cynoteck", "stage": "Mid-size", "sector": "IT Services"},
    {"name": "App Starr", "stage": "Mid-size", "sector": "Mobile Apps"},
    {"name": "Bridg", "stage": "Series A", "sector": "MarTech"},
    {"name": "Crowd Analyzer", "stage": "Series A", "sector": "AI/Analytics"},
    {"name": "Mawdoo3", "stage": "Series B", "sector": "AI/Content"},
    {"name": "Shorooq", "stage": "Series A", "sector": "FinTech"},
    {"name": "YAP", "stage": "Series A", "sector": "FinTech"},
    {"name": "Riyad Capital", "stage": "Public", "sector": "FinTech"},
    {"name": "Fuel7", "stage": "Series A", "sector": "E-commerce"},
    {"name": "Tribal", "stage": "Series A", "sector": "MarTech"},
    {"name": "Cloudify", "stage": "Series B", "sector": "Cloud"},
    {"name": "Debut", "stage": "Series A", "sector": "HR Tech"},
    {"name": "URE", "stage": "Series A", "sector": "PropTech"},
]

def fetch_remoteok_jobs():
    """Fetch full stack jobs from RemoteOK API"""
    jobs = []
    try:
        req = urllib.request.Request("https://remoteok.com/api?tag=fullstack")
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            for job in data[1:]:  # Skip first element (legal)
                # Filter for UAE/Gulf related
                location = job.get("location", "")
                if any(x in location.lower() for x in ["uae", "dubai", "gulf", "abudhabi", "middle east", "saudi", "qatar"]):
                    jobs.append({
                        "company": job.get("company", ""),
                        "title": job.get("position", ""),
                        "location": location,
                        "url": job.get("url", ""),
                        "date": job.get("date", ""),
                        "salary": f"${job.get('salary_min', 0)}-${job.get('salary_max', 0)}",
                        "source": "RemoteOK"
                    })
    except Exception as e:
        print(f"Error fetching RemoteOK: {e}")
    return jobs

def fetch_remotive_jobs():
    """Fetch jobs from Remotive API"""
    jobs = []
    try:
        req = urllib.request.Request("https://remotive.com/api/remote-jobs?category=software-dev&search=fullstack")
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            for job in data.get("jobs", []):
                location = job.get("candidate_required_location", "")
                if any(x in location.lower() for x in ["uae", "dubai", "gulf", "abudhabi", "middle east", "saudi", "qatar", "europe"]):
                    jobs.append({
                        "company": job.get("company_name", ""),
                        "title": job.get("title", ""),
                        "location": location,
                        "url": job.get("url", ""),
                        "date": job.get("publication_date", ""),
                        "salary": job.get("salary", ""),
                        "source": "Remotive"
                    })
    except Exception as e:
        print(f"Error fetching Remotive: {e}")
    return jobs

def save_to_csv(jobs, filename="dubai_jobs.csv"):
    """Save jobs to CSV file"""
    import os
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    
    fieldnames = ["Company", "Job Title", "Location", "Salary", "URL", "Posted Date", "Source"]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow({
                "Company": job.get("company", ""),
                "Job Title": job.get("title", ""),
                "Location": job.get("location", ""),
                "Salary": job.get("salary", ""),
                "URL": job.get("url", ""),
                "Posted Date": job.get("date", ""),
                "Source": job.get("source", "")
            })
    print(f"✅ Saved {len(jobs)} jobs to {filepath}")

def main():
    print("🔍 Fetching Dubai/UAE full stack jobs...")
    
    all_jobs = []
    
    # Fetch from APIs
    print("📡 Fetching from RemoteOK...")
    remoteok_jobs = fetch_remoteok_jobs()
    all_jobs.extend(remoteok_jobs)
    print(f"   Found {len(remoteok_jobs)} jobs")
    
    print("📡 Fetching from Remotive...")
    remotive_jobs = fetch_remotive_jobs()
    all_jobs.extend(remotive_jobs)
    print(f"   Found {len(remotive_jobs)} jobs")
    
    # Save
    if all_jobs:
        save_to_csv(all_jobs, "data/dubai_fullstack_jobs.csv")
    else:
        print("⚠️ No jobs found. Try checking manually.")
    
    print("\n📋 Known Dubai Series A+ Companies to target:")
    for co in DUBAI_COMPANIES[:10]:
        print(f"   • {co['name']} ({co['stage']}) - {co['sector']}")

if __name__ == "__main__":
    main()
