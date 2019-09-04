import React from "react";
import SchemaComponent from "../schema/SchemaComponent";
function SchemaListComponent(props) {
  return (
    <div className="container dropable">
      {/* <h4>Server List</h4> */}
      <div className="database-list">
        {props.schemaList.map((schema, key) => (
          <SchemaComponent key={key}  schema={schema}></SchemaComponent>
        ))}
      </div>
    </div>
  );
}
export default SchemaListComponent;
