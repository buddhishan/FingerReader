cd home/root/

mv text_audio.wav temp_audio.wav
./bin/ffmpeg/ffmpeg -i temp_audio.wav -acodec pcm_u8 -ar 22050 text_audio.wav
rm temp_audio.wav

cd 
