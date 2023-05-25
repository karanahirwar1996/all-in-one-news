def short_link(link):
    import urllib.parse
    import urllib.request
    endpoint = 'http://tinyurl.com/api-create.php'
    long_url = link
    params = {'url': long_url}
    encoded_params = urllib.parse.urlencode(params).encode('utf-8')
    response = urllib.request.urlopen(endpoint + '?' + encoded_params.decode('utf-8'))
    if response.status == 200:
        short_url = response.read().decode('utf-8')
        return short_url
    else:
        return link
