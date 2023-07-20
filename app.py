#app.py

from flask import Flask, request, jsonify
import subprocess
import requests
import json

app = Flask(__name__)

TERRAFORM_API_TOKEN = "e1QMd3wblDjntQ.atlasv1.zVveHuPFPK2Fj3UPRj1vuuXHkwEaCNXurJFDzN4kWcxjkQwIGQvwonzbI9i1LaSgm6E"
TERRAFORM_WORKSPACE_ID = "ws-nqGgwH4VhMCF6zat"

@app.route('/run-workload', methods=['POST'])
def run_workload():
    try:
        # Trigger Terraform run via Terraform Cloud API
        headers = {
            "Authorization": f"Bearer {TERRAFORM_API_TOKEN}",
            "Content-Type": "application/vnd.api+json"
        }
        subprocess.run(['terraform', 'apply', '-auto-approve'], check=True)
        return jsonify({'message': 'Workload successfully run.'}), 200
        payload = {
            "data": {
                "attributes": {
                    "workspace": {
                        "id": TERRAFORM_WORKSPACE_ID,
                        "type": "workspaces"
                    }
                }
            }
        }
        response = requests.post("https://app.terraform.io/api/v2/runs", headers=headers, json=payload)

        if response.status_code == 201:
            return jsonify({'message': 'Workload run initiated.'}), 200
        else:
            return jsonify({'error': 'Failed to run workload.'}), response.status_code

    except Exception as e:
        print(f'Error running Terraform: {e}')
        return jsonify({'error': 'Failed to run workload.'}), 500

@app.route('/destroy-workload', methods=['POST'])
def destroy_workload():
    try:
        subprocess.run(['terraform', 'destroy', '-auto-approve'], check=True)
        return jsonify({'message': 'Workload successfully destroyed.'}), 200
    except subprocess.CalledProcessError as e:
        print(f'Error running Terraform: {e}')
        return jsonify({'error': 'Failed to destroy workload.'}), 500

@app.route('/run-status', methods=['GET'])
def get_run_status():
    try:
        # Retrieve the status of the most recent run via Terraform Cloud API
        headers = {
            "Authorization": f"Bearer {TERRAFORM_API_TOKEN}"
        }
        response = requests.get(f"https://app.terraform.io/api/v2/workspaces/{TERRAFORM_WORKSPACE_ID}/runs?filter%5Borganization%5D%5Bname%5D=my-org&filter%5Bworkspace%5D%5Bname%5D=my-workspace&sort=-created-at&page%5Bnumber%5D=1&page%5Bsize%5D=1", headers=headers)

        if response.status_code == 200:
            data = response.json()
            run_status = data.get('data')[0].get('attributes').get('status')
            return jsonify({'status': run_status}), 200
        else:
            return jsonify({'error': 'Failed to retrieve run status.'}), response.status_code

    except Exception as e:
        print(f'Error retrieving run status: {e}')
        return jsonify({'error': 'Failed to retrieve run status.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
