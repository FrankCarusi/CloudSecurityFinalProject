from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb')
table_name = 'final-project-security-database'
table = dynamodb.Table(table_name)

@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        response = table.scan(ProjectionExpression='teamName')
        team_names = [item['teamName'] for item in response.get('Items', [])]
        return jsonify({'allTeams': team_names}), 200
    except Exception as e:
        return jsonify({'message': "Failure"}), 500

@app.route('/team', methods=['GET'])
def get_team_record():
    team_name = request.args.get('team')
    if not team_name:
        return jsonify({'message': "Team name is required"}), 400

    try:
        team_record = table.get_item(Key={'teamName': team_name})
        if 'Item' not in team_record:
            return jsonify({'message': "Team not found"}), 404

        item = team_record['Item']
        wins = int(item.get('Home_Win', 0)) + int(item.get('Away_Win', 0))
        loses = int(item.get('Home_Loss', 0)) + int(item.get('Away_Loss', 0))

        res_body = {
            'record': {
                "wins": wins,
                "loses": loses
            },
            'homeWL': f"{int(item.get('Home_Win', 0))}-{int(item.get('Home_Loss', 0))}",
            'awayWL': f"{int(item.get('Away_Win', 0))}-{int(item.get('Away_Loss', 0))}"
        }
        return jsonify(res_body), 200
    except Exception as e:
        return jsonify({'message': "Failure"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 
