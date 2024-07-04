from flask import Flask, render_template, request, jsonify
from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
import os
import tempfile

app = Flask(__name__)

# Hume AI client setup
client = HumeBatchClient("oP3Gspr4CdSzj0DjVZl6IqnPuSR4C9M7GebeiNiwtQ1o9ToA")
config = ProsodyConfig()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'}), 400
  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'}), 400
  if file:
    # Save the file temporarily
    _, temp_path = tempfile.mkstemp(suffix='.wav')
    file.save(temp_path)

    # Process the file
    try:
      job = client.submit_job([temp_path], [config])
      result = job.await_complete()
      predictions = client.get_job_predictions(job_id=job.id)

      # Clean up the temporary file
      os.remove(temp_path)

      return jsonify(predictions)
    except Exception as e:
      return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=2080, debug=True)
