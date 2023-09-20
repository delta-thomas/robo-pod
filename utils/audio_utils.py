from pydub import AudioSegment

def combine_mp3s(intro_path, generated_path, output_path):
    intro = AudioSegment.from_mp3(intro_path)
    generated = AudioSegment.from_mp3(generated_path)

    combined = intro + generated
    combined.export(output_path, format="mp3")
