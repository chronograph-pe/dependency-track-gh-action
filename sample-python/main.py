requests


def main():
    bom = read_bom()
    
    components = get_components(bom)


def read_bom():
    with open ("bom.xml", "r") as f:
        data = f.read()

    return xmltodict.parse(data)

def get_components(bom):
    components = bom["bom"]["components"]["component"]
    for component in components:
        print(component)
        print()
        

if __name__ == "__main__":
    main()
