from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

@app.route('/repos/<username>', methods=['GET'])
def get_repos(username):
    token = "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"
    headers = {"Authorization": f"{token}"}
    response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
    responses = requests.get(f"https://api.github.com/users/{username}/repos", headers=headers)

    if response.status_code == 200 and responses.status_code == 200:
        output_dir = './FLASK/github_shortlist'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.splitext(username)[0] + ".json"
        output_path = os.path.join(output_dir, output_file)
        data = {"user_info": response.json(), "repos": responses.json()}
        simplify_json(data)
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{username} saved to {output_path}")
        return {"message": f"{username} fetched from github and saved to {output_path} successfully"}
    else:
        print("Error:", response.status_code, responses.status_code)
        return {"message": "Error fetching data from GitHub API"}, 500


def simplify_json(github_data):
    user_info = github_data["user_info"]
    keys_to_keep = ["login", "url", "name", "company", "location", "email", "bio", "twitter_username", "public_repos", "followers", "following", "created_at", "updated_at"]
    # Modify the dictionary to keep only the desired keys and their values
    user_info = {k: v for k, v in user_info.items() if k in keys_to_keep}
    print(f"user_info: {user_info}")

    repos_list = github_data["repos"]
    sorted_repo_details = []
    for repos in repos_list:
        repo_keys_to_keep = ["name", "full_name", "private", "description", "url", "commits_url", "created_at",
                             "updated_at", "pushed_at", "clone_url", "size", "watchers_count", "language", "owner"]
        # Modify the dictionary to keep only the desired keys and their values
        repo_dict = {k: v for k, v in repos.items() if k in repo_keys_to_keep}
        owner = repo_dict.pop("owner")
        repo_dict["owner_name"] = owner["login"]
        repo_dict["owner_url"] = owner["url"]
        sorted_repo_details.append(repo_dict)

    github_data["user_info"] = user_info
    github_data["repos"] = sorted_repo_details
    # print(github_data)
    output_dir='./FLASK/success'
    os.makedirs(output_dir, exist_ok=True)
    username = github_data["user_info"]["login"]
    output_path = os.path.join(output_dir, f"{username}.json")
    with open(output_path, 'w') as f:
        json.dump(github_data, f, indent=4)
    print(f"data saved to {output_path}")