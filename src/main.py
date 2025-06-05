from texnode import TextType, TextNode

def main():
    node = TextNode("this is a link", TextType.LINK, "https://google.com")
    print(node)

if __name__ == "__main__":
    main()