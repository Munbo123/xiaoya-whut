import json

import urllib.parse

encode_url = r'https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?code=0xbSJAVhIoCkq66266833505&state=my09pl&schoolCode=10497'

decoded_url = urllib.parse.unquote(encode_url)
parsed_url = urllib.parse.urlparse(decoded_url)

# Create a dictionary to store the parsed URL components
url_data = {
    "base_url": f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}",
    "query_parameters": {}
}

# Add query parameters to the dictionary
query_params = urllib.parse.parse_qs(parsed_url.query)
for key, value in query_params.items():
    url_data["query_parameters"][key] = value[0]

# Convert to JSON and print
json_output = json.dumps(url_data, ensure_ascii=False, indent=2)
print(json_output)