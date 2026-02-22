import requests


RAPIDAPI_KEY = "a0fbb1d680msh8caa6a62ef0c33ap1430c7jsn786df43d7c46"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
BASE_URL = "https://jsearch.p.rapidapi.com/search"


def fetch_jobs(query, location="United States", page=1, num_pages=1, limit=5):

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    params = {
        "query": f"{query} jobs in {location}",
        "page": page,
        "num_pages": num_pages,
        "country": "us",
        "date_posted": "all"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    data = response.json()

    jobs = []

    for job in data.get("data", []):

        location_text = (
            job.get("job_location")
            or f"{job.get('job_city','')} {job.get('job_state','')}"
            or "Multiple locations"
        )

        jobs.append({
            "company": job.get("employer_name", "N/A"),
            "title": job.get("job_title", "N/A"),
            "link": job.get("job_apply_link"),
            "description": job.get("job_description"),
            "date_posted": job.get("job_posted_human_readable") or "Recently",
            "job_location": location_text,
            "job_type": job.get("job_employment_type_text") or "Not specified"
        })

    return jobs[:limit]