class APIError(Exception):
    def __init__(self, code, json):
        self.code = code
        self.status = json['status']
        self.reason = json['reason']
        
    def __str__(self):
        return self.code + ': ' + self.reason