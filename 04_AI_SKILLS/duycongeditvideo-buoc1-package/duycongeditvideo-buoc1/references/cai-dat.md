# Cài đặt môi trường (máy mới)

Cần: Python 3.9+, ffmpeg + ffprobe gọi được từ terminal, thư viện `faster-whisper numpy`.

## Windows
```bash
winget install Gyan.FFmpeg
pip install faster-whisper numpy
# Có card NVIDIA (GTX 16xx/RTX...): bật GPU cho Whisper
pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
```
Mở terminal MỚI sau khi cài ffmpeg. Scripts tự thêm `site-packages/nvidia/*/bin` vào đường tìm DLL — không cần cài CUDA Toolkit, chỉ cần driver NVIDIA đời mới.

## macOS
```bash
brew install ffmpeg
pip3 install faster-whisper numpy
```
(Mac không có CUDA → Whisper chạy CPU; video dài 1 giờ mất khoảng 40–80 phút. Nên chạy nền.)

## Linux
```bash
sudo apt install ffmpeg
pip install faster-whisper numpy nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"
```

## Model
Lần đầu chạy Whisper sẽ tự tải `large-v3` (~3 GB) — cần mạng. Sau đó chạy offline.

## Kiểm tra
```bash
python "<skill>/scripts/preflight.py" --gpu
```
Dòng cuối `DU HET. CHAY DUOC ROI.` là xong. `Whisper: chay tren cuda/int8_float16` = đang dùng GPU.

## Tốc độ tham khảo (GTX 1660 Super)
- Nhận dạng video gốc: ~1/3 thời lượng lời nói (GPU) — 54 phút lời nói ≈ 15–20 phút.
- Cắt ghép (h264_nvenc): ~30–60 s mỗi video 1440×2560.
- Hồ sơ + kiểm tra: ~25 s mỗi video 60–90 s (GPU).
