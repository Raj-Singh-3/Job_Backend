from flask import Blueprint, request, jsonify
from app.scraper import JobScraper

main = Blueprint('main', __name__)
scraper = JobScraper()

@main.route('/api/analyze', methods=['POST'])
def analyze_job():
    data = request.get_json()
    url = data.get('url')
    job_post = data.get('job_post')

    if not url and not job_post:
        return jsonify({'error': 'Please provide either a URL or job post'}), 400

    try:
        if url:
            # Scrape job data from URL
            job_data = scraper.scrape_job(url=url)
        else:
            # Extract data from provided job post
            job_data = scraper.scrape_job(post_text=job_post)

        if not job_data:
            return jsonify({'error': 'Failed to extract job data'}), 400

        return jsonify(job_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200