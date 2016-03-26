from struct import Struct


chunk = Struct('<4si')

def chunks(data):
  counter, filesize = 0, len(data)
  while counter < filesize:
    magic, size = chunk.unpack_from(data, counter)
    counter += chunk.size
    contents = data[counter:counter+size]
    yield magic, size, contents
    counter += size
