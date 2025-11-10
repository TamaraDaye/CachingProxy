This a CLI tool that starts a caching proxy server,
it forwards requests to the actual server and caches
responses if the same request is made again the cache
returns the response


Requirements
Users can start the proxy server by running 
caching-proxy --port <number> --origin <url>

--port is the port in which the caching proxy runs
--origin is the url that is being reverse proxied

Example
caching-proxy --port 3000 --origin http://example.com


The caching proxy server will start on port 3000 and forward each request
to 'www.example.com'


The user makes a request to http://localhost:3000/products, 
The caching proxy server should forward the request to http://dummyjson.com/products,
return the response along with headers and cache the response.
Also, add the headers to the response that indicate whether the response is from the cache or the server.


everything written with low level sockets
