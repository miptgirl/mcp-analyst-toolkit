import requests
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict

# Global configuration
DEFAULT_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitHub-Query-Script"
}

BASE_URL = "https://api.github.com"

def get_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = DEFAULT_HEADERS.copy()
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def parse_repo_url(repo_url: str) -> tuple:
    # Remove .git suffix if present
    repo_url = repo_url.rstrip('.git')
    
    # Extract owner/repo from various URL formats
    if repo_url.startswith('https://github.com/'):
        parts = repo_url.replace('https://github.com/', '').split('/')
    elif repo_url.startswith('github.com/'):
        parts = repo_url.replace('github.com/', '').split('/')
    elif '/' in repo_url and not repo_url.startswith('http'):
        parts = repo_url.split('/')
    else:
        raise ValueError(f"Invalid repository URL format: {repo_url}")
    
    if len(parts) < 2:
        raise ValueError(f"Cannot extract owner/repo from: {repo_url}")
    
    return parts[0], parts[1]

def get_recent_prs(repo_url: str, days: int, token: Optional[str] = None) -> List[Dict]:
    try:
        owner, repo = parse_repo_url(repo_url)
    except ValueError as e:
        return {"error": str(e)}
    
    headers = get_headers(token)
    
    # Calculate date threshold
    since_date = datetime.now() - timedelta(days=days)
    
    # GitHub API endpoint for pull requests
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    
    params = {
        'state': 'all',  # all, open, closed
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100  # Max per page
    }
    
    all_prs = []
    page = 1
    
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return {
                "error": f"API request failed: {response.status_code}",
                "message": response.json().get('message', 'Unknown error') if response.content else 'Unknown error'
            }
        
        prs = response.json()
        if not prs:  # No more pages
            break
        
        # Filter PRs by date
        for pr in prs:
            pr_updated = datetime.strptime(pr['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
            if pr_updated >= since_date:
                all_prs.append({
                    'id': pr['number'],
                    'title': pr['title'],
                    'url': pr['html_url'],
                    'api_url': pr['url'],
                    'state': pr['state'],
                    'created_at': pr['created_at'],
                    'updated_at': pr['updated_at'],
                    'author': pr['user']['login']
                })
            else:
                # PRs are sorted by updated date, so we can stop here
                return all_prs
        
        page += 1
        
        # Safety check to avoid infinite loops
        if page > 100:  # Adjust based on your needs
            break
            print('Warning: Execution stopped after 100 pages')
    
    return all_prs

def extract_pr_number_from_url(pr_url: str) -> Optional[int]:
    match = re.search(r'/pull/(\d+)', pr_url)
    if match:
        return int(match.group(1))
    return None

def get_pr_commits(owner: str, repo: str, pr_number: int, token: Optional[str] = None) -> List[Dict]:
    headers = get_headers(token)
    commits_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/commits"
    
    response = requests.get(commits_url, headers=headers)
    if response.status_code != 200:
        return []
    
    commits = response.json()
    return [
        {
            'sha': commit['sha'][:7],
            'message': commit['commit']['message'].split('\n')[0],
            'author': commit['commit']['author']['name'],
            'date': commit['commit']['author']['date']
        }
        for commit in commits
    ]

def get_pr_files(owner: str, repo: str, pr_number: int, token: Optional[str] = None) -> List[Dict]:
    headers = get_headers(token)
    files_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    response = requests.get(files_url, headers=headers)
    if response.status_code != 200:
        return []
    
    files = response.json()
    return [
        {
            'filename': file['filename'],
            'status': file['status'],
            'additions': file['additions'],
            'deletions': file['deletions'],
            'changes': file['changes']
        }
        for file in files
    ]

def get_pr_details(repo_url: str, pr_identifier, token: Optional[str] = None) -> Dict:
    try:
        owner, repo = parse_repo_url(repo_url)
    except ValueError as e:
        return {"error": str(e)}
    
    headers = get_headers(token)
    
    # Handle different PR identifier formats
    if isinstance(pr_identifier, str) and 'github.com' in pr_identifier:
        pr_number = extract_pr_number_from_url(pr_identifier)
        if pr_number is None:
            return {"error": "Cannot extract PR number from URL"}
    else:
        try:
            pr_number = int(pr_identifier)
        except (ValueError, TypeError):
            return {"error": "PR identifier must be a number or valid GitHub PR URL"}
    
    # Get PR details
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {
            "error": f"API request failed: {response.status_code}",
            "message": response.json().get('message', 'PR not found') if response.content else 'PR not found'
        }
    
    pr = response.json()
    
    # Get additional details
    commits = get_pr_commits(owner, repo, pr_number, token)
    files = get_pr_files(owner, repo, pr_number, token)
    
    return {
        'id': pr['number'],
        'title': pr['title'],
        'body': pr['body'],
        'url': pr['html_url'],
        'state': pr['state'],
        'created_at': pr['created_at'],
        'updated_at': pr['updated_at'],
        'closed_at': pr['closed_at'],
        'merged_at': pr['merged_at'],
        'author': {
            'login': pr['user']['login'],
            'url': pr['user']['html_url']
        },
        'assignees': [user['login'] for user in pr['assignees']],
        'reviewers': [user['login'] for user in pr['requested_reviewers']],
        'labels': [label['name'] for label in pr['labels']],
        'milestone': pr['milestone']['title'] if pr['milestone'] else None,
        'base_branch': pr['base']['ref'],
        'head_branch': pr['head']['ref'],
        'commits_count': len(commits),
        'commits': commits,
        'files_changed': len(files),
        'files': files,
        'additions': pr['additions'],
        'deletions': pr['deletions'],
        'changed_files': pr['changed_files'],
        'mergeable': pr['mergeable'],
        'merged': pr['merged']
    }