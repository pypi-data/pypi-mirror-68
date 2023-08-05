"""
This file contains css source that will be written to a css file on the fly when creating
documentation, this data is used by aa_doc.py file.
"""


from string import Template

stylesheet_source_data = Template(
"""

body {
    color: #333;
    font-size: large;
    margin-top: 25px;
    margin-left: 40px !important;
    font-family: 'Courier New', Courier, monospace;
}

div {
    /* color: #2196f3; */
}

.author {
    /* Keep the color else it will default to blue */
    color: #2196f3 !important;
}

.date {
    color: #2196f3;
}

.constant {
    color: #2196f3;
}

.copyright {
    color: #444343;
}

.default {
    color: #2196f3;
}

.deprecated {
    color: #2196f3;
}

.description {
    display: block;
    padding-top: 15px;
    padding-bottom: 15px;
    color: #333;
    width: 75%;
}

.file {
    /* padding-bottom: 10px; */
    display: block;
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: 36px;
    font-style: normal;
    font-weight: bold;
    color: #125e9c;

}

.property-title{
    display: block;
    margin-bottom: 10px;
    margin-top: 10px;
    font-size: 15px;
    font-style: normal;
    font-weight: bold;
    color: #3979ad;
}

.function {
    display: block;
    margin-bottom: 10px;
    margin-top: 10px;
    font-size: 25px;
    font-style: normal;
    font-weight: bold;
    color: #333;
}

.global {
    color: #2196f3;
}

.ignore {
    color: #2196f3;
}

.license {
    color: #2196f3;
}

.module {
    color: #2196f3;
}

.name {
    color: #2196f3;
}

.namespace {
    color: #2196f3;
}

.package {
    color: #2196f3;
}

.param {
    color: #2196f3;
}

.requires {
    color: #2196f3;
}

.returns {
    color: #2196f3;
}

.see {
    color: #2196f3;
}

.since {
    color: #2196f3;
}

.summary {
    color: #2196f3;
}

.throws {
    color: #2196f3;
}

.todo {
    color: #2196f3;
}

.type {
    color: #2196f3;
}

.version {
    color: #2196f3;
}

.label {
    display: block;
    border-left: 2px solid #2196f3;
    padding-left: 15px;
    padding-top: 10px;
    padding-bottom: 10px;
    margin-left: 0px;
    /* 
     * label items should not have margins
     * because we want them to align with each other
     */
    margin-top: 0px !important;
    margin-bottom: 0px !important;
}

table {
    border-collapse: collapse;
    /* width: 100%; */
}

.param-table {
    margin-top: 15px;
    margin-bottom: 15px;
    border: 2px solid #2196f3;
}

.param-header-row {
    background-color: #2196f3;
    color: white;
}

th, td {
    /* border: 0px solid gray;  */
}

.param-table-cell {
    border: 1px solid gray;
    padding: 5px;
}

hr {
    border: none;
    border-top: 3px solid #333;
    color: #333;
    overflow: visible;
    text-align: center;
    height: 5px;
}

.file-link {
    margin-bottom: 10px;
    font-size: 25px;
    font-style: normal;
    font-weight: bold;
    color: #333;
}

.footer {
   position: fixed;
   left: 0;
   bottom: 0;
   width: 100%;
   background-color: #ddd;
   color: gray;
   text-align: center;
}

.footer-content {
   margin-top: 5px;
   margin-bottom: 5px;
}

.header {
    display: block;
    margin-bottom: 10px;
    font-size: 40px;
    font-style: normal;
    font-weight: bold;
    color: #125e9c;
}

.property-title{
    display: block;
    margin-bottom: 10px;
    margin-top: 10px;
    font-size: 20px;
    font-style: normal;
    font-weight: bold;
    color: #333;
}


#aa {
    font-size: inherit;
    color: #333;
    background-color: #2196f3;
    padding: inherit;
}

#doc {
    color: #ddd;
    background-color: #333;
    padding: 3px;
    border-radius: 3px;
}
"""
).safe_substitute()