

class Record:
    timestamp: int

    response_time_ns: int
    response_process_time_ns: int

    has_exception: bool

    request_method: str
    url: str
    query_string: str
    request_headers: str
    path: str
    remote_addr: str

    status_code: str
    response_headers: str
    trace: str
