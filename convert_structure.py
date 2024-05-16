import os
import yaml

def parse_key(key):
    # Split the key into parts based on '-'
    parts = key.split('-')
    # Determine the section and sub-section based on the parts
    section = parts[0]
    subsection = parts[1]
    attribute = '-'.join(parts[2:])
    return section, subsection, attribute

def convert_to_nested(data):
    nested = {'title': data.get('title', 'No Title')}
    # Remove the title from processing
    if 'title' in data:
        del data['title']
    
    for key, value in data.items():
        section, subsection, attribute = parse_key(key)
        if section not in nested:
            nested[section] = {}
        if subsection not in nested[section]:
            nested[section][subsection] = {}
        
        # Check for a license for this attribute
        license_key = f"{section}-{subsection}-{attribute}-license"
        if attribute.endswith('license'):
            continue  # skip the direct assignment of licenses here
        
        # Prepare value and license structure
        nested[section][subsection][attribute] = {'value': value}
        if license_key in data:
            nested[section][subsection][attribute]['license'] = data[license_key]

    return nested

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.yaml') or filename.endswith('.yml') or filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                try:
                    data = yaml.load_all(file, yaml.FullLoader)
                    data = [x for x in data][0]
                    nested_data = convert_to_nested(data)
                    new_filepath = os.path.join(directory, f'converted_{filename}')
                    with open(new_filepath, 'w') as new_file:
                        yaml.dump(nested_data, new_file, default_flow_style=False, sort_keys=False)
                    print(f'Processed and saved: {new_filepath}')
                except yaml.YAMLError as exc:
                    print(f"Error processing {filename}: {exc}")

# Specify the directory containing the YAML or Markdown files
directory = '_llms'
process_directory(directory)
