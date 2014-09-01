import values

x = values.Values()
x.transaction_id = 1234

empty_obj = x.objects.add()

obj = x.objects.add()
obj.token.discriminator = 'keys'
obj.token.keys.key_a = 1
obj.token.keys.key_b = 2
obj.token.keys.key_c = 3
obj.values[:] = [1, 2, 3, 4, 5]
obj.updated_values = '\x0e'

# human readable representation of data
print x

# this is how data can be encoded
data = x.encode('<')

from binascii import hexlify

print hexlify(data)

# this is how data can be decoded
x.decode(data, '<')
