import assemblyai as aai
from api_secrets import API_KEY_ASSEMBLYAI
import requests
import sys

# upload local file for transcription

filename = sys.argv[1]

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"


def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': API_KEY_ASSEMBLYAI}
    response = requests.post(upload_endpoint, headers=headers, data=read_file(filename))

    if response.status_code != 200:
        print(f"Error uploading file: {response.status_code}, {response.text}")
        sys.exit(1)

    audio_url = response.json()['upload_url']
    return audio_url


def transcribe(audio_url):
    headers = {'authorization': API_KEY_ASSEMBLYAI}
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    if transcript_response.status_code != 200:
        print(f"Error creating transcript: {transcript_response.status_code}, {transcript_response.text}")
        sys.exit(1)

    job_id = transcript_response.json()['id']
    return job_id




# waiting for assemblyai to prepare transcription
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers={'authorization': API_KEY_ASSEMBLYAI})
    return polling_response.json()


def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data,None
        elif data['status'] == 'error':
            return data,data['error']


# save transcript function


def save_transcript(audio_url):
    data, error = get_transcription_result_url(audio_url)
    if data:
        txtfilename = filename + ".txt"
        with open(txtfilename,"w") as f:
            f.write(data['text'])
        print('Transcription saved')
    elif error:
        print("Error: ",error)



audio_url = upload(filename)
save_transcript(audio_url)