import json

def convert_to_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        idioms = []
        idiom = {}
        for line in lines:
            line = line.strip()
            if line == '':
                if idiom:
                    idioms.append(idiom)
                    idiom = {}
            elif line.startswith('Context:'):
                idiom['context'] = line[8:].strip().split(',')
            else:
                idiom['phrase'] = line

        if idiom:  # add the last idiom if it exists
            idioms.append(idiom)

        with open('idioms.json', 'w', encoding='utf-8') as file:
            json.dump({'idioms': idioms}, file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")

convert_to_json('idioms.txt')


# import json

# def convert_to_json(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     idioms = []
#     idiom = {}
#     for line in lines:
#         line = line.strip()
#         if line == '':
#             if idiom:
#                 idioms.append(idiom)
#                 idiom = {}
#         elif line.startswith('Context:'):
#             idiom['context'] = line[8:].strip()
#         else:
#             idiom['phrase'] = line

#     if idiom:  # add the last idiom if it exists
#         idioms.append(idiom)

#     with open('idioms.json', 'w') as file:
#         json.dump({'idioms': idioms}, file, indent=4)

# convert_to_json('idioms.txt')