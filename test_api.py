#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://127.0.0.1:5555"

def test_get_reviews():
    """Test GET /reviews"""
    print("Testing GET /reviews...")
    response = requests.get(f"{BASE_URL}/reviews")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        reviews = response.json()
        print(f"Found {len(reviews)} reviews")
        if reviews:
            print(f"First review: {reviews[0]}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_create_review():
    """Test POST /reviews"""
    print("Testing POST /reviews...")
    
    # First, get available users and games
    users_response = requests.get(f"{BASE_URL}/users")
    games_response = requests.get(f"{BASE_URL}/games")
    
    if users_response.status_code == 200 and games_response.status_code == 200:
        users = users_response.json()
        games = games_response.json()
        
        if users and games:
            # Create a new review
            review_data = {
                'score': '9',
                'comment': 'Great game! Highly recommend.',
                'user_id': str(users[0]['id']),
                'game_id': str(games[0]['id'])
            }
            
            response = requests.post(f"{BASE_URL}/reviews", data=review_data)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 201:
                new_review = response.json()
                print(f"Created review: {new_review}")
                return new_review['id']
            else:
                print(f"Error: {response.text}")
    print("-" * 50)
    return None

def test_get_review_by_id(review_id):
    """Test GET /reviews/<id>"""
    if not review_id:
        print("Skipping GET /reviews/<id> test - no review ID available")
        return
    
    print(f"Testing GET /reviews/{review_id}...")
    response = requests.get(f"{BASE_URL}/reviews/{review_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        review = response.json()
        print(f"Retrieved review: {review}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_update_review(review_id):
    """Test PATCH /reviews/<id>"""
    if not review_id:
        print("Skipping PATCH /reviews/<id> test - no review ID available")
        return
    
    print(f"Testing PATCH /reviews/{review_id}...")
    update_data = {
        'score': '10',
        'comment': 'Actually, this game is perfect!'
    }
    
    response = requests.patch(f"{BASE_URL}/reviews/{review_id}", data=update_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        updated_review = response.json()
        print(f"Updated review: {updated_review}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_delete_review(review_id):
    """Test DELETE /reviews/<id>"""
    if not review_id:
        print("Skipping DELETE /reviews/<id> test - no review ID available")
        return
    
    print(f"Testing DELETE /reviews/{review_id}...")
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Delete result: {result}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_get_nonexistent_review():
    """Test GET /reviews/<id> with non-existent ID"""
    print("Testing GET /reviews/99999 (non-existent)...")
    response = requests.get(f"{BASE_URL}/reviews/99999")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 404:
        error = response.json()
        print(f"Expected 404 error: {error}")
    else:
        print(f"Unexpected response: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Flask API CRUD Operations")
    print("=" * 50)
    
    # Test all endpoints
    test_get_reviews()
    
    # Create a new review and test other operations
    review_id = test_create_review()
    test_get_review_by_id(review_id)
    test_update_review(review_id)
    test_delete_review(review_id)
    
    # Test error handling
    test_get_nonexistent_review()
    
    print("All tests completed!")