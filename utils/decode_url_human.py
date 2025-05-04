import urllib.parse


encode_url = r'https://infra.ai-augmented.com/api/auth/cas/login?school_certify=10497&client_id=xy_client_whut&state=9anva5&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback&response_type=code&week_no_login_status=0&scope=&next=https%3A%2F%2Finfra.ai-augmented.com%2Fapp%2Fauth%2Foauth2%2FsecurityNotice%3Fresponse_type%3Dcode%26state%3D9anva5%26client_id%3Dxy_client_whut%26redirect_uri%3Dhttps%3A%2F%2Fwhut.ai-augmented.com%2Fapi%2Fjw-starcmooc%2Fuser%2FauthorCallback%26school%3D10497%26lang%3Dzh_CN&back=https%3A%2F%2Finfra.ai-augmented.com%2Fapp%2Fauth%2Foauth2%2Flogin%3Fresponse_type%3Dcode%26state%3D9anva5%26client_id%3Dxy_client_whut%26redirect_uri%3Dhttps%3A%2F%2Fwhut.ai-augmented.com%2Fapi%2Fjw-starcmooc%2Fuser%2FauthorCallback%26school%3D10497%26lang%3Dzh_CN'


decoded_url = urllib.parse.unquote(encode_url)
parsed_url = urllib.parse.urlparse(decoded_url)


print("\nBase URL:")
print(f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}")


print("\nQuery parameters:")
query_params = urllib.parse.parse_qs(parsed_url.query)
for key, value in query_params.items():
    print(f"\033[32m{key}\033[0m: {value[0]}")