import os, time, asyncio, subprocess, json
from helper.utils import metadata_text

async def change_metadata(input_file, output_file, metadata):
    author, title, video_title, audio_title, subtitle_title = await metadata_text(metadata)
    
    # Get the video metadata
    # Uses ffprobe to read streams
    try:
        output = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-print_format', 'json', input_file])
        data = json.loads(output)
        streams = data['streams']
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return False

    # Create the FFmpeg command to change metadata
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-map', '0',  # Map all streams
        '-c:v', 'copy',  # Copy video stream
        '-c:a', 'copy',  # Copy audio stream
        '-c:s', 'copy',  # Copy subtitles stream
        '-metadata', f'title={title}',
        '-metadata', f'author={author}',
    ]

    # Add title to video/audio/subtitle streams based on their index
    for stream in streams:
        stream_index = stream.get('index')
        codec_type = stream.get('codec_type')
        
        if codec_type == 'video' and video_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={video_title}'])
        elif codec_type == 'audio' and audio_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={audio_title}'])
        elif codec_type == 'subtitle' and subtitle_title:
            cmd.extend([f'-metadata:s:{stream_index}', f'title={subtitle_title}'])

    cmd.extend(['-metadata', f'comment=Added by @Digital_Rename_Bot'])
    cmd.extend(['-f', 'matroska']) # Force output format to mkv (container supports most streams)
    cmd.append(output_file)
    
    # Debug print
    # print(cmd)
    
    # Execute the command
    try:
        # Run ffmpeg command
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print("FFmpeg Error:", e.stderr.decode('utf-8'))
        return False
    except Exception as e:
        print(f"General Error in change_metadata: {e}")
        return False
