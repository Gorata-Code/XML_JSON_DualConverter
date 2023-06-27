import os
import sys
import json
from xml.etree import ElementTree as elementTree


def dict_types_files_converter(file_name: str) -> None:

    """
    The entry point of our script. Reads a file and converts it to the opposite format based on its current format
    :param file_name: The file to be read and converted
    :return: None
    """

    print(f'\n\tReading your {os.path.splitext(file_name)[-1][1:].upper()} file...')

    # JSON ----> XML
    if os.path.splitext(file_name)[-1].casefold() == '.xml':

        print(f'\n\tWriting your JSON file...')

        # We start by reading our xml file data
        data_from_xml_file: (str, {}) = xml_reader(file_name)

        # We then write our xml data to a new JSON file
        with open(resource_path(f'../{data_from_xml_file[0]}.json'), mode='w') as json_file:
            json.dump(data_from_xml_file[1], fp=json_file, indent=4)

            print('\n\tSUCCESS! Your JSON file has been successfully created.')

    # XML ----> JSON
    elif os.path.splitext(file_name)[-1].casefold() == '.json':

        print(f'\n\tWriting your XML file...\n')

        # We read our json data as a dictionary
        data_from_json: {} = json_reader(file_name)

        # We use the main key as our root element's tag
        root_tag = list(data_from_json.keys())[0]

        # We create a root (parent) element
        parent_element: elementTree.Element = elementTree.Element(f'{root_tag}')

        # We traverse the nested dict values and add each value as a sub element of its associative key
        # I believe there is a better approach to this - a dynamic, perhaps less verbose approach
        for _, child_element in data_from_json.items():
            for child_element_key in child_element.keys():
                level_1_sub_element = elementTree.SubElement(parent_element, child_element_key)
                for value_of_child_element_key in child_element[child_element_key]:
                    level_2_sub_element = elementTree.SubElement(level_1_sub_element, value_of_child_element_key)
                    for index, value_of_child_element_key_child_element in enumerate(child_element[child_element_key][
                                                                                         value_of_child_element_key]):
                        level_1_sub_element_tag = elementTree.SubElement(level_2_sub_element,
                                                                         value_of_child_element_key_child_element)
                        level_1_sub_element_tag.text = str(list(child_element[child_element_key][
                                                                    value_of_child_element_key].values())[index])

        # We convert our parent element and all its sub elements to an element tree
        final_xml: elementTree = elementTree.ElementTree(parent_element)

        # We write our XMl file
        with open(resource_path(f"../{root_tag}.xml"), mode='wb') as xml_file:
            final_xml.write(xml_file, encoding='UTF-8', xml_declaration=True)

            print(f'\n\tSUCCESS! Your XML file has been successfully created.')


def xml_reader(file_name: str) -> (str, {}):

    """
    Read an xml file and convert its level-2-sub-tags to column headings and their text to row values
    :param file_name: The name of the xml file to be read / converted
    :return: A two value tuple containing the root-tag for naming the new file and a dictionary of all the records
    """

    # We read (parse) our xml file data here
    our_xml_source_file: elementTree = elementTree.parse(resource_path(f"../{file_name}"))

    # We access the main element to serve later as a file name and as the main key for our resulting json file
    parent_element: elementTree.Element = our_xml_source_file.getroot()

    name_of_resulting_file: str = parent_element.tag

    # Retrieve every sub-element of the (first) main sub-element as a Column Heading and add it to a list
    columns: [] = [element.tag for element in parent_element[0]]

    # Getting the individual records and adding them to a list
    rows: [list] = [[el.text.replace('\n', '').strip() for el in element] for element in parent_element]

    # Make each row into a dictionary with columns as keys
    rows_list: [{}] = [dict(zip(columns, row)) for row in rows]

    # Add the list of dictionaries to a new dictionary with the root tag as the key
    xml_content: {} = {parent_element.tag: rows_list}

    return name_of_resulting_file, xml_content


def json_reader(file_name) -> {}:
    """
    Read a JSON file and return its content
    :param file_name: The name of the JSON file to be converted
    :return: A Dictionary / Python Object
    """

    with open(resource_path(resource_path(f'../{file_name}')), mode='r', encoding='UTF-8') as json_source_file:
        return json.load(json_source_file)


def resource_path(relative_path) -> [str, bytes]:
    """
    For managing file resources.
    :param: relative_path: The relative path (relative to the script file) of the target file as a string
    :return: A list of bytes (file content) and string (file path)
    """

    base_path: [] = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
