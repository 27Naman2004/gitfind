#!/usr/bin/env python3
"""Test script with mocking to avoid API rate limits."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unittest.mock import patch, Mock
from gitfind.core import repo_summary

def test_with_mock():
    """Test with mocked API responses."""
    print("🧪 Testing with mocked API responses...")
    
    # Mock responses
    mock_repo_response = Mock()
    mock_repo_response.status_code = 200
    mock_repo_response.json.return_value = {
        'stargazers_count': 100,
        'forks_count': 50,
        'contributors_url': 'https://api.github.com/repos/python/cpython/contributors',
        'languages_url': 'https://api.github.com/repos/python/cpython/languages',
        'pushed_at': '2023-01-01T00:00:00Z',
        'description': 'The Python programming language',
        'name': 'cpython'
    }
    
    mock_contributors_response = Mock()
    mock_contributors_response.status_code = 200
    mock_contributors_response.json.return_value = [{}, {}, {}]  # 3 contributors
    
    mock_languages_response = Mock()
    mock_languages_response.status_code = 200
    mock_languages_response.json.return_value = {
        'Python': 8000,
        'C': 2000,
        'C++': 500
    }
    
    mock_commits_response = Mock()
    mock_commits_response.status_code = 200
    mock_commits_response.json.return_value = [{
        'commit': {
            'author': {
                'date': '2023-01-01T00:00:00Z'
            }
        }
    }]
    
    # Patch the requests.get method
    with patch('gitfind.core.requests.get') as mock_get:
        mock_get.side_effect = [
            mock_repo_response,
            mock_contributors_response,
            mock_languages_response,
            mock_commits_response
        ]
        
        try:
            result = repo_summary('https://github.com/python/cpython')
            
            print("✅ Mock test passed!")
            print(f"Stars: {result['Total Stars']} (expected: 100)")
            print(f"Forks: {result['Total Forks']} (expected: 50)")
            print(f"Contributors: {result['Total Contributors']} (expected: 3)")
            print(f"Languages: {result['Primary Programming Languages']}")
            print(f"Summary: {result['Auto-generated summary report']}")
            
            # Verify expected values
            assert result['Total Stars'] == 100
            assert result['Total Forks'] == 50
            assert result['Total Contributors'] == 3
            assert 'Python' in result['Primary Programming Languages']
            
            return True
            
        except Exception as e:
            print(f"❌ Mock test failed: {e}")
            return False

if __name__ == "__main__":
    success = test_with_mock()
    if success:
        print("\n🎉 Mock test completed successfully!")
    else:
        print("\n❌ Mock test failed!")