connect: {"from": "stage",     "to": "id", "invert": true, "style": "curved=1;fontSize=11;"}
connect: {"from": "terraform", "to": "id",                 "style": "curved=1;fontSize=11;"}
connect: {"from": "branch",    "to": "id",                 "style": "curved=1;fontSize=11;"}
connect: {"from": "ansible",   "to": "id",                 "style": "curved=1;fontSize=11;"}

# Node label with placeholders and HTML.
# Default is '%name_of_first_column%'.

# label: %label%<br><i style="color:gray;">%type%</i><br><a href="mailto:%email%">Email</a>
# label: %label%<br><i style="color:gray;">%type%</i>
label: %name%<br><b><i style="color:gray;">%type%</i></b>

# Node style (placeholders are replaced once).
# Default is the current style for nodes.

style: label;image=%image%;whiteSpace=wrap;html=1;rounded=1;fillColor=%fill%;strokeColor=%stroke%;fontColor=#000000

# Node width. Possible value is a number (in px), auto or an @ sign followed by a column
# name that contains the value for the width. Default is auto.

width: auto

# Node height. Possible value is a number (in px), auto or an @ sign followed by a column
# name that contains the value for the height. Default is auto.

height: auto

# Padding for autosize. Default is 0.

padding: 0

# Name of layout. Possible values are auto, none, verticaltree, horizontaltree,
# verticalflow, horizontalflow, organic, circle. Default is auto.

layout: verticalflow

# Comma-separated list of ignored columns for metadata. (These can be
# used for connections and styles but will not be added as metadata.)

ignore: image, fill, stroke

# Node x-coordinate. Possible value is a column name. Default is empty. Layouts will
# override this value.

left: 

# Node y-coordinate. Possible value is a column name. Default is empty. Layouts will
# override this value.

top: 

# Node width. Possible value is a number (in px), auto or an @ sign followed by a column
# name that contains the value for the width. Default is auto.

width: auto

# Node height. Possible value is a number (in px), auto or an @ sign followed by a column
# name that contains the value for the height. Default is auto.

height: auto

# Parent style for nodes with child nodes (placeholders are replaced once).

parentstyle: swimlane;whiteSpace=wrap;html=1;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;

