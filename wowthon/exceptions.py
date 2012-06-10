class APIError(Exception):
    """
    Raised when an invalid API request is made.
    
    """
    def __init__(self, code, json):
        self.code = code
        self.status = json['status']
        self.reason = json['reason']
        
    def __str__(self):
        return str(self.code) + ': ' + self.reason
        
    def __repr__(self):
        return 'APIError <' + str(self) + '>'