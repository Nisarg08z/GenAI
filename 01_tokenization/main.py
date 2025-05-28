import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "hello, i am nisarg"
token = enc.encode(text)

print("token: ", token)

tokens = [24912, 11, 575, 939, 55609, 1170]
decoded = enc.decode(tokens)
print("decoded: ", decoded)