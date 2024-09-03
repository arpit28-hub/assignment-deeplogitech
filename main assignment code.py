# **************Steps of the Algorithm******************
# S1-Fetch the HTML content of the Time.com homepage
# S2-Check if the request was successful
# S3-Extract the latest stories using basic string processing
# S4-Find the start of the story title
# S5-Extract the story title and link
# S6-Convert the stories to JSON format 



import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_time_stories():
    response = requests.get('https://time.com/')
    
    if response.status_code != 200:
        print(f"Failed to retrieve content, status code: {response.status_code}")
        return []
    
    html_content = response.text

    stories = []
    start_marker = '<h3 class="latest-stories__item-headline">'
    end_marker = '</h3>'
    current_index = 0

    while len(stories) < 6:
        start_index = html_content.find(start_marker, current_index)
        if start_index == -1:
            break
        
        start_index += len(start_marker)
        end_index = html_content.find(end_marker, start_index)
        if end_index == -1:
            break
        
        title_html = html_content[start_index:end_index]
        title_start = title_html.find('">') + 2
        title_end = title_html.find('</a>')
        title = title_html[title_start:title_end].strip()
        
        link_start = title_html.find('href="') + 6
        link_end = title_html.find('">', link_start)
        link = "https://time.com" + title_html[link_start:link_end].strip()
        
        stories.append({
            "title": title,
            "link": link
        })
        
        current_index = end_index

    return stories

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            stories = get_time_stories()
            
            json_response = json.dumps(stories, indent=4)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            
            self.wfile.write(json_response.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
#OUTPUT JSON URL: http://localhost:8000/getTimeStories
