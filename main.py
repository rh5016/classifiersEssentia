from fastapi import FastAPI, UploadFile, File
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages/essentia')
import essentia
import tempfile, shutil

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    features, _ = essentia.MusicExtractor(lowlevelSilentFrames='drop')(filename=tmp_path)

    bpm = features['rhythm.bpm']
    key = features['tonal.key_key']
    scale = features['tonal.key_scale']
    genre = features['metadata.tags.genre'][0] if features['metadata.tags.genre'] else 'Unknown'

    return {"bpm": bpm, "key": f"{key} {scale}", "genre": genre}
