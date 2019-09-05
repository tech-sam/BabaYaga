import React from "react";

function SchemaComponent(props) {
    return (
        <div
            className="card"
            draggable
            onDragStart={(ev, id) => ev.dataTransfer.setData('data', JSON.stringify(props.schema))}
        >
            {props.schema.schemaName}
        </div>
    );
}

export default SchemaComponent;
