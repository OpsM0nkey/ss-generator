class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        # TODO: maybe add in validation for children (should be of type HTMLNode??)

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Method requires override")
    
    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        
        if not isinstance(self.props, dict):
            raise TypeError(f"HTMLNode.props attribute must be a dict. Type was {type(self.props)}")
        
        property_string = ""
        for k,v in self.props.items():
            # leading whitespace below is intentional
            property_string += f' {k}="{v}"'

        return property_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = "", props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value cannot be None.")
    
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        # if self.tag != None:
        #     output_string = output_string.replace(output_string,f"<{self.tag}{self.props_to_html()}>{output_string}</{self.tag}>")
        
        # return output_string
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None or len(self.tag) == 0:
            raise ValueError("Tag cannot be None or empty")
        if self.children == None:
            raise ValueError("ParentNode must include a children property")
        
        output_text = ""
        for node in self.children:
            output_text += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{output_text}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

        
