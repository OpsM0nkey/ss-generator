class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children = None, props: dict = None):
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