"""
contrived file i/o helpers, james anderson 2015
"""
def load(fn):
  """
  return the contents of a file as a str
  """
  with open(fn, mode='rb') as f: return f.read()

def save(fn, content):
  """
  saves the specified contents to the specified filename
  """
  with open(fn, mode='wb') as f:
    f.write(content)
