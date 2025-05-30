import os
import tempfile
from flask import Flask,request,jsonify,send_file
from helpers.convert import convert_media
from helpers.download import download_file

app=Flask(__name__)
def safe_delete(path):
    if path and os.path.exists(path) and os.path.isfile(path):
        try:
            os.unlink(path)
        except Exception as e:
            print(f"Warning: Could not delete file {path}: {str(e)}")

@app.route('/convert/url/audio',methods=['POST'])
def url_a2a():
    inp=out=None
    data=request.json
    url=data.get('url')
    outformat=data.get('output_format')
    if not url or not outformat:
        return jsonify({'error':'Missing URL or output format'}),400
    try:
        inp=download_file(url)
        out=convert_media(inp,outformat)
        return send_file(out,as_attachment=True,download_name=f"converted.{outformat}")
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:
        safe_delete(inp)
        safe_delete(out)
@app.route('/convert/url/video',methods=['POST'])
def url_v2a():
    inp=out=None

    data=request.json
    url=data.get('url')
    outformat=data.get('output_format')
    if not url or not outformat:
        return jsonify({'error':'Missing URL or output format'}),400
    try:
        inp=download_file(url)
        out=convert_media(inp,outformat,is_video=True)
        return send_file(out,as_attachment=True,download_name=f"converted.{outformat}")
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:
        safe_delete(inp)
        safe_delete(out)

@app.route('/convert/upload/audio',methods=['POST'])
def upload_a2a():
    inp=outpath=None
    if 'file' not in request.files:
        return jsonify({'error':'No files provided'}),400
    file=request.files['file']
    outformat=request.form.get('output_format')
    if not outformat:
        return jsonify({'error':'Missing output format'}),400
    try:
        _,ext=os.path.splitext(file.filename)
        with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as temp_file:
            file.save(temp_file.name)
            inp=temp_file.name
        
        outpath=convert_media(inp,outformat)
        return send_file(outpath,as_attachment=True,download_name=f"converted.{outformat}")
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:   
        safe_delete(inp)
        safe_delete(outpath)

@app.route('/convert/upload/video',methods=['POST'])
def upload_v2a():
    inp=outpath=None
    if 'file' not in request.files:
        return jsonify({'error':'No files provided'}),400
    file=request.files['file']
    outformat=request.form.get('output_format')
    if not outformat:
        return jsonify({'error':'Missing output format'}),400
    try:
        _,ext=os.path.splitext(file.filename)
        with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as temp_file:
            file.save(temp_file.name)
            inp=temp_file.name
        
        outpath=convert_media(inp,outformat,is_video=True)
        return send_file(outpath,as_attachment=True,download_name=f"converted.{outformat}")
    except Exception as e:
        return jsonify({'error':str(e)}),500
    finally:   
        safe_delete(inp)
        safe_delete(outpath)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
