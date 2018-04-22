from enum import Enum


"""
Describes a batch of differences between two APIs
"""
class ApiDifferential(): 

    def __init__(self,
                api_name='',
                api_server='',
                api_old_version='',
                api_new_version='',
                element_differentials=[]
            ):

        self.api_name = api_name
        self.api_server = api_server
        self.api_old_version = api_old_version
        self.api_new_version = api_new_version
        self.element_differentials = element_differentials

    def addElementDifferential(self, diff):
        self.element_differentials.append(diff)


"""
Describes a single atomic difference between two APIs at the element level
"""
class ElementDifferential():

    def __init__(self,
                differential_type,
                element_path,
                old_element,
                new_element
            ):
        self.differential_type = differential_type
        self.element_path = element_path
        self.old_element = old_element
        self.new_element = new_element


"""
Defines the values allowed for element differential types
"""
class DifferentialType(Enum):
    ADD = 1
    DELETE = 2
    MODIFY = 3
