import html2text
import io
import os

h2t = html2text.HTML2Text()
h2t.ignore_links = True

input_handle = os.path.abspath('./docs/_build/html/README.html')
input_file_desc = io.open(input_handle, mode='rb')
read_into_buffer = input_file_desc.read()
input_file_desc.close()

parsed_contents = h2t.handle(read_into_buffer.decode('utf_8'))
safe_text = parsed_contents.encode('ascii', 'ignore')

out_file_buffer = io.open(os.path.abspath('./docs/_build/README_OUT.md'), mode='wb')
out_file_buffer.write(safe_text)
out_file_buffer.close()
