import React from 'react'

function SchemaComponent(props) {

    console.log('hjjh', props.schema);
    return (
        <div>{props.schema.text}</div>
    )
}

export default SchemaComponent