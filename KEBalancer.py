from flask import Flask, request, jsonify
import asyncio
import aiohttp
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest, start_http_server, Summary, Counter, Histogram

app = Flask(__name__)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Number of requests processed')
ERROR_COUNT = Counter('error_count', 'Number of errors encountered')
REQUEST_IN_PROGRESS = Gauge('requests_in_progress', 'Number of requests in progress')

async def fetch(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()


async def fetch(session, url, data):
    async with session.post(url, json=data) as response:
        start_time = asyncio.get_event_loop().time()
        content_type = response.headers.get('content-type', '').lower()

        if 'application/json' in content_type:
            result = await response.json()
        else:
            # Handle unexpected content type gracefully, e.g., log the issue
            result = {'error': 'Unexpected content type', 'body': await response.text()}

        end_time = asyncio.get_event_loop().time()
        return {
            "url": url,
            "status": response.status,
            "response_time": end_time - start_time,
            "result": result
        }

async def get_response(urls, data, max_response_time):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, url, data)) for url in urls]
        longest_response = None

        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            
            for task in done:
                response_data = await task
                if response_data["status"] == 200:  # Successful response code
                    print(response_data)
                    if (longest_response is None or 
                        (response_data["response_time"] > longest_response["response_time"] and
                         response_data["response_time"] <= max_response_time)):
                        longest_response = response_data
                else:
                    continue        
        return longest_response


@app.route('/', methods=['POST'])
@REQUEST_TIME.time()
async def forward_request():
    data = request.json
    print(data)
    urls = [
        'http://localhost:3007/',
        'http://localhost:3001/',
        'http://localhost:3004/',
        # 'http://localhost:3005/',
    ]
    response = await get_response(urls, data, 10)
    return jsonify({'response': response})

@app.route("/metrics", methods=["GET"])
def metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_TIME)
    registry.register(REQUEST_COUNT)
    registry.register(ERROR_COUNT)
    registry.register(REQUEST_IN_PROGRESS)
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    import hypercorn.asyncio
    import hypercorn.config

    config = hypercorn.config.Config()
    config.bind = ["0.0.0.0:5020"]
    
    asyncio.run(hypercorn.asyncio.serve(app, config))
