from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import base64
import io
import mimetypes

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <h1>Image to Base64 Converter</h1>
            <form action="/upload-image" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*">
                <input type="submit" value="Upload Image">
            </form>
            <br>
            <h1>Base64 to Image Converter</h1>
            <form action="/convert-base64-to-image" method="post">
                <textarea name="base64_string" rows="10" cols="50"></textarea>
                <br>
                <input type="submit" value="Convert to Image">
            </form>
        </body>
    </html>
    """

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    mime_type = file.content_type
    base64_encoded_data = base64.b64encode(content)
    base64_string = base64_encoded_data.decode('utf-8')
    
    base64_with_mime = f"data:{mime_type};base64,{base64_string}"
    
    return HTMLResponse(content=f"""
    <html>
        <body>
            <h1>Image to Base64 Converter</h1>
            <form action="/upload-image" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*">
                <input type="submit" value="Upload Image">
            </form>
            <br>
            <h1>Base64 to Image Converter</h1>
            <form action="/convert-base64-to-image" method="post">
                <textarea name="base64_string" rows="10" cols="50">{base64_with_mime}</textarea>
                <br>
                <input type="submit" value="Convert to Image">
            </form>
        </body>
    </html>
    """)

@app.post("/convert-base64-to-image")
async def convert_base64_to_image(base64_string: str = Form(...)):
    try:
        # Check if the base64 string includes MIME type data
        if base64_string.startswith('data:'):
            mime_type, base64_string = base64_string.split(';base64,', 1)
        else:
            mime_type = 'image/png'  # Default MIME type if not specified
        
        # Decode the base64 string
        base64_decoded_data = base64.b64decode(base64_string)
        image_stream = io.BytesIO(base64_decoded_data)
        
        # Determine the file extension based on MIME type
        extension = mimetypes.guess_extension(mime_type)
        if extension is None:
            extension = '.png'  # Default to PNG if MIME type is unknown
        
        headers = {
            'Content-Disposition': f'attachment; filename="output{extension}"'
        }
        return StreamingResponse(image_stream, media_type=mime_type, headers=headers)
    except Exception as e:
        return HTMLResponse(content=f"An error occurred: {str(e)}", status_code=400)
