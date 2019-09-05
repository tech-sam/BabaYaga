import React from "react";
import SchemaComponent from "../schema/SchemaComponent";
import LoaderComponent from '../loader/LoaderComponent';
import "./SchemaListComponent.scss"

function SchemaListComponent(props) {
    function renderContent() {
        if (props.isLoading) {
            return [
                <div className="loader-wrapper">
                    <LoaderComponent />
                </div>
            ];
        }
      
        return [
            <div className="database-list">
                {props.schemaList.map((schema, key) => (
                    <SchemaComponent key={key} schema={schema}></SchemaComponent>
                ))}
            </div>
        ];
    }
    return (
        <div>
            <div className="form-group border-bottom border-danger">
                <legend className="form-header">{props.formName} Schema List</legend>
            </div>
            <div className="container dropable">
                {renderContent()}
            </div>
        </div>
    );
}
export default SchemaListComponent;
