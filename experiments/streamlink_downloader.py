import streamlink
import subprocess
import os
import time
from pathlib import Path
from datetime import datetime

class TwitchStreamRecorder:
    """Record Twitch streams in 15-second segments."""
    
    def __init__(self, channel_url):
        """
        Initialize the recorder.
        
        Args:
            channel_url: Twitch channel URL (e.g., 'https://twitch.tv/channelname')
        """
        self.channel_url = channel_url
        self.channel_name = channel_url.rstrip('/').split('/')[-1]
        
        # Create subfolder in current directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(os.getcwd()) / f"{self.channel_name}_{timestamp}"
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"Output directory: {self.output_dir}")
        
        self.segment_count = 0
        self.is_recording = False
    
    def get_stream_url(self):
        """Get the direct stream URL."""
        try:
            streams = streamlink.streams(self.channel_url)
            
            if not streams:
                print("Stream is offline or not found")
                return None
            
            # Use worst quality for speed
            if 'worst' in streams:
                return streams['best'].url
            else:
                return streams[list(streams.keys())[0]].url
                
        except Exception as e:
            print(f"Error getting stream: {e}")
            return None
    
    def record_segments(self):
        """Record stream in 15-second segments continuously."""
        stream_url = self.get_stream_url()
        
        if not stream_url:
            return
        
        print(f"Starting segmented recording...")
        print(f"Segment duration: 15 seconds")
        print(f"Press Ctrl+C to stop\n")
        
        self.is_recording = True
        
        try:
            while self.is_recording:
                self.segment_count += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                video_file = self.output_dir / f"segment_{self.segment_count:05d}_{timestamp}.mp4"
                audio_file = self.output_dir / f"segment_{self.segment_count:05d}_{timestamp}.mp3"
                
                print(f"Recording segment {self.segment_count}...")
                
                # Record video + audio
                video_cmd = [
                    'ffmpeg',
                    '-i', stream_url,
                    '-t', '15',  # 15 seconds
                    '-c', 'copy',  # Copy streams (fastest, no re-encoding)
                    '-y',  # Overwrite
                    str(video_file)
                ]
                
                # Record audio only
                audio_cmd = [
                    'ffmpeg',
                    '-i', stream_url,
                    '-t', '15',
                    '-vn',  # No video
                    '-acodec', 'libmp3lame',
                    '-ab', '64k',  # Low bitrate for speed
                    '-y',
                    str(audio_file)
                ]
                
                # Run both in parallel for speed
                video_proc = subprocess.Popen(video_cmd, 
                                             stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL)
                audio_proc = subprocess.Popen(audio_cmd, 
                                             stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL)
                
                # Wait for both to complete
                video_proc.wait()
                audio_proc.wait()
                
                print(f"✓ Segment {self.segment_count} saved")
                
        except KeyboardInterrupt:
            print("\n\nRecording stopped by user")
            self.is_recording = False
        except Exception as e:
            print(f"Error during recording: {e}")
            self.is_recording = False
        
        print(f"\nTotal segments recorded: {self.segment_count}")
        print(f"Files saved in: {self.output_dir}")


# Usage example
if __name__ == "__main__":
    # Replace with your Twitch channel URL
    channel = "https://twitch.tv/danmanplayz"
    
    recorder = TwitchStreamRecorder(channel)
    recorder.record_segments()