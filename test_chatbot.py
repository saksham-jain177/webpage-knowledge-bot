import requests

url = "http://localhost:5000/chat"
headers = {"Content-Type": "application/json"}

while True:    
    user_input = input("Enter your query: ")
    payload = {"query": user_input}

    try:
        # Send request to chatbot API
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    # Ask if user wants to continue
    while True:
        choice = input("Would you like to continue? (yes/no): ").strip().lower()
        if choice in ['yes', 'no']:
            break
        print("Please enter 'yes' or 'no'.")
    
    if choice == 'no':
        print("Goodbye!")
        break