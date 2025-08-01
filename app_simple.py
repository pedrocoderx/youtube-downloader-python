#!/usr/bin/env python3
"""
Enhanced YouTube Video Downloader - Web App
Flask-based web application with folder selection, quality options, and optimized downloads
"""

from flask import Flask, render_template, request, jsonify
import subprocess
import json
import os
import re
import threading
import time
from datetime import datetime
import urllib.parse
import glob

app = Flask(__name__)

# Global variables for download tracking
download_progress = {}
download_status = {}

class EnhancedYouTubeDownloader:
    def __init__(self):
        # Use /tmp for cloud deployments, fallback to Downloads for local
        if os.path.exists('/tmp'):
            self.download_path = "/tmp"
        else:
            self.download_path = os.path.expanduser("~/Downloads")
        self.ffmpeg_available = self.check_ffmpeg()
        
    def check_ffmpeg(self):
        """Check if FFmpeg is available in the system"""
        try:
            # Try the standard PATH first
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True
        except:
            pass
        
        # Try common FFmpeg installation paths on Windows
        ffmpeg_paths = [
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe",
            os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg.exe")
        ]
        
        for path in ffmpeg_paths:
            try:
                if os.path.exists(path):
                    result = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        # Store the path for later use
                        self.ffmpeg_path = path
                        return True
            except:
                continue
        
        return False
    
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+'
        ]
        
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    def sanitize_filename(self, filename):
        """Sanitize filename for safe file system usage"""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename.strip()
    
    def merge_with_ffmpeg(self, video_file, audio_file, output_file):
        """Merge video and audio files using FFmpeg"""
        try:
            # First, let's check if the files exist
            if not os.path.exists(video_file):
                print(f"Video file not found: {video_file}")
                return False
            if not os.path.exists(audio_file):
                print(f"Audio file not found: {audio_file}")
                return False
                
            print(f"Video file: {video_file} (size: {os.path.getsize(video_file)} bytes)")
            print(f"Audio file: {audio_file} (size: {os.path.getsize(audio_file)} bytes)")
            
            # Use stored FFmpeg path if available, otherwise use the specific path
            ffmpeg_cmd = getattr(self, 'ffmpeg_path', r"C:\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe")
            
            # Use a more robust FFmpeg command
            cmd = [
                ffmpeg_cmd,
                "-i", video_file,
                "-i", audio_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-strict", "experimental",
                "-y",  # Overwrite output file
                output_file
            ]
            
            print(f"Running FFmpeg command: {' '.join(cmd)}")
            
            # Run FFmpeg with timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            print(f"FFmpeg return code: {result.returncode}")
            if result.stdout:
                print(f"FFmpeg stdout: {result.stdout}")
            if result.stderr:
                print(f"FFmpeg stderr: {result.stderr}")
            
            if result.returncode == 0:
                # Check if output file was created
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    print(f"✅ Successfully merged to: {output_file}")
                    return True
                else:
                    print(f"❌ Output file not created or empty: {output_file}")
                    return False
            else:
                print(f"❌ FFmpeg failed with return code: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ FFmpeg merge timed out")
            return False
        except Exception as e:
            print(f"❌ FFmpeg merge error: {e}")
            return False
        
    def get_video_info(self, url):
        """Get video information using yt-dlp with enhanced quality detection"""
        try:
            cmd = [
                "py", "-m", "yt_dlp",
                "--dump-json",
                "--no-playlist",
                "--format-sort", "res,fps,codec:h264",
                "--no-warnings",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "--extractor-args", "youtube:player_client=web",
                "--extractor-args", "youtube:player_skip=webpage",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                # Try with a different approach if the first attempt fails
                print("First attempt failed, trying alternative approach...")
                alt_cmd = [
                    "py", "-m", "yt_dlp",
                    "--dump-json",
                    "--no-playlist",
                    "--format-sort", "res,fps,codec:h264",
                    "--no-warnings",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "--extractor-args", "youtube:player_client=android",
                    url
                ]
                
                result = subprocess.run(alt_cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    raise Exception(f"yt-dlp error: {result.stderr}")
            
            video_data = json.loads(result.stdout)
            

            
            # Extract quality options with better filtering
            formats = video_data.get('formats', [])
            quality_options = []
            
            # Process all formats
            for fmt in formats:
                height = fmt.get('height', 0)
                filesize = fmt.get('filesize', 0)
                fps = fmt.get('fps', 0)
                vcodec = fmt.get('vcodec', 'none')
                acodec = fmt.get('acodec', 'none')
                format_id = fmt.get('format_id', '')
                
                # Only include formats with video
                if vcodec != 'none':
                    size_mb = filesize / (1024 * 1024) if filesize else 0
                    
                    # Create display name
                    if height:
                        display_name = f"{height}p"
                        if fps and fps > 0:
                            display_name += f"@{fps}fps"
                    else:
                        display_name = "Unknown quality"
                    
                    quality_options.append({
                        'format_id': format_id,
                        'height': int(height) if height else 0,
                        'fps': int(fps) if fps else 0,
                        'size_mb': size_mb,
                        'display': display_name,
                        'is_combined': acodec != 'none',
                        'vcodec': vcodec,
                        'acodec': acodec
                    })
            
            # Add audio-only option
            audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
            if audio_formats:
                best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) if x.get('abr') else 0)
                quality_options.append({
                    'format_id': best_audio.get('format_id', ''),
                    'height': 0,
                    'fps': 0,
                    'size_mb': best_audio.get('filesize', 0) / (1024 * 1024) if best_audio.get('filesize') else 0,
                    'display': f"Audio Only ({best_audio.get('abr', 0)}kbps)",
                    'is_combined': False,
                    'vcodec': 'none',
                    'acodec': best_audio.get('acodec', 'none')
                })
            
            # Remove duplicates and sort by quality (best to worst)
            unique_qualities = {}
            for quality in quality_options:
                key = f"{quality['height']}_{quality['fps']}"
                if key not in unique_qualities:
                    unique_qualities[key] = quality
            
            quality_options = sorted(unique_qualities.values(), 
                                  key=lambda x: (x['height'], x['fps']), reverse=True)
            
            title = video_data.get('title', 'Unknown')
            
            return {
                'success': True,
                'title': title,
                'duration': video_data.get('duration', 0),
                'view_count': video_data.get('view_count', 0),
                'uploader': video_data.get('uploader', 'Unknown'),
                'thumbnail': video_data.get('thumbnail', ''),
                'qualities': quality_options
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_video(self, url, quality_format_id, download_path, download_id):
        """Download video with exact quality and merge with audio using FFmpeg"""
        try:
            # Set initial progress
            download_progress[download_id] = 0
            download_status[download_id] = {'status': 'downloading'}
            
            # Get video title for filename using the same method as get_video_info
            cmd = [
                "py", "-m", "yt_dlp",
                "--dump-json",
                "--no-playlist",
                "--no-warnings",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "--extractor-args", "youtube:player_client=web",
                "--extractor-args", "youtube:player_skip=webpage",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                # Try with android client as fallback
                alt_cmd = [
                    "py", "-m", "yt_dlp",
                    "--dump-json",
                    "--no-playlist",
                    "--no-warnings",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "--extractor-args", "youtube:player_client=android",
                    url
                ]
                
                result = subprocess.run(alt_cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    video_title = "youtube_video"
                else:
                    video_data = json.loads(result.stdout)
                    video_title = video_data.get('title', 'youtube_video')
                    video_title = self.sanitize_filename(video_title)
            else:
                video_data = json.loads(result.stdout)
                video_title = video_data.get('title', 'youtube_video')
                video_title = self.sanitize_filename(video_title)
            
            if quality_format_id == "0" or quality_format_id == 0:
                # Audio only download
                cmd = [
                    "py", "-m", "yt_dlp",
                    "-f", "bestaudio",
                    "-o", f"{video_title}.%(ext)s",
                    "--no-playlist",
                    "--no-warnings",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--ffmpeg-location", "C:\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    url
                ]
                
                print(f"Starting audio download: {' '.join(cmd)}")
                
                # Run audio download
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=download_path)
                
                # Monitor progress
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(f"Audio download: {output.strip()}")
                        download_progress[download_id] = min(download_progress[download_id] + 10, 90)
                
                return_code = process.wait()
                
                if return_code == 0:
                    # Find the downloaded audio file
                    files = [f for f in os.listdir(download_path) if f.startswith(video_title) and f.endswith('.mp3')]
                    if files:
                        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_path, x)))
                        file_path = os.path.join(download_path, latest_file)
                        
                        download_progress[download_id] = 100
                        download_status[download_id] = {
                            'status': 'completed',
                            'file_path': file_path,
                            'filename': latest_file
                        }
                        print(f"✅ Audio download completed: {file_path}")
                    else:
                        download_status[download_id] = {'status': 'error', 'error': 'No audio file found'}
                else:
                    stderr_output = process.stderr.read()
                    download_status[download_id] = {'status': 'error', 'error': f"Audio download failed: {stderr_output}"}
                
            else:
                # Video download with FFmpeg merging
                print(f"Starting video download in quality {quality_format_id} with FFmpeg merging...")
                
                # Download video in exact quality
                video_cmd = [
                    "py", "-m", "yt_dlp",
                    "-f", str(quality_format_id),
                    "-o", f"{video_title}_video.%(ext)s",
                    "--no-playlist",
                    "--no-warnings",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    url
                ]
                
                # Download audio
                audio_cmd = [
                    "py", "-m", "yt_dlp",
                    "-f", "bestaudio",
                    "-o", f"{video_title}_audio.%(ext)s",
                    "--no-playlist",
                    "--no-warnings",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--ffmpeg-location", "C:\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe",
                    "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    url
                ]
                
                print(f"Video command: {' '.join(video_cmd)}")
                print(f"Audio command: {' '.join(audio_cmd)}")
                
                # Download video first
                download_progress[download_id] = 10
                video_process = subprocess.Popen(video_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=download_path)
                
                while True:
                    output = video_process.stdout.readline()
                    if output == '' and video_process.poll() is not None:
                        break
                    if output:
                        print(f"Video download: {output.strip()}")
                        download_progress[download_id] = min(download_progress[download_id] + 5, 40)
                
                video_return = video_process.wait()
                
                if video_return == 0:
                    # Download audio
                    download_progress[download_id] = 45
                    audio_process = subprocess.Popen(audio_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=download_path)
                    
                    while True:
                        output = audio_process.stdout.readline()
                        if output == '' and audio_process.poll() is not None:
                            break
                        if output:
                            print(f"Audio download: {output.strip()}")
                            download_progress[download_id] = min(download_progress[download_id] + 5, 80)
                    
                    audio_return = audio_process.wait()
                    
                    if audio_return == 0:
                        # Find downloaded files
                        video_files = [f for f in os.listdir(download_path) if f.startswith(f"{video_title}_video")]
                        audio_files = [f for f in os.listdir(download_path) if f.startswith(f"{video_title}_audio")]
                        
                        if video_files and audio_files:
                            video_file = os.path.join(download_path, video_files[0])
                            audio_file = os.path.join(download_path, audio_files[0])
                            output_file = os.path.join(download_path, f"{video_title}.mp4")
                            
                            print(f"Found video: {video_file}")
                            print(f"Found audio: {audio_file}")
                            
                            # Merge with FFmpeg
                            download_progress[download_id] = 85
                            if self.merge_with_ffmpeg(video_file, audio_file, output_file):
                                download_progress[download_id] = 100
                                download_status[download_id] = {
                                    'status': 'completed',
                                    'file_path': output_file,
                                    'filename': f"{video_title}.mp4"
                                }
                                print(f"✅ Video download and merge completed: {output_file}")
                                
                                # Clean up separate files
                                try:
                                    os.remove(video_file)
                                    os.remove(audio_file)
                                    print("✅ Cleaned up separate files")
                                except:
                                    pass
                            else:
                                download_status[download_id] = {'status': 'error', 'error': 'FFmpeg merge failed'}
                        else:
                            download_status[download_id] = {'status': 'error', 'error': f'Missing files. Video: {video_files}, Audio: {audio_files}'}
                    else:
                        stderr = audio_process.stderr.read()
                        download_status[download_id] = {'status': 'error', 'error': f"Audio download failed: {stderr}"}
                else:
                    stderr = video_process.stderr.read()
                    download_status[download_id] = {'status': 'error', 'error': f"Video download failed: {stderr}"}
            
        except Exception as e:
            print(f"Download exception: {str(e)}")
            download_status[download_id] = {'status': 'error', 'error': str(e)}

# Initialize downloader
downloader = EnhancedYouTubeDownloader()

# Show FFmpeg status
if downloader.ffmpeg_available:
    print("✅ FFmpeg is available - will use separate video/audio downloads with merging")
else:
    print("⚠️  FFmpeg not found - will download single files with audio included")

@app.route('/')
def index():
    """Main page"""
    return render_template('index_simple.html')

@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """Get video information API endpoint"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'Please provide a URL'})
    
    if not downloader.is_valid_youtube_url(url):
        return jsonify({'success': False, 'error': 'Please provide a valid YouTube URL'})
    
    result = downloader.get_video_info(url)
    return jsonify(result)

@app.route('/api/download', methods=['POST'])
def start_download():
    """Start download API endpoint with default path"""
    data = request.get_json()
    url = data.get('url', '').strip()
    quality_format_id = data.get('quality_format_id')
    
    if not url or quality_format_id is None:
        return jsonify({'success': False, 'error': 'Missing required parameters'})
    
    # Always use default Downloads folder
    download_path = downloader.download_path
    
    # Generate unique download ID
    download_id = f"download_{int(time.time())}"
    
    # Start download in background thread
    thread = threading.Thread(
        target=downloader.download_video,
        args=(url, quality_format_id, download_path, download_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'download_id': download_id,
        'download_path': download_path
    })

@app.route('/api/progress/<download_id>')
def get_progress(download_id):
    """Get download progress API endpoint"""
    progress = download_progress.get(download_id, 0)
    status = download_status.get(download_id, {'status': 'unknown'})
    
    return jsonify({
        'progress': progress,
        'status': status
    })

if __name__ == '__main__':
    # Use environment variable for port if available, otherwise default to 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 