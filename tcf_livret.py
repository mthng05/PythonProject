import requests
from pydub import AudioSegment

# Config API
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"

class SpeechToText:
    def __init__(self):
        pass

    def speech_to_text(self, audio_file):
        audio_file_name = audio_file.split("/")[-1].replace(".mp3", "")
        audio = AudioSegment.from_file(audio_file)
        chunks = self.chunk_audio_segment(audio)

        with open(f"output/{audio_file_name}.txt", "w") as text_file:
            for idx, chunk in enumerate(chunks):
                chunk_path = f"process/chunk_{idx}.mp3"
                chunk.export(chunk_path, format="mp3")

                with open(chunk_path, "rb") as f:
                    data = f.read()
                    response = requests.post(
                        API_URL,
                        headers= { **HEADERS, "Content-Type": "audio/mpeg"},
                        data=data
                    )

                if response.status_code == 200:
                    text = response.json().get("text", "")
                    print(f"Chunk {idx}: {text}")
                    text_file.write(f"{text}\n")
                else:
                    print(f"Lỗi xử lý chunk {idx}: {response.text}")

    def chunk_audio_segment(self, audio):
        chunk_length_ms = 15 * 1000
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        return chunks

if __name__ == "__main__":
    instance = SpeechToText()
    instance.speech_to_text(audio_file="input/tcf8-podcast.mp3")