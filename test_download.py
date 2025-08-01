#!/usr/bin/env python3
"""
Test script to verify yt-dlp download functionality
"""

import subprocess
import os
import json

def test_yt_dlp():
    """Test if yt-dlp can download a video"""
    
    # Test URL (Rick Astley - Never Gonna Give You Up)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🎬 Testing yt-dlp download functionality")
    print("=" * 50)
    
    # Test 1: Get video info
    print("\n1. Testing video info retrieval...")
    try:
        cmd = [
            "py", "-m", "yt_dlp",
            "--dump-json",
            "--no-playlist",
            test_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            video_data = json.loads(result.stdout)
            print(f"✅ Video info retrieved successfully!")
            print(f"   Title: {video_data.get('title', 'Unknown')}")
            print(f"   Duration: {video_data.get('duration', 0)} seconds")
            print(f"   Uploader: {video_data.get('uploader', 'Unknown')}")
        else:
            print(f"❌ Failed to get video info: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting video info: {str(e)}")
        return False
    
    # Test 2: Download a small video
    print("\n2. Testing video download...")
    try:
        # Create test directory
        test_dir = "test_downloads"
        os.makedirs(test_dir, exist_ok=True)
        
        # Download with low quality for speed
        cmd = [
            "py", "-m", "yt_dlp",
            "-f", "worst[height<=360]",  # Low quality for faster download
            "-o", os.path.join(test_dir, "test_video.%(ext)s"),
            "--no-playlist",
            test_url
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        print(f"Download result: {result.returncode}")
        print(f"Download stdout: {result.stdout}")
        print(f"Download stderr: {result.stderr}")
        
        if result.returncode == 0:
            # Check if file was downloaded
            files = os.listdir(test_dir)
            video_files = [f for f in files if f.startswith("test_video.")]
            
            if video_files:
                print(f"✅ Download successful! File: {video_files[0]}")
                print(f"   File size: {os.path.getsize(os.path.join(test_dir, video_files[0]))} bytes")
                
                # Clean up
                for file in video_files:
                    os.remove(os.path.join(test_dir, file))
                os.rmdir(test_dir)
                
                return True
            else:
                print("❌ Download completed but no file found")
                return False
        else:
            print(f"❌ Download failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during download: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_yt_dlp()
    if success:
        print("\n🎉 All tests passed! yt-dlp is working correctly.")
    else:
        print("\n❌ Tests failed. There might be an issue with yt-dlp.") 