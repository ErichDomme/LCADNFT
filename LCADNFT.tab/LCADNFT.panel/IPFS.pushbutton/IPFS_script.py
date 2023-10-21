import clr

clr.AddReference("System")
clr.AddReference("System.IO")
clr.AddReference("System.Net")

from System import Uri
from System.Net import HttpWebRequest
from System.Text import Encoding
from System.IO import FileStream, FileMode

# Define IPFS API endpoint
ipfs_api_url = "http://127.0.0.1:5001/api/v0/add"

# Open the file you want to add to IPFS
file_path = "path_to_your_file.txt"
with FileStream(file_path, FileMode.Open) as file_stream:

    # Create an HTTP request
    request = HttpWebRequest.Create(Uri(ipfs_api_url))
    request.Method = "POST"
    request.ContentType = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"  # Adjust boundary as needed

    # Here you'd construct the request body to contain your file's binary data
    # (this is a bit more complex due to the multipart/form-data format)
    # This is just a basic example; you might need to modify it based on your exact needs.
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    header = '--{0}\r\nContent-Disposition: form-data; name="file"; filename="{1}"\r\nContent-Type: application/octet-stream\r\n\r\n'.format(
        boundary, file_path
    )
    footer = "\r\n--{0}--\r\n".format(boundary)

    # Convert header and footer to bytes
    header_bytes = Encoding.ASCII.GetBytes(header)
    footer_bytes = Encoding.ASCII.GetBytes(footer)

    request.ContentLength = (
        header_bytes.Length + file_stream.Length + footer_bytes.Length
    )

    # Write the data to request stream
    with request.GetRequestStream() as request_stream:
        request_stream.Write(header_bytes, 0, header_bytes.Length)
        clr.System.IO.Stream.CopyTo(file_stream, request_stream)
        request_stream.Write(footer_bytes, 0, footer_bytes.Length)

    # Send the request and read the response
    response = request.GetResponse()
    response_stream = response.GetResponseStream()
    reader = clr.System.IO.StreamReader(response_stream)
    result = reader.ReadToEnd()

    print(result)
