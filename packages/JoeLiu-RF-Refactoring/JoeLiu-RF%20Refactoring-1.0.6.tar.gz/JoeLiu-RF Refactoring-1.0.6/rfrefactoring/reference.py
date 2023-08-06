class Reference:
    def __init__(self, reference, present_method, replace_method):
        self.reference = reference
        self.present_method = present_method
        self.replace_method = replace_method
    
    def get_present_value(self):
        return self.present_method(self.reference)
    
    def replace(self, old, new):
        self.replace_method(self.reference, old, new)