import React from "react";
import SchemaComponent from "../schema/SchemaComponent";
function SchemaListComponent(props) {
    return (
        <div>
            <div className="form-group border-bottom border-danger">
                <legend className="form-header">{props.formName} Schema List</legend>
            </div>
            <div className="container dropable">
     
                <div className="database-list">
                    {props.schemaList.map((schema, key) => (
                        <SchemaComponent key={key} schema={schema}></SchemaComponent>
                    ))}
                </div>
            </div>
        </div>
    );
}
export default SchemaListComponent;
