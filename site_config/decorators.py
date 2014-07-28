

def determine_website(the_func):

    def _decorated(*args, **kwargs):
        print("ARRRRRRGs", kwargs)
        return the_func(*args, **kwargs)
    return _decorated