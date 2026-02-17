from quart import Quart, render_template, jsonify
import json
import os

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('viz.html')

@app.route('/api/data')
async def get_data():
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'test.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data) if isinstance(data, list) else 1
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Data file not found'
        }), 404
    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': 'Invalid JSON format'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
