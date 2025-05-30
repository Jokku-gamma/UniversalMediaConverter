from moviepy.editor import AudioFileClip, VideoFileClip
import tempfile
def convert_media(inp,out,is_video=False):
    try:
        if is_video:
            clip=VideoFileClip(inp)
            audio=clip.audio
        else:
            audio=AudioFileClip(inp)
        outpath=tempfile.mktemp(suffix=f'.{out}')
        audio.write_audiofile(outpath,logger=None)
        audio.close()
        if is_video:
            clip.close()
        return outpath
    except Exception as e:
        print(f"Error converting media: {e}")
        return None