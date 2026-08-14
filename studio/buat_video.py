import sys, subprocess, json, os

def generate_naskah_dan_visual(topik, durasi):
    print(f"🎬 Bikin video {durasi} detik soal: {topik}")
    print("🧠 Gemini menyusun naskah + rencana visual...")

    prompt = f"""Kamu adalah sutradara video pendek edutainment Bahasa Indonesia, gaya casual dan santai.

Buat naskah voice over untuk video berdurasi {durasi} detik tentang: {topik}

Balas HANYA dalam format JSON persis seperti ini, tanpa teks lain, tanpa markdown backticks:
{{
  "naskah_lengkap": "seluruh naskah digabung jadi satu paragraf, buat dibaca voice over",
  "scenes": [
    {{"urutan": 1, "teks": "kalimat/segmen ini", "visual": "deskripsi singkat visual/background yang cocok", "mood": "misterius/kaget/santai/dramatis"}}
  ]
}}

Bagi naskah jadi 4-6 scene. Pastikan total durasi baca natural sekitar {durasi} detik."""

    result = subprocess.run(
        ["gemini", "-p", prompt],
        capture_output=True, text=True, check=True
    )

    output = result.stdout.strip()
    # Bersihkan kalau ada markdown code fence
    if output.startswith("```"):
        output = output.split("```")[1]
        if output.startswith("json"):
            output = output[4:]

    data = json.loads(output)

    os.makedirs("src/data", exist_ok=True)
    with open("src/data/rencana_video.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open("src/script.txt", "w", encoding="utf-8") as f:
        f.write(data["naskah_lengkap"])

    print(f"✅ Naskah + {len(data['scenes'])} scene tersimpan")
    return data

def buat_voice_over():
    print("🎙️ Generate voice over...")
    os.makedirs("src/audio", exist_ok=True)
    subprocess.run([
        "edge-tts", "--voice", "id-ID-ArdiNeural",
        "--file", "src/script.txt",
        "--write-media", "src/audio/voiceover.mp3"
    ], check=True)
    print("✅ Voice over selesai")

def buat_subtitle_timing():
    print("💬 Generate subtitle timing...")
    subprocess.run([
        "whisper", "src/audio/voiceover.mp3",
        "--language", "Indonesian", "--model", "small",
        "--output_format", "json", "--output_dir", "src/data"
    ], check=True)
    print("✅ Subtitle timing selesai")

def render_video():
    print("🎥 Render video final...")
    subprocess.run(["npx", "remotion", "render"], check=True)
    print("✅ Video jadi! Cek folder out/")

def buat_video(topik, durasi):
    generate_naskah_dan_visual(topik, durasi)
    buat_voice_over()
    buat_subtitle_timing()
    render_video()
    print(f"\n🎉 SELESAI! Video '{topik}' udah jadi di folder out/")

if __name__ == "__main__":
    topik = sys.argv[1] if len(sys.argv) > 1 else "topik default"
    durasi = sys.argv[2] if len(sys.argv) > 2 else "55"
    buat_video(topik, durasi)
