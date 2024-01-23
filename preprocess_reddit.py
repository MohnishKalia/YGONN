import json
import os


def replace_crlf(str):
    return str.replace("\n", " ").replace("\r", " ")

def recurse_replies(dst, replies):
    # no replies is empty string, kick out exec
    if (type(replies) == str): return

    for comment in replies["data"]["children"]:
        if comment["data"]["author"] != "YugiohLinkBot" and comment["data"]["body"] != "[deleted]":
            dst.write(replace_crlf(comment["data"]["body"]))
            dst.write("\n")
            recurse_replies(dst, comment["data"]["replies"])

output_filepath = os.path.join(os.getcwd(), "reddit_complex.txt");

# remove output if already exists
os.unlink(output_filepath)

for filename in os.listdir("./reddit_posts"):
   with open(os.path.join(os.getcwd(), "reddit_posts", filename), 'rt') as src: # open in readonly mode
        with open(output_filepath, 'at', newline='\n') as dst: # open in readonly mode
            post = json.load(src)
            dst.write(replace_crlf(post[0]["data"]["children"][0]["data"]["selftext"]))
            dst.write("\n")
            for comment in post[1]["data"]["children"]:
                if comment["data"]["author"] != "YugiohLinkBot" and comment["data"]["body"] != "[deleted]":
                    dst.write(replace_crlf(comment["data"]["body"]))
                    dst.write("\n")
                    recurse_replies(dst, comment["data"]["replies"])
