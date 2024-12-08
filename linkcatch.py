import re

def is_link(text: str) -> bool:
    pattern = r"(https|http)(://)(www\.)?([A-z0-9]+\.)([A-z0-9])"

    if re.search(pattern=pattern, string=text) is None:
        pattern = r"(https|http)?(://)?(www\.)([A-z0-9]+\.)([A-z0-9])"

        if re.search(pattern=pattern, string=text) is None:
            pattern = r"([A-z0-9]+\.)(com|dev|org|gg)"

            if re.search(pattern=pattern, string=text) is None:
                return False
    
    return True

if __name__ == "__main__":
    text: str = """Hello My name Is Moatasem and I have This Server discord.gg/hello
     and my protofolio www.moatasem.com
     welcome to https://pythex.org"""
    print(is_link(text))

