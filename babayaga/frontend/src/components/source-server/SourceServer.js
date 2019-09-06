import React, {Component} from 'react'
import FormComponent from '../form/FormComponent';
import Axios from 'axios';
import SchemaListComponent from '../schema-list/SchemaListComponent';
import { getBaseUrl } from '../../global';
import Button from "react-bootstrap/Button";
import sourceDefault from "../../static-data/static-source-data.json";


const formName = 'Source'

class SourceServer extends Component {
    
    constructor() {
        super();
        this.state = {
            response: {}
        }
        this.formValue = {};
        this.submited = false;
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.createSource = this.createSource.bind(this);
        this.setDefaultValue = this.setDefaultValue.bind(this);

        this.httpClient = Axios.create();
        this.httpClient.defaults.timeout = 1000;

    }

    handleChange(event) {
        const { name, value } = event.target;
        this.formValue[name] = value;
    }

    handleSubmit(e) {
        this.createSource();
        this.submited = true;
    }

    createSource() {
        Axios.post(`${getBaseUrl()}api/schemas`, this.formValue)
            .then((response) => {
                this.setState({ response: response.data });
            });
    }
    setDefaultValue() {
        this.submited = true;
        this.setState({ ...this.state, response: sourceDefault });
        
    }

    

    render() {
        if (!this.submited) {
            return (
                <div>
                    <Button className="btn-default" onClick={evt => { this.setDefaultValue(); }}>
                        Default Source Database
                    </Button>
                    <FormComponent
                        formName={formName}
                        handleChange={this.handleChange}
                        handleSubmit={this.handleSubmit}
                        data={this.state}
                    />
                </div>
            );
        }
        else {
            return (
                <div>
                    <SchemaListComponent formName={formName} formValue={this.formValue} schemaList={this.state.response}></SchemaListComponent>
                </div>
            );
        }
    }
}

export default SourceServer;